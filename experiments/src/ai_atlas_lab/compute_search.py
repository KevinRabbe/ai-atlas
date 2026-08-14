from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Protocol

from .core import CostMeter

DIFFICULTIES = (0.15, 0.35, 0.80)
TASK_VALUES = (0.8, 1.5, 3.0)


@dataclass(frozen=True)
class SearchTask:
    true_values: tuple[float, ...]
    heuristics: tuple[float, ...]
    heuristic_sigma: float
    task_value: float
    evaluation_cost: float


@dataclass(frozen=True)
class SearchComputeConfig:
    seed: int = 0
    task_count: int = 1200
    evaluation_cost: float = 0.08
    fixed_budgets: tuple[int, ...] = (1, 3, 8, 20)
    optimism: float = 0.25


def generate_search_tasks(config: SearchComputeConfig) -> tuple[SearchTask, ...]:
    rng = random.Random(config.seed)
    tasks: list[SearchTask] = []
    for _ in range(config.task_count):
        count = rng.randint(6, 26)
        sigma = rng.choice(DIFFICULTIES)
        value = rng.choice(TASK_VALUES)
        true_values = [rng.gauss(0.0, 1.0) for _ in range(count)]
        heuristics = [true + rng.gauss(0.0, sigma) for true in true_values]
        order = sorted(range(count), key=lambda index: heuristics[index], reverse=True)
        tasks.append(SearchTask(tuple(true_values[index] for index in order), tuple(heuristics[index] for index in order), sigma, value, config.evaluation_cost))
    return tuple(tasks)


class SearchPolicy(Protocol):
    name: str
    def solve(self, task: SearchTask, cost: CostMeter) -> tuple[float, int]: ...


@dataclass(frozen=True)
class FixedSearchBudget:
    evaluations: int

    @property
    def name(self) -> str:
        return f"fixed_eval_{self.evaluations}"

    def solve(self, task: SearchTask, cost: CostMeter) -> tuple[float, int]:
        count = min(self.evaluations, len(task.true_values))
        cost.verifications += count
        cost.operations += count
        return max(task.true_values[:count]), count


@dataclass(frozen=True)
class AdaptiveValueOfSearch:
    optimism: float = 0.25
    name: str = "adaptive_value_of_search"

    def solve(self, task: SearchTask, cost: CostMeter) -> tuple[float, int]:
        best = -1e30
        used = 0
        for true_value, heuristic in zip(task.true_values, task.heuristics):
            if used:
                optimistic = heuristic + self.optimism * task.heuristic_sigma
                potential_improvement = max(0.0, optimistic - best)
                cost.operations += 3
                cost.comparisons += 1
                if task.task_value * potential_improvement <= task.evaluation_cost:
                    break
            best = max(best, true_value)
            used += 1
            cost.verifications += 1
            cost.operations += 1
        return best, used


def evaluate_search_policy(policy: SearchPolicy, tasks: tuple[SearchTask, ...]) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    regret = utility = used = 0.0
    by_difficulty = {difficulty: [] for difficulty in DIFFICULTIES}
    by_value = {value: [] for value in TASK_VALUES}
    for task in tasks:
        chosen, evaluations = policy.solve(task, cost)
        used += evaluations
        regret += max(task.true_values) - chosen
        utility += task.task_value * chosen - task.evaluation_cost * evaluations
        by_difficulty[task.heuristic_sigma].append(evaluations)
        by_value[task.task_value].append(evaluations)
    metrics: dict[str, float | int] = {
        "mean_regret": regret / len(tasks),
        "net_utility": utility / len(tasks),
        "avg_evaluations": used / len(tasks),
    }
    for difficulty, values in by_difficulty.items():
        metrics[f"avg_evaluations_sigma_{str(difficulty).replace('.', '_')}"] = sum(values) / len(values)
    for task_value, values in by_value.items():
        metrics[f"avg_evaluations_value_{str(task_value).replace('.', '_')}"] = sum(values) / len(values)
    return metrics, cost


def run_search_compute_experiment(config: SearchComputeConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    tasks = generate_search_tasks(config)
    policies: list[SearchPolicy] = [FixedSearchBudget(budget) for budget in config.fixed_budgets]
    policies.append(AdaptiveValueOfSearch(config.optimism))
    return [(policy.name, *evaluate_search_policy(policy, tasks)) for policy in policies]
