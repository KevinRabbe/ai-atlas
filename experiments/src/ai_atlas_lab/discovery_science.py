from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class ScienceWorld:
    model: int

    def passive_observation(self) -> int:
        return 1

    def intervene(self, experiment: int) -> int:
        signatures = (
            (0, 1),
            (1, 0),
            (1, 1),
        )
        return signatures[self.model][experiment]


@dataclass(frozen=True)
class ScienceDiscoveryConfig:
    seed: int = 0
    task_count: int = 900
    experiment_cost: float = 0.05
    correct_theory_utility: float = 1.0
    wrong_theory_utility: float = -1.0
    unresolved_utility: float = 0.0


def _consistent(models: tuple[int, ...], experiment: int, outcome: int) -> tuple[int, ...]:
    return tuple(model for model in models if ScienceWorld(model).intervene(experiment) == outcome)


def _stop_value(models: tuple[int, ...], config: ScienceDiscoveryConfig) -> float:
    if len(models) == 1:
        return config.correct_theory_utility
    p_correct = 1.0 / len(models)
    assert_value = (
        p_correct * config.correct_theory_utility
        + (1.0 - p_correct) * config.wrong_theory_utility
    )
    return max(config.unresolved_utility, assert_value)


def _plan_value(
    models: tuple[int, ...],
    available: tuple[int, ...],
    config: ScienceDiscoveryConfig,
) -> tuple[float, int | None]:
    best_value = _stop_value(models, config)
    best_experiment: int | None = None
    for experiment in available:
        remaining = tuple(item for item in available if item != experiment)
        expected = -config.experiment_cost
        for outcome in (0, 1):
            subset = _consistent(models, experiment, outcome)
            if not subset:
                continue
            probability = len(subset) / len(models)
            future, _ = _plan_value(subset, remaining, config)
            expected += probability * future
        if expected > best_value:
            best_value = expected
            best_experiment = experiment
    return best_value, best_experiment


def run_teacher_baseline(config: ScienceDiscoveryConfig) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    correct = 0
    utility = 0.0
    for _ in range(config.task_count):
        hidden = rng.randrange(3)
        prediction = 0
        correct += int(prediction == hidden)
        utility += (
            config.correct_theory_utility
            if prediction == hidden
            else config.wrong_theory_utility
        )
    return {
        "theory_accuracy": correct / config.task_count,
        "unresolved_rate": 0.0,
        "avg_experiments": 0.0,
        "avg_net_utility": utility / config.task_count,
        "beyond_teacher": 0,
    }


def run_fixed_experiment(config: ScienceDiscoveryConfig) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    correct = 0
    utility = 0.0
    experiments = 0
    for _ in range(config.task_count):
        hidden = rng.randrange(3)
        world = ScienceWorld(hidden)
        outcome = world.intervene(0)
        models = _consistent((0, 1, 2), 0, outcome)
        prediction = models[0]
        correct += int(prediction == hidden)
        experiments += 1
        utility += (
            config.correct_theory_utility
            if prediction == hidden
            else config.wrong_theory_utility
        ) - config.experiment_cost
    accuracy = correct / config.task_count
    return {
        "theory_accuracy": accuracy,
        "unresolved_rate": 0.0,
        "avg_experiments": experiments / config.task_count,
        "avg_net_utility": utility / config.task_count,
        "beyond_teacher": int(accuracy > 1.0 / 3.0),
    }


def run_fixed_experiment_multi(config: ScienceDiscoveryConfig) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    correct = 0
    unresolved = 0
    utility = 0.0
    experiments = 0
    for _ in range(config.task_count):
        hidden = rng.randrange(3)
        world = ScienceWorld(hidden)
        outcome = world.intervene(0)
        models = _consistent((0, 1, 2), 0, outcome)
        experiments += 1
        if len(models) == 1:
            prediction = models[0]
            correct += int(prediction == hidden)
            terminal = (
                config.correct_theory_utility
                if prediction == hidden
                else config.wrong_theory_utility
            )
        else:
            unresolved += 1
            terminal = config.unresolved_utility
        utility += terminal - config.experiment_cost
    accuracy = correct / config.task_count
    return {
        "theory_accuracy": accuracy,
        "unresolved_rate": unresolved / config.task_count,
        "avg_experiments": experiments / config.task_count,
        "avg_net_utility": utility / config.task_count,
        "beyond_teacher": int(accuracy > 1.0 / 3.0),
    }


def run_active_science(config: ScienceDiscoveryConfig) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    correct = 0
    unresolved = 0
    utility = 0.0
    experiments = 0
    for _ in range(config.task_count):
        hidden = rng.randrange(3)
        world = ScienceWorld(hidden)
        models = (0, 1, 2)
        available = (0, 1)
        used = 0
        while len(models) > 1 and available:
            _, experiment = _plan_value(models, available, config)
            if experiment is None:
                break
            outcome = world.intervene(experiment)
            used += 1
            experiments += 1
            models = _consistent(models, experiment, outcome)
            available = tuple(item for item in available if item != experiment)

        if len(models) == 1:
            prediction = models[0]
            correct += int(prediction == hidden)
            terminal = (
                config.correct_theory_utility
                if prediction == hidden
                else config.wrong_theory_utility
            )
        else:
            unresolved += 1
            terminal = config.unresolved_utility
        utility += terminal - used * config.experiment_cost

    accuracy = correct / config.task_count
    return {
        "theory_accuracy": accuracy,
        "unresolved_rate": unresolved / config.task_count,
        "avg_experiments": experiments / config.task_count,
        "avg_net_utility": utility / config.task_count,
        "beyond_teacher": int(accuracy > 1.0 / 3.0),
    }


def run_science_discovery_experiment(
    config: ScienceDiscoveryConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    return [
        ("teacher_passive", run_teacher_baseline(config)),
        ("fixed_experiment", run_fixed_experiment(config)),
        ("fixed_experiment_multi", run_fixed_experiment_multi(config)),
        ("active_hypothesis_science", run_active_science(config)),
    ]
