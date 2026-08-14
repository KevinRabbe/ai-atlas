from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable

from .core import CostMeter


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: int
    subject_id: int
    source_ref: str
    payload_ref: str | None = None


@dataclass(frozen=True)
class PredictiveRecord:
    subject_id: int
    source_ref: str
    state_ref: str


@dataclass
class AuthorityRecord:
    allowed: bool
    version: int = 0


@dataclass(frozen=True)
class ResourceLease:
    resource_id: str
    holder_id: int
    version: int


@dataclass(frozen=True)
class TransitionProposal:
    proposal_id: int
    kind: str
    target_id: int | None
    expected_value: float
    cost: float
    uncertainty: float
    consequence: float
    reversible: bool
    authority_class: str = "temporary"
    resource_units: int = 1

    @property
    def net_value(self) -> float:
        return self.expected_value - self.cost


@dataclass(frozen=True)
class AssuranceToken:
    token_id: int
    proposal_id: int
    independent: bool
    approved: bool
    evidence_ref: str


@dataclass
class TopologyChange:
    change_id: int
    proposal_id: int
    old_labels: tuple[int, ...]
    new_labels: tuple[int, ...]
    moved_subjects: tuple[int, ...]
    consequence: float
    requires_assurance: bool
    status: str = "staged"


@dataclass
class RuntimeEvent:
    event_id: int
    target_id: int
    due_step: int
    external: bool
    created_epoch: int
    processed: bool = False
    forwarded: bool = False


@dataclass(frozen=True)
class AllocationResult:
    proposal_ids: tuple[int, ...]
    net_value: float
    resource_units: int


class TypedScopeRuntime:
    """Persistent architecture substrate derived from Atlas I04-I09.

    Topology is revisable organizational state. Exact semantic identities,
    provenance, authority and resource leases remain independently addressed.
    """

    def __init__(
        self,
        subjects: Iterable[int],
        *,
        structural_assurance_threshold: float = 4.0,
    ) -> None:
        subject_tuple = tuple(subjects)
        if not subject_tuple:
            raise ValueError("runtime requires at least one subject")
        if len(set(subject_tuple)) != len(subject_tuple):
            raise ValueError("subject identities must be unique")

        self.subjects = subject_tuple
        self._subject_set = set(subject_tuple)
        self.topology_labels: tuple[int, ...] = tuple(range(len(subject_tuple)))
        self.topology_epoch = 0
        self.structural_assurance_threshold = structural_assurance_threshold

        self.evidence: dict[int, EvidenceRecord] = {}
        self.predictive: dict[int, PredictiveRecord] = {}
        self.authority: dict[int, AuthorityRecord] = {
            subject: AuthorityRecord(True, 0) for subject in subject_tuple
        }
        self.leases: dict[str, ResourceLease] = {}
        self.events: dict[int, RuntimeEvent] = {}
        self.proposals: dict[int, TransitionProposal] = {}
        self.assurance: dict[int, AssuranceToken] = {}
        self.topology_changes: dict[int, TopologyChange] = {}

        self._next_evidence_id = 0
        self._next_proposal_id = 0
        self._next_token_id = 0
        self._next_change_id = 0
        self._next_event_id = 0
        self._lease_version = 0

        self.costs = CostMeter()
        self.forwarded_events = 0
        self.blocked_external_events = 0
        self.executed_events = 0
        self.executed_proposals: set[int] = set()

    def _require_subject(self, subject_id: int) -> None:
        if subject_id not in self._subject_set:
            raise KeyError(f"unknown subject {subject_id}")

    def attach_evidence(
        self,
        subject_id: int,
        source_ref: str,
        payload_ref: str | None = None,
    ) -> EvidenceRecord:
        self._require_subject(subject_id)
        evidence_id = self._next_evidence_id
        self._next_evidence_id += 1
        record = EvidenceRecord(evidence_id, subject_id, source_ref, payload_ref)
        self.evidence[evidence_id] = record
        self.costs.writes += 1
        return record

    def register_predictive_state(
        self,
        subject_id: int,
        state_ref: str,
        source_ref: str,
    ) -> PredictiveRecord:
        self._require_subject(subject_id)
        record = PredictiveRecord(subject_id, source_ref, state_ref)
        self.predictive[subject_id] = record
        self.costs.writes += 1
        return record

    def rematerialize(self, subject_id: int) -> str:
        self._require_subject(subject_id)
        self.costs.reads += 1
        try:
            return self.predictive[subject_id].source_ref
        except KeyError as exc:
            raise KeyError(f"no recoverable predictive source for {subject_id}") from exc

    def set_authority(self, subject_id: int, allowed: bool) -> AuthorityRecord:
        self._require_subject(subject_id)
        record = self.authority[subject_id]
        if record.allowed != allowed:
            record.allowed = allowed
            record.version += 1
            self.costs.writes += 1
        return AuthorityRecord(record.allowed, record.version)

    def read_authority(self, subject_id: int) -> AuthorityRecord:
        self._require_subject(subject_id)
        self.costs.reads += 1
        record = self.authority[subject_id]
        return AuthorityRecord(record.allowed, record.version)

    def lease_resource(self, resource_id: str, holder_id: int) -> ResourceLease:
        self._require_subject(holder_id)
        existing = self.leases.get(resource_id)
        if existing is not None and existing.holder_id != holder_id:
            raise ValueError(
                f"resource {resource_id!r} already leased to {existing.holder_id}"
            )
        if existing is not None:
            return existing
        self._lease_version += 1
        lease = ResourceLease(resource_id, holder_id, self._lease_version)
        self.leases[resource_id] = lease
        self.costs.writes += 1
        return lease

    def transfer_resource(self, resource_id: str, new_holder_id: int) -> ResourceLease:
        self._require_subject(new_holder_id)
        if resource_id not in self.leases:
            raise KeyError(f"resource {resource_id!r} has no current lease")
        self._lease_version += 1
        lease = ResourceLease(resource_id, new_holder_id, self._lease_version)
        self.leases[resource_id] = lease
        self.costs.writes += 1
        return lease

    def propose_transition(
        self,
        kind: str,
        *,
        target_id: int | None,
        expected_value: float,
        cost: float,
        uncertainty: float,
        consequence: float,
        reversible: bool,
        authority_class: str = "temporary",
        resource_units: int = 1,
    ) -> TransitionProposal:
        if target_id is not None:
            self._require_subject(target_id)
        if resource_units < 0:
            raise ValueError("resource_units cannot be negative")
        proposal = TransitionProposal(
            proposal_id=self._next_proposal_id,
            kind=kind,
            target_id=target_id,
            expected_value=expected_value,
            cost=cost,
            uncertainty=uncertainty,
            consequence=consequence,
            reversible=reversible,
            authority_class=authority_class,
            resource_units=resource_units,
        )
        self._next_proposal_id += 1
        self.proposals[proposal.proposal_id] = proposal
        self.costs.writes += 1
        return proposal

    def allocate_bundle(
        self,
        proposals: Iterable[TransitionProposal],
        *,
        capacity: int,
        interactions: dict[frozenset[int], float] | None = None,
    ) -> AllocationResult:
        proposal_list = list(proposals)
        if capacity < 0:
            raise ValueError("capacity cannot be negative")
        interactions = interactions or {}

        best_ids: tuple[int, ...] = ()
        best_value = 0.0
        best_units = 0

        # Exact small-set allocator for experiments. The public API encodes
        # interaction semantics without committing a mature runtime to brute force.
        for count in range(len(proposal_list) + 1):
            for subset in combinations(proposal_list, count):
                units = sum(item.resource_units for item in subset)
                if units > capacity:
                    continue
                ids = tuple(sorted(item.proposal_id for item in subset))
                value = sum(item.net_value for item in subset)
                id_set = set(ids)
                for key, delta in interactions.items():
                    if key.issubset(id_set):
                        value += delta
                self.costs.comparisons += 1
                if value > best_value:
                    best_value = value
                    best_ids = ids
                    best_units = units

        return AllocationResult(best_ids, best_value, best_units)

    def request_assurance(
        self,
        proposal_id: int,
        *,
        independent: bool,
        approved: bool,
        evidence_ref: str,
    ) -> AssuranceToken:
        if proposal_id not in self.proposals:
            raise KeyError(f"unknown proposal {proposal_id}")
        token = AssuranceToken(
            token_id=self._next_token_id,
            proposal_id=proposal_id,
            independent=independent,
            approved=approved,
            evidence_ref=evidence_ref,
        )
        self._next_token_id += 1
        self.assurance[token.token_id] = token
        self.costs.verifications += 1
        self.costs.writes += 1
        return token

    def _valid_assurance(
        self,
        proposal_id: int,
        assurance_token_id: int | None,
    ) -> bool:
        if assurance_token_id is None:
            return False
        token = self.assurance.get(assurance_token_id)
        return bool(
            token is not None
            and token.proposal_id == proposal_id
            and token.independent
            and token.approved
        )

    def execute_transition(
        self,
        proposal_id: int,
        *,
        assurance_token_id: int | None = None,
    ) -> None:
        proposal = self.proposals[proposal_id]
        if proposal_id in self.executed_proposals:
            raise ValueError(f"proposal {proposal_id} already executed")

        if proposal.authority_class == "external_effect":
            if proposal.target_id is None:
                raise ValueError("external effects require an exact target identity")
            current = self.read_authority(proposal.target_id)
            if not current.allowed:
                raise PermissionError("current capability authority denies external effect")
            if (
                proposal.consequence >= self.structural_assurance_threshold
                and not self._valid_assurance(proposal_id, assurance_token_id)
            ):
                raise PermissionError(
                    "high-consequence external effect requires independent assurance"
                )
        elif proposal.authority_class == "durable_knowledge":
            if not self._valid_assurance(proposal_id, assurance_token_id):
                raise PermissionError(
                    "durable knowledge promotion requires independent assurance"
                )
        elif proposal.authority_class == "structural":
            if (
                proposal.consequence >= self.structural_assurance_threshold
                and not self._valid_assurance(proposal_id, assurance_token_id)
            ):
                raise PermissionError(
                    "high-consequence structural transition requires independent assurance"
                )

        self.executed_proposals.add(proposal_id)
        self.costs.operations += 1
        self.costs.writes += 1

    def _normalized_labels(self, labels: Iterable[int]) -> tuple[int, ...]:
        raw = tuple(labels)
        if len(raw) != len(self.subjects):
            raise ValueError("topology label count must match subject count")
        remap: dict[int, int] = {}
        normalized: list[int] = []
        for label in raw:
            if label not in remap:
                remap[label] = len(remap)
            normalized.append(remap[label])
        return tuple(normalized)

    def _scope_members(
        self,
        labels: tuple[int, ...],
        index: int,
    ) -> frozenset[int]:
        label = labels[index]
        return frozenset(
            subject
            for pos, subject in enumerate(self.subjects)
            if labels[pos] == label
        )

    def stage_scope_change(
        self,
        labels: Iterable[int],
        *,
        consequence: float,
    ) -> TopologyChange:
        new_labels = self._normalized_labels(labels)
        moved = tuple(
            subject
            for index, subject in enumerate(self.subjects)
            if self._scope_members(self.topology_labels, index)
            != self._scope_members(new_labels, index)
        )
        proposal = self.propose_transition(
            "topology_change",
            target_id=None,
            expected_value=float(len(moved)),
            cost=0.0,
            uncertainty=0.0,
            consequence=consequence,
            reversible=True,
            authority_class="structural",
            resource_units=max(1, len(moved)),
        )
        change = TopologyChange(
            change_id=self._next_change_id,
            proposal_id=proposal.proposal_id,
            old_labels=self.topology_labels,
            new_labels=new_labels,
            moved_subjects=moved,
            consequence=consequence,
            requires_assurance=(
                len(moved) * consequence >= self.structural_assurance_threshold
            ),
        )
        self._next_change_id += 1
        self.topology_changes[change.change_id] = change
        self.costs.writes += 1
        return change

    def commit_scope_change(
        self,
        change_id: int,
        *,
        assurance_token_id: int | None = None,
    ) -> int:
        change = self.topology_changes[change_id]
        if change.status != "staged":
            raise ValueError(f"change {change_id} is {change.status}, not staged")

        if change.requires_assurance and not self._valid_assurance(
            change.proposal_id,
            assurance_token_id,
        ):
            raise PermissionError(
                "structural change requires independent approved assurance"
            )

        if change.new_labels != self.topology_labels:
            self.topology_labels = change.new_labels
            self.topology_epoch += 1
            self.costs.messages += len(change.moved_subjects)
            self.costs.writes += len(change.moved_subjects)
        change.status = "committed"
        return self.topology_epoch

    def rollback_scope_change(self, change_id: int) -> None:
        change = self.topology_changes[change_id]
        if change.status == "committed":
            raise ValueError("committed topology changes require a compensating change")
        if change.status != "staged":
            raise ValueError(f"change {change_id} is {change.status}")
        change.status = "rolled_back"
        self.costs.writes += 1

    def enqueue_event(
        self,
        target_id: int,
        *,
        due_step: int,
        external: bool = False,
    ) -> RuntimeEvent:
        self._require_subject(target_id)
        event = RuntimeEvent(
            event_id=self._next_event_id,
            target_id=target_id,
            due_step=due_step,
            external=external,
            created_epoch=self.topology_epoch,
        )
        self._next_event_id += 1
        self.events[event.event_id] = event
        self.costs.writes += 1
        return event

    def process_due_events(self, step: int) -> tuple[int, ...]:
        processed: list[int] = []
        for event in self.events.values():
            if event.processed or event.due_step > step:
                continue

            if event.created_epoch != self.topology_epoch:
                event.forwarded = True
                self.forwarded_events += 1
                self.costs.messages += 1

            if event.external:
                current = self.read_authority(event.target_id)
                if not current.allowed:
                    self.blocked_external_events += 1
                    event.processed = True
                    processed.append(event.event_id)
                    self.costs.operations += 1
                    continue

            event.processed = True
            processed.append(event.event_id)
            self.executed_events += 1
            self.costs.operations += 1
        return tuple(processed)

    def semantic_invariants(self) -> dict[str, bool]:
        evidence_subjects_valid = all(
            record.subject_id in self._subject_set
            for record in self.evidence.values()
        )
        predictive_subjects_valid = all(
            subject in self._subject_set for subject in self.predictive
        )
        lease_subjects_valid = all(
            lease.holder_id in self._subject_set for lease in self.leases.values()
        )
        authority_complete = set(self.authority) == self._subject_set
        events_target_valid = all(
            event.target_id in self._subject_set for event in self.events.values()
        )
        return {
            "evidence_identity": evidence_subjects_valid,
            "predictive_identity": predictive_subjects_valid,
            "resource_identity": lease_subjects_valid,
            "authority_complete": authority_complete,
            "event_identity": events_target_valid,
            "topology_shape": len(self.topology_labels) == len(self.subjects),
        }
