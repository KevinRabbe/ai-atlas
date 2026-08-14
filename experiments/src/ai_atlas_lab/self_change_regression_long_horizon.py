from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class LongHorizonRegressionConfig:
    seed: int = 0
    rounds: int = 300
    candidates_per_round: int = 30
    shift_round: int = 150
    visible_horizon: int = 10
    fixed_hidden_horizon: int = 20
    rotating_low: int = 20
    rotating_high_pre: int = 40
    rotating_high_post: int = 120
    check_cost_per_step: float = 0.0004
    base_delta_mean: float = 0.012
    base_delta_sd: float = 0.025
    visible_boost_mean: float = 0.045
    instability_mean: float = 0.0018
    instability_sd: float = 0.0016


@dataclass(frozen=True)
class LongHorizonPolicy:
    name: str


VISIBLE_ONLY = LongHorizonPolicy("visible_only")
FIXED_HIDDEN = LongHorizonPolicy("fixed_hidden")
ROTATING_HIDDEN = LongHorizonPolicy("rotating_hidden")
ADVERSARIAL_ROTATING = LongHorizonPolicy("adversarial_rotating")


def _visible_effect(base: float, boost: float, instability: float, horizon: int) -> float:
    return base + boost - instability * (horizon ** 1.25)


def _deployment_effect(base: float, boost: float, instability: float, horizon: int) -> float:
    return base + 0.35 * boost - instability * (horizon ** 1.25)


def run_long_horizon_regression(config: LongHorizonRegressionConfig, policy: LongHorizonPolicy) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    quality = 0.5
    harmful_accepted = 0
    accepted = 0
    good_rejected = 0
    evaluation_cost = 0.0
    history: list[float] = []

    for round_index in range(config.rounds):
        deployment_horizon = 30 if round_index < config.shift_round else 100
        candidates: list[tuple[float, float, float, float]] = []

        for _ in range(config.candidates_per_round):
            base = rng.gauss(config.base_delta_mean, config.base_delta_sd)
            boost = max(0.0, rng.gauss(config.visible_boost_mean, 0.02))
            instability = max(0.0, rng.gauss(config.instability_mean, config.instability_sd))
            visible = _visible_effect(base, boost, instability, config.visible_horizon)
            candidates.append((visible, base, boost, instability))

        visible, base, boost, instability = max(candidates, key=lambda item: item[0])
        true_delta = _deployment_effect(base, boost, instability, deployment_horizon)

        if policy == VISIBLE_ONLY:
            allow = visible > 0.0
            round_cost = 0.0
        elif policy == FIXED_HIDDEN:
            hidden = _deployment_effect(base, boost, instability, config.fixed_hidden_horizon)
            allow = visible > 0.0 and hidden > 0.0
            round_cost = config.fixed_hidden_horizon * config.check_cost_per_step
        elif policy == ROTATING_HIDDEN:
            upper = config.rotating_high_pre if round_index < config.shift_round else config.rotating_high_post
            horizon = rng.randint(config.rotating_low, upper)
            hidden = _deployment_effect(base, boost, instability, horizon)
            allow = visible > 0.0 and hidden > 0.0
            round_cost = horizon * config.check_cost_per_step
        elif policy == ADVERSARIAL_ROTATING:
            horizon = config.rotating_high_post
            hidden = _deployment_effect(base, boost, instability, horizon)
            allow = visible > 0.0 and hidden > 0.0
            round_cost = horizon * config.check_cost_per_step * 1.2
        else:
            raise ValueError(f"unknown policy: {policy.name}")

        evaluation_cost += round_cost
        if allow:
            accepted += 1
            if true_delta < 0.0:
                harmful_accepted += 1
            quality = min(1.0, max(0.0, quality + true_delta))
        elif true_delta > 0.0:
            good_rejected += 1
        history.append(quality)

    pre = history[config.shift_round - 30 : config.shift_round]
    post = history[-30:]
    average_cost = evaluation_cost / config.rounds
    return {
        "pre_shift_true_score": sum(pre) / len(pre),
        "post_shift_true_score": sum(post) / len(post),
        "final_true_score": history[-1],
        "harmful_accepted": harmful_accepted,
        "accepted_changes": accepted,
        "good_rejected": good_rejected,
        "evaluation_cost_per_round": average_cost,
        "lifetime_utility": sum(history) / len(history) - average_cost,
    }


def run_long_horizon_regression_experiment(config: LongHorizonRegressionConfig) -> list[tuple[str, dict[str, float | int]]]:
    policies = (VISIBLE_ONLY, FIXED_HIDDEN, ROTATING_HIDDEN, ADVERSARIAL_ROTATING)
    return [(policy.name, run_long_horizon_regression(config, policy)) for policy in policies]
