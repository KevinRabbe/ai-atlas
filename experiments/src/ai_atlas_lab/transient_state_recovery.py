from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class CacheRecoveryConfig:
    seed: int = 0
    episodes: int = 4_000
    items: int = 24
    persist_cost: float = 0.05
    rematerialize_cost: float = 0.22
    stale_reuse_penalty: float = 1.0
    estimate_noise_reuse: float = 0.08
    estimate_noise_stale: float = 0.06


@dataclass(frozen=True)
class CreditRecoveryConfig:
    seed: int = 0
    episodes: int = 8_000
    trace_items: int = 6
    unversioned_persist_cost: float = 0.01
    replay_cost: float = 0.14
    survival_probability_after_change: float = 0.55
    false_blame_penalty: float = 1.5
    change_estimate_noise: float = 0.08


def run_cache_recovery(config: CacheRecoveryConfig, policy: str) -> dict[str, float]:
    """Recover source-backed hot/predictive state across crash/reorganization."""

    valid = {"persist_all", "rematerialize", "discard", "adaptive"}
    if policy not in valid:
        raise ValueError(f"unknown cache recovery policy: {policy}")

    rng = random.Random(config.seed)
    # (future reuse probability, probability the hot value became stale)
    regimes = ((0.12, 0.05), (0.72, 0.05), (0.12, 0.28), (0.72, 0.28))
    metrics: dict[str, float] = defaultdict(float)

    for episode in range(config.episodes):
        reuse_probability, stale_probability = regimes[(episode // 250) % len(regimes)]
        observed_reuse = max(
            0.0,
            min(1.0, reuse_probability + rng.gauss(0.0, config.estimate_noise_reuse)),
        )
        observed_stale = max(
            0.0,
            min(1.0, stale_probability + rng.gauss(0.0, config.estimate_noise_stale)),
        )

        for _ in range(config.items):
            reused = rng.random() < reuse_probability
            stale = rng.random() < stale_probability

            if policy == "persist_all":
                choice = "persist"
            elif policy == "rematerialize":
                choice = "rematerialize"
            elif policy == "discard":
                choice = "discard"
            else:
                persist_value = (
                    observed_reuse
                    * (
                        (1.0 - observed_stale)
                        - observed_stale * config.stale_reuse_penalty
                    )
                    - config.persist_cost
                )
                rematerialize_value = observed_reuse * (
                    1.0 - config.rematerialize_cost
                )
                choice = max(
                    (
                        ("persist", persist_value),
                        ("rematerialize", rematerialize_value),
                        ("discard", 0.0),
                    ),
                    key=lambda item: item[1],
                )[0]

            if choice == "persist":
                metrics["utility"] -= config.persist_cost
                metrics["persisted_items"] += 1.0
                if reused:
                    if stale:
                        metrics["utility"] -= config.stale_reuse_penalty
                        metrics["stale_reuse"] += 1.0
                    else:
                        metrics["utility"] += 1.0
                        metrics["successful_reuse"] += 1.0

            elif choice == "rematerialize":
                if reused:
                    metrics["utility"] += 1.0 - config.rematerialize_cost
                    metrics["rematerialized_items"] += 1.0
                    metrics["successful_reuse"] += 1.0

            else:
                if reused:
                    metrics["missed_reuse"] += 1.0

    denominator = config.episodes * config.items
    return {key: value / denominator for key, value in metrics.items()}


def run_credit_recovery(config: CreditRecoveryConfig, policy: str) -> dict[str, float]:
    """Recover delayed causal-credit eligibility across structural change.

    `unversioned` restores old positional/local trace entries into the current
    structure. `versioned` retains exact causal identity and only updates
    transitions that still have a valid semantic target. `source_replay`
    reconstructs the valid historical trace from retained source history.
    """

    valid = {"discard", "unversioned", "versioned", "source_replay", "adaptive"}
    if policy not in valid:
        raise ValueError(f"unknown credit recovery policy: {policy}")

    rng = random.Random(config.seed)
    # (structural-change probability, exact identity-trace persistence cost)
    regimes = ((0.03, 0.04), (0.65, 0.04), (0.03, 0.24), (0.65, 0.24))
    metrics: dict[str, float] = defaultdict(float)

    for episode in range(config.episodes):
        change_probability, versioned_cost = regimes[(episode // 500) % len(regimes)]
        observed_change_probability = max(
            0.0,
            min(
                1.0,
                change_probability + rng.gauss(0.0, config.change_estimate_noise),
            ),
        )
        changed = rng.random() < change_probability
        survived = [
            True
            if not changed
            else rng.random() < config.survival_probability_after_change
            for _ in range(config.trace_items)
        ]

        if policy == "discard":
            choice = "discard"
        elif policy == "unversioned":
            choice = "unversioned"
        elif policy == "versioned":
            choice = "versioned"
        elif policy == "source_replay":
            choice = "source_replay"
        else:
            survival = config.survival_probability_after_change
            unversioned_value = (
                (1.0 - observed_change_probability)
                + observed_change_probability
                * (
                    survival
                    - (1.0 - survival) * config.false_blame_penalty
                )
                - config.unversioned_persist_cost
            )
            valid_credit_probability = (
                (1.0 - observed_change_probability)
                + observed_change_probability * survival
            )
            versioned_value = valid_credit_probability - versioned_cost
            replay_value = valid_credit_probability - config.replay_cost
            choice = max(
                (
                    ("unversioned", unversioned_value),
                    ("versioned", versioned_value),
                    ("source_replay", replay_value),
                    ("discard", 0.0),
                ),
                key=lambda item: item[1],
            )[0]

        if choice == "discard":
            metrics["missed_credit"] += config.trace_items
            continue

        if choice == "unversioned":
            metrics["utility"] -= (
                config.unversioned_persist_cost * config.trace_items
            )
            metrics["persisted_trace_items"] += config.trace_items
            for valid in survived:
                if valid:
                    metrics["utility"] += 1.0
                    metrics["correct_credit"] += 1.0
                else:
                    metrics["utility"] -= config.false_blame_penalty
                    metrics["false_blame"] += 1.0
            continue

        if choice == "versioned":
            metrics["utility"] -= versioned_cost * config.trace_items
            metrics["persisted_trace_items"] += config.trace_items
        else:
            metrics["utility"] -= config.replay_cost * config.trace_items
            metrics["replayed_trace_items"] += config.trace_items

        for valid in survived:
            if valid:
                metrics["utility"] += 1.0
                metrics["correct_credit"] += 1.0
            else:
                metrics["missed_credit"] += 1.0

    denominator = config.episodes * config.trace_items
    return {key: value / denominator for key, value in metrics.items()}
