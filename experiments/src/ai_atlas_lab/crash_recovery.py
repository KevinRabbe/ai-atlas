from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


POLICIES = (
    "assurance_replay",
    "phase_recheck",
    "version_fenced",
    "atomic_snapshot",
)

_STAGES = (
    "prepared",
    "assured",
    "published_unmarked",
    "published_marked",
    "superseded",
)
_STAGE_WEIGHTS = (0.16, 0.26, 0.22, 0.20, 0.16)


@dataclass(frozen=True)
class I14Config:
    seed: int = 0
    trials: int = 10_000
    revoke_probability: float = 0.08
    retract_probability: float = 0.10


def _mean_metrics(total: dict[str, float], trials: int) -> dict[str, float]:
    return {key: value / trials for key, value in total.items()}


def run_resource_recovery(config: I14Config, policy: str) -> dict[str, float]:
    if policy not in POLICIES:
        raise ValueError(f"unknown I14 policy: {policy}")
    rng = random.Random(config.seed)
    metrics: dict[str, float] = defaultdict(float)

    for _ in range(config.trials):
        stage = rng.choices(_STAGES, _STAGE_WEIGHTS)[0]
        base_version = 10
        target_version = 11
        current_version = base_version
        owner = 0
        phase = "prepared"
        assured = False
        current_authority = True

        if stage == "assured":
            assured = True
            phase = "assured"
            current_authority = rng.random() >= config.revoke_probability
        elif stage == "published_unmarked":
            assured = True
            phase = "assured"
            current_version = target_version
            owner = 1
        elif stage == "published_marked":
            assured = True
            phase = "published"
            current_version = target_version
            owner = 1
        elif stage == "superseded":
            assured = True
            phase = "assured"
            current_version = 12
            owner = 2

        action = "none"
        if policy == "assurance_replay":
            if assured and phase != "published":
                current_version += 1
                owner = 1
                action = "publish"
        elif policy == "phase_recheck":
            if assured and phase != "published" and current_authority:
                current_version += 1
                owner = 1
                action = "publish"
        elif policy == "version_fenced":
            if phase == "published":
                action = "complete"
            elif current_version == target_version and owner == 1:
                action = "complete"
            elif current_version == base_version and assured and current_authority:
                current_version = target_version
                owner = 1
                action = "publish"
            else:
                action = "discard"
        else:  # atomic-snapshot upper-bound comparator
            if stage == "assured" and current_authority:
                current_version = target_version
                owner = 1
                action = "publish"
            elif stage in {"published_unmarked", "published_marked"}:
                action = "complete"
            else:
                action = "discard"

        if stage == "assured" and current_authority:
            correct = current_version == target_version and owner == 1
        elif stage == "assured":
            correct = current_version == base_version and owner == 0
        elif stage == "prepared":
            correct = current_version == base_version and owner == 0
        elif stage in {"published_unmarked", "published_marked"}:
            correct = current_version == target_version and owner == 1
        else:
            correct = current_version == 12 and owner == 2

        metrics["correct_recovery"] += float(correct)
        metrics["duplicate_publication"] += float(
            stage == "published_unmarked" and action == "publish"
        )
        metrics["revoked_publication"] += float(
            stage == "assured" and not current_authority and action == "publish"
        )
        metrics["superseded_overwrite"] += float(
            stage == "superseded" and action == "publish"
        )
        metrics["recovery_publications"] += float(action == "publish")

    return _mean_metrics(metrics, config.trials)


def run_knowledge_recovery(config: I14Config, policy: str) -> dict[str, float]:
    if policy not in POLICIES:
        raise ValueError(f"unknown I14 policy: {policy}")
    rng = random.Random(config.seed)
    metrics: dict[str, float] = defaultdict(float)

    for _ in range(config.trials):
        stage = rng.choices(_STAGES, _STAGE_WEIGHTS)[0]
        base_version = 20
        target_version = 21
        current_version = base_version
        claim = "old"
        phase = "prepared"
        assured = False
        evidence_current = True

        if stage == "assured":
            assured = True
            phase = "assured"
            evidence_current = rng.random() >= config.retract_probability
        elif stage == "published_unmarked":
            assured = True
            phase = "assured"
            current_version = target_version
            claim = "candidate"
        elif stage == "published_marked":
            assured = True
            phase = "published"
            current_version = target_version
            claim = "candidate"
        elif stage == "superseded":
            assured = True
            phase = "assured"
            current_version = 22
            claim = "newer"

        action = "none"
        if policy == "assurance_replay":
            if assured and phase != "published":
                current_version += 1
                claim = "candidate"
                action = "publish"
        elif policy == "phase_recheck":
            if assured and phase != "published" and evidence_current:
                current_version += 1
                claim = "candidate"
                action = "publish"
        elif policy == "version_fenced":
            if phase == "published":
                action = "complete"
            elif current_version == target_version and claim == "candidate":
                action = "complete"
            elif current_version == base_version and assured and evidence_current:
                current_version = target_version
                claim = "candidate"
                action = "publish"
            else:
                action = "discard"
        else:
            if stage == "assured" and evidence_current:
                current_version = target_version
                claim = "candidate"
                action = "publish"
            elif stage in {"published_unmarked", "published_marked"}:
                action = "complete"
            else:
                action = "discard"

        if stage == "assured" and evidence_current:
            correct = current_version == target_version and claim == "candidate"
        elif stage == "assured":
            correct = current_version == base_version and claim == "old"
        elif stage == "prepared":
            correct = current_version == base_version and claim == "old"
        elif stage in {"published_unmarked", "published_marked"}:
            correct = current_version == target_version and claim == "candidate"
        else:
            correct = current_version == 22 and claim == "newer"

        metrics["correct_recovery"] += float(correct)
        metrics["duplicate_publication"] += float(
            stage == "published_unmarked" and action == "publish"
        )
        metrics["retracted_promotion"] += float(
            stage == "assured" and not evidence_current and action == "publish"
        )
        metrics["superseded_overwrite"] += float(
            stage == "superseded" and action == "publish"
        )
        metrics["recovery_publications"] += float(action == "publish")

    return _mean_metrics(metrics, config.trials)


def run_i14_experiment(config: I14Config) -> dict[str, dict[str, dict[str, float]]]:
    return {
        policy: {
            "resource": run_resource_recovery(config, policy),
            "knowledge": run_knowledge_recovery(config, policy),
        }
        for policy in POLICIES
    }
