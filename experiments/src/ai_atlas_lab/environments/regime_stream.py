from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class RegimeObservation:
    step: int
    true_state: int
    observed_state: int
    switched: bool


def generate_regime_stream(
    *,
    seed: int,
    steps: int = 4000,
    switch_probability: float = 0.012,
    observation_reliability: float = 0.82,
) -> tuple[RegimeObservation, ...]:
    rng = random.Random(seed)
    true_state = 1 if rng.random() < 0.5 else -1
    stream: list[RegimeObservation] = []
    for step in range(steps):
        switched = False
        if step > 0 and rng.random() < switch_probability:
            true_state *= -1
            switched = True
        observed = true_state if rng.random() < observation_reliability else -true_state
        stream.append(RegimeObservation(step, true_state, observed, switched))
    return tuple(stream)
