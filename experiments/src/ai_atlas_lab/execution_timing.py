from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class ExecutionTimingConfig:
    seed: int = 0
    steps: int = 1200
    sparse_nodes: int = 80
    sparse_events: int = 3
    sparse_query_nodes: int = 12
    operation_cost: float = 0.0018
    message_cost: float = 0.0005
    error_penalty: float = 1.2
    coupled_nodes: int = 48
    coupled_update_probability: float = 0.55
    coupled_query_probability: float = 0.30
    coupled_partial_delivery: int = 8
    barrier_latency_cost: float = 0.04


def run_sparse_event_graph(
    config: ExecutionTimingConfig,
    variant: str,
) -> dict[str, float | int]:
    if variant not in {"sync_global", "async_naive", "scoped_event"}:
        raise ValueError(f"unknown variant: {variant}")

    rng = random.Random(config.seed)
    downstream = {
        node: tuple(
            rng.sample(
                [candidate for candidate in range(config.sparse_nodes) if candidate != node],
                2,
            )
        )
        for node in range(config.sparse_nodes)
    }

    dirty: set[int] = set()
    total_utility = 0.0
    operations = 0
    messages = 0
    stale_reads = 0
    total_reads = 0

    for _ in range(config.steps):
        sources = rng.sample(range(config.sparse_nodes), config.sparse_events)
        affected = set(sources)
        for source in sources:
            affected.update(downstream[source])
        dirty.update(affected)

        step_operations = 0
        step_messages = 0
        if variant == "sync_global":
            step_operations = config.sparse_nodes
            dirty.clear()
        elif variant == "async_naive":
            step_operations = len(sources)
            for source in sources:
                dirty.discard(source)
        else:
            step_operations = len(affected)
            step_messages = len(affected) - len(sources)
            dirty.difference_update(affected)

        query = rng.sample(range(config.sparse_nodes), config.sparse_query_nodes)
        bad = sum(node in dirty for node in query)
        stale_reads += bad
        total_reads += len(query)

        if variant == "async_naive" and bad:
            # A stale read exposes the missed dependency and repairs that node lazily.
            step_operations += bad
            for node in query:
                dirty.discard(node)

        operations += step_operations
        messages += step_messages
        total_utility += (
            1.0
            - config.error_penalty * bad / len(query)
            - config.operation_cost * step_operations
            - config.message_cost * step_messages
        )

    return {
        "net_utility_per_step": total_utility / config.steps,
        "stale_read_rate": stale_reads / total_reads,
        "operations_per_step": operations / config.steps,
        "messages_per_step": messages / config.steps,
    }


def run_version_coupled_workload(
    config: ExecutionTimingConfig,
    variant: str,
) -> dict[str, float | int]:
    if variant not in {"sync_global", "async_naive", "scoped_event"}:
        raise ValueError(f"unknown variant: {variant}")

    rng = random.Random(config.seed + 500)
    current_version = 0
    materialized_versions = [0] * config.coupled_nodes

    total_reward = 0.0
    operations = 0
    messages = 0
    inconsistent_queries = 0
    queries = 0
    barriers = 0
    barrier_waits = 0

    for _ in range(config.steps):
        if rng.random() < config.coupled_update_probability:
            current_version += 1
            if variant == "sync_global":
                materialized_versions = [current_version] * config.coupled_nodes
                operations += config.coupled_nodes
            elif variant == "async_naive":
                for node in rng.sample(range(config.coupled_nodes), config.coupled_partial_delivery):
                    materialized_versions[node] = current_version
                operations += config.coupled_partial_delivery
                messages += config.coupled_partial_delivery
            else:
                # Keep only the new logical version until a consistent snapshot is required.
                messages += 1

        if rng.random() < config.coupled_query_probability:
            queries += 1
            if variant == "scoped_event" and any(
                version != current_version for version in materialized_versions
            ):
                changed = sum(
                    version != current_version for version in materialized_versions
                )
                materialized_versions = [current_version] * config.coupled_nodes
                operations += changed
                messages += changed
                barriers += 1
                barrier_waits += 1
                total_reward -= config.barrier_latency_cost

            consistent = all(
                version == current_version for version in materialized_versions
            )
            if consistent:
                total_reward += 1.0
            else:
                total_reward -= config.error_penalty
                inconsistent_queries += 1

    total_reward -= config.operation_cost * operations
    total_reward -= config.message_cost * messages

    return {
        "net_utility_per_step": total_reward / config.steps,
        "inconsistent_query_rate": inconsistent_queries / max(1, queries),
        "operations_per_step": operations / config.steps,
        "messages_per_step": messages / config.steps,
        "barriers_per_query": barriers / max(1, queries),
        "barrier_wait_rate": barrier_waits / max(1, queries),
        "queries": queries,
    }


def run_execution_timing_experiment(
    config: ExecutionTimingConfig,
) -> dict[str, list[tuple[str, dict[str, float | int]]]]:
    variants = ("sync_global", "async_naive", "scoped_event")
    return {
        "sparse_event_graph": [
            (variant, run_sparse_event_graph(config, variant))
            for variant in variants
        ],
        "version_coupled_workload": [
            (variant, run_version_coupled_workload(config, variant))
            for variant in variants
        ],
    }
