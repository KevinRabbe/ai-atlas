from __future__ import annotations

from dataclasses import dataclass

from .organism_runtime import TypedScopeRuntime


@dataclass
class PreparedPublication:
    publication_id: int
    kind: str
    proposal_id: int
    expected_topology_epoch: int
    topology_change_id: int | None = None
    resource_id: str | None = None
    expected_lease_version: int | None = None
    new_holder_id: int | None = None
    consequence: float = 0.0
    requires_assurance: bool = False
    status: str = "prepared"

    @property
    def publication_ref(self) -> str:
        # Stable inside the persisted prepared-publication identity. A mature
        # implementation may use another globally unique encoding; Atlas only
        # requires that the authoritative state can identify this publication.
        return f"{self.kind}:{self.proposal_id}:{self.publication_id}"


class PublicationProtocol:
    """Failure-isolated prepare -> validate -> publish protocol.

    Preparation never grants authority or changes live ownership/topology. The
    publication fence checks that the state being replaced is still the state
    the candidate was prepared against, re-reads current authority, and stamps
    publication provenance into the same modeled authoritative state change.
    """

    def __init__(self, runtime: TypedScopeRuntime) -> None:
        self.runtime = runtime
        self.publications: dict[int, PreparedPublication] = {}
        self._next_publication_id = 0

    def prepare_topology(
        self,
        labels: tuple[int, ...],
        *,
        consequence: float,
    ) -> PreparedPublication:
        change = self.runtime.stage_scope_change(labels, consequence=consequence)
        publication = PreparedPublication(
            publication_id=self._next_publication_id,
            kind="topology",
            proposal_id=change.proposal_id,
            expected_topology_epoch=self.runtime.topology_epoch,
            topology_change_id=change.change_id,
            consequence=consequence,
            requires_assurance=change.requires_assurance,
        )
        self._next_publication_id += 1
        self.publications[publication.publication_id] = publication
        return publication

    def prepare_resource_handoff(
        self,
        resource_id: str,
        new_holder_id: int,
        *,
        consequence: float,
    ) -> PreparedPublication:
        self.runtime._require_subject(new_holder_id)
        current = self.runtime.leases.get(resource_id)
        if current is None:
            raise KeyError(f"resource {resource_id!r} has no current lease")
        if current.holder_id == new_holder_id:
            raise ValueError("resource is already held by the proposed new holder")

        proposal = self.runtime.propose_transition(
            "resource_handoff",
            target_id=new_holder_id,
            expected_value=consequence,
            cost=0.0,
            uncertainty=0.0,
            consequence=consequence,
            reversible=True,
            authority_class="structural",
            resource_units=1,
        )
        publication = PreparedPublication(
            publication_id=self._next_publication_id,
            kind="resource_handoff",
            proposal_id=proposal.proposal_id,
            expected_topology_epoch=self.runtime.topology_epoch,
            resource_id=resource_id,
            expected_lease_version=current.version,
            new_holder_id=new_holder_id,
            consequence=consequence,
            requires_assurance=(
                consequence >= self.runtime.structural_assurance_threshold
            ),
        )
        self._next_publication_id += 1
        self.publications[publication.publication_id] = publication
        return publication

    def _require_prepared(self, publication_id: int) -> PreparedPublication:
        publication = self.publications[publication_id]
        if publication.status != "prepared":
            raise ValueError(
                f"publication {publication_id} is {publication.status}, not prepared"
            )
        return publication

    def _check_assurance(
        self,
        publication: PreparedPublication,
        assurance_token_id: int | None,
    ) -> None:
        if publication.requires_assurance and not self.runtime._valid_assurance(
            publication.proposal_id,
            assurance_token_id,
        ):
            raise PermissionError(
                "publication requires independent approved assurance"
            )

    def publish(
        self,
        publication_id: int,
        *,
        assurance_token_id: int | None = None,
    ) -> None:
        publication = self._require_prepared(publication_id)
        self._check_assurance(publication, assurance_token_id)

        if publication.kind == "topology":
            if self.runtime.topology_epoch != publication.expected_topology_epoch:
                raise RuntimeError("stale topology publication fence")
            assert publication.topology_change_id is not None
            self.runtime.commit_scope_change(
                publication.topology_change_id,
                assurance_token_id=assurance_token_id,
                publication_ref=publication.publication_ref,
            )

        elif publication.kind == "resource_handoff":
            assert publication.resource_id is not None
            assert publication.expected_lease_version is not None
            assert publication.new_holder_id is not None

            current_lease = self.runtime.leases.get(publication.resource_id)
            if (
                current_lease is None
                or current_lease.version != publication.expected_lease_version
            ):
                raise RuntimeError("stale resource-lease publication fence")

            # Preparation cannot capture authority. Publication must resolve the
            # latest categorical state, including revocations after preparation.
            current_authority = self.runtime.read_authority(
                publication.new_holder_id
            )
            if not current_authority.allowed:
                raise PermissionError(
                    "current authority denies prepared resource handoff"
                )

            self.runtime.transfer_resource(
                publication.resource_id,
                publication.new_holder_id,
                publication_ref=publication.publication_ref,
            )
        else:
            raise AssertionError(f"unsupported publication kind {publication.kind}")

        publication.status = "published"
        self.runtime.costs.writes += 1

    def discard(self, publication_id: int) -> None:
        publication = self._require_prepared(publication_id)
        if publication.kind == "topology" and publication.topology_change_id is not None:
            change = self.runtime.topology_changes[publication.topology_change_id]
            if change.status == "staged":
                self.runtime.rollback_scope_change(change.change_id)
        publication.status = "discarded"
        self.runtime.costs.writes += 1
