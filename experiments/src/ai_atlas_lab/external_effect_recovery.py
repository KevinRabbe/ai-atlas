from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class ExternalLedgerConfig:
    seed: int = 0
    trials: int = 20_000
    query_cost: float = 0.06
    stable_identity_cost: float = 0.025
    effect_value: float = 1.0
    duplicate_penalty: float = 4.0
    missed_penalty: float = 1.0


@dataclass(frozen=True)
class PhysicalEffectConfig:
    seed: int = 0
    trials: int = 20_000
    query_cost: float = 0.04
    sensor_true_positive: float = 0.88
    sensor_false_positive: float = 0.18
    effect_value: float = 1.0
    duplicate_penalty: float = 4.0
    missed_penalty: float = 1.0


def _finish(metrics: dict[str, float], trials: int) -> dict[str, float]:
    return {key: value / trials for key, value in metrics.items()}


def run_external_ledger(config: ExternalLedgerConfig, policy: str) -> dict[str, float]:
    """Crash recovery when the external service can identify this exact effect.

    `stable_identity` represents replay with an external effect identity the
    receiver deduplicates. `reconcile` queries that exact identity before retry.
    Neither name commits the architecture to an HTTP idempotency-key product.
    """

    valid = {"blind_retry", "local_marker", "stable_identity", "reconcile", "abstain"}
    if policy not in valid:
        raise ValueError(f"unknown external-ledger policy: {policy}")

    rng = random.Random(config.seed)
    stages = ("before_send", "applied_unknown", "response_lost", "complete")
    weights = (0.16, 0.30, 0.24, 0.30)
    metrics: dict[str, float] = defaultdict(float)

    for _ in range(config.trials):
        stage = rng.choices(stages, weights)[0]
        already_applied = stage in {"applied_unknown", "response_lost", "complete"}
        query_cost = 0.0
        identity_cost = 0.0

        if stage == "complete":
            final_count = 1
        elif policy in {"blind_retry", "local_marker"}:
            final_count = int(already_applied) + 1
        elif policy == "stable_identity":
            identity_cost = config.stable_identity_cost
            # Retrying the same externally recognized effect identity is
            # deduplicated if the effect was already applied.
            final_count = 1
        elif policy == "reconcile":
            query_cost = config.query_cost
            # The query is about this exact effect identity, not an aggregate
            # world-state heuristic. Retry only when the effect is absent.
            final_count = 1
        else:  # abstain
            final_count = int(already_applied)

        duplicate = final_count > 1
        missed = final_count < 1
        utility = (
            config.effect_value
            - float(duplicate) * config.duplicate_penalty
            - float(missed) * config.missed_penalty
            - query_cost
            - identity_cost
        )

        metrics["utility"] += utility
        metrics["duplicate_effect"] += float(duplicate)
        metrics["missed_effect"] += float(missed)
        metrics["reconciliation_queries"] += float(query_cost > 0.0)
        metrics["identity_replays"] += float(
            policy == "stable_identity" and stage != "complete"
        )

    return _finish(metrics, config.trials)


def _posterior_applied(
    observed_applied: bool,
    config: PhysicalEffectConfig,
) -> float:
    # Conditional prior among crash-ambiguous physical trials: 0.48 already
    # applied versus 0.22 not yet applied. The remaining 0.30 are completed and
    # need no recovery decision.
    prior = 0.48 / (0.48 + 0.22)
    if observed_applied:
        numerator = prior * config.sensor_true_positive
        denominator = numerator + (1.0 - prior) * config.sensor_false_positive
    else:
        numerator = prior * (1.0 - config.sensor_true_positive)
        denominator = numerator + (1.0 - prior) * (1.0 - config.sensor_false_positive)
    return numerator / denominator


def run_physical_effect(config: PhysicalEffectConfig, policy: str) -> dict[str, float]:
    """Crash recovery when the outside world cannot identify this effect exactly.

    The only post-crash evidence is a noisy aggregate sensor. A stable local
    request identity cannot make the physical environment deduplicate an action
    it does not understand as the same effect.
    """

    valid = {"blind_retry", "abstain", "sensor_reconcile", "risk_sensitive"}
    if policy not in valid:
        raise ValueError(f"unknown physical-effect policy: {policy}")

    rng = random.Random(config.seed)
    stages = ("before_send", "applied_unknown", "complete")
    weights = (0.22, 0.48, 0.30)
    metrics: dict[str, float] = defaultdict(float)

    for _ in range(config.trials):
        stage = rng.choices(stages, weights)[0]
        already_applied = stage in {"applied_unknown", "complete"}
        queried = False

        if stage == "complete":
            final_count = 1
        else:
            if policy == "blind_retry":
                retry = True
            elif policy == "abstain":
                retry = False
            else:
                queried = True
                observed_applied = rng.random() < (
                    config.sensor_true_positive
                    if already_applied
                    else config.sensor_false_positive
                )
                if policy == "sensor_reconcile":
                    retry = not observed_applied
                else:
                    posterior = _posterior_applied(observed_applied, config)
                    retry_harm = posterior * config.duplicate_penalty
                    abstain_harm = (1.0 - posterior) * config.missed_penalty
                    retry = retry_harm < abstain_harm

            final_count = int(already_applied) + int(retry)

        duplicate = final_count > 1
        missed = final_count < 1
        utility = (
            config.effect_value
            - float(duplicate) * config.duplicate_penalty
            - float(missed) * config.missed_penalty
            - float(queried) * config.query_cost
        )

        metrics["utility"] += utility
        metrics["duplicate_effect"] += float(duplicate)
        metrics["missed_effect"] += float(missed)
        metrics["reconciliation_queries"] += float(queried)

    return _finish(metrics, config.trials)


def run_i15_experiment(seed: int = 0) -> dict[str, dict[str, dict[str, float]]]:
    ledger = ExternalLedgerConfig(seed=seed)
    physical = PhysicalEffectConfig(seed=seed)
    return {
        "external_ledger": {
            policy: run_external_ledger(ledger, policy)
            for policy in ("blind_retry", "stable_identity", "reconcile", "abstain")
        },
        "physical_effect": {
            policy: run_physical_effect(physical, policy)
            for policy in ("blind_retry", "abstain", "sensor_reconcile", "risk_sensitive")
        },
    }
