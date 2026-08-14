from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class AdaptiveBreadthConfig:
    seed: int = 0
    segment_lengths: tuple[int, ...] = (1600, 1600, 1600)
    goal_switch_probabilities: tuple[float, ...] = (0.01, 0.45, 0.02)
    active_group_bits: int = 3
    active_rent_per_bit: float = 0.002
    reacquire_cost_per_bit: float = 0.030
    estimator_window: int = 120
    hysteresis: float = 0.10


@dataclass(frozen=True)
class BreadthStep:
    step: int
    segment: int
    goal: int
    switched: bool


def generate_goal_stream(config: AdaptiveBreadthConfig) -> tuple[BreadthStep, ...]:
    if len(config.segment_lengths) != len(config.goal_switch_probabilities):
        raise ValueError("segment_lengths and goal_switch_probabilities must match")
    rng = random.Random(config.seed)
    goal = 0
    steps: list[BreadthStep] = []
    index = 0
    for segment, (length, switch_probability) in enumerate(
        zip(config.segment_lengths, config.goal_switch_probabilities)
    ):
        for _ in range(length):
            switched = False
            if index > 0 and rng.random() < switch_probability:
                goal = 1 - goal
                switched = True
            steps.append(BreadthStep(index, segment, goal, switched))
            index += 1
    return tuple(steps)


def _evaluate_fixed(
    config: AdaptiveBreadthConfig,
    stream: tuple[BreadthStep, ...],
    *,
    broad: bool,
) -> dict[str, float | int]:
    active_bits = config.active_group_bits * (2 if broad else 1)
    cost = 0.0
    reacquisitions = 0
    segment_cost = [0.0 for _ in config.segment_lengths]
    segment_broad = [0 for _ in config.segment_lengths]
    segment_steps = [0 for _ in config.segment_lengths]

    for item in stream:
        step_cost = active_bits * config.active_rent_per_bit
        if not broad and item.switched:
            step_cost += config.active_group_bits * config.reacquire_cost_per_bit
            reacquisitions += 1
        cost += step_cost
        segment_cost[item.segment] += step_cost
        segment_steps[item.segment] += 1
        segment_broad[item.segment] += int(broad)

    metrics: dict[str, float | int] = {
        "accuracy": 1.0,
        "cost_per_step": cost / len(stream),
        "net_utility": 1.0 - cost / len(stream),
        "reacquisitions": reacquisitions,
        "broad_fraction": float(broad),
    }
    for segment in range(len(config.segment_lengths)):
        metrics[f"cost_segment_{segment}"] = segment_cost[segment] / segment_steps[segment]
        metrics[f"broad_fraction_segment_{segment}"] = segment_broad[segment] / segment_steps[segment]
    return metrics


def _evaluate_adaptive(
    config: AdaptiveBreadthConfig,
    stream: tuple[BreadthStep, ...],
) -> dict[str, float | int]:
    window: list[int] = []
    broad = False
    cost = 0.0
    reacquisitions = 0
    transitions = 0
    broad_steps = 0
    segment_cost = [0.0 for _ in config.segment_lengths]
    segment_broad = [0 for _ in config.segment_lengths]
    segment_steps = [0 for _ in config.segment_lengths]

    extra_hot_cost = config.active_group_bits * config.active_rent_per_bit
    reacquire_cost = config.active_group_bits * config.reacquire_cost_per_bit
    base_threshold = extra_hot_cost / reacquire_cost

    for item in stream:
        window.append(int(item.switched))
        if len(window) > config.estimator_window:
            window.pop(0)
        estimated_switch_rate = sum(window) / len(window)

        enter = base_threshold * (1.0 + config.hysteresis)
        leave = base_threshold * (1.0 - config.hysteresis)
        next_broad = broad
        if broad and estimated_switch_rate < leave:
            next_broad = False
        elif (not broad) and estimated_switch_rate > enter:
            next_broad = True
        if next_broad != broad:
            transitions += 1
        broad = next_broad

        active_bits = config.active_group_bits * (2 if broad else 1)
        step_cost = active_bits * config.active_rent_per_bit
        if not broad and item.switched:
            step_cost += reacquire_cost
            reacquisitions += 1
        cost += step_cost
        broad_steps += int(broad)
        segment_cost[item.segment] += step_cost
        segment_broad[item.segment] += int(broad)
        segment_steps[item.segment] += 1

    metrics: dict[str, float | int] = {
        "accuracy": 1.0,
        "cost_per_step": cost / len(stream),
        "net_utility": 1.0 - cost / len(stream),
        "reacquisitions": reacquisitions,
        "broad_fraction": broad_steps / len(stream),
        "breadth_transitions": transitions,
        "break_even_switch_rate": base_threshold,
    }
    for segment in range(len(config.segment_lengths)):
        metrics[f"cost_segment_{segment}"] = segment_cost[segment] / segment_steps[segment]
        metrics[f"broad_fraction_segment_{segment}"] = segment_broad[segment] / segment_steps[segment]
    return metrics


def run_adaptive_breadth_experiment(
    config: AdaptiveBreadthConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    stream = generate_goal_stream(config)
    return [
        ("always_broad", _evaluate_fixed(config, stream, broad=True)),
        ("always_narrow", _evaluate_fixed(config, stream, broad=False)),
        ("adaptive_breadth", _evaluate_adaptive(config, stream)),
    ]
