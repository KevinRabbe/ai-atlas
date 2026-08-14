from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class NoiseVolatilityConfig:
    seed: int = 0
    steps: int = 6000
    switch_probability: float = 0.001
    sensor_reliability: float = 0.78
    high_threshold: float = 4.2
    low_threshold: float = 1.8
    volatility_window: int = 100
    rate_low: float = 0.005
    rate_high: float = 0.055
    secondary_sensor_cost: float = 0.006
    sparse_sample_interval: int = 10
    disagreement_window: int = 30
    disagreement_on: float = 0.18
    disagreement_off: float = 0.12


def generate_stream(config: NoiseVolatilityConfig):
    rng = random.Random(config.seed)
    truth = 1 if rng.random() < 0.5 else -1
    result = []
    for step in range(config.steps):
        switched = False
        if step > 0 and rng.random() < config.switch_probability:
            truth *= -1
            switched = True
        primary = truth if rng.random() < config.sensor_reliability else -truth
        secondary = truth if rng.random() < config.sensor_reliability else -truth
        result.append((truth, primary, secondary, switched))
    return tuple(result)


class VolatilityCore:
    def __init__(self, config: NoiseVolatilityConfig) -> None:
        self.config = config
        self.durable: int | None = None
        self.evidence = 0.0
        self.run_value: int | None = None
        self.run_count = 0
        self.confirmed: int | None = None
        self.transitions: deque[int] = deque()
        self.step = 0
        self.threshold = config.high_threshold

    def observe_value(self, observation: int | None) -> bool:
        if observation is not None:
            if observation == self.run_value:
                self.run_count += 1
            else:
                self.run_value = observation
                self.run_count = 1
            if self.run_count == 2 and self.confirmed != observation:
                if self.confirmed is not None:
                    self.transitions.append(self.step)
                self.confirmed = observation

        cutoff = self.step - self.config.volatility_window
        while self.transitions and self.transitions[0] <= cutoff:
            self.transitions.popleft()
        rate = len(self.transitions) / self.config.volatility_window
        span = max(1e-9, self.config.rate_high - self.config.rate_low)
        normalized = min(1.0, max(0.0, (rate - self.config.rate_low) / span))
        self.threshold = self.config.high_threshold - normalized * (
            self.config.high_threshold - self.config.low_threshold
        )
        self.step += 1

        if observation is None:
            self.evidence *= 0.8
            return False
        if self.durable is None:
            self.durable = observation
            return False
        if observation == self.durable:
            self.evidence *= 0.55
        else:
            self.evidence += 1.0
        if self.evidence < self.threshold:
            return False
        self.durable *= -1
        self.evidence = 0.0
        return True


class SingleSensorPolicy:
    name = "single_sensor_adaptive"

    def __init__(self, config: NoiseVolatilityConfig) -> None:
        self.core = VolatilityCore(config)
        self.secondary_reads = 0

    @property
    def durable(self):
        return self.core.durable

    def observe(self, primary: int, secondary: int) -> bool:
        return self.core.observe_value(primary)


class AlwaysCorroboratePolicy:
    name = "always_corroborate"

    def __init__(self, config: NoiseVolatilityConfig) -> None:
        self.core = VolatilityCore(config)
        self.secondary_reads = 0

    @property
    def durable(self):
        return self.core.durable

    def observe(self, primary: int, secondary: int) -> bool:
        self.secondary_reads += 1
        return self.core.observe_value(primary if primary == secondary else None)


class AdaptiveCorroborationPolicy:
    name = "adaptive_corroboration"

    def __init__(self, config: NoiseVolatilityConfig) -> None:
        self.config = config
        self.core = VolatilityCore(config)
        self.secondary_reads = 0
        self.disagreements: deque[int] = deque(maxlen=config.disagreement_window)
        self.full = False
        self.step = 0

    @property
    def durable(self):
        return self.core.durable

    def observe(self, primary: int, secondary: int) -> bool:
        use_secondary = self.full or self.step % self.config.sparse_sample_interval == 0
        self.step += 1
        if not use_secondary:
            return self.core.observe_value(primary)

        self.secondary_reads += 1
        self.disagreements.append(int(primary != secondary))
        if len(self.disagreements) >= 10:
            rate = sum(self.disagreements) / len(self.disagreements)
            if self.full and rate < self.config.disagreement_off:
                self.full = False
            elif not self.full and rate > self.config.disagreement_on:
                self.full = True
        return self.core.observe_value(primary if primary == secondary else None)


def evaluate_policy(policy, stream, config: NoiseVolatilityConfig):
    correct = false_updates = 0
    pending = None
    delays = []
    for step, (truth, primary, secondary, switched) in enumerate(stream):
        if switched:
            pending = step
        changed = policy.observe(primary, secondary)
        if changed and policy.durable != truth:
            false_updates += 1
        if pending is not None and policy.durable == truth:
            delays.append(step - pending)
            pending = None
        correct += int(policy.durable == truth)

    accuracy = correct / len(stream)
    secondary_rate = policy.secondary_reads / len(stream)
    return {
        "accuracy": accuracy,
        "false_updates": false_updates,
        "avg_switch_delay": sum(delays) / len(delays) if delays else math.nan,
        "secondary_read_rate": secondary_rate,
        "net_utility": accuracy - secondary_rate * config.secondary_sensor_cost,
    }


def run_noise_volatility_experiment(config: NoiseVolatilityConfig):
    stream = generate_stream(config)
    policies = (
        SingleSensorPolicy(config),
        AlwaysCorroboratePolicy(config),
        AdaptiveCorroborationPolicy(config),
    )
    return [(policy.name, evaluate_policy(policy, stream, config)) for policy in policies]
