from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math
import random
from typing import Protocol

from .core import CostMeter
from .consolidation import EvidenceThresholdPolicy


@dataclass(frozen=True)
class VolatilityObservation:
    step: int
    segment: int
    true_state: int
    observed_state: int
    switched: bool
    hidden_switch_probability: float


@dataclass(frozen=True)
class VolatilityExperimentConfig:
    seed: int = 0
    segment_lengths: tuple[int, ...] = (1800, 700, 1800, 700)
    switch_probabilities: tuple[float, ...] = (0.0005, 0.10, 0.001, 0.07)
    observation_reliability: float = 0.94
    fixed_thresholds: tuple[float, ...] = (1.8, 2.4, 3.4, 4.4)
    adaptive_high_threshold: float = 4.2
    adaptive_low_threshold: float = 1.8
    volatility_window: int = 120
    confirmed_run: int = 2
    rate_low: float = 0.005
    rate_high: float = 0.055
    evidence_decay: float = 0.55


def generate_volatility_stream(config: VolatilityExperimentConfig) -> tuple[VolatilityObservation, ...]:
    if len(config.segment_lengths) != len(config.switch_probabilities):
        raise ValueError("segment_lengths and switch_probabilities must match")
    rng = random.Random(config.seed)
    true_state = 1 if rng.random() < 0.5 else -1
    result: list[VolatilityObservation] = []
    step = 0
    for segment, (length, switch_probability) in enumerate(zip(config.segment_lengths, config.switch_probabilities)):
        for _ in range(length):
            switched = False
            if step > 0 and rng.random() < switch_probability:
                true_state *= -1
                switched = True
            observed = true_state if rng.random() < config.observation_reliability else -true_state
            result.append(VolatilityObservation(step, segment, true_state, observed, switched, switch_probability))
            step += 1
    return tuple(result)


class AdaptiveVolatilityPolicy:
    name = "adaptive_volatility_threshold"

    def __init__(
        self,
        *,
        high_threshold: float = 4.2,
        low_threshold: float = 1.8,
        volatility_window: int = 120,
        confirmed_run: int = 2,
        rate_low: float = 0.005,
        rate_high: float = 0.055,
        evidence_decay: float = 0.55,
    ) -> None:
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold
        self.volatility_window = volatility_window
        self.confirmed_run = confirmed_run
        self.rate_low = rate_low
        self.rate_high = rate_high
        self.evidence_decay = evidence_decay
        self._durable: int | None = None
        self._evidence = 0.0
        self._run_value: int | None = None
        self._run_count = 0
        self._confirmed_observed_state: int | None = None
        self._transition_steps: deque[int] = deque()
        self._step = 0
        self.last_threshold = high_threshold

    @property
    def durable_state(self) -> int | None:
        return self._durable

    def _observe_volatility(self, observation: int, cost: CostMeter) -> None:
        if observation == self._run_value:
            self._run_count += 1
        else:
            self._run_value = observation
            self._run_count = 1
        cost.operations += 1
        cost.reads += 1

        if self._run_count == self.confirmed_run and self._confirmed_observed_state != observation:
            if self._confirmed_observed_state is not None:
                self._transition_steps.append(self._step)
                cost.writes += 1
            self._confirmed_observed_state = observation

        cutoff = self._step - self.volatility_window
        while self._transition_steps and self._transition_steps[0] <= cutoff:
            self._transition_steps.popleft()
            cost.operations += 1
        rate = len(self._transition_steps) / self.volatility_window
        span = max(1e-9, self.rate_high - self.rate_low)
        normalized = min(1.0, max(0.0, (rate - self.rate_low) / span))
        self.last_threshold = self.high_threshold - normalized * (self.high_threshold - self.low_threshold)
        self._step += 1
        cost.operations += 4

    def observe(self, observation: int, cost: CostMeter) -> bool:
        self._observe_volatility(observation, cost)
        cost.reads += 1
        if self._durable is None:
            self._durable = observation
            cost.writes += 1
            return False
        if observation == self._durable:
            self._evidence *= self.evidence_decay
        else:
            self._evidence += 1.0
        cost.writes += 1
        cost.operations += 1
        if self._evidence < self.last_threshold:
            return False
        self._durable *= -1
        self._evidence = 0.0
        cost.writes += 1
        return True


class Policy(Protocol):
    name: str

    @property
    def durable_state(self) -> int | None: ...
    def observe(self, observation: int, cost: CostMeter) -> bool: ...


def evaluate_volatility_policy(policy: Policy, stream: tuple[VolatilityObservation, ...]) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    correct = durable_updates = false_updates = actual_switches = 0
    pending_switch_step: int | None = None
    delays: list[int] = []
    previous_truth: int | None = None
    segment_correct: dict[int, int] = {}
    segment_total: dict[int, int] = {}
    segment_thresholds: dict[int, list[float]] = {}

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
            delays.append(item.step - pending_switch_step)
            pending_switch_step = None
        if after == item.true_state:
            correct += 1
            segment_correct[item.segment] = segment_correct.get(item.segment, 0) + 1
        segment_total[item.segment] = segment_total.get(item.segment, 0) + 1
        if isinstance(policy, AdaptiveVolatilityPolicy):
            segment_thresholds.setdefault(item.segment, []).append(policy.last_threshold)

    metrics: dict[str, float | int] = {
        "accuracy": correct / len(stream),
        "actual_switches": actual_switches,
        "durable_updates": durable_updates,
        "false_updates": false_updates,
        "avg_switch_delay": sum(delays) / len(delays) if delays else math.nan,
        "resolved_switches": len(delays),
    }
    for segment in sorted(segment_total):
        metrics[f"accuracy_segment_{segment}"] = segment_correct.get(segment, 0) / segment_total[segment]
        if segment in segment_thresholds:
            values = segment_thresholds[segment]
            metrics[f"avg_threshold_segment_{segment}"] = sum(values) / len(values)
    return metrics, cost


def run_adaptive_volatility_experiment(config: VolatilityExperimentConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    stream = generate_volatility_stream(config)
    policies: list[Policy] = [EvidenceThresholdPolicy(threshold=t, evidence_decay=config.evidence_decay) for t in config.fixed_thresholds]
    policies.append(
        AdaptiveVolatilityPolicy(
            high_threshold=config.adaptive_high_threshold,
            low_threshold=config.adaptive_low_threshold,
            volatility_window=config.volatility_window,
            confirmed_run=config.confirmed_run,
            rate_low=config.rate_low,
            rate_high=config.rate_high,
            evidence_decay=config.evidence_decay,
        )
    )
    return [(policy.name, *evaluate_volatility_policy(policy, stream)) for policy in policies]
