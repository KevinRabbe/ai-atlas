from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I17Config:
    seed: int = 0
    trials: int = 30_000
    stale_probability: float = 0.35
    shared_error_fresh: float = 0.06
    shared_error_stale: float = 0.28
    independent_error: float = 0.02
    independent_cost: float = 0.10
    duplicate_penalty: float = 2.0
    omission_penalty: float = 1.5
    selective_consequence_threshold: float = 3.0
    unresolved_penalty: float = 0.35


def run_i17(config: I17Config, policy: str) -> dict[str, float]:
    """Recover execution state from correlated and independent external evidence.

    Three visible receipts share one failure lineage. They therefore count as
    one evidence source even though a naive voter sees three agreeing records.
    An independent reconciliation source can be purchased separately.
    """

    valid = {
        "trust_primary",
        "correlated_majority",
        "majority_plus_independent",
        "uniform_independent",
        "selective_independent",
        "unresolved_on_conflict",
    }
    if policy not in valid:
        raise ValueError(f"unknown I17 policy: {policy}")

    rng = random.Random(config.seed)
    metrics: dict[str, float] = defaultdict(float)

    for _ in range(config.trials):
        effect_applied = rng.random() < 0.62
        stale = rng.random() < config.stale_probability
        consequence = rng.choice((1.0, 2.0, 4.0, 8.0))

        shared_error_probability = (
            config.shared_error_stale if stale else config.shared_error_fresh
        )
        shared_wrong = rng.random() < shared_error_probability
        lineage_a = not effect_applied if shared_wrong else effect_applied
        correlated_votes = (lineage_a, lineage_a, lineage_a)

        queried = False
        independent = None
        if policy in {
            "majority_plus_independent",
            "uniform_independent",
            "selective_independent",
            "unresolved_on_conflict",
        }:
            if policy in {"selective_independent", "unresolved_on_conflict"}:
                queried = stale or consequence >= config.selective_consequence_threshold
            else:
                queried = True

            if queried:
                independent = (
                    not effect_applied
                    if rng.random() < config.independent_error
                    else effect_applied
                )

        believed_applied: bool | None
        if policy == "trust_primary":
            believed_applied = lineage_a
        elif policy == "correlated_majority":
            believed_applied = sum(correlated_votes) >= 2
        elif policy == "majority_plus_independent":
            # Raw vote count still lets three correlated copies dominate one
            # genuinely independent observation.
            assert independent is not None
            believed_applied = (sum(correlated_votes) + int(independent)) >= 3
        elif policy == "uniform_independent":
            assert independent is not None
            believed_applied = independent
        elif policy == "selective_independent":
            believed_applied = independent if queried else lineage_a
        else:
            if queried and independent != lineage_a:
                believed_applied = None
            else:
                believed_applied = independent if queried else lineage_a

        duplicate = False
        omitted = False
        unresolved = believed_applied is None
        if believed_applied is True:
            omitted = not effect_applied
        elif believed_applied is False:
            duplicate = effect_applied

        weighted_harm = (
            float(duplicate) * config.duplicate_penalty * consequence
            + float(omitted) * config.omission_penalty * consequence
            + float(unresolved) * config.unresolved_penalty * consequence
        )
        utility = (
            1.2 * consequence
            - weighted_harm
            - float(queried) * config.independent_cost
        )

        metrics["utility"] += utility
        metrics["duplicate_effect"] += float(duplicate)
        metrics["omitted_effect"] += float(omitted)
        metrics["unresolved"] += float(unresolved)
        metrics["independent_queries"] += float(queried)
        metrics["weighted_harm"] += weighted_harm

    return {key: value / config.trials for key, value in metrics.items()}
