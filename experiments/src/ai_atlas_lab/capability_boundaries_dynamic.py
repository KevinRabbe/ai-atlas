from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class DynamicAuthorityConfig:
    seed: int = 0
    tasks: int = 8000
    principals: int = 24
    flip_probability: float = 0.012
    live_lookup_cost: float = 0.018
    refresh_cost: float = 0.05
    contextual_high_fraction: float = 0.28
    low_context_risk: float = 0.02
    high_context_risk: float = 0.33
    behavior_sensitivity: float = 0.84
    harm_scale: float = 5.0


@dataclass(frozen=True)
class DynamicBoundaryPolicy:
    name: str


BEHAVIOR_ONLY = DynamicBoundaryPolicy("behavior_only")
STATIC_HYBRID = DynamicBoundaryPolicy("static_hybrid")
LIVE_HYBRID = DynamicBoundaryPolicy("live_hybrid")
VERSIONED_HYBRID = DynamicBoundaryPolicy("versioned_hybrid")


def run_dynamic_authority(config: DynamicAuthorityConfig, policy: DynamicBoundaryPolicy) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    authority = [rng.random() < 0.72 for _ in range(config.principals)]
    versions = [0 for _ in range(config.principals)]
    static_authority = authority.copy()
    cached_authority = authority.copy()
    cached_versions = versions.copy()

    total_utility = 0.0
    invariant_violations = 0
    contextual_harms = 0
    live_lookups = 0
    refreshes = 0
    blocked = 0
    useful_successes = 0

    for _ in range(config.tasks):
        if rng.random() < config.flip_probability:
            index = rng.randrange(config.principals)
            authority[index] = not authority[index]
            versions[index] += 1

        principal = rng.randrange(config.principals)
        high_context_risk = rng.random() < config.contextual_high_fraction
        true_risk = config.high_context_risk if high_context_risk else config.low_context_risk
        consequence = rng.choice((1.0, 2.0, 4.0))
        value = rng.choice((1.0, 2.0, 4.0))

        if high_context_risk:
            observed_high = rng.random() < config.behavior_sensitivity
        else:
            observed_high = rng.random() < 0.07

        estimated_risk = config.high_context_risk if observed_high else config.low_context_risk
        behavioral_allow = value - estimated_risk * config.harm_scale * consequence * value > 0.0

        if policy == BEHAVIOR_ONLY:
            allow = behavioral_allow
        elif policy == STATIC_HYBRID:
            allow = static_authority[principal] and behavioral_allow
        elif policy == LIVE_HYBRID:
            total_utility -= config.live_lookup_cost
            live_lookups += 1
            allow = authority[principal] and behavioral_allow
        elif policy == VERSIONED_HYBRID:
            if cached_versions[principal] != versions[principal]:
                total_utility -= config.refresh_cost
                refreshes += 1
                cached_versions[principal] = versions[principal]
                cached_authority[principal] = authority[principal]
            allow = cached_authority[principal] and behavioral_allow
        else:
            raise ValueError(f"unknown policy: {policy.name}")

        if not allow:
            blocked += 1
            continue

        if not authority[principal]:
            invariant_violations += 1
            total_utility -= 10.0 * consequence * value
            continue

        if rng.random() < true_risk:
            contextual_harms += 1
            total_utility -= config.harm_scale * consequence * value
        else:
            useful_successes += 1
            total_utility += value

    return {
        "net_utility_per_task": total_utility / config.tasks,
        "invariant_violations": invariant_violations,
        "contextual_harms": contextual_harms,
        "live_lookups_per_task": live_lookups / config.tasks,
        "refreshes_per_task": refreshes / config.tasks,
        "blocked_rate": blocked / config.tasks,
        "useful_success_rate": useful_successes / config.tasks,
    }


def run_dynamic_authority_experiment(config: DynamicAuthorityConfig) -> list[tuple[str, dict[str, float | int]]]:
    policies = (BEHAVIOR_ONLY, STATIC_HYBRID, LIVE_HYBRID, VERSIONED_HYBRID)
    return [(policy.name, run_dynamic_authority(config, policy)) for policy in policies]
