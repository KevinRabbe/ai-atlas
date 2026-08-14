from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class I13BConfig:
    seed: int = 0
    handoffs: int = 500
    failure_probability: float = 0.20
    request_rate: float = 10.0
    write_fraction: float = 0.30
    detection_delay: int = 8
    request_value: float = 0.04
    lost_request_penalty: float = 0.08
    duplicate_write_penalty: float = 0.30
    state_prepare_cost: float = 0.008
    direct_handoff_cost: float = 0.004
    stop_world_time: float = 1.20
    latency_penalty: float = 0.010
    lease_fence_pause: float = 0.15
    lease_fence_cost: float = 0.012
    dual_handoff_steps: int = 3
    dual_carry_cost: float = 0.002
    read_forward_cost: float = 0.0002


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


def run_i13b(config: I13BConfig, policy: str) -> dict[str, float]:
    valid = {
        "make_before_break",
        "break_before_make",
        "stop_world_transfer",
        "staged_lease_fence",
        "dual_read_single_write",
    }
    if policy not in valid:
        raise ValueError(f"unknown I13B policy: {policy}")

    rng = random.Random(config.seed)
    total_utility = 0.0
    ownership_violations = 0
    duplicate_writes = 0
    lost_requests = 0
    downtime = 0.0
    successful_handoffs = 0
    aborted_handoffs = 0

    for _ in range(config.handoffs):
        failed = rng.random() < config.failure_probability
        failure_stage = rng.choice((1, 2, 3)) if failed else 4

        if policy == "make_before_break":
            total_utility -= config.direct_handoff_cost
            # prepare -> activate new -> deactivate old
            if failed and failure_stage == 1:
                aborted_handoffs += 1
            elif failed and failure_stage == 2:
                aborted_handoffs += 1
                ownership_violations += 1
                arrivals = _poisson(
                    rng,
                    config.request_rate * config.detection_delay,
                )
                writes = sum(
                    rng.random() < config.write_fraction
                    for _ in range(arrivals)
                )
                conflicts = sum(rng.random() < 0.50 for _ in range(writes))
                duplicate_writes += conflicts
                total_utility -= config.duplicate_write_penalty * conflicts
            else:
                successful_handoffs += 1

        elif policy == "break_before_make":
            total_utility -= config.direct_handoff_cost
            # prepare -> deactivate old -> activate new
            if failed and failure_stage == 1:
                aborted_handoffs += 1
            elif failed and failure_stage == 2:
                aborted_handoffs += 1
                ownership_violations += 1
                arrivals = _poisson(
                    rng,
                    config.request_rate * config.detection_delay,
                )
                lost_requests += arrivals
                total_utility -= config.lost_request_penalty * arrivals
            else:
                successful_handoffs += 1

        elif policy == "stop_world_transfer":
            blocked_time = config.stop_world_time * (0.50 if failed else 1.0)
            arrivals = _poisson(rng, config.request_rate * blocked_time)
            downtime += blocked_time
            total_utility -= (
                config.state_prepare_cost
                + config.latency_penalty * arrivals
            )
            if failed:
                aborted_handoffs += 1
            else:
                successful_handoffs += 1

        elif policy == "staged_lease_fence":
            total_utility -= config.state_prepare_cost
            if failed:
                # Unpublished candidate state is discarded; old lease stays current.
                aborted_handoffs += 1
            else:
                arrivals = _poisson(
                    rng,
                    config.request_rate * config.lease_fence_pause,
                )
                downtime += config.lease_fence_pause
                total_utility -= (
                    config.lease_fence_cost
                    + config.latency_penalty * arrivals
                )
                successful_handoffs += 1

        else:  # dual_read_single_write
            total_utility -= config.state_prepare_cost
            if failed:
                aborted_handoffs += 1
            else:
                arrivals = _poisson(
                    rng,
                    config.request_rate * config.dual_handoff_steps,
                )
                reads = sum(
                    rng.random() >= config.write_fraction
                    for _ in range(arrivals)
                )
                total_utility -= (
                    config.dual_carry_cost * config.dual_handoff_steps
                    + config.read_forward_cost * reads
                    + config.lease_fence_cost
                )
                successful_handoffs += 1

        # Ordinary service after the handoff attempt remains available from
        # whichever valid owner survived/was promoted. This common value makes
        # transition-path losses/costs comparable without privileging success.
        total_utility += config.request_value * config.request_rate * 2.0

    handoffs = config.handoffs
    return {
        "net_utility_per_handoff": total_utility / handoffs,
        "ownership_violation_rate": ownership_violations / handoffs,
        "duplicate_writes_per_handoff": duplicate_writes / handoffs,
        "lost_requests_per_handoff": lost_requests / handoffs,
        "downtime_per_handoff": downtime / handoffs,
        "successful_handoff_rate": successful_handoffs / handoffs,
        "aborted_handoff_rate": aborted_handoffs / handoffs,
    }
