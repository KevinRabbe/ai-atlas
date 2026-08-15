from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random

from .evidence_derivation import EvidenceDerivationModel


@dataclass(frozen=True)
class I28AConfig:
    seed: int = 0
    tasks: int = 12_000
    late_start: int = 4_000
    parent_error: float = 0.25
    child_check_rate: float = 0.40
    child_check_error: float = 0.03
    independent_d_error: float = 0.18
    independent_e_error: float = 0.22
    passive_resolution: float = 0.12
    decay: float = 0.995
    inherited_agreement_weight: float = 0.15
    static_child_weight: float = 0.40


class DirectionalAggregationLearner:
    """Learn source quality plus conditional evidence along inferred derivation.

    The directional graph is supplied by `EvidenceDerivationModel`, not by
    hidden experiment labels. Once A->B/A->C are sufficiently supported, the
    learner models child correctness separately according to whether the parent
    itself was correct. This captures the key asymmetry between inherited
    agreement and child-originated correction.
    """

    def __init__(self, config: I28AConfig) -> None:
        self.config = config
        self.source_error = {
            source: 0.15 for source in ("A", "B", "C", "D", "E")
        }
        self.child_correct = {
            child: {True: 0.85, False: 0.85}
            for child in ("B", "C")
        }
        self.derivation = EvidenceDerivationModel(decay=config.decay)
        for source in self.source_error:
            self.derivation.register_source(source)

    def observe_resolution(self, labels: dict[str, bool], truth: bool) -> None:
        decay = self.config.decay
        for source, label in labels.items():
            self.source_error[source] = (
                decay * self.source_error[source]
                + (1.0 - decay) * float(label != truth)
            )

        parent_correct = labels["A"] == truth
        for child in ("B", "C"):
            self.child_correct[child][parent_correct] = (
                decay * self.child_correct[child][parent_correct]
                + (1.0 - decay) * float(labels[child] == truth)
            )

        self.derivation.observe_resolution(labels, truth)

    def direction_ready(self) -> bool:
        return (
            self.derivation.inferred_parent("B") == "A"
            and self.derivation.inferred_parent("C") == "A"
        )

    def directional_posterior(self, labels: dict[str, bool]) -> float:
        if not self.direction_ready():
            return _symmetric_group_posterior(labels, self.source_error)

        def likelihood(truth: bool) -> float:
            probability = 0.5
            for source in ("A", "D", "E"):
                error = _bounded_error(self.source_error[source])
                probability *= (1.0 - error) if labels[source] == truth else error

            parent_correct = labels["A"] == truth
            for child in ("B", "C"):
                correct_probability = self.child_correct[child][parent_correct]
                correct_probability = min(0.999, max(0.001, correct_probability))
                probability *= (
                    correct_probability
                    if labels[child] == truth
                    else 1.0 - correct_probability
                )
            return probability

        positive = likelihood(True)
        negative = likelihood(False)
        total = positive + negative
        return 0.5 if total <= 0.0 else positive / total


def _bounded_error(error: float) -> float:
    return min(0.499, max(0.001, error))


def _weight(error: float) -> float:
    bounded = _bounded_error(error)
    return math.log((1.0 - bounded) / bounded)


def _posterior_from_weighted_sources(
    labels: dict[str, bool],
    source_error: dict[str, float],
    *,
    factor,
) -> float:
    log_odds = 0.0
    for source, label in labels.items():
        contribution = _weight(source_error[source]) * factor(source, label, labels)
        log_odds += contribution if label else -contribution
    return 1.0 / (1.0 + math.exp(-log_odds))


def _independent_quality_posterior(
    labels: dict[str, bool],
    source_error: dict[str, float],
) -> float:
    return _posterior_from_weighted_sources(
        labels,
        source_error,
        factor=lambda _source, _label, _labels: 1.0,
    )


def _symmetric_group_posterior(
    labels: dict[str, bool],
    source_error: dict[str, float],
) -> float:
    """Current generic-group analogue: one contribution per failure group."""

    groups = (("A", "B", "C"), ("D",), ("E",))
    log_odds = 0.0
    used = 0
    for group in groups:
        best_error = min(source_error[source] for source in group)
        best_sources = [
            source
            for source in group
            if abs(source_error[source] - best_error) < 1e-12
        ]
        best_labels = {labels[source] for source in best_sources}
        if len(best_labels) != 1:
            continue
        source = min(best_sources)
        contribution = _weight(source_error[source])
        log_odds += contribution if labels[source] else -contribution
        used += 1
    if used == 0:
        return 0.5
    return 1.0 / (1.0 + math.exp(-log_odds))


def _static_inheritance_discount_posterior(
    labels: dict[str, bool],
    source_error: dict[str, float],
    config: I28AConfig,
) -> float:
    return _posterior_from_weighted_sources(
        labels,
        source_error,
        factor=lambda source, _label, _labels: (
            config.static_child_weight if source in {"B", "C"} else 1.0
        ),
    )


def _novelty_weighted_posterior(
    labels: dict[str, bool],
    source_error: dict[str, float],
    config: I28AConfig,
) -> float:
    def factor(source: str, label: bool, all_labels: dict[str, bool]) -> float:
        if source not in {"B", "C"}:
            return 1.0
        if label != all_labels["A"]:
            return 1.0
        return config.inherited_agreement_weight

    return _posterior_from_weighted_sources(
        labels,
        source_error,
        factor=factor,
    )


def _oracle_posterior(labels: dict[str, bool], config: I28AConfig) -> float:
    def likelihood(truth: bool) -> float:
        parent = labels["A"]
        probability = 0.5 * (
            1.0 - config.parent_error
            if parent == truth
            else config.parent_error
        )
        for child in ("B", "C"):
            child_label = labels[child]
            probability *= (
                (1.0 - config.child_check_rate) * float(child_label == parent)
                + config.child_check_rate
                * (
                    1.0 - config.child_check_error
                    if child_label == truth
                    else config.child_check_error
                )
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
    config: I28AConfig,
) -> tuple[bool, dict[str, bool], float]:
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
        if rng.random() < config.independent_d_error
        else truth
    )
    labels["E"] = (
        not truth
        if rng.random() < config.independent_e_error
        else truth
    )
    consequence = rng.choice((1.0, 2.0, 4.0, 8.0))
    return truth, labels, consequence


def run_i28a(config: I28AConfig, policy: str) -> dict[str, float]:
    valid = {
        "independent_quality",
        "symmetric_group",
        "inheritance_discount",
        "novelty_weighted",
        "learned_directional",
        "oracle",
    }
    if policy not in valid:
        raise ValueError(f"unknown I28A policy: {policy}")

    rng = random.Random(config.seed)
    learner = DirectionalAggregationLearner(config)
    metrics: dict[str, float] = defaultdict(float)
    departure_cases = 0
    late_cases = 0
    late_departure_cases = 0
    direction_established_step: int | None = None

    for step in range(config.tasks):
        truth, labels, consequence = _generate_task(rng, config)

        if policy == "independent_quality":
            posterior = _independent_quality_posterior(
                labels,
                learner.source_error,
            )
        elif policy == "symmetric_group":
            posterior = _symmetric_group_posterior(
                labels,
                learner.source_error,
            )
        elif policy == "inheritance_discount":
            posterior = _static_inheritance_discount_posterior(
                labels,
                learner.source_error,
                config,
            )
        elif policy == "novelty_weighted":
            posterior = _novelty_weighted_posterior(
                labels,
                learner.source_error,
                config,
            )
        elif policy == "learned_directional":
            posterior = learner.directional_posterior(labels)
        else:
            posterior = _oracle_posterior(labels, config)

        if direction_established_step is None and learner.direction_ready():
            direction_established_step = step

        decision = posterior >= 0.5
        incorrect = decision != truth
        outcome = 1.0 if truth else 0.0
        metrics["errors"] += float(incorrect)
        metrics["brier"] += (posterior - outcome) ** 2
        metrics["weighted_harm"] += float(incorrect) * consequence
        metrics["utility"] += (
            consequence if not incorrect else -3.0 * consequence
        )

        departure = (
            labels["B"] != labels["A"]
            or labels["C"] != labels["A"]
        )
        if departure:
            departure_cases += 1
            metrics["departure_errors"] += float(incorrect)

        if step >= config.late_start:
            late_cases += 1
            metrics["late_errors"] += float(incorrect)
            metrics["late_brier"] += (posterior - outcome) ** 2
            if departure:
                late_departure_cases += 1
                metrics["late_departure_errors"] += float(incorrect)

        if rng.random() < config.passive_resolution:
            learner.observe_resolution(labels, truth)
            metrics["passive_resolutions"] += 1.0

    return {
        "error_rate": metrics["errors"] / config.tasks,
        "brier": metrics["brier"] / config.tasks,
        "weighted_harm": metrics["weighted_harm"] / config.tasks,
        "utility": metrics["utility"] / config.tasks,
        "departure_error": (
            metrics["departure_errors"] / departure_cases
            if departure_cases
            else 0.0
        ),
        "late_error": (
            metrics["late_errors"] / late_cases if late_cases else 0.0
        ),
        "late_brier": (
            metrics["late_brier"] / late_cases if late_cases else 0.0
        ),
        "late_departure_error": (
            metrics["late_departure_errors"] / late_departure_cases
            if late_departure_cases
            else 0.0
        ),
        "direction_established_step": float(
            config.tasks
            if direction_established_step is None
            else direction_established_step
        ),
        "passive_resolutions": metrics["passive_resolutions"] / config.tasks,
        "learned_parent_b_is_a": float(
            learner.derivation.inferred_parent("B") == "A"
        ),
        "learned_parent_c_is_a": float(
            learner.derivation.inferred_parent("C") == "A"
        ),
    }
