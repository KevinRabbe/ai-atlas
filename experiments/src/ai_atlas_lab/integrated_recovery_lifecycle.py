from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random

from .evidence_lineage import EvidenceLineageRegistry
from .external_effect_protocol import ExternalEffectIntent, ExternalExecutionObservation
from .organism_recovery import OrganismRecoveryCoordinator
from .organism_runtime import TypedScopeRuntime
from .publication_protocol import PublicationProtocol
from .transient_state import TransientStateRegistry


@dataclass(frozen=True)
class I23Config:
    seed: int = 0
    episodes: int = 2_000
    source_change_probability: float = 0.28
    authority_revoke_probability: float = 0.30
    transition_survival_probability: float = 0.60
    stale_receipt_probability: float = 0.30
    receipt_error_fresh: float = 0.07
    receipt_error_stale: float = 0.24
    independent_error: float = 0.025
    independent_cost: float = 0.10
    hot_rematerialize_cost: float = 0.20


def _attach_receipt_lineage(
    runtime: TypedScopeRuntime,
    registry: EvidenceLineageRegistry,
    *,
    claim_ref: str,
    label: bool,
    stale: bool,
) -> None:
    for index in range(3):
        source = f"receipt-copy-{index}"
        if source not in registry.sources:
            registry.register_source(
                source,
                lineage_id="receipt-lineage-a",
                validity_steps=2 if stale else 20,
            )
        record = runtime.attach_evidence(0, source_ref=source)
        registry.annotate(
            record.evidence_id,
            source_id=source,
            claim_ref=claim_ref,
            observed_step=0,
            resolves_claim=True,
            value_ref="applied" if label else "absent",
        )


def _external_outcome_utility(
    *,
    truth_applied: bool,
    action: str,
    current_authority: bool,
) -> tuple[float, bool, bool, bool]:
    duplicate = False
    omitted = False
    unauthorized = False

    if truth_applied:
        if action in {"retry", "retry_same_identity"}:
            duplicate = True
    else:
        if action == "mark_complete":
            omitted = True
        elif action in {"retry", "retry_same_identity"}:
            unauthorized = not current_authority
        elif action in {"blocked", "unresolved", "abstain"}:
            # A blocked effect under revoked authority is not an authorization
            # failure. An unresolved/abstained effect remains an opportunity
            # cost rather than a fabricated completion.
            omitted = current_authority

    utility = 1.0
    utility -= 3.0 * float(duplicate)
    utility -= 2.0 * float(omitted)
    utility -= 5.0 * float(unauthorized)
    if action == "unresolved":
        utility -= 0.4
    return utility, duplicate, omitted, unauthorized


def run_i23(config: I23Config, policy: str) -> dict[str, float]:
    valid = {"typed", "opaque_snapshot", "discard_transient"}
    if policy not in valid:
        raise ValueError(f"unknown I23 policy: {policy}")

    rng = random.Random(config.seed)
    metrics: dict[str, float] = defaultdict(float)

    for episode in range(config.episodes):
        runtime = TypedScopeRuntime((0, 1, 2))
        runtime.lease_resource("compute", 0)
        evidence = EvidenceLineageRegistry(runtime)
        transient = TransientStateRegistry(runtime)
        protocol = PublicationProtocol(runtime)
        recovery = OrganismRecoveryCoordinator(runtime, evidence)

        scope_sensitive = rng.random() < 0.60
        hot = transient.register_hot_state(
            0,
            state_ref=f"hot:{episode}",
            source_ref=f"source:{episode}",
            source_version=1,
            scope_sensitive=scope_sensitive,
        )
        trace = transient.register_credit_trace(
            0,
            transition_ref=f"transition:{episode}",
            replay_source_ref=f"history:{episode}",
        )
        runtime.enqueue_event(1, due_step=1, external=True)

        publication = protocol.prepare_topology((0, 0, 1), consequence=0.2)
        published_before_crash = rng.random() < 0.50
        if published_before_crash:
            protocol.publish(publication.publication_id)

        # Changes while the process is down.
        current_source_version = (
            2 if rng.random() < config.source_change_probability else 1
        )
        if rng.random() < config.authority_revoke_probability:
            runtime.set_authority(1, False)
        current_authority = runtime.read_authority(1).allowed

        effect_applied = rng.random() < 0.55
        stale_receipt = rng.random() < config.stale_receipt_probability
        receipt_error = (
            config.receipt_error_stale
            if stale_receipt
            else config.receipt_error_fresh
        )
        primary_label = (
            not effect_applied
            if rng.random() < receipt_error
            else effect_applied
        )
        claim_ref = f"effect:{episode}"
        _attach_receipt_lineage(
            runtime,
            evidence,
            claim_ref=claim_ref,
            label=primary_label,
            stale=stale_receipt,
        )

        # Recover/complete topology publication first because transient-state
        # validity depends on the resulting authoritative epoch.
        if policy in {"typed", "discard_transient"}:
            publication_decision = recovery.recover_publication(
                publication,
                current_assurance_ok=True,
                current_validation_ok=True,
            )
            if publication_decision.action == "retry_publish":
                protocol.publish(publication.publication_id)
            elif publication_decision.action != "mark_complete":
                metrics["publication_recovery_failure"] += 1.0
        else:
            # Opaque snapshot restore remembers only "prepared". If publication
            # actually happened before crash it attempts the transition again;
            # authoritative typed state prevents corruption, but the recovery
            # layer itself failed to identify completion.
            if published_before_crash:
                metrics["duplicate_publication_attempt"] += 1.0
                metrics["utility"] -= 1.5
            else:
                protocol.publish(publication.publication_id)

        topology_changed = runtime.topology_epoch > 0
        transition_survives = (
            not topology_changed
            or rng.random() < config.transition_survival_probability
        )
        valid_transitions = (
            {trace.transition_ref} if transition_survives else {f"new:{episode}"}
        )

        # Hot-state recovery.
        hot_status = transient.assess_hot_recovery(
            hot.hot_id,
            current_source_version=current_source_version,
        )
        if policy == "typed":
            if hot_status.persisted_valid:
                metrics["utility"] += 1.0
                metrics["hot_persisted_use"] += 1.0
            elif hot_status.rematerializable:
                metrics["utility"] += 1.0 - config.hot_rematerialize_cost
                metrics["hot_rematerialized"] += 1.0
            else:
                metrics["hot_missed"] += 1.0
        elif policy == "opaque_snapshot":
            metrics["hot_persisted_use"] += 1.0
            if hot_status.persisted_valid:
                metrics["utility"] += 1.0
            else:
                metrics["stale_hot_use"] += 1.0
                metrics["utility"] -= 1.0
        else:
            metrics["hot_missed"] += 1.0

        # Delayed credit recovery.
        credit_status = transient.assess_credit_recovery(
            trace.trace_id,
            valid_transition_refs=valid_transitions,
        )
        if policy == "typed":
            if credit_status.exact_target_valid:
                metrics["correct_credit"] += 1.0
                metrics["utility"] += 1.0
            elif credit_status.replayable:
                metrics["credit_replay"] += 1.0
                metrics["credit_missed"] += 1.0
                metrics["utility"] -= 0.15
            else:
                metrics["credit_missed"] += 1.0
        elif policy == "opaque_snapshot":
            if credit_status.positional_restore_safe or credit_status.exact_target_valid:
                metrics["correct_credit"] += 1.0
                metrics["utility"] += 1.0
            else:
                metrics["false_credit"] += 1.0
                metrics["utility"] -= 1.5
        else:
            metrics["credit_missed"] += 1.0

        # Old-epoch event work. Typed/discard policies let the common runtime
        # forward by stable target identity and re-read current authority.
        if policy in {"typed", "discard_transient"}:
            processed = runtime.process_due_events(1)
            if len(processed) != 1:
                metrics["event_exactly_once_failure"] += 1.0
            metrics["event_forwarded"] += float(runtime.forwarded_events > 0)
            metrics["event_blocked_by_authority"] += float(
                runtime.blocked_external_events > 0
            )
            if current_authority:
                metrics["utility"] += 0.5
        else:
            # Opaque event route is restored with the old scope/permission view.
            if topology_changed:
                metrics["stale_event_route"] += 1.0
                metrics["utility"] -= 0.5
            if not current_authority:
                metrics["unauthorized_event"] += 1.0
                metrics["utility"] -= 3.0
            else:
                metrics["utility"] += 0.5

        # External execution evidence. Typed/discard use lineage-aware planning;
        # opaque restore trusts the three correlated receipt copies.
        if policy in {"typed", "discard_transient"}:
            plan = recovery.plan_external_execution_evidence(
                claim_ref,
                current_step=10,
                current_label=primary_label,
                estimated_current_error=0.20 if stale_receipt else 0.09,
                estimated_independent_error=0.04,
                consequence=4.0,
                duplicate_penalty=4.0,
                missed_penalty=1.5,
                independent_cost=config.independent_cost,
                unresolved_penalty=0.7,
            )
            if plan.action == "acquire_independent":
                metrics["independent_reconciliation"] += 1.0
                independent_label = (
                    not effect_applied
                    if rng.random() < config.independent_error
                    else effect_applied
                )
                observation = ExternalExecutionObservation(
                    "applied" if independent_label else "absent",
                    effect_specific=True,
                    evidence_ref=f"reconcile:{episode}",
                )
            elif plan.action == "use_current":
                observation = ExternalExecutionObservation(
                    "applied" if primary_label else "absent",
                    effect_specific=True,
                    evidence_ref=f"receipt:{episode}",
                )
            else:
                observation = ExternalExecutionObservation(
                    "unknown",
                    effect_specific=False,
                )
        else:
            observation = ExternalExecutionObservation(
                "applied" if primary_label else "absent",
                effect_specific=True,
                evidence_ref=f"snapshot-receipt:{episode}",
            )

        external_decision = recovery.recover_external_effect(
            ExternalEffectIntent(
                effect_id=f"effect:{episode}",
                target_ref="remote:1",
                consequence=4.0,
            ),
            target_id=1,
            observation=observation,
            receiver_recognizes_identity=False,
            duplicate_penalty=4.0,
            missed_penalty=1.5,
        )
        effect_utility, duplicate, omitted, unauthorized = _external_outcome_utility(
            truth_applied=effect_applied,
            action=external_decision.action,
            current_authority=current_authority,
        )
        metrics["utility"] += effect_utility
        metrics["duplicate_external_effect"] += float(duplicate)
        metrics["omitted_external_effect"] += float(omitted)
        metrics["unauthorized_external_retry"] += float(unauthorized)
        metrics["external_unresolved"] += float(
            external_decision.action == "unresolved"
        )

        invariants = runtime.semantic_invariants()
        metrics["semantic_invariant_failure"] += float(not all(invariants.values()))

    return {key: value / config.episodes for key, value in metrics.items()}
