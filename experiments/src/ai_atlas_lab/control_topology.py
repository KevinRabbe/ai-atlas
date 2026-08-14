from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Protocol

from .core import CostMeter

OPERATIONS = ("retrieve", "verify", "observe", "search")


@dataclass(frozen=True)
class AllocationTask:
    required: frozenset[int]
    signals: tuple[float, ...]
    dependencies: tuple[tuple[int, int], ...]  # (prerequisite, dependent)
    prices: tuple[float, ...]

    def required_closure(self) -> frozenset[int]:
        selected = set(self.required)
        changed = True
        while changed:
            changed = False
            for prereq, dependent in self.dependencies:
                if dependent in selected and prereq not in selected:
                    selected.add(prereq)
                    changed = True
        return frozenset(selected)


class AllocationPolicy(Protocol):
    name: str

    def allocate(self, task: AllocationTask, cost: CostMeter) -> set[int]: ...


@dataclass(frozen=True)
class HierarchicalAllocator:
    threshold: float = 0.5
    price_sensitivity: float = 0.12

    @property
    def name(self) -> str:
        return "hierarchical_global"

    def allocate(self, task: AllocationTask, cost: CostMeter) -> set[int]:
        cost.operations += 2
        cost.reads += len(task.signals)
        selected = {
            idx
            for idx, signal in enumerate(task.signals)
            if signal >= self.threshold + self.price_sensitivity * task.prices[idx]
        }
        cost.comparisons += len(task.signals)

        changed = True
        while changed:
            changed = False
            for prereq, dependent in task.dependencies:
                cost.comparisons += 1
                if dependent in selected and prereq not in selected:
                    selected.add(prereq)
                    changed = True
        cost.messages += len(selected)
        cost.operations += len(selected)
        return selected


@dataclass(frozen=True)
class DistributedAllocator:
    rounds: int = 1
    threshold: float = 0.5
    price_sensitivity: float = 0.12

    @property
    def name(self) -> str:
        return f"distributed_r{self.rounds}"

    def allocate(self, task: AllocationTask, cost: CostMeter) -> set[int]:
        selected: set[int] = set()
        for idx, signal in enumerate(task.signals):
            cost.reads += 1
            cost.comparisons += 1
            cost.operations += 1
            if signal >= self.threshold + self.price_sensitivity * task.prices[idx]:
                selected.add(idx)

        for _ in range(self.rounds):
            additions: set[int] = set()
            for prereq, dependent in task.dependencies:
                if dependent in selected and prereq not in selected:
                    cost.messages += 1
                    cost.operations += 1
                    additions.add(prereq)
            if not additions:
                break
            selected.update(additions)
        cost.operations += len(selected)
        return selected


@dataclass(frozen=True)
class ControlTopologyExperimentConfig:
    seed: int = 0
    task_count: int = 1500
    dependency_density: float = 0.25
    required_probability: float = 0.28
    signal_noise: float = 0.55
    price_scale: float = 1.0
    distributed_rounds: tuple[int, ...] = (1, 3)


def generate_allocation_tasks(config: ControlTopologyExperimentConfig) -> tuple[AllocationTask, ...]:
    rng = random.Random(config.seed)
    tasks: list[AllocationTask] = []
    for _ in range(config.task_count):
        required = {idx for idx in range(len(OPERATIONS)) if rng.random() < config.required_probability}
        if not required:
            required.add(rng.randrange(len(OPERATIONS)))

        signals = tuple(
            rng.gauss(1.15 if idx in required else 0.0, config.signal_noise)
            for idx in range(len(OPERATIONS))
        )
        prices = tuple(config.price_scale * rng.uniform(0.5, 1.5) for _ in OPERATIONS)

        dependencies: list[tuple[int, int]] = []
        for dependent in range(1, len(OPERATIONS)):
            for prereq in range(dependent):
                if rng.random() < config.dependency_density:
                    dependencies.append((prereq, dependent))
        tasks.append(AllocationTask(frozenset(required), signals, tuple(dependencies), prices))
    return tuple(tasks)


def _evaluate_policy(policy: AllocationPolicy, tasks: Iterable[AllocationTask]) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    successes = missed = unnecessary = tail_total = tail_failures = selected_total = task_count = 0
    utility_total = 0.0

    for task in tasks:
        task_count += 1
        selected = policy.allocate(task, cost)
        truth = task.required_closure()
        task_success = truth.issubset(selected)
        successes += int(task_success)
        missed += len(truth - selected)
        unnecessary += len(selected - truth)
        selected_total += len(selected)
        if len(truth) >= 3:
            tail_total += 1
            tail_failures += int(not task_success)
        operation_price = sum(task.prices[idx] for idx in selected)
        utility_total += (1.0 if task_success else -1.0) - 0.04 * operation_price

    metrics: dict[str, float | int] = {
        "success_rate": successes / task_count,
        "avg_utility_before_coordination_cost": utility_total / task_count,
        "avg_selected_operations": selected_total / task_count,
        "missed_escalations_per_task": missed / task_count,
        "unnecessary_escalations_per_task": unnecessary / task_count,
        "messages_per_task": cost.messages / task_count,
        "operations_per_task": cost.operations / task_count,
        "tail_failure_rate": (tail_failures / tail_total) if tail_total else 0.0,
        "tail_task_count": tail_total,
    }
    metrics["avg_utility_with_coordination_cost"] = (
        utility_total - 0.01 * cost.messages - 0.002 * cost.operations
    ) / task_count
    return metrics, cost


def run_control_topology_experiment(config: ControlTopologyExperimentConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    tasks = generate_allocation_tasks(config)
    policies: list[AllocationPolicy] = [HierarchicalAllocator()]
    policies.extend(DistributedAllocator(rounds=n) for n in config.distributed_rounds)
    return [(policy.name, *_evaluate_policy(policy, tasks)) for policy in policies]
