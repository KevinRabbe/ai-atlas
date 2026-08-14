from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Protocol

from .core import CostMeter
from .environments.noisy_evidence import EvidenceTask, generate_evidence_tasks


class ComputePolicy(Protocol):
    name: str
    max_samples: int

    def solve(self, task: EvidenceTask, cost: CostMeter) -> tuple[int, int, float]: ...


@dataclass(frozen=True)
class FixedComputePolicy:
    samples: int

    @property
    def name(self) -> str:
        return f"fixed_{self.samples}"

    @property
    def max_samples(self) -> int:
        return self.samples

    def solve(self, task: EvidenceTask, cost: CostMeter) -> tuple[int, int, float]:
        total = 0.0
        for idx in range(self.samples):
            total += task.sample(idx)
            cost.samples += 1
            cost.operations += 1
        confidence = abs(total) / math.sqrt(self.samples)
        return (1 if total >= 0 else -1), self.samples, confidence


@dataclass(frozen=True)
class AdaptiveComputePolicy:
    threshold: float = 1.75
    min_samples: int = 2
    max_samples: int = 15

    @property
    def name(self) -> str:
        return f"adaptive_t{self.threshold:g}_max{self.max_samples}"

    def solve(self, task: EvidenceTask, cost: CostMeter) -> tuple[int, int, float]:
        total = 0.0
        used = 0
        confidence = 0.0
        for idx in range(self.max_samples):
            total += task.sample(idx)
            used += 1
            cost.samples += 1
            cost.operations += 1
            confidence = abs(total) / math.sqrt(used)
            if used >= self.min_samples and confidence >= self.threshold:
                break
        return (1 if total >= 0 else -1), used, confidence


@dataclass(frozen=True)
class AdaptiveComputeExperimentConfig:
    seed: int = 0
    task_count: int = 1200
    fixed_samples: tuple[int, ...] = (2, 5, 10, 15)
    threshold: float = 1.75
    min_samples: int = 2
    max_samples: int = 15


def evaluate_compute_policy(
    policy: ComputePolicy,
    tasks: tuple[EvidenceTask, ...],
) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    correct = 0
    total_used = 0
    used_by_signal: dict[float, list[int]] = {}
    correct_by_signal: dict[float, int] = {}
    total_by_signal: dict[float, int] = {}

    for task in tasks:
        prediction, used, _confidence = policy.solve(task, cost)
        total_used += used
        used_by_signal.setdefault(task.signal, []).append(used)
        total_by_signal[task.signal] = total_by_signal.get(task.signal, 0) + 1
        if prediction == task.label:
            correct += 1
            correct_by_signal[task.signal] = correct_by_signal.get(task.signal, 0) + 1

    metrics: dict[str, float | int] = {
        "accuracy": correct / len(tasks),
        "avg_samples": total_used / len(tasks),
        "task_count": len(tasks),
        "max_samples": policy.max_samples,
    }
    for signal in sorted(used_by_signal):
        suffix = str(signal).replace(".", "_")
        values = used_by_signal[signal]
        metrics[f"avg_samples_signal_{suffix}"] = sum(values) / len(values)
        metrics[f"accuracy_signal_{suffix}"] = correct_by_signal.get(signal, 0) / total_by_signal[signal]
    return metrics, cost


def run_adaptive_compute_experiment(
    config: AdaptiveComputeExperimentConfig,
) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    tasks = generate_evidence_tasks(seed=config.seed, count=config.task_count)
    policies: list[ComputePolicy] = [FixedComputePolicy(samples=n) for n in config.fixed_samples]
    policies.append(
        AdaptiveComputePolicy(
            threshold=config.threshold,
            min_samples=config.min_samples,
            max_samples=config.max_samples,
        )
    )
    return [(policy.name, *evaluate_compute_policy(policy, tasks)) for policy in policies]
