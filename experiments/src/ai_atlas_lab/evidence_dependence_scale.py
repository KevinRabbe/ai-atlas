from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I26DConfig:
    seed: int = 0
    tasks: int = 10_000
    source_count: int = 128
    group_size: int = 4
    active_pool_size: int = 32
    coupled_panel_probability: float = 0.55
    relation_query_cost: float = 0.015
    relation_storage_cost: float = 0.00002
    relation_ttl: int = 500
    false_independence_harm: float = 0.15


def _pairs(panel: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        tuple(sorted((left, right)))
        for index, left in enumerate(panel)
        for right in panel[index + 1 :]
    )


def run_i26d(config: I26DConfig, policy: str) -> dict[str, float]:
    valid = {
        "assume_independent",
        "dense_exact",
        "query_every_time",
        "cache_forever",
        "scoped_ttl",
    }
    if policy not in valid:
        raise ValueError(f"unknown I26D policy: {policy}")
    if config.source_count % config.group_size:
        raise ValueError("source_count must be divisible by group_size")
    if config.active_pool_size % config.group_size:
        raise ValueError("active_pool_size must be divisible by group_size")
    if config.active_pool_size * 2 > config.source_count:
        raise ValueError("experiment requires two disjoint active pools")

    rng = random.Random(config.seed)
    group = {
        source: source // config.group_size
        for source in range(config.source_count)
    }
    first_pool = tuple(range(config.active_pool_size))
    second_start = config.source_count - config.active_pool_size
    second_pool = tuple(range(second_start, config.source_count))
    possible_pairs = config.source_count * (config.source_count - 1) // 2

    cache: dict[tuple[int, int], int] = {}
    metrics: dict[str, float] = defaultdict(float)

    if policy == "dense_exact":
        metrics["relation_cost"] += (
            possible_pairs * config.relation_query_cost
        )
        metrics["relation_queries"] += possible_pairs

    for step in range(config.tasks):
        active_pool = (
            first_pool if step < config.tasks // 2 else second_pool
        )
        active_groups = tuple(sorted({group[source] for source in active_pool}))

        if rng.random() < config.coupled_panel_probability:
            shared_group = rng.choice(active_groups)
            shared_members = tuple(
                source for source in active_pool if group[source] == shared_group
            )
            left, right = rng.sample(shared_members, 2)
            independent_pool = tuple(
                source for source in active_pool if group[source] != shared_group
            )
            other_a, other_b = rng.sample(independent_pool, 2)
            panel = (left, right, other_a, other_b)
        else:
            selected_groups = rng.sample(active_groups, 4)
            panel = tuple(
                rng.choice(
                    tuple(
                        source
                        for source in active_pool
                        if group[source] == selected_group
                    )
                )
                for selected_group in selected_groups
            )

        consequence = rng.choice((1.0, 2.0, 4.0, 8.0))
        active_pairs = _pairs(panel)
        dependent_pairs = tuple(
            pair for pair in active_pairs if group[pair[0]] == group[pair[1]]
        )

        if policy == "assume_independent":
            metrics["assurance_harm"] += (
                len(dependent_pairs)
                * config.false_independence_harm
                * consequence
            )

        elif policy == "dense_exact":
            metrics["relation_cost"] += (
                possible_pairs * config.relation_storage_cost
            )

        elif policy == "query_every_time":
            metrics["relation_queries"] += len(active_pairs)
            metrics["relation_cost"] += (
                len(active_pairs) * config.relation_query_cost
            )

        elif policy == "cache_forever":
            for pair in active_pairs:
                if pair not in cache:
                    cache[pair] = config.tasks
                    metrics["relation_queries"] += 1.0
                    metrics["relation_cost"] += config.relation_query_cost
            metrics["relation_cost"] += (
                len(cache) * config.relation_storage_cost
            )

        else:  # scoped_ttl
            expired = [pair for pair, expiry in cache.items() if expiry < step]
            for pair in expired:
                del cache[pair]
            for pair in active_pairs:
                if pair not in cache:
                    metrics["relation_queries"] += 1.0
                    metrics["relation_cost"] += config.relation_query_cost
                cache[pair] = step + config.relation_ttl
            metrics["relation_cost"] += (
                len(cache) * config.relation_storage_cost
            )

        metrics["base_utility"] += 1.0
        metrics["max_cached_relations"] = max(
            metrics["max_cached_relations"],
            float(len(cache)),
        )

    final_state = (
        possible_pairs
        if policy == "dense_exact"
        else len(cache)
        if policy in {"cache_forever", "scoped_ttl"}
        else 0
    )
    net_utility = (
        metrics["base_utility"]
        - metrics["relation_cost"]
        - metrics["assurance_harm"]
    ) / config.tasks
    return {
        "utility": net_utility,
        "relation_cost": metrics["relation_cost"] / config.tasks,
        "assurance_harm": metrics["assurance_harm"] / config.tasks,
        "relation_queries": metrics["relation_queries"] / config.tasks,
        "final_relation_state": float(final_state),
        "max_cached_relations": metrics["max_cached_relations"],
        "possible_pair_relations": float(possible_pairs),
    }
