from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class RegressionExposureConfig:
    seed: int = 0
    rounds: int = 300
    candidates_per_round: int = 30
    scenarios: int = 40
    visible_count: int = 8
    hidden_count: int = 8
    shift_round: int = 150
    targeted_boost_mean: float = 0.05
    tradeoff_scale: float = 0.012
    general_mean: float = 0.01
    general_sd: float = 0.025
    effect_noise: float = 0.018
    hidden_check_cost: float = 0.002
    novel_penalty_mean: float = 0.045
    novel_penalty_sd: float = 0.03


@dataclass(frozen=True)
class RegressionPolicy:
    name: str


VISIBLE_ONLY = RegressionPolicy("visible_only")
FIXED_HIDDEN = RegressionPolicy("fixed_hidden")
ROTATING_HIDDEN = RegressionPolicy("rotating_hidden")
ADVERSARIAL_ROTATING = RegressionPolicy("adversarial_rotating")


def run_regression_exposure(config: RegressionExposureConfig, policy: RegressionPolicy) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    incumbent = [0.5 for _ in range(config.scenarios)]
    visible = list(range(config.visible_count))
    fixed_hidden = list(range(config.visible_count, config.visible_count + config.hidden_count))

    harmful_accepted = 0
    accepted = 0
    good_rejected = 0
    evaluation_cost = 0.0
    history: list[float] = []

    for round_index in range(config.rounds):
        active = (
            list(range(0, config.scenarios // 2))
            if round_index < config.shift_round
            else list(range(config.scenarios // 2, config.scenarios))
        )

        candidates: list[tuple[float, list[float]]] = []
        for _ in range(config.candidates_per_round):
            general_delta = rng.gauss(config.general_mean, config.general_sd)
            visible_boost = max(0.0, rng.gauss(config.targeted_boost_mean, 0.02))
            novel_penalty = (
                max(0.0, rng.gauss(config.novel_penalty_mean, config.novel_penalty_sd))
                if round_index >= config.shift_round
                else 0.0
            )

            effects: list[float] = []
            for scenario in range(config.scenarios):
                effect = general_delta + rng.gauss(0.0, config.effect_noise)
                if scenario in visible:
                    effect += visible_boost
                else:
                    effect -= visible_boost * config.tradeoff_scale / config.targeted_boost_mean
                if round_index >= config.shift_round and scenario >= config.scenarios // 2:
                    effect -= novel_penalty
                effects.append(effect)

            visible_gain = sum(effects[index] for index in visible) / len(visible)
            candidates.append((visible_gain, effects))

        visible_gain, effects = max(candidates, key=lambda item: item[0])
        true_delta = sum(effects[index] for index in active) / len(active)

        if policy == VISIBLE_ONLY:
            allow = visible_gain > 0.0
            round_cost = 0.0
        elif policy == FIXED_HIDDEN:
            hidden_gain = sum(effects[index] for index in fixed_hidden) / len(fixed_hidden)
            allow = visible_gain > 0.0 and hidden_gain > 0.0
            round_cost = config.hidden_count * config.hidden_check_cost
        elif policy == ROTATING_HIDDEN:
            pool = [index for index in active if index not in visible]
            hidden = rng.sample(pool, min(config.hidden_count, len(pool)))
            hidden_gain = sum(effects[index] for index in hidden) / len(hidden)
            allow = visible_gain > 0.0 and hidden_gain > 0.0
            round_cost = len(hidden) * config.hidden_check_cost
        elif policy == ADVERSARIAL_ROTATING:
            pool = [index for index in active if index not in visible]
            hidden = sorted(pool, key=lambda index: effects[index])[: min(config.hidden_count, len(pool))]
            hidden_gain = sum(effects[index] for index in hidden) / len(hidden)
            allow = visible_gain > 0.0 and hidden_gain > 0.0
            round_cost = len(hidden) * config.hidden_check_cost * 1.25
        else:
            raise ValueError(f"unknown policy: {policy.name}")

        evaluation_cost += round_cost

        if allow:
            accepted += 1
            if true_delta < 0.0:
                harmful_accepted += 1
            incumbent = [
                min(1.0, max(0.0, old + delta))
                for old, delta in zip(incumbent, effects)
            ]
        elif true_delta > 0.0:
            good_rejected += 1

        history.append(sum(incumbent[index] for index in active) / len(active))

    tail = history[-30:]
    pre_shift_tail = history[config.shift_round - 30 : config.shift_round]
    average_check_cost = evaluation_cost / config.rounds

    return {
        "final_true_score": history[-1],
        "pre_shift_true_score": sum(pre_shift_tail) / len(pre_shift_tail),
        "post_shift_true_score": sum(tail) / len(tail),
        "harmful_accepted": harmful_accepted,
        "accepted_changes": accepted,
        "good_rejected": good_rejected,
        "evaluation_cost_per_round": average_check_cost,
        "lifetime_utility": sum(history) / len(history) - average_check_cost,
    }


def run_regression_exposure_experiment(config: RegressionExposureConfig) -> list[tuple[str, dict[str, float | int]]]:
    policies = (VISIBLE_ONLY, FIXED_HIDDEN, ROTATING_HIDDEN, ADVERSARIAL_ROTATING)
    return [(policy.name, run_regression_exposure(config, policy)) for policy in policies]
