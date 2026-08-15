from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class I28CConfig:
    seed: int = 0
    tasks: int = 12_000
    late_start: int = 4_000
    rounds: int = 2
    initial_error: float = 0.22
    peer_copy_rate: float = 0.65
    self_check_error: float = 0.04
    independent_error: float = 0.18
    passive_resolution: float = 0.12
    decay: float = 0.995


class TemporalCycleLearner:
    """Learn versioned transition evidence for mutually adapting sources."""

    def __init__(self, config: I28CConfig) -> None:
        self.config = config
        self.source_error = {
            f"{source}{generation}": 0.18
            for source in ("A", "B")
            for generation in range(config.rounds + 1)
        }
        self.source_error["D"] = 0.18
        self.a_correct_given_parent = {True: 0.85, False: 0.50}
        self.b_correct_given_parent = {True: 0.85, False: 0.50}

    def observe_resolution(self, history: dict[str, bool], truth: bool) -> None:
        decay = self.config.decay
        for source_version, label in history.items():
            self.source_error[source_version] = (
                decay * self.source_error[source_version]
                + (1.0 - decay) * float(label != truth)
            )

        for generation in range(1, self.config.rounds + 1):
            b_previous_correct = history[f"B{generation - 1}"] == truth
            self.a_correct_given_parent[b_previous_correct] = (
                decay * self.a_correct_given_parent[b_previous_correct]
                + (1.0 - decay) * float(history[f"A{generation}"] == truth)
            )

            a_current_correct = history[f"A{generation}"] == truth
            self.b_correct_given_parent[a_current_correct] = (
                decay * self.b_correct_given_parent[a_current_correct]
                + (1.0 - decay) * float(history[f"B{generation}"] == truth)
            )


def _bounded_error(error: float) -> float:
    return min(0.499, max(0.001, error))


def _weight(error: float) -> float:
    bounded = _bounded_error(error)
    return math.log((1.0 - bounded) / bounded)


def _weighted_posterior(
    labels: dict[str, bool],
    errors: dict[str, float],
) -> float:
    log_odds = 0.0
    for source_version, label in labels.items():
        contribution = _weight(errors[source_version])
        log_odds += contribution if label else -contribution
    return 1.0 / (1.0 + math.exp(-log_odds))


def _static_cycle_collapse_posterior(
    history: dict[str, bool],
    learner: TemporalCycleLearner,
) -> float:
    generation = learner.config.rounds
    a = f"A{generation}"
    b = f"B{generation}"
    best = min((a, b), key=lambda source: learner.source_error[source])
    return _weighted_posterior(
        {best: history[best], "D": history["D"]},
        learner.source_error,
    )


def _versioned_root_posterior(
    history: dict[str, bool],
    root_by_version: dict[str, str],
    learner: TemporalCycleLearner,
) -> float:
    generation = learner.config.rounds
    a = f"A{generation}"
    b = f"B{generation}"
    if root_by_version[a] == root_by_version[b]:
        best = min((a, b), key=lambda source: learner.source_error[source])
        labels = {best: history[best], "D": history["D"]}
    else:
        labels = {
            a: history[a],
            b: history[b],
            "D": history["D"],
        }
    return _weighted_posterior(labels, learner.source_error)


def _learned_temporal_posterior(
    history: dict[str, bool],
    learner: TemporalCycleLearner,
) -> float:
    def likelihood(truth: bool) -> float:
        probability = 0.5
        for source_version in ("A0", "B0", "D"):
            error = _bounded_error(learner.source_error[source_version])
            probability *= (
                1.0 - error if history[source_version] == truth else error
            )

        for generation in range(1, learner.config.rounds + 1):
            b_previous_correct = history[f"B{generation - 1}"] == truth
            a_probability = min(
                0.999,
                max(0.001, learner.a_correct_given_parent[b_previous_correct]),
            )
            probability *= (
                a_probability
                if history[f"A{generation}"] == truth
                else 1.0 - a_probability
            )

            a_current_correct = history[f"A{generation}"] == truth
            b_probability = min(
                0.999,
                max(0.001, learner.b_correct_given_parent[a_current_correct]),
            )
            probability *= (
                b_probability
                if history[f"B{generation}"] == truth
                else 1.0 - b_probability
            )
        return probability

    positive = likelihood(True)
    negative = likelihood(False)
    total = positive + negative
    return 0.5 if total <= 0.0 else positive / total


def _oracle_temporal_posterior(
    history: dict[str, bool],
    config: I28CConfig,
) -> float:
    def likelihood(truth: bool) -> float:
        probability = 0.5
        for source_version, error in (
            ("A0", config.initial_error),
            ("B0", config.initial_error),
            ("D", config.independent_error),
        ):
            probability *= (
                1.0 - error if history[source_version] == truth else error
            )

        for generation in range(1, config.rounds + 1):
            for child, parent in (
                (f"A{generation}", f"B{generation - 1}"),
                (f"B{generation}", f"A{generation}"),
            ):
                child_label = history[child]
                parent_label = history[parent]
                probability *= (
                    config.peer_copy_rate * float(child_label == parent_label)
                    + (1.0 - config.peer_copy_rate)
                    * (
                        1.0 - config.self_check_error
                        if child_label == truth
                        else config.self_check_error
                    )
                )
        return probability

    positive = likelihood(True)
    negative = likelihood(False)
    total = positive + negative
    return 0.5 if total <= 0.0 else positive / total


def _generate_history(
    rng: random.Random,
    config: I28CConfig,
) -> tuple[bool, dict[str, bool], dict[str, str], float]:
    truth = rng.random() < 0.5
    history: dict[str, bool] = {}
    roots: dict[str, str] = {}

    for source in ("A", "B"):
        version = f"{source}0"
        history[version] = (
            not truth if rng.random() < config.initial_error else truth
        )
        roots[version] = version

    for generation in range(1, config.rounds + 1):
        a = f"A{generation}"
        b_previous = f"B{generation - 1}"
        if rng.random() < config.peer_copy_rate:
            history[a] = history[b_previous]
            roots[a] = roots[b_previous]
        else:
            history[a] = (
                not truth if rng.random() < config.self_check_error else truth
            )
            roots[a] = f"{a}:check"

        b = f"B{generation}"
        if rng.random() < config.peer_copy_rate:
            history[b] = history[a]
            roots[b] = roots[a]
        else:
            history[b] = (
                not truth if rng.random() < config.self_check_error else truth
            )
            roots[b] = f"{b}:check"

    history["D"] = (
        not truth if rng.random() < config.independent_error else truth
    )
    roots["D"] = "D"
    consequence = rng.choice((1.0, 2.0, 4.0, 8.0))
    return truth, history, roots, consequence


def run_i28c(config: I28CConfig, policy: str) -> dict[str, float]:
    valid = {
        "final_independent",
        "static_cycle_collapse",
        "history_independent",
        "versioned_root_groups",
        "learned_temporal",
        "oracle",
    }
    if policy not in valid:
        raise ValueError(f"unknown I28C policy: {policy}")

    rng = random.Random(config.seed)
    learner = TemporalCycleLearner(config)
    metrics: dict[str, float] = defaultdict(float)
    same_root_cases = 0
    distinct_root_cases = 0
    late_cases = 0

    for step in range(config.tasks):
        truth, history, roots, consequence = _generate_history(rng, config)
        generation = config.rounds
        final_a = f"A{generation}"
        final_b = f"B{generation}"

        if policy == "final_independent":
            posterior = _weighted_posterior(
                {
                    final_a: history[final_a],
                    final_b: history[final_b],
                    "D": history["D"],
                },
                learner.source_error,
            )
        elif policy == "static_cycle_collapse":
            posterior = _static_cycle_collapse_posterior(history, learner)
        elif policy == "history_independent":
            posterior = _weighted_posterior(history, learner.source_error)
        elif policy == "versioned_root_groups":
            posterior = _versioned_root_posterior(history, roots, learner)
        elif policy == "learned_temporal":
            posterior = _learned_temporal_posterior(history, learner)
        else:
            posterior = _oracle_temporal_posterior(history, config)

        decision = posterior >= 0.5
        incorrect = decision != truth
        outcome = 1.0 if truth else 0.0
        metrics["errors"] += float(incorrect)
        metrics["brier"] += (posterior - outcome) ** 2
        metrics["weighted_harm"] += float(incorrect) * consequence
        metrics["utility"] += (
            consequence if not incorrect else -3.0 * consequence
        )

        same_root = roots[final_a] == roots[final_b]
        if same_root:
            same_root_cases += 1
            metrics["same_root_errors"] += float(incorrect)
        else:
            distinct_root_cases += 1
            metrics["distinct_root_errors"] += float(incorrect)

        if step >= config.late_start:
            late_cases += 1
            metrics["late_errors"] += float(incorrect)
            metrics["late_brier"] += (posterior - outcome) ** 2

        if rng.random() < config.passive_resolution:
            learner.observe_resolution(history, truth)
            metrics["passive_resolutions"] += 1.0

    return {
        "error_rate": metrics["errors"] / config.tasks,
        "brier": metrics["brier"] / config.tasks,
        "weighted_harm": metrics["weighted_harm"] / config.tasks,
        "utility": metrics["utility"] / config.tasks,
        "same_root_rate": same_root_cases / config.tasks,
        "same_root_error": (
            metrics["same_root_errors"] / same_root_cases
            if same_root_cases
            else 0.0
        ),
        "distinct_root_error": (
            metrics["distinct_root_errors"] / distinct_root_cases
            if distinct_root_cases
            else 0.0
        ),
        "late_error": metrics["late_errors"] / late_cases if late_cases else 0.0,
        "late_brier": metrics["late_brier"] / late_cases if late_cases else 0.0,
        "passive_resolutions": metrics["passive_resolutions"] / config.tasks,
    }
