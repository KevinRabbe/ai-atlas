from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Protocol

from .core import CostMeter

RESOURCES = ("memory", "compute", "observe", "verify")
RESOURCE_QUALITY = (
    (0.93, 0.68, 0.78, 0.72),
    (0.70, 0.92, 0.80, 0.76),
    (0.76, 0.77, 0.95, 0.82),
    (0.67, 0.78, 0.83, 0.90),
)
PRICE_REGIMES = (
    (0.25, 0.50, 1.10, 2.50),
    (1.30, 0.75, 0.42, 1.25),
    (0.95, 0.80, 0.70, 0.55),
)
VALUES = (0.8, 1.6, 3.2)


@dataclass(frozen=True)
class ResourceTask:
    task_type: int
    value: float
    price_regime: int
    outcomes: tuple[bool, bool, bool, bool]


@dataclass(frozen=True)
class CrossResourceConfig:
    seed: int = 0
    warmup_tasks: int = 1000
    measured_tasks_per_regime: int = 2000
    epsilon: float = 0.04
    prior_successes: float = 8.0
    prior_trials: float = 10.0


def generate_resource_tasks(config: CrossResourceConfig) -> tuple[ResourceTask, ...]:
    rng = random.Random(config.seed)
    result: list[ResourceTask] = []
    total = config.warmup_tasks + config.measured_tasks_per_regime * len(PRICE_REGIMES)
    for index in range(total):
        regime = 0 if index < config.warmup_tasks else min(len(PRICE_REGIMES) - 1, (index - config.warmup_tasks) // config.measured_tasks_per_regime)
        task_type = rng.randrange(len(RESOURCE_QUALITY))
        value = rng.choice(VALUES)
        outcomes = tuple(rng.random() < RESOURCE_QUALITY[task_type][resource] for resource in range(len(RESOURCES)))
        result.append(ResourceTask(task_type, value, regime, outcomes))
    return tuple(result)


def true_expected_utility(task: ResourceTask, resource: int) -> float:
    probability = RESOURCE_QUALITY[task.task_type][resource]
    return task.value * (2 * probability - 1) - PRICE_REGIMES[task.price_regime][resource]


def oracle_resource(task: ResourceTask) -> int:
    return max(range(len(RESOURCES)), key=lambda resource: true_expected_utility(task, resource))


class Policy(Protocol):
    name: str
    def choose(self, task: ResourceTask, cost: CostMeter) -> int: ...
    def update(self, task: ResourceTask, resource: int, cost: CostMeter) -> None: ...


class QualityLearner:
    def __init__(self, config: CrossResourceConfig, seed: int) -> None:
        self.epsilon = config.epsilon
        self.rng = random.Random(seed)
        self.successes = [[config.prior_successes for _ in RESOURCES] for _ in RESOURCE_QUALITY]
        self.trials = [[config.prior_trials for _ in RESOURCES] for _ in RESOURCE_QUALITY]

    def estimate(self, task_type: int, resource: int, cost: CostMeter) -> float:
        cost.reads += 2
        cost.operations += 1
        return self.successes[task_type][resource] / self.trials[task_type][resource]

    def update(self, task: ResourceTask, resource: int, cost: CostMeter) -> None:
        self.trials[task.task_type][resource] += 1.0
        self.successes[task.task_type][resource] += 1.0 if task.outcomes[resource] else 0.0
        cost.writes += 2
        cost.operations += 1


class AdaptiveCrossResourcePolicy(QualityLearner):
    name = "adaptive_cross_resource"

    def choose(self, task: ResourceTask, cost: CostMeter) -> int:
        if self.rng.random() < self.epsilon:
            cost.operations += 1
            return self.rng.randrange(len(RESOURCES))
        prices = PRICE_REGIMES[task.price_regime]
        scores: list[float] = []
        for resource in range(len(RESOURCES)):
            probability = self.estimate(task.task_type, resource, cost)
            scores.append(task.value * (2 * probability - 1) - prices[resource])
            cost.operations += 4
        cost.comparisons += len(RESOURCES) - 1
        return max(range(len(RESOURCES)), key=scores.__getitem__)


class FrozenInitialEconomicsPolicy(QualityLearner):
    name = "frozen_initial_economics"

    def choose(self, task: ResourceTask, cost: CostMeter) -> int:
        if self.rng.random() < self.epsilon:
            cost.operations += 1
            return self.rng.randrange(len(RESOURCES))
        prices = PRICE_REGIMES[0]
        scores: list[float] = []
        for resource in range(len(RESOURCES)):
            probability = self.estimate(task.task_type, resource, cost)
            scores.append(task.value * (2 * probability - 1) - prices[resource])
            cost.operations += 4
        cost.comparisons += len(RESOURCES) - 1
        return max(range(len(RESOURCES)), key=scores.__getitem__)


class ResourceLocalBidPolicy(QualityLearner):
    name = "resource_local_bids"

    def choose(self, task: ResourceTask, cost: CostMeter) -> int:
        if self.rng.random() < self.epsilon:
            cost.messages += 1
            cost.operations += 1
            return self.rng.randrange(len(RESOURCES))
        prices = PRICE_REGIMES[task.price_regime]
        bids: list[tuple[float, int]] = []
        for resource in range(len(RESOURCES)):
            probability = self.estimate(task.task_type, resource, cost)
            bid = task.value * (2 * probability - 1) - prices[resource]
            bids.append((bid, resource))
            cost.messages += 1
            cost.operations += 4
        cost.messages += 1
        cost.comparisons += len(RESOURCES) - 1
        return max(bids)[1]


def evaluate_cross_resource_policy(policy: Policy, tasks: tuple[ResourceTask, ...], config: CrossResourceConfig) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    for task in tasks[:config.warmup_tasks]:
        resource = policy.choose(task, cost)
        policy.update(task, resource, cost)

    stats = {regime: {"n": 0, "correct": 0, "spend": 0.0, "regret": 0.0, "expected": 0.0, "choices": [0] * len(RESOURCES)} for regime in range(len(PRICE_REGIMES))}
    for task in tasks[config.warmup_tasks:]:
        resource = policy.choose(task, cost)
        policy.update(task, resource, cost)
        row = stats[task.price_regime]
        row["n"] += 1
        row["correct"] += int(task.outcomes[resource])
        row["spend"] += PRICE_REGIMES[task.price_regime][resource]
        row["expected"] += true_expected_utility(task, resource)
        row["regret"] += true_expected_utility(task, oracle_resource(task)) - true_expected_utility(task, resource)
        row["choices"][resource] += 1

    metrics: dict[str, float | int] = {}
    total_measured = sum(row["n"] for row in stats.values())
    for regime, row in stats.items():
        count = row["n"]
        metrics[f"accuracy_regime_{regime}"] = row["correct"] / count
        metrics[f"spend_regime_{regime}"] = row["spend"] / count
        metrics[f"regret_regime_{regime}"] = row["regret"] / count
        metrics[f"expected_utility_regime_{regime}"] = row["expected"] / count
        for resource, name in enumerate(RESOURCES):
            metrics[f"choice_{name}_regime_{regime}"] = row["choices"][resource] / count
    shifted_count = sum(stats[regime]["n"] for regime in range(1, len(PRICE_REGIMES)))
    metrics["post_shift_mean_regret"] = sum(stats[regime]["regret"] for regime in range(1, len(PRICE_REGIMES))) / shifted_count
    metrics["messages_per_measured_task"] = cost.messages / total_measured
    metrics["operations_per_measured_task"] = cost.operations / total_measured
    return metrics, cost


def run_cross_resource_experiment(config: CrossResourceConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    tasks = generate_resource_tasks(config)
    policies: list[Policy] = [
        AdaptiveCrossResourcePolicy(config, config.seed + 1),
        FrozenInitialEconomicsPolicy(config, config.seed + 1),
        ResourceLocalBidPolicy(config, config.seed + 1),
    ]
    return [(policy.name, *evaluate_cross_resource_policy(policy, tasks, config)) for policy in policies]
