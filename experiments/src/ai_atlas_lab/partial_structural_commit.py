from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class I13Config:
    seed: int = 0
    migrations: int = 500
    moved_subjects: int = 12
    failure_probability: float = 0.20
    event_rate: float = 8.0
    dwell_steps: int = 80
    topology_benefit_per_step: float = 0.06
    stale_topology_penalty_per_step: float = 0.03
    naive_operation_cost: float = 0.001
    latency_penalty: float = 0.012
    naive_detection_delay: int = 10
    corruption_penalty_per_step: float = 0.12
    rollback_operation_cost: float = 0.0012
    stop_copy_cost: float = 0.0015
    stop_time_per_subject: float = 0.12
    transaction_stage_cost: float = 0.0022
    transaction_validation_cost: float = 0.012
    transaction_commit_pause: float = 0.50
    dual_stage_cost: float = 0.0025
    dual_handoff_steps: int = 3
    dual_carry_cost: float = 0.001


def _poisson(rng: random.Random, mean: float) -> int:
    if mean <= 0.0:
        return 0
    limit = math.exp(-mean)
    product = 1.0
    count = 0
    while product > limit:
        count += 1
        product *= rng.random()
    return count - 1


def run_i13(config: I13Config, policy: str) -> dict[str, float]:
    valid = {
        "naive_in_place",
        "stop_world_replace",
        "staged_transaction",
        "dual_version_handoff",
    }
    if policy not in valid:
        raise ValueError(f"unknown I13 policy: {policy}")
    if config.moved_subjects < 2:
        raise ValueError("I13 needs at least two moved subjects to expose partial commit")

    rng = random.Random(config.seed)
    total_utility = 0.0
    corrupt_migrations = 0
    lost_events = 0
    duplicate_events = 0
    downtime = 0.0
    rollback_operations = 0
    copied_operations = 0
    successful_migrations = 0
    aborted_migrations = 0
    ambiguous_resource_exposure = 0

    for _ in range(config.migrations):
        failed = rng.random() < config.failure_probability
        fail_at = (
            rng.randint(1, config.moved_subjects - 1)
            if failed
            else config.moved_subjects
        )

        if policy == "naive_in_place":
            copied_operations += fail_at
            total_utility -= config.naive_operation_cost * fail_at
            if failed:
                aborted_migrations += 1
                corrupt_migrations += 1
                ambiguous_resource_exposure += fail_at

                mixed_fraction = (
                    2.0
                    * min(fail_at, config.moved_subjects - fail_at)
                    / config.moved_subjects
                )
                arrivals = _poisson(
                    rng,
                    config.event_rate * config.naive_detection_delay,
                )
                lost = sum(
                    rng.random() < 0.45 * mixed_fraction
                    for _ in range(arrivals)
                )
                duplicates = sum(
                    rng.random() < 0.08 * mixed_fraction
                    for _ in range(max(0, arrivals - lost))
                )
                lost_events += lost
                duplicate_events += duplicates
                total_utility -= 0.08 * lost + 0.05 * duplicates
                total_utility -= (
                    config.corruption_penalty_per_step
                    * config.naive_detection_delay
                    * mixed_fraction
                )
                rollback_operations += fail_at
                total_utility -= config.rollback_operation_cost * fail_at
                total_utility -= (
                    config.stale_topology_penalty_per_step * config.dwell_steps
                )
            else:
                successful_migrations += 1
                total_utility += (
                    config.topology_benefit_per_step * config.dwell_steps
                )

        elif policy == "stop_world_replace":
            touched = fail_at if failed else config.moved_subjects
            copied_operations += touched
            blocked_time = config.stop_time_per_subject * touched
            downtime += blocked_time
            arrivals = _poisson(rng, config.event_rate * blocked_time)
            total_utility -= (
                config.stop_copy_cost * touched
                + config.latency_penalty * arrivals
            )
            if failed:
                aborted_migrations += 1
                total_utility -= (
                    config.stale_topology_penalty_per_step * config.dwell_steps
                )
            else:
                successful_migrations += 1
                total_utility += (
                    config.topology_benefit_per_step * config.dwell_steps
                )

        elif policy == "staged_transaction":
            touched = fail_at if failed else config.moved_subjects
            copied_operations += touched
            total_utility -= config.transaction_stage_cost * touched
            if failed:
                aborted_migrations += 1
                rollback_operations += touched
                total_utility -= config.rollback_operation_cost * touched
                total_utility -= (
                    config.stale_topology_penalty_per_step * config.dwell_steps
                )
            else:
                total_utility -= config.transaction_validation_cost
                downtime += config.transaction_commit_pause
                arrivals = _poisson(
                    rng,
                    config.event_rate * config.transaction_commit_pause,
                )
                total_utility -= config.latency_penalty * arrivals
                successful_migrations += 1
                total_utility += (
                    config.topology_benefit_per_step * config.dwell_steps
                )

        else:  # dual_version_handoff
            touched = fail_at if failed else config.moved_subjects
            copied_operations += touched
            total_utility -= config.dual_stage_cost * touched
            if failed:
                aborted_migrations += 1
                rollback_operations += touched
                total_utility -= config.rollback_operation_cost * touched
                total_utility -= (
                    config.stale_topology_penalty_per_step * config.dwell_steps
                )
            else:
                arrivals = _poisson(
                    rng,
                    config.event_rate * config.dual_handoff_steps,
                )
                total_utility -= (
                    config.dual_carry_cost
                    * config.dual_handoff_steps
                    * config.moved_subjects
                    + 0.001 * arrivals
                )
                successful_migrations += 1
                total_utility += (
                    config.topology_benefit_per_step * config.dwell_steps
                )

    migrations = config.migrations
    return {
        "net_utility_per_migration": total_utility / migrations,
        "corrupt_migration_rate": corrupt_migrations / migrations,
        "lost_events_per_migration": lost_events / migrations,
        "duplicate_events_per_migration": duplicate_events / migrations,
        "downtime_per_migration": downtime / migrations,
        "rollback_operations_per_migration": rollback_operations / migrations,
        "copy_operations_per_migration": copied_operations / migrations,
        "successful_migration_rate": successful_migrations / migrations,
        "aborted_migration_rate": aborted_migrations / migrations,
        "ambiguous_resource_exposure_per_migration": (
            ambiguous_resource_exposure / migrations
        ),
    }
