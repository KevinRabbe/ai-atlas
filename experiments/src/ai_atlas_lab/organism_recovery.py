from __future__ import annotations

from dataclasses import dataclass

from .external_effect_protocol import (
    ExternalEffectIntent,
    ExternalExecutionObservation,
    ExternalRecoveryDecision,
    decide_external_effect_recovery,
)
from .organism_runtime import TypedScopeRuntime
from .publication_protocol import PreparedPublication
from .recovery_protocol import (
    RecoveryDecision,
    RecoveryObservation,
    RecoveryRecord,
    decide_recovery,
)


def _topology_ref(labels: tuple[int, ...]) -> str:
    return "topology:" + ",".join(str(value) for value in labels)


def _resource_ref(resource_id: str, holder_id: int) -> str:
    return f"resource:{resource_id}:holder:{holder_id}"


@dataclass
class OrganismRecoveryCoordinator:
    """Compose I14-I18 recovery semantics over the common typed runtime.

    The coordinator does not own authority. It observes authoritative runtime
    state/provenance, resolves current permission where a NEW attempt is
    required, and returns a typed recovery decision.
    """

    runtime: TypedScopeRuntime

    def record_for_publication(self, publication: PreparedPublication) -> RecoveryRecord:
        if publication.kind == "resource_handoff":
            if publication.resource_id is None or publication.new_holder_id is None:
                raise ValueError("resource publication is missing target semantics")
            if publication.expected_lease_version is None:
                raise ValueError("resource publication is missing base lease version")
            return RecoveryRecord(
                publication_id=publication.publication_ref,
                kind="resource_handoff",
                expected_base_version=publication.expected_lease_version,
                # Runtime-wide lease numbering means the exact resulting
                # numeric version need not be knowable before publication.
                target_version=None,
                target_ref=_resource_ref(
                    publication.resource_id,
                    publication.new_holder_id,
                ),
                validation_refs=(f"authority:{publication.new_holder_id}",),
            )

        if publication.kind == "topology":
            if publication.topology_change_id is None:
                raise ValueError("topology publication is missing change identity")
            change = self.runtime.topology_changes[publication.topology_change_id]
            return RecoveryRecord(
                publication_id=publication.publication_ref,
                kind="topology",
                expected_base_version=publication.expected_topology_epoch,
                target_version=None,
                target_ref=_topology_ref(change.new_labels),
                validation_refs=(f"topology-change:{change.change_id}",),
            )

        raise ValueError(f"unsupported publication kind {publication.kind}")

    def observe_publication(self, publication: PreparedPublication) -> RecoveryObservation:
        if publication.kind == "resource_handoff":
            if publication.resource_id is None:
                raise ValueError("resource publication is missing resource identity")
            lease = self.runtime.leases[publication.resource_id]
            return RecoveryObservation(
                current_version=lease.version,
                current_ref=_resource_ref(lease.resource_id, lease.holder_id),
                current_publication_id=lease.publication_ref,
            )

        if publication.kind == "topology":
            return RecoveryObservation(
                current_version=self.runtime.topology_epoch,
                current_ref=_topology_ref(self.runtime.topology_labels),
                current_publication_id=self.runtime.topology_publication_ref,
            )

        raise ValueError(f"unsupported publication kind {publication.kind}")

    def recover_publication(
        self,
        publication: PreparedPublication,
        *,
        current_assurance_ok: bool,
        current_validation_ok: bool | None = None,
    ) -> RecoveryDecision:
        record = self.record_for_publication(publication)
        observation = self.observe_publication(publication)

        if publication.kind == "resource_handoff":
            assert publication.new_holder_id is not None
            current_validation = self.runtime.read_authority(
                publication.new_holder_id
            ).allowed
        else:
            current_validation = (
                True if current_validation_ok is None else current_validation_ok
            )

        return decide_recovery(
            record,
            observation,
            current_validation_ok=current_validation,
            current_assurance_ok=current_assurance_ok,
        )

    def recover_external_effect(
        self,
        intent: ExternalEffectIntent,
        *,
        target_id: int,
        observation: ExternalExecutionObservation,
        receiver_recognizes_identity: bool,
        duplicate_penalty: float,
        missed_penalty: float,
        retry_cost: float = 0.0,
    ) -> ExternalRecoveryDecision:
        current_authority = self.runtime.read_authority(target_id).allowed
        return decide_external_effect_recovery(
            intent,
            observation,
            current_authority=current_authority,
            receiver_recognizes_identity=receiver_recognizes_identity,
            duplicate_penalty=duplicate_penalty,
            missed_penalty=missed_penalty,
            retry_cost=retry_cost,
        )
