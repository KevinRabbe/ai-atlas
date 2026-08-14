from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class RepairScopeConfig:
    seed: int = 0
    steps: int = 2400
    components: int = 12
    family: str = "isolated"
    isolated_incident_probability: float = 0.06
    component_incident_probability: float = 0.45
    systemic_incident_probability: float = 0.55
    post_root_fix_incident_probability: float = 0.05
    local_cost: float = 0.04
    component_cost: float = 0.18
    structural_cost: float = 0.65
    local_success: float = 0.95
    component_success: float = 0.985
    structural_success: float = 0.96
    local_regression: float = 0.01
    component_regression: float = 0.025
    structural_regression: float = 0.12
    incident_damage: float = 1.0
    unresolved_penalty: float = 1.0
    regression_penalty: float = 2.0
    component_trigger_recurrences: int = 2
    structural_trigger_distinct_components: int = 4
    trigger_window: int = 24
    structural_retry_cooldown: int = 120


POLICIES = ("local_only", "component_only", "structural_only", "adaptive_scope")


def _repair(rng: random.Random, scope: str, config: RepairScopeConfig):
    if scope == "local":
        return rng.random() < config.local_success, rng.random() < config.local_regression, config.local_cost
    if scope == "component":
        return rng.random() < config.component_success, rng.random() < config.component_regression, config.component_cost
    if scope == "structural":
        return rng.random() < config.structural_success, rng.random() < config.structural_regression, config.structural_cost
    raise ValueError(scope)


def run_repair_scope(config: RepairScopeConfig, policy: str) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    hot_component = rng.randrange(config.components)
    component_root_fixed = False
    systemic_root_fixed = False
    recent_incidents: list[tuple[int, int]] = []
    last_structural_attempt = -10_000

    total_utility = 0.0
    change_cost = 0.0
    regressions = unresolved = incidents = 0
    local_changes = component_changes = structural_changes = 0

    for step in range(config.steps):
        if config.family == "isolated":
            p_incident = config.isolated_incident_probability
            if rng.random() >= p_incident:
                continue
            component = rng.randrange(config.components)
        elif config.family == "component":
            p_incident = (
                config.post_root_fix_incident_probability
                if component_root_fixed
                else config.component_incident_probability
            )
            if rng.random() >= p_incident:
                continue
            component = (
                hot_component
                if not component_root_fixed and rng.random() < 0.85
                else rng.randrange(config.components)
            )
        elif config.family == "systemic":
            p_incident = (
                config.post_root_fix_incident_probability
                if systemic_root_fixed
                else config.systemic_incident_probability
            )
            if rng.random() >= p_incident:
                continue
            component = rng.randrange(config.components)
        else:
            raise ValueError(config.family)

        incidents += 1
        total_utility -= config.incident_damage
        recent_incidents.append((step, component))
        recent_incidents = [
            item for item in recent_incidents
            if step - item[0] < config.trigger_window
        ]

        if policy == "local_only":
            scope = "local"
        elif policy == "component_only":
            scope = "component"
        elif policy == "structural_only":
            scope = "structural"
        elif policy == "adaptive_scope":
            distinct = len({component_id for _, component_id in recent_incidents})
            same_component = sum(
                1 for _, component_id in recent_incidents
                if component_id == component
            )
            can_structural = step - last_structural_attempt >= config.structural_retry_cooldown
            if distinct >= config.structural_trigger_distinct_components and can_structural:
                scope = "structural"
            elif same_component >= config.component_trigger_recurrences:
                scope = "component"
            else:
                scope = "local"
        else:
            raise ValueError(policy)

        success, regression, cost = _repair(rng, scope, config)
        total_utility -= cost
        change_cost += cost
        if scope == "local":
            local_changes += 1
        elif scope == "component":
            component_changes += 1
        else:
            structural_changes += 1
            last_structural_attempt = step

        if regression:
            regressions += 1
            total_utility -= config.regression_penalty

        if not success:
            unresolved += 1
            total_utility -= config.unresolved_penalty
            continue

        if config.family == "component":
            if scope == "component" and component == hot_component:
                component_root_fixed = True
            elif scope == "structural":
                component_root_fixed = True
        elif config.family == "systemic" and scope == "structural":
            systemic_root_fixed = True

    return {
        "net_utility_per_step": total_utility / config.steps,
        "incidents_per_step": incidents / config.steps,
        "change_cost_per_step": change_cost / config.steps,
        "regressions": regressions,
        "unresolved": unresolved,
        "local_changes": local_changes,
        "component_changes": component_changes,
        "structural_changes": structural_changes,
        "root_fixed": int(component_root_fixed or systemic_root_fixed),
    }


def run_repair_scope_experiment(config: RepairScopeConfig):
    return [(policy, run_repair_scope(config, policy)) for policy in POLICIES]
