from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class I28BConfig:
    seed: int = 0
    tasks: int = 12_000
    late_start: int = 5_000
    parent_error: float = 0.25
    b_check_rate: float = 0.30
    b_check_error: float = 0.04
    c_local_copy_rate: float = 0.50
    c_check_rate: float = 0.30
    c_root_shortcut_rate: float = 0.20
    c_check_error: float = 0.03
    independent_d_error: float = 0.18
    independent_e_error: float = 0.22
    passive_resolution: float = 0.12
    decay: float = 0.995
    inherited_agreement_weight: float = 0.15

    def __post_init__(self) -> None:
        total = (
            self.c_local_copy_rate
            + self.c_check_rate
            + self.c_root_shortcut_rate
        )
        if abs(total - 1.0) > 1e-9:
            raise ValueError("C mode probabilities must sum to 1")


class MultiHopAggregationLearner:
    """Learn local and path-conditioned evidence behavior for A->B->C."""

    def __init__(self, config: I28BConfig) -> None:
        self.config = config
        self.source_error = {source: 0.15 for source in ("A", "B", "C", "D", "E")}
        self.b_correct = {True: 0.85, False: 0.85}
        self.c_local_correct = {True: 0.85, False: 0.85}
        self.c_path_correct = {
            (a_correct, b_correct): 0.85
            for a_correct in (False, True)
            for b_correct in (False, True)
        }

    def observe_resolution(self, labels: dict[str, bool], truth: bool) -> None:
        decay = self.config.decay
        for source, label in labels.items():
            self.source_error[source] = (
                decay * self.source_error[source]
                + (1.0 - decay) * float(label != truth)
            )

        a_correct = labels["A"] == truth
        b_correct = labels["B"] == truth
        self.b_correct[a_correct] = (
            decay * self.b_correct[a_correct]
            + (1.0 - decay) * float(labels["B"] == truth)
        )
        self.c_local_correct[b_correct] = (
            decay * self.c_local_correct[b_correct]
            + (1.0 - decay) * float(labels["C"] == truth)
        )
        self.c_path_correct[(a_correct, b_correct)] = (
            decay * self.c_path_correct[(a_correct, b_correct)]
            + (1.0 - decay) * float(labels["C"] == truth)
        )


def _bounded_error(error: float) -> float:
    return min(0.499, max(0.001, error))


def _weight(error: float) -> float:
    bounded = _bounded_error(error)
    return math.log((1.0 - bounded) / bounded)


def _posterior_from_factors(
    labels: dict[str, bool],
    errors: dict[str, float],
    factor,
) -> float:
    log_odds = 0.0
    for source, label in labels.items():
        contribution = _weight(errors[source]) * factor(source, label, labels)
        log_odds += contribution if label else -contribution
    return 1.0 / (1.0 + math.exp(-log_odds))


def _symmetric_group_posterior(
    labels: dict[str, bool],
    errors: dict[str, float],
) -> float:
    groups = (("A", "B", "C"), ("D",), ("E",))
    log_odds = 0.0
    used = 0
    for group in groups:
        best_error = min(errors[source] for source in group)
        best = [
            source
            for source in group
            if abs(errors[source] - best_error) < 1e-12
        ]
        best_labels = {labels[source] for source in best}
        if len(best_labels) != 1:
            continue
        source = min(best)
        contribution = _weight(errors[source])
        log_odds += contribution if labels[source] else -contribution
        used += 1
    return 0.5 if used == 0 else 1.0 / (1.0 + math.exp(-log_odds))


def _local_edge_novelty_posterior(
    labels: dict[str, bool],
    errors: dict[str, float],
    config: I28BConfig,
) -> float:
    def factor(source: str, label: bool, all_labels: dict[str, bool]) -> float:
        if source == "B":
            return 1.0 if label != all_labels["A"] else config.inherited_agreement_weight
        if source == "C":
            return 1.0 if label != all_labels["B"] else config.inherited_agreement_weight
        return 1.0

    return _posterior_from_factors(labels, errors, factor)


def _root_provenance_novelty_posterior(
    labels: dict[str, bool],
    errors: dict[str, float],
    config: I28BConfig,
) -> float:
    def factor(source: str, label: bool, all_labels: dict[str, bool]) -> float:
        if source in {"B", "C"}:
            return 1.0 if label != all_labels["A"] else config.inherited_agreement_weight
        return 1.0

    return _posterior_from_factors(labels, errors, factor)


def _learned_local_conditional_posterior(
    labels: dict[str, bool],
    learner: MultiHopAggregationLearner,
) -> float:
    def likelihood(truth: bool) -> float:
        probability = 0.5
        for source in ("A", "D", "E"):
            error = _bounded_error(learner.source_error[source])
            probability *= (1.0 - error) if labels[source] == truth else error

        a_correct = labels["A"] == truth
        b_correct_probability = min(0.999, max(0.001, learner.b_correct[a_correct]))
        probability *= (
            b_correct_probability
            if labels["B"] == truth
            else 1.0 - b_correct_probability
        )

        b_correct = labels["B"] == truth
        c_correct_probability = min(
            0.999,
            max(0.001, learner.c_local_correct[b_correct]),
        )
        probability *= (
            c_correct_probability
            if labels["C"] == truth
            else 1.0 - c_correct_probability
        )
        return probability

    positive = likelihood(True)
    negative = likelihood(False)
    total = positive + negative
    return 0.5 if total <= 0.0 else positive / total


def _learned_path_conditional_posterior(
    labels: dict[str, bool],
    learner: MultiHopAggregationLearner,
) -> float:
    def likelihood(truth: bool) -> float:
        probability = 0.5
        for source in ("A", "D", "E"):
            error = _bounded_error(learner.source_error[source])
            probability *= (1.0 - error) if labels[source] == truth else error

        a_correct = labels["A"] == truth
        b_correct_probability = min(0.999, max(0.001, learner.b_correct[a_correct]))
        probability *= (
            b_correct_probability
            if labels["B"] == truth
            else 1.0 - b_correct_probability
        )

        b_correct = labels["B"] == truth
        c_correct_probability = min(
            0.999,
            max(0.001, learner.c_path_correct[(a_correct, b_correct)]),
        )
        probability *= (
            c_correct_probability
            if labels["C"] == truth
            else 1.0 - c_correct_probability
        )
        return probability

    positive = likelihood(True)
    negative = likelihood(False)
    total = positive + negative
    return 0.5 if total <= 0.0 else positive / total


def _oracle_posterior(labels: dict[str, bool], config: I28BConfig) -> float:
    def likelihood(truth: bool) -> float:
        a = labels["A"]
        b = labels["B"]
        c = labels["C"]
        probability = 0.5 * (
            1.0 - config.parent_error if a == truth else config.parent_error
        )
        probability *= (
            (1.0 - config.b_check_rate) * float(b == a)
            + config.b_check_rate
            * (
                1.0 - config.b_check_error if b == truth else config.b_check_error
            )
        )
        probability *= (
            config.c_local_copy_rate * float(c == b)
            + config.c_check_rate
            * (
                1.0 - config.c_check_error if c == truth else config.c_check_error
            )
            + config.c_root_shortcut_rate * float(c == a)
        )
        for source, error in (
            ("D", config.independent_d_error),
            ("E", config.independent_e_error),
        ):
            probability *= (1.0 - error) if labels[source] == truth else error
        return probability

    positive = likelihood(True)
    negative = likelihood(False)
    total = positive + negative
    return 0.5 if total <= 0.0 else positive / total


def _generate_task(
    rng: random.Random,
    config: I28BConfig,
) -> tuple[bool, dict[str, bool], float]:
    truth = rng.random() < 0.5
    a = not truth if rng.random() < config.parent_error else truth

    if rng.random() < config.b_check_rate:
        b = not truth if rng.random() < config.b_check_error else truth
    else:
        b = a

    mode = rng.random()
    if mode < config.c_local_copy_rate:
        c = b
    elif mode < config.c_local_copy_rate + config.c_check_rate:
        c = not truth if rng.random() < config.c_check_error else truth
    else:
        c = a

    labels = {"A": a, "B": b, "C": c}
    labels["D"] = (
        not truth if rng.random() < config.independent_d_error else truth
    )
    labels["E"] = (
        not truth if rng.random() < config.independent_e_error else truth
    )
    consequence = rng.choice((1.0, 2.0, 4.0, 8.0))
    return truth, labels, consequence


def run_i28b(config: I28BConfig, policy: str) -> dict[str, float]:
    valid = {
        "symmetric_group",
        "local_edge_novelty",
        "root_provenance_novelty",
        "learned_local_conditional",
        "learned_path_conditional",
        "oracle",
    }
    if policy not in valid:
        raise ValueError(f"unknown I28B policy: {policy}")

    rng = random.Random(config.seed)
    learner = MultiHopAggregationLearner(config)
    metrics: dict[str, float] = defaultdict(float)
    bypass_cases = 0
    late_cases = 0
    late_bypass_cases = 0

    for step in range(config.tasks):
        truth, labels, consequence = _generate_task(rng, config)

        if policy == "symmetric_group":
            posterior = _symmetric_group_posterior(labels, learner.source_error)
        elif policy == "local_edge_novelty":
            posterior = _local_edge_novelty_posterior(
                labels,
                learner.source_error,
                config,
            )
        elif policy == "root_provenance_novelty":
            posterior = _root_provenance_novelty_posterior(
                labels,
                learner.source_error,
                config,
            )
        elif policy == "learned_local_conditional":
            posterior = _learned_local_conditional_posterior(labels, learner)
        elif policy == "learned_path_conditional":
            posterior = _learned_path_conditional_posterior(labels, learner)
        else:
            posterior = _oracle_posterior(labels, config)

        decision = posterior >= 0.5
        incorrect = decision != truth
        outcome = 1.0 if truth else 0.0
        metrics["errors"] += float(incorrect)
        metrics["brier"] += (posterior - outcome) ** 2
        metrics["weighted_harm"] += float(incorrect) * consequence
        metrics["utility"] += (
            consequence if not incorrect else -3.0 * consequence
        )

        # This pattern is the path-provenance discriminator: B departed from A,
        # while C returned to A. A local C-vs-B novelty rule can incorrectly
        # treat C as another independent departure even when it consulted A.
        bypass_pattern = labels["A"] != labels["B"] and labels["C"] == labels["A"]
        if bypass_pattern:
            bypass_cases += 1
            metrics["bypass_errors"] += float(incorrect)

        if step >= config.late_start:
            late_cases += 1
            metrics["late_errors"] += float(incorrect)
            metrics["late_brier"] += (posterior - outcome) ** 2
            if bypass_pattern:
                late_bypass_cases += 1
                metrics["late_bypass_errors"] += float(incorrect)

        if rng.random() < config.passive_resolution:
            learner.observe_resolution(labels, truth)
            metrics["passive_resolutions"] += 1.0

    return {
        "error_rate": metrics["errors"] / config.tasks,
        "brier": metrics["brier"] / config.tasks,
        "weighted_harm": metrics["weighted_harm"] / config.tasks,
        "utility": metrics["utility"] / config.tasks,
        "bypass_error": (
            metrics["bypass_errors"] / bypass_cases if bypass_cases else 0.0
        ),
        "late_error": (
            metrics["late_errors"] / late_cases if late_cases else 0.0
        ),
        "late_brier": (
            metrics["late_brier"] / late_cases if late_cases else 0.0
        ),
        "late_bypass_error": (
            metrics["late_bypass_errors"] / late_bypass_cases
            if late_bypass_cases
            else 0.0
        ),
        "bypass_case_rate": bypass_cases / config.tasks,
        "passive_resolutions": metrics["passive_resolutions"] / config.tasks,
    }
