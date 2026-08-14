from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class FidelityConfig:
    seed: int = 0
    threshold_tasks: int = 8000
    low_step: float = 0.25
    low_cost: float = 0.01
    high_cost: float = 0.08
    trajectory_episodes: int = 5000
    trajectory_low_step: float = 0.08
    low_cost_per_step: float = 0.0005
    high_cost_per_step: float = 0.003
    safety_limit: float = 1.0
    start_state: float = 0.35
    trajectory_margin_scale: float = 0.48


def _quantize(value: float, step: float) -> float:
    return round(value / step) * step


def run_threshold_fidelity(
    config: FidelityConfig,
    variant: str,
) -> dict[str, float | int]:
    if variant not in {"low", "high", "adaptive"}:
        raise ValueError(f"unknown variant: {variant}")

    rng = random.Random(config.seed)
    utility = 0.0
    errors = 0
    high_calls = 0
    total_cost = 0.0
    consequence_counts = {1: 0, 3: 0, 6: 0}
    consequence_high = {1: 0, 3: 0, 6: 0}

    for _ in range(config.threshold_tasks):
        value = rng.uniform(-1.0, 1.0)
        task_value = rng.choice((1.0, 2.0, 4.0))
        consequence = rng.choice((1, 3, 6))
        consequence_counts[consequence] += 1

        truth = value >= 0.0
        approximate = _quantize(value, config.low_step)

        if variant == "low":
            prediction = approximate > 0.0
            cost = config.low_cost
        elif variant == "high":
            prediction = truth
            cost = config.high_cost
            high_calls += 1
            consequence_high[consequence] += 1
        else:
            quantization_bound = config.low_step / 2.0
            sensitive = abs(approximate) <= quantization_bound
            if consequence >= 6 and abs(approximate) <= config.low_step:
                sensitive = True
            if sensitive:
                prediction = truth
                cost = config.low_cost + config.high_cost
                high_calls += 1
                consequence_high[consequence] += 1
            else:
                prediction = approximate >= 0.0
                cost = config.low_cost

        correct = prediction == truth
        errors += int(not correct)
        total_cost += cost
        utility += (
            task_value if correct else -consequence * task_value
        ) - cost

    result: dict[str, float | int] = {
        "net_utility_per_task": utility / config.threshold_tasks,
        "error_rate": errors / config.threshold_tasks,
        "high_fidelity_rate": high_calls / config.threshold_tasks,
        "mean_fidelity_cost": total_cost / config.threshold_tasks,
    }
    for consequence in (1, 3, 6):
        result[f"high_rate_consequence_{consequence}"] = (
            consequence_high[consequence] / consequence_counts[consequence]
        )
    return result


def run_trajectory_fidelity(
    config: FidelityConfig,
    variant: str,
) -> dict[str, float | int]:
    if variant not in {"low", "high", "adaptive"}:
        raise ValueError(f"unknown variant: {variant}")

    rng = random.Random(config.seed + 900)
    utility = 0.0
    errors = 0
    false_safe = 0
    high_calls = 0
    consequence_counts = {4: 0, 8: 0, 12: 0}
    consequence_high = {4: 0, 8: 0, 12: 0}

    for _ in range(config.trajectory_episodes):
        horizon = rng.randint(40, 100)
        consequence = rng.choice((4, 8, 12))
        consequence_counts[consequence] += 1
        increments = [rng.gauss(0.006, 0.065) for _ in range(horizon)]

        true_state = config.start_state
        true_peak = true_state
        approximate_state = config.start_state
        approximate_peak = approximate_state
        for increment in increments:
            true_state += increment
            true_peak = max(true_peak, true_state)
            approximate_state = _quantize(
                approximate_state + increment,
                config.trajectory_low_step,
            )
            approximate_peak = max(approximate_peak, approximate_state)

        truth_safe = true_peak < config.safety_limit
        low_prediction = approximate_peak < config.safety_limit

        if variant == "low":
            prediction = low_prediction
            cost = config.low_cost_per_step * horizon
        elif variant == "high":
            prediction = truth_safe
            cost = config.high_cost_per_step * horizon
            high_calls += 1
            consequence_high[consequence] += 1
        else:
            uncertainty_margin = (
                config.trajectory_margin_scale
                * config.trajectory_low_step
                * math.sqrt(horizon)
                * (consequence / 8.0) ** 0.4
            )
            sensitive = abs(approximate_peak - config.safety_limit) <= uncertainty_margin
            if sensitive:
                # Recoverable source increments allow an exact replay only when needed.
                prediction = truth_safe
                cost = (
                    config.low_cost_per_step + config.high_cost_per_step
                ) * horizon
                high_calls += 1
                consequence_high[consequence] += 1
            else:
                prediction = low_prediction
                cost = config.low_cost_per_step * horizon

        correct = prediction == truth_safe
        if not correct:
            errors += 1
            if prediction and not truth_safe:
                false_safe += 1

        if correct:
            reward = 1.0
        elif prediction and not truth_safe:
            reward = -float(consequence)
        else:
            reward = -1.0
        utility += reward - cost

    result: dict[str, float | int] = {
        "net_utility_per_episode": utility / config.trajectory_episodes,
        "error_rate": errors / config.trajectory_episodes,
        "false_safe_rate": false_safe / config.trajectory_episodes,
        "high_fidelity_rate": high_calls / config.trajectory_episodes,
    }
    for consequence in (4, 8, 12):
        result[f"high_rate_consequence_{consequence}"] = (
            consequence_high[consequence] / consequence_counts[consequence]
        )
    return result


def run_fidelity_experiment(
    config: FidelityConfig,
) -> dict[str, list[tuple[str, dict[str, float | int]]]]:
    variants = ("low", "high", "adaptive")
    return {
        "threshold_decision": [
            (variant, run_threshold_fidelity(config, variant))
            for variant in variants
        ],
        "trajectory_constraint": [
            (variant, run_trajectory_fidelity(config, variant))
            for variant in variants
        ],
    }
