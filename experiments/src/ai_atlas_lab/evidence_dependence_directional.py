from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I26BConfig:
    seed: int = 0
    tasks: int = 12_000
    parent_error: float = 0.25
    child_check_rate: float = 0.40
    child_check_error: float = 0.03
    independent_error: float = 0.18
    passive_resolution: float = 0.12
    decay: float = 0.995
    direction_threshold: float = 0.20
    min_parent_error_gap: float = 0.015


class DirectionalDependenceEstimator:
    """Infer a directional error-inheritance relation from resolved outcomes.

    If child errors are mostly a subset of parent errors while the child is
    measurably more accurate, the parent is a plausible upstream source whose
    failures are inherited by the child. The estimator is deliberately small:
    I26B tests whether direction carries useful semantics, not a mature graph-
    learning algorithm.
    """

    def __init__(self, config: I26BConfig) -> None:
        self.config = config
        self.sources = ("A", "B", "C", "D")
        self.error_rate = {source: 0.15 for source in self.sources}
        self.joint_error = {
            (left, right): 0.15**2
            for index, left in enumerate(self.sources)
            for right in self.sources[index + 1 :]
        }

    def _pair(self, left: str, right: str) -> tuple[str, str]:
        return (left, right) if left < right else (right, left)

    def observe_resolution(self, labels: dict[str, bool], truth: bool) -> None:
        decay = self.config.decay
        errors = {
            source: int(labels[source] != truth)
            for source in self.sources
        }
        for source, error in errors.items():
            self.error_rate[source] = (
                decay * self.error_rate[source]
                + (1.0 - decay) * error
            )
        for index, left in enumerate(self.sources):
            for right in self.sources[index + 1 :]:
                pair = (left, right)
                self.joint_error[pair] = (
                    decay * self.joint_error[pair]
                    + (1.0 - decay) * errors[left] * errors[right]
                )

    def direction_score(self, parent: str, child: str) -> float:
        if parent == child:
            return -1.0
        child_error = max(self.error_rate[child], 1e-9)
        joint = self.joint_error[self._pair(parent, child)]
        parent_given_child_error = joint / child_error
        inherited_error_excess = (
            parent_given_child_error - self.error_rate[parent]
        )
        accuracy_gap = self.error_rate[parent] - self.error_rate[child]
        if accuracy_gap <= self.config.min_parent_error_gap:
            return -1.0
        return inherited_error_excess

    def inferred_parent(self, child: str) -> str | None:
        candidates = [
            (self.direction_score(parent, child), parent)
            for parent in self.sources
            if parent != child
        ]
        score, parent = max(candidates)
        return parent if score > self.config.direction_threshold else None


def _record_count_decision(labels: dict[str, bool]) -> bool:
    votes = sum(labels[source] for source in ("A", "B", "C", "D"))
    if votes > 2:
        return True
    if votes < 2:
        return False
    # D is the intentionally independent comparator and resolves a 2:2 tie.
    return labels["D"]


def _symmetric_lineage_decision(labels: dict[str, bool]) -> bool:
    # Treat A/B/C as one undirected lineage, then compare that group with D.
    # If the two lineages disagree, D is the independent tie-breaker. This
    # intentionally demonstrates the information discarded by a symmetric
    # collapse: it cannot tell inherited agreement from child-originated repair.
    abc = sum(labels[source] for source in ("A", "B", "C")) >= 2
    return abc if abc == labels["D"] else labels["D"]


def _directional_decision(labels: dict[str, bool]) -> bool:
    parent = labels["A"]
    child_b = labels["B"]
    child_c = labels["C"]

    if child_b == child_c and child_b != parent:
        # Both derived sources independently departed from the upstream value.
        return child_b
    if (child_b != parent) ^ (child_c != parent):
        # One child carries a possible correction signal. Use the independent
        # comparator rather than counting inherited parent copies as two votes.
        return labels["D"]
    # All three agree: child agreement is mostly inherited consistency rather
    # than three independent confirmations.
    return parent


def _oracle_bayes_decision(labels: dict[str, bool], config: I26BConfig) -> bool:
    def likelihood(truth: bool) -> float:
        a = labels["A"]
        probability = (
            1.0 - config.parent_error if a == truth else config.parent_error
        )
        for child in ("B", "C"):
            child_value = labels[child]
            probability *= (
                (1.0 - config.child_check_rate)
                * float(child_value == a)
                + config.child_check_rate
                * (
                    1.0 - config.child_check_error
                    if child_value == truth
                    else config.child_check_error
                )
            )
        probability *= (
            1.0 - config.independent_error
            if labels["D"] == truth
            else config.independent_error
        )
        return probability

    return likelihood(True) >= likelihood(False)


def run_i26b(config: I26BConfig, policy: str) -> dict[str, float]:
    valid = {
        "record_count",
        "symmetric_lineage",
        "directional_provenance",
        "learned_direction",
        "oracle",
    }
    if policy not in valid:
        raise ValueError(f"unknown I26B policy: {policy}")

    rng = random.Random(config.seed)
    estimator = DirectionalDependenceEstimator(config)
    metrics: dict[str, float] = defaultdict(float)
    correction_cases = 0
    direction_established_step: int | None = None

    for step in range(config.tasks):
        truth = rng.random() < 0.5
        parent = (
            not truth if rng.random() < config.parent_error else truth
        )
        labels = {"A": parent}
        for child in ("B", "C"):
            if rng.random() < config.child_check_rate:
                labels[child] = (
                    not truth
                    if rng.random() < config.child_check_error
                    else truth
                )
            else:
                labels[child] = parent
        labels["D"] = (
            not truth
            if rng.random() < config.independent_error
            else truth
        )
        consequence = rng.choice((1.0, 2.0, 4.0, 8.0))

        learned_ready = (
            estimator.inferred_parent("B") == "A"
            and estimator.inferred_parent("C") == "A"
        )
        if learned_ready and direction_established_step is None:
            direction_established_step = step

        if policy == "record_count":
            decision = _record_count_decision(labels)
        elif policy == "symmetric_lineage":
            decision = _symmetric_lineage_decision(labels)
        elif policy == "directional_provenance":
            decision = _directional_decision(labels)
        elif policy == "learned_direction":
            decision = (
                _directional_decision(labels)
                if learned_ready
                else _record_count_decision(labels)
            )
        else:
            decision = _oracle_bayes_decision(labels, config)

        incorrect = decision != truth
        metrics["errors"] += float(incorrect)
        metrics["weighted_harm"] += float(incorrect) * consequence
        metrics["utility"] += (
            consequence if not incorrect else -3.0 * consequence
        )

        correction_case = (
            labels["B"] != labels["A"]
            or labels["C"] != labels["A"]
        )
        if correction_case:
            correction_cases += 1
            metrics["correction_errors"] += float(incorrect)

        if rng.random() < config.passive_resolution:
            estimator.observe_resolution(labels, truth)
            metrics["passive_resolutions"] += 1.0

    result = {
        "error_rate": metrics["errors"] / config.tasks,
        "weighted_harm": metrics["weighted_harm"] / config.tasks,
        "utility": metrics["utility"] / config.tasks,
        "correction_case_error": (
            metrics["correction_errors"] / correction_cases
            if correction_cases
            else 0.0
        ),
        "passive_resolutions": metrics["passive_resolutions"] / config.tasks,
        "direction_established_step": float(
            config.tasks
            if direction_established_step is None
            else direction_established_step
        ),
        "learned_parent_b_is_a": float(
            estimator.inferred_parent("B") == "A"
        ),
        "learned_parent_c_is_a": float(
            estimator.inferred_parent("C") == "A"
        ),
        "a_to_b_score": estimator.direction_score("A", "B"),
        "a_to_c_score": estimator.direction_score("A", "C"),
        "d_to_b_score": estimator.direction_score("D", "B"),
    }
    return result
