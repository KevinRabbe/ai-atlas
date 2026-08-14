from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class CapabilityBoundaryConfig:
    seed: int = 0
    tasks: int = 6000
    shift_at: int = 3000
    privileged_fraction: float = 0.28
    authorized_given_privileged: float = 0.72
    high_context_risk_fraction: float = 0.32
    low_context_risk: float = 0.03
    high_context_risk: float = 0.38
    behavior_sensitivity: float = 0.82
    spoof_after_shift: float = 0.65
    harm_scale: float = 5.0


@dataclass(frozen=True)
class BoundaryPolicy:
    name: str


BEHAVIOR_ONLY = BoundaryPolicy("behavior_only")
NARROW_HARD_ONLY = BoundaryPolicy("narrow_hard_only")
BROAD_HARD = BoundaryPolicy("broad_hard")
HYBRID = BoundaryPolicy("hybrid")


def run_capability_boundary(config: CapabilityBoundaryConfig, policy: BoundaryPolicy) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    total_utility = 0.0
    invariant_violations = [0, 0]
    contextual_harms = [0, 0]
    blocked = 0
    useful_successes = 0

    for task_index in range(config.tasks):
        phase = 0 if task_index < config.shift_at else 1
        privileged = rng.random() < config.privileged_fraction
        authorized = not privileged or rng.random() < config.authorized_given_privileged
        high_context_risk = rng.random() < config.high_context_risk_fraction
        true_context_risk = config.high_context_risk if high_context_risk else config.low_context_risk
        consequence = rng.choice((1.0, 2.0, 4.0))
        value = rng.choice((1.0, 2.0, 4.0))

        if high_context_risk:
            observed_high_risk = rng.random() < config.behavior_sensitivity
        else:
            observed_high_risk = rng.random() < 0.08

        # Distribution shift attacks the behavioral estimate without
        # changing the exact authorization fact available to the boundary.
        if phase == 1 and privileged and not authorized and rng.random() < config.spoof_after_shift:
            observed_high_risk = False

        estimated_risk = config.high_context_risk if observed_high_risk else config.low_context_risk
        behavior_allows = (
            value
            - estimated_risk * config.harm_scale * consequence * value
            > 0.0
        )
        categorical_authority = not (privileged and not authorized)

        if policy == BEHAVIOR_ONLY:
            allow = behavior_allows
        elif policy == NARROW_HARD_ONLY:
            allow = categorical_authority
        elif policy == BROAD_HARD:
            allow = not privileged
        elif policy == HYBRID:
            allow = categorical_authority and behavior_allows
        else:
            raise ValueError(f"unknown policy: {policy.name}")

        if not allow:
            blocked += 1
            continue

        if privileged and not authorized:
            invariant_violations[phase] += 1
            total_utility -= 8.0 * consequence * value
            continue

        if rng.random() < true_context_risk:
            contextual_harms[phase] += 1
            total_utility -= config.harm_scale * consequence * value
        else:
            useful_successes += 1
            total_utility += value

    return {
        "net_utility_per_task": total_utility / config.tasks,
        "invariant_violations": sum(invariant_violations),
        "phase0_invariant_violations": invariant_violations[0],
        "phase1_invariant_violations": invariant_violations[1],
        "contextual_harms": sum(contextual_harms),
        "blocked_rate": blocked / config.tasks,
        "useful_success_rate": useful_successes / config.tasks,
    }


def run_capability_boundary_experiment(config: CapabilityBoundaryConfig) -> list[tuple[str, dict[str, float | int]]]:
    policies = (BEHAVIOR_ONLY, NARROW_HARD_ONLY, BROAD_HARD, HYBRID)
    return [(policy.name, run_capability_boundary(config, policy)) for policy in policies]
