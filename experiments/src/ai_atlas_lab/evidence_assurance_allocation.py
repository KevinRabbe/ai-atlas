from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I20Config:
    seed: int = 0
    trials: int = 30_000
    stale_probability: float = 0.30
    primary_error_fresh: float = 0.07
    primary_error_stale: float = 0.24
    estimated_primary_error_fresh: float = 0.09
    estimated_primary_error_stale: float = 0.20
    independent_error: float = 0.025
    estimated_independent_error: float = 0.04
    independent_unavailable: float = 0.18
    independent_cost: float = 0.18


def _penalties(family: str) -> tuple[float, float, float]:
    """Return false-positive, false-negative, unresolved penalties.

    External claims: true means "effect applied". A false positive may omit a
    needed effect; a false negative may duplicate one.

    Metacognitive claims: true means "approved verifier/candidate family is
    safe enough". A false positive can promote bad durable state; a false
    negative misses a useful improvement.
    """

    if family == "external":
        return 1.5, 4.0, 0.65
    if family == "metacognitive":
        return 6.0, 1.2, 0.80
    raise ValueError(f"unknown evidence family: {family}")


def run_i20(config: I20Config, policy: str) -> dict[str, float]:
    """Use one evidence-allocation rule across external and metacognitive claims.

    The value-aware policy receives imperfect source-error estimates, not hidden
    truth. It sees whether the current lineage is stale, the decision
    consequence, and the current lineage's binary conclusion. Three visible
    copies remain one failure lineage; their record count does not improve the
    estimated error probability.
    """

    valid = {
        "record_count_confidence",
        "stale_only",
        "uniform_independent",
        "lineage_value",
    }
    if policy not in valid:
        raise ValueError(f"unknown I20 policy: {policy}")

    rng = random.Random(config.seed)
    metrics: dict[str, float] = defaultdict(float)

    for _ in range(config.trials):
        family = "external" if rng.random() < 0.5 else "metacognitive"
        truth = rng.random() < 0.5
        stale = rng.random() < config.stale_probability
        consequence = rng.choice((1.0, 2.0, 4.0, 8.0))

        actual_primary_error = (
            config.primary_error_stale if stale else config.primary_error_fresh
        )
        estimated_primary_error = (
            config.estimated_primary_error_stale
            if stale
            else config.estimated_primary_error_fresh
        )
        primary_label = (
            not truth if rng.random() < actual_primary_error else truth
        )

        # The visible interface exposes three records, but all three descend
        # from the same lineage and therefore carry the same label/failure.
        visible_records = (primary_label, primary_label, primary_label)
        false_positive_penalty, false_negative_penalty, unresolved_penalty = _penalties(
            family
        )

        wrong_penalty = (
            false_positive_penalty if primary_label else false_negative_penalty
        )
        current_expected_harm = (
            estimated_primary_error * wrong_penalty * consequence
        )
        average_independent_wrong_penalty = (
            false_positive_penalty + false_negative_penalty
        ) / 2.0
        expected_independent_harm = (
            config.estimated_independent_error
            * average_independent_wrong_penalty
            * consequence
        )

        queried = False
        unresolved = False
        decision: bool | None

        if policy == "record_count_confidence":
            # Naive vote-count confidence: three agreeing records are treated as
            # strong confirmation despite sharing one failure lineage.
            decision = sum(visible_records) >= 2

        elif policy == "stale_only":
            queried = stale
            if not queried:
                decision = primary_label
            elif rng.random() < config.independent_unavailable:
                decision = None
                unresolved = True
            else:
                decision = (
                    not truth
                    if rng.random() < config.independent_error
                    else truth
                )

        elif policy == "uniform_independent":
            queried = True
            if rng.random() < config.independent_unavailable:
                decision = None
                unresolved = True
            else:
                decision = (
                    not truth
                    if rng.random() < config.independent_error
                    else truth
                )

        else:  # lineage_value
            expected_gain = (
                current_expected_harm
                - expected_independent_harm
                - config.independent_cost
            )
            queried = expected_gain > 0.0
            if not queried:
                decision = primary_label
            elif rng.random() < config.independent_unavailable:
                # Missing resolution is not positive evidence. Decide whether
                # retaining uncertainty is cheaper than trusting the current
                # imperfect lineage; otherwise retain the primary decision.
                if current_expected_harm > unresolved_penalty * consequence:
                    decision = None
                    unresolved = True
                else:
                    decision = primary_label
            else:
                decision = (
                    not truth
                    if rng.random() < config.independent_error
                    else truth
                )

        if queried:
            metrics["independent_queries"] += 1.0

        if unresolved:
            harm = unresolved_penalty * consequence
            metrics["unresolved"] += 1.0
        elif decision == truth:
            harm = 0.0
        elif decision:
            harm = false_positive_penalty * consequence
            metrics["false_positive"] += 1.0
        else:
            harm = false_negative_penalty * consequence
            metrics["false_negative"] += 1.0

        metrics["weighted_harm"] += harm
        metrics[f"{family}_weighted_harm"] += harm
        metrics[f"{family}_count"] += 1.0
        metrics["utility"] += (
            1.2 * consequence
            - harm
            - float(queried) * config.independent_cost
        )

    result = {key: value / config.trials for key, value in metrics.items()}
    for family in ("external", "metacognitive"):
        family_count = metrics[f"{family}_count"]
        result[f"{family}_harm_per_family_task"] = (
            metrics[f"{family}_weighted_harm"] / family_count
            if family_count
            else 0.0
        )
    return result
