from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I05CConfig:
    seed: int = 0
    tasks: int = 6_000
    shift_task: int = 3_000
    audit_cost: float = 0.08
    independent_error: float = 0.03
    correlated_error_fresh: float = 0.10
    correlated_error_stale: float = 0.32
    unresolved_probability: float = 0.22
    discovery_value: float = 2.0
    false_durable_penalty: float = 12.0
    decay: float = 0.995
    selective_value_threshold: float = 3.0


@dataclass
class _Rate:
    successes: float = 3.0
    total: float = 4.0

    @property
    def mean(self) -> float:
        return self.successes / self.total

    def update(self, success: bool, decay: float) -> None:
        self.successes *= decay
        self.total *= decay
        self.successes += float(success)
        self.total += 1.0


def _approved_candidate_correct_probability(family: int, regime: int) -> float:
    if regime == 0:
        return (0.93, 0.58)[family]
    return (0.60, 0.94)[family]


def run_i05c(config: I05CConfig, policy: str) -> dict[str, float]:
    """Learn verifier-family quality from correlated/partial audit evidence."""

    valid = {
        "none",
        "correlated_majority",
        "majority_plus_independent",
        "uniform_independent",
        "selective_independent",
        "missing_as_success",
    }
    if policy not in valid:
        raise ValueError(f"unknown I05C policy: {policy}")

    rng = random.Random(config.seed)
    rates = [_Rate(), _Rate()]
    metrics: dict[str, float] = defaultdict(float)

    for task_index in range(config.tasks):
        regime = int(task_index >= config.shift_task)
        family = rng.randrange(2)
        value = rng.choice((1.0, 2.0, 4.0))
        true_probability = _approved_candidate_correct_probability(family, regime)
        candidate_correct = rng.random() < true_probability

        estimate = rates[family].mean
        expected_utility = (
            estimate * config.discovery_value * value
            - (1.0 - estimate) * config.false_durable_penalty * value
        )
        accept = expected_utility > 0.0

        if accept:
            if candidate_correct:
                metrics["utility"] += config.discovery_value * value
                metrics["correct_durable_writes"] += 1.0
            else:
                metrics["utility"] -= config.false_durable_penalty * value
                metrics["false_durable_writes"] += 1.0
                if value >= 4.0:
                    metrics["high_value_false_writes"] += 1.0

        # The visible audit lineage consists of three copies of one underlying
        # source. Its error becomes much worse during the post-shift stale
        # window, so vote count cannot be treated as source independence.
        stale = config.shift_task <= task_index < config.shift_task + 500
        correlated_error = (
            config.correlated_error_stale
            if stale
            else config.correlated_error_fresh
        )
        lineage_a_label = (
            not candidate_correct
            if rng.random() < correlated_error
            else candidate_correct
        )

        independent_available = rng.random() >= config.unresolved_probability
        used_label: bool | None = None
        queried = False
        unresolved = False

        decision_boundary = (
            config.false_durable_penalty
            / (config.false_durable_penalty + config.discovery_value)
        )
        near_boundary = abs(estimate - decision_boundary) < 0.06
        selective_need = (
            stale
            or value >= config.selective_value_threshold
            or near_boundary
        )

        if policy == "none":
            pass
        elif policy == "correlated_majority":
            used_label = lineage_a_label
        elif policy == "majority_plus_independent":
            queried = True
            # Even when available, one independent vote cannot change a raw
            # 3:1 majority made from three copies of lineage A.
            if independent_available:
                _ = (
                    not candidate_correct
                    if rng.random() < config.independent_error
                    else candidate_correct
                )
            used_label = lineage_a_label
        elif policy == "uniform_independent":
            queried = True
            if independent_available:
                used_label = (
                    not candidate_correct
                    if rng.random() < config.independent_error
                    else candidate_correct
                )
            else:
                unresolved = True
        elif policy == "selective_independent":
            if selective_need:
                queried = True
                if independent_available:
                    used_label = (
                        not candidate_correct
                        if rng.random() < config.independent_error
                        else candidate_correct
                    )
                else:
                    unresolved = True
            else:
                used_label = lineage_a_label
        else:  # missing_as_success
            queried = True
            if independent_available:
                used_label = (
                    not candidate_correct
                    if rng.random() < config.independent_error
                    else candidate_correct
                )
            else:
                # Deliberately bad epistemic shortcut: no resolving evidence is
                # treated as though the approved candidate was correct.
                used_label = True

        if queried:
            metrics["utility"] -= config.audit_cost
            metrics["audit_queries"] += 1.0
        if used_label is not None:
            rates[family].update(used_label, config.decay)
            metrics["feedback_updates"] += 1.0
        if unresolved:
            metrics["unresolved_feedback"] += 1.0

        metrics["estimate_error"] += abs(rates[family].mean - true_probability)

    return {key: value / config.tasks for key, value in metrics.items()}
