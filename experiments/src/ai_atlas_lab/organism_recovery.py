from __future__ import annotations

from dataclasses import dataclass

from .evidence_aggregation import BinaryEvidenceEstimate, aggregate_binary_evidence
from .evidence_assurance import EvidenceAssuranceDecision, decide_evidence_assurance
from .evidence_dependence import EvidenceDependenceModel
from .evidence_lineage import EvidenceLineageRegistry
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


@dataclass(frozen=True)
class ExternalEvidencePlan:
    estimate: BinaryEvidenceEstimate
    assurance: EvidenceAssuranceDecision


@dataclass
class OrganismRecoveryCoordinator:
    """Compose crash, publication and external-evidence recovery semantics.

    The coordinator does not own authority or truth. It observes authoritative
    runtime state/provenance, resolves current permission where a NEW attempt is
    required, and uses the shared evidence-assurance layer to decide whether
    external execution evidence is sufficient, needs another failure mode, or
    should remain unresolved.

    Exact source lineage is optional. When a learned EvidenceDependenceModel is
    attached, evidence summaries and aggregation combine exact provenance with
    sufficiently supported learned effective dependence.
    """

    runtime: TypedScopeRuntime
    evidence_registry: EvidenceLineageRegistry | None = None
    evidence_dependence_model: EvidenceDependenceModel | None = None

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

    def plan_external_execution_evidence(
        self,
        claim_ref: str,
        *,
        current_step: int,
        current_label: bool | None,
        estimated_current_error: float,
        estimated_independent_error: float,
        consequence: float,
        duplicate_penalty: float,
        missed_penalty: float,
        independent_cost: float,
        unresolved_penalty: float,
        dependence_context: str | None = None,
        minimum_independence_confidence: float = 0.50,
    ) -> EvidenceAssuranceDecision:
        if self.evidence_registry is None:
            raise RuntimeError("external evidence planning requires an EvidenceLineageRegistry")
        summary = self.evidence_registry.summarize_effective(
            claim_ref,
            current_step=current_step,
            dependence_model=self.evidence_dependence_model,
            dependence_context=dependence_context,
            minimum_independence_confidence=minimum_independence_confidence,
        )
        # External binary label semantics: True = effect applied. A false True
        # risks omission; a false False risks duplicate retry.
        return decide_evidence_assurance(
            summary,
            current_label=current_label,
            estimated_current_error=estimated_current_error,
            estimated_independent_error=estimated_independent_error,
            consequence=consequence,
            false_positive_penalty=missed_penalty,
            false_negative_penalty=duplicate_penalty,
            independent_cost=independent_cost,
            unresolved_penalty=unresolved_penalty,
        )

    def plan_external_execution_evidence_from_sources(
        self,
        claim_ref: str,
        *,
        current_step: int,
        source_error_estimates: dict[str, float],
        estimated_independent_error: float,
        consequence: float,
        duplicate_penalty: float,
        missed_penalty: float,
        independent_cost: float,
        unresolved_penalty: float,
        dependence_context: str | None = None,
        minimum_independence_confidence: float = 0.50,
    ) -> ExternalEvidencePlan:
        """Aggregate raw current records before pricing another evidence path.

        This closes the privileged-caller gap in the older planning method:
        copied records cannot first be converted into an overconfident label and
        then handed to lineage-aware assurance. The current label/error estimate
        is derived from effective failure groups inside the common evidence path.
        """

        if self.evidence_registry is None:
            raise RuntimeError("external evidence planning requires an EvidenceLineageRegistry")
        estimate = aggregate_binary_evidence(
            self.evidence_registry,
            claim_ref,
            current_step=current_step,
            source_error_estimates=source_error_estimates,
            positive_value_ref="applied",
            negative_value_ref="absent",
            dependence_model=self.evidence_dependence_model,
            dependence_context=dependence_context,
            minimum_independence_confidence=minimum_independence_confidence,
        )
        assurance = self.plan_external_execution_evidence(
            claim_ref,
            current_step=current_step,
            current_label=estimate.label,
            estimated_current_error=estimate.estimated_error,
            estimated_independent_error=estimated_independent_error,
            consequence=consequence,
            duplicate_penalty=duplicate_penalty,
            missed_penalty=missed_penalty,
            independent_cost=independent_cost,
            unresolved_penalty=unresolved_penalty,
            dependence_context=dependence_context,
            minimum_independence_confidence=minimum_independence_confidence,
        )
        return ExternalEvidencePlan(estimate=estimate, assurance=assurance)

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
