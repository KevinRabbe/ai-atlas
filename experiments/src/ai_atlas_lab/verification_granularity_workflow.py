from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class WorkflowVerificationConfig:
    seed: int = 0
    tasks: int = 5000
    process_check_cost: float = 0.20
    outcome_check_cost: float = 0.20
    check_sensitivity: float = 0.96
    process_low_risk: float = 0.04
    process_high_risk: float = 0.35
    outcome_low_risk: float = 0.03
    outcome_high_risk: float = 0.30
    high_risk_cue_probability: float = 0.30


@dataclass(frozen=True)
class VerificationPolicy:
    name: str


PROCESS_ONLY = VerificationPolicy("process_only")
OUTCOME_ONLY = VerificationPolicy("outcome_only")
UNIFORM_BOTH = VerificationPolicy("uniform_both")
ADAPTIVE_GRANULARITY = VerificationPolicy("adaptive_granularity")


def run_workflow_verification(config: WorkflowVerificationConfig, policy: VerificationPolicy) -> dict[str, float]:
    rng = random.Random(config.seed)
    total_utility = 0.0
    process_harms = 0
    outcome_harms = 0
    process_checks = 0
    outcome_checks = 0

    for _ in range(config.tasks):
        process_cue_high = rng.random() < config.high_risk_cue_probability
        outcome_cue_high = rng.random() < config.high_risk_cue_probability
        process_risk = config.process_high_risk if process_cue_high else config.process_low_risk
        outcome_risk = config.outcome_high_risk if outcome_cue_high else config.outcome_low_risk
        consequence = rng.choice((1.0, 3.0, 8.0))
        task_reward = rng.choice((1.0, 2.0, 4.0))
        process_failure = rng.random() < process_risk
        outcome_failure = rng.random() < outcome_risk

        check_process = False
        check_outcome = False
        if policy == PROCESS_ONLY:
            check_process = True
        elif policy == OUTCOME_ONLY:
            check_outcome = True
        elif policy == UNIFORM_BOTH:
            check_process = True
            check_outcome = True
        elif policy == ADAPTIVE_GRANULARITY:
            estimated_process_harm_reduction = process_risk * 1.5 * consequence * config.check_sensitivity
            estimated_outcome_harm_reduction = outcome_risk * consequence * config.check_sensitivity
            check_process = estimated_process_harm_reduction > config.process_check_cost
            check_outcome = estimated_outcome_harm_reduction > config.outcome_check_cost
        else:
            raise ValueError(f"unknown policy: {policy.name}")

        if check_process:
            process_checks += 1
            total_utility -= config.process_check_cost
            if process_failure and rng.random() < config.check_sensitivity:
                process_failure = False

        if check_outcome:
            outcome_checks += 1
            total_utility -= config.outcome_check_cost
            if outcome_failure and rng.random() < config.check_sensitivity:
                outcome_failure = False

        total_utility += task_reward
        if process_failure:
            total_utility -= 1.5 * consequence
            process_harms += 1
        if outcome_failure:
            total_utility -= consequence
            outcome_harms += 1

    return {
        "net_utility_per_task": total_utility / config.tasks,
        "process_harm_rate": process_harms / config.tasks,
        "outcome_harm_rate": outcome_harms / config.tasks,
        "checks_per_task": (process_checks + outcome_checks) / config.tasks,
        "process_checks_per_task": process_checks / config.tasks,
        "outcome_checks_per_task": outcome_checks / config.tasks,
    }


def run_workflow_verification_experiment(config: WorkflowVerificationConfig) -> list[tuple[str, dict[str, float]]]:
    policies = (PROCESS_ONLY, OUTCOME_ONLY, UNIFORM_BOTH, ADAPTIVE_GRANULARITY)
    return [(policy.name, run_workflow_verification(config, policy)) for policy in policies]
