from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Protocol

from .core import CostMeter
from .environments.regime_stream import RegimeObservation, generate_regime_stream


class ConsolidationPolicy(Protocol):
    name: str

    @property
    def durable_state(self) -> int | None: ...
    def observe(self, observation: int, cost: CostMeter) -> bool: ...


class ImmediateDurablePolicy:
    name = "immediate_durable"

    def __init__(self) -> None:
        self._durable: int | None = None

    @property
    def durable_state(self) -> int | None:
        return self._durable

    def observe(self, observation: int, cost: CostMeter) -> bool:
        changed = self._durable is not None and self._durable != observation
        self._durable = observation
        cost.reads += 1
        cost.writes += 1
        cost.operations += 1
        return changed


@dataclass
class ConsecutiveStagingPolicy:
    confirmations: int = 3

    def __post_init__(self) -> None:
        self._durable: int | None = None
        self._candidate: int | None = None
        self._count = 0

    @property
    def name(self) -> str:
        return f"staged_{self.confirmations}"

    @property
    def durable_state(self) -> int | None:
        return self._durable

    def observe(self, observation: int, cost: CostMeter) -> bool:
        cost.reads += 1
        cost.operations += 1
        if self._durable is None:
            self._durable = observation
            cost.writes += 1
            return False

        if observation == self._durable:
            self._candidate = None
            self._count = 0
            return False

        if self._candidate == observation:
            self._count += 1
        else:
            self._candidate = observation
            self._count = 1
        cost.writes += 1

        if self._count < self.confirmations:
            return False

        self._durable = observation
        self._candidate = None
        self._count = 0
        cost.writes += 1
        return True


@dataclass
class EvidenceThresholdPolicy:
    threshold: float = 2.4
    evidence_decay: float = 0.55

    def __post_init__(self) -> None:
        self._durable: int | None = None
        self._evidence = 0.0

    @property
    def name(self) -> str:
        return f"evidence_t{self.threshold:g}"

    @property
    def durable_state(self) -> int | None:
        return self._durable

    def observe(self, observation: int, cost: CostMeter) -> bool:
        cost.reads += 1
        cost.operations += 1
        if self._durable is None:
            self._durable = observation
            cost.writes += 1
            return False

        if observation == self._durable:
            self._evidence *= self.evidence_decay
        else:
            self._evidence += 1.0
        cost.writes += 1

        if self._evidence < self.threshold:
            return False
        self._durable *= -1
        self._evidence = 0.0
        cost.writes += 1
        return True


@dataclass(frozen=True)
class ConsolidationExperimentConfig:
    seed: int = 0
    steps: int = 4000
    switch_probability: float = 0.012
    observation_reliability: float = 0.82
    confirmations: tuple[int, ...] = (2, 3, 5)
    evidence_thresholds: tuple[float, ...] = (2.4, 3.4)


def evaluate_consolidation_policy(
    policy: ConsolidationPolicy,
    stream: tuple[RegimeObservation, ...],
) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    correct = 0
    durable_updates = 0
    false_updates = 0
    actual_switches = 0
    pending_switch_step: int | None = None
    switch_delays: list[int] = []

    previous_truth: int | None = None
    for item in stream:
        if previous_truth is not None and item.true_state != previous_truth:
            actual_switches += 1
            pending_switch_step = item.step
        previous_truth = item.true_state

        changed = policy.observe(item.observed_state, cost)
        after = policy.durable_state

        if changed:
            durable_updates += 1
            if after != item.true_state:
                false_updates += 1

        if pending_switch_step is not None and after == item.true_state:
            switch_delays.append(item.step - pending_switch_step)
            pending_switch_step = None

        if after == item.true_state:
            correct += 1

    avg_delay = sum(switch_delays) / len(switch_delays) if switch_delays else math.nan
    metrics: dict[str, float | int] = {
        "accuracy": correct / len(stream),
        "steps": len(stream),
        "actual_switches": actual_switches,
        "durable_updates": durable_updates,
        "false_updates": false_updates,
        "avg_switch_delay": avg_delay,
        "resolved_switches": len(switch_delays),
    }
    return metrics, cost


def run_consolidation_experiment(
    config: ConsolidationExperimentConfig,
) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    stream = generate_regime_stream(
        seed=config.seed,
        steps=config.steps,
        switch_probability=config.switch_probability,
        observation_reliability=config.observation_reliability,
    )
    policies: list[ConsolidationPolicy] = [ImmediateDurablePolicy()]
    policies.extend(ConsecutiveStagingPolicy(n) for n in config.confirmations)
    policies.extend(EvidenceThresholdPolicy(t) for t in config.evidence_thresholds)
    return [(policy.name, *evaluate_consolidation_policy(policy, stream)) for policy in policies]
