from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Protocol

from .core import CostMeter


@dataclass(frozen=True)
class VerificationTask:
    value: float
    confidence: float
    base_correct: bool

    @property
    def expected_gain(self) -> float:
        return self.value * (1.0 - self.confidence)


class ContentionPolicy(Protocol):
    name: str
    def allocate(self, tasks: tuple[VerificationTask, ...], slots: int, cost: CostMeter) -> set[int]: ...


@dataclass(frozen=True)
class HierarchicalBatchAllocator:
    name: str = "hierarchical_batch"

    def allocate(self, tasks: tuple[VerificationTask, ...], slots: int, cost: CostMeter) -> set[int]:
        cost.reads += len(tasks) * 2
        cost.operations += len(tasks) * 2
        ranked = sorted(range(len(tasks)), key=lambda i: tasks[i].expected_gain, reverse=True)
        cost.comparisons += max(0, len(tasks) - 1)
        selected = set(ranked[:slots])
        cost.messages += len(selected)
        return selected


@dataclass(frozen=True)
class DistributedThresholdAllocator:
    request_threshold: float = 0.16
    name: str = "distributed_threshold"

    def allocate(self, tasks: tuple[VerificationTask, ...], slots: int, cost: CostMeter) -> set[int]:
        requests: list[int] = []
        for idx, task in enumerate(tasks):
            cost.reads += 2
            cost.operations += 2
            cost.comparisons += 1
            if task.expected_gain >= self.request_threshold:
                requests.append(idx)
                cost.messages += 1
        return set(requests[:slots])


@dataclass(frozen=True)
class DistributedAuctionAllocator:
    request_threshold: float = 0.04
    name: str = "distributed_resource_auction"

    def allocate(self, tasks: tuple[VerificationTask, ...], slots: int, cost: CostMeter) -> set[int]:
        bids: list[tuple[float, int]] = []
        for idx, task in enumerate(tasks):
            cost.reads += 2
            cost.operations += 2
            cost.comparisons += 1
            gain = task.expected_gain
            if gain >= self.request_threshold:
                bids.append((gain, idx))
                cost.messages += 1
        bids.sort(reverse=True)
        cost.comparisons += max(0, len(bids) - 1)
        selected = {idx for _gain, idx in bids[:slots]}
        cost.messages += len(selected)
        return selected


@dataclass(frozen=True)
class ControlContentionExperimentConfig:
    seed: int = 0
    batch_count: int = 800
    batch_size: int = 24
    slot_fraction: float = 0.20
    confidence_min: float = 0.50
    confidence_max: float = 0.98


def generate_batches(config: ControlContentionExperimentConfig) -> tuple[tuple[VerificationTask, ...], ...]:
    rng = random.Random(config.seed)
    batches: list[tuple[VerificationTask, ...]] = []
    for _ in range(config.batch_count):
        batch: list[VerificationTask] = []
        for _ in range(config.batch_size):
            confidence = rng.uniform(config.confidence_min, config.confidence_max)
            value = rng.uniform(0.25, 2.5)
            base_correct = rng.random() < confidence
            batch.append(VerificationTask(value=value, confidence=confidence, base_correct=base_correct))
        batches.append(tuple(batch))
    return tuple(batches)


def _evaluate(policy: ContentionPolicy, batches: tuple[tuple[VerificationTask, ...], ...], slots: int) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    total_value = correct_value = selected_gain = optimal_gain = 0.0
    total_selected = 0
    for batch in batches:
        chosen = policy.allocate(batch, slots, cost)
        total_selected += len(chosen)
        optimal_gain += sum(sorted((task.expected_gain for task in batch), reverse=True)[:slots])
        selected_gain += sum(batch[idx].expected_gain for idx in chosen)
        for idx, task in enumerate(batch):
            total_value += task.value
            if idx in chosen or task.base_correct:
                correct_value += task.value
    task_count = len(batches) * len(batches[0])
    metrics: dict[str, float | int] = {
        "weighted_correctness": correct_value / total_value,
        "verification_rate": total_selected / task_count,
        "allocation_efficiency_vs_oracle_gain": selected_gain / optimal_gain if optimal_gain else 1.0,
        "messages_per_task": cost.messages / task_count,
        "operations_per_task": cost.operations / task_count,
        "slots_per_batch": slots,
    }
    return metrics, cost


def run_control_contention_experiment(config: ControlContentionExperimentConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    batches = generate_batches(config)
    slots = max(1, round(config.batch_size * config.slot_fraction))
    policies: list[ContentionPolicy] = [HierarchicalBatchAllocator(), DistributedThresholdAllocator(), DistributedAuctionAllocator()]
    return [(policy.name, *_evaluate(policy, batches, slots)) for policy in policies]
