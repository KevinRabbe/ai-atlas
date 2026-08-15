from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I18Config:
    seed: int = 0
    trials: int = 30_000
    unrelated_publication_max: int = 4
    ours_publish_probability: float = 0.60
    same_target_collision_probability: float = 0.22


def _finish(metrics: dict[str, float], trials: int) -> dict[str, float]:
    return {key: value / trials for key, value in metrics.items()}


def _decide(policy: str, *, base: int, current_version: int, current_ref: str, publication_ref: str | None) -> str:
    if policy == "predicted_target_version":
        if current_version == base + 1 and current_ref == "B":
            return "complete"
        if current_version == base:
            return "retry"
        return "discard"

    if policy == "state_ref_only":
        if current_ref == "B":
            return "complete"
        if current_version == base:
            return "retry"
        return "discard"

    if policy == "publication_provenance":
        if publication_ref == "ours":
            return "complete"
        if current_version == base:
            return "retry"
        return "discard"

    raise ValueError(f"unknown I18 policy: {policy}")


def run_unpredictable_target_version(config: I18Config, policy: str) -> dict[str, float]:
    """Unrelated publications advance a global counter before our publish."""

    rng = random.Random(config.seed)
    metrics: dict[str, float] = defaultdict(float)
    base = 10

    for _ in range(config.trials):
        unrelated = rng.randint(0, config.unrelated_publication_max)
        ours_published = rng.random() < config.ours_publish_probability

        if ours_published:
            current_version = base + 1 + unrelated
            current_ref = "B"
            publication_ref = "ours"
            expected = "complete"
        else:
            current_version = base
            current_ref = "A"
            publication_ref = None
            expected = "retry"

        action = _decide(
            policy,
            base=base,
            current_version=current_version,
            current_ref=current_ref,
            publication_ref=publication_ref,
        )

        metrics["correct_recovery"] += float(action == expected)
        metrics["missed_completion"] += float(ours_published and action != "complete")
        metrics["false_completion"] += float(not ours_published and action == "complete")

    return _finish(metrics, config.trials)


def run_same_target_collision(config: I18Config, policy: str) -> dict[str, float]:
    """Another publication can create the same state value as our candidate."""

    rng = random.Random(config.seed)
    metrics: dict[str, float] = defaultdict(float)
    base = 10

    for _ in range(config.trials):
        ours_published = rng.random() < config.ours_publish_probability

        if ours_published:
            current_version = 11
            current_ref = "B"
            publication_ref = "ours"
            expected = "complete"
        else:
            other_same_target = rng.random() < config.same_target_collision_probability
            if other_same_target:
                current_version = 11
                current_ref = "B"
                publication_ref = "other"
                expected = "discard"
            else:
                current_version = base
                current_ref = "A"
                publication_ref = None
                expected = "retry"

        action = _decide(
            policy,
            base=base,
            current_version=current_version,
            current_ref=current_ref,
            publication_ref=publication_ref,
        )

        metrics["correct_recovery"] += float(action == expected)
        metrics["missed_completion"] += float(ours_published and action != "complete")
        metrics["false_completion"] += float(not ours_published and action == "complete")

    return _finish(metrics, config.trials)
