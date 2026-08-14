from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I12Config:
    seed: int = 0
    cycles: int = 5
    regime_duration: int = 180
    threshold: float = 0.25
    event_probability: float = 0.68
    false_event_probability: float = 0.015
    evidence_decay: float = 0.94
    event_value: float = 0.045
    missed_event_penalty: float = 0.060
    directed_link_cost: float = 0.0016
    symmetric_extra_cost: float = 0.0009
    shared_scope_member_cost: float = 0.0020
    directed_dispatch_cost: float = 0.0008
    internal_dispatch_cost: float = 0.0001
    global_scope_cost: float = 0.13
    false_flow_cost: float = 0.0012


def _true_edges(regime: str) -> set[tuple[int, int]]:
    nodes = 12
    if regime == "sparse_directional":
        return {(node, (node + 4) % nodes) for node in range(nodes)}

    groups = (range(0, 4), range(4, 8), range(8, 12))
    reciprocal = {
        (left, right)
        for group in groups
        for left in group
        for right in group
        if left != right
    }
    if regime == "reciprocal_clusters":
        return reciprocal
    if regime == "mixed":
        return reciprocal | {(0, 4), (1, 5), (6, 10), (7, 11)}
    raise ValueError(f"unknown I12 regime: {regime}")


def _reciprocal_components(
    rates: dict[tuple[int, int], float],
    threshold: float,
    nodes: int = 12,
) -> list[int]:
    adjacency: list[list[int]] = [[] for _ in range(nodes)]
    for left in range(nodes):
        for right in range(left + 1, nodes):
            if rates[(left, right)] >= threshold and rates[(right, left)] >= threshold:
                adjacency[left].append(right)
                adjacency[right].append(left)

    labels = [-1] * nodes
    group = 0
    for start in range(nodes):
        if labels[start] >= 0:
            continue
        labels[start] = group
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in adjacency[node]:
                if labels[neighbor] < 0:
                    labels[neighbor] = group
                    stack.append(neighbor)
        group += 1
    return labels


def _represented(
    policy: str,
    rates: dict[tuple[int, int], float],
    config: I12Config,
) -> tuple[set[tuple[int, int]], list[int], float]:
    nodes = 12
    labels = list(range(nodes))

    if policy == "global_scope":
        return set(rates), [0] * nodes, config.global_scope_cost

    if policy == "directed_links":
        links = {edge for edge, value in rates.items() if value >= config.threshold}
        return links, labels, config.directed_link_cost * len(links)

    if policy == "symmetric_links":
        links: set[tuple[int, int]] = set()
        for left in range(nodes):
            for right in range(left + 1, nodes):
                if (
                    rates[(left, right)] >= config.threshold
                    or rates[(right, left)] >= config.threshold
                ):
                    links.add((left, right))
                    links.add((right, left))
        return (
            links,
            labels,
            (config.directed_link_cost + config.symmetric_extra_cost) * len(links),
        )

    if policy != "reciprocity_adaptive":
        raise ValueError(f"unknown I12 policy: {policy}")

    labels = _reciprocal_components(rates, config.threshold, nodes)
    links: set[tuple[int, int]] = set()
    for left in range(nodes):
        for right in range(nodes):
            if left == right:
                continue
            if labels[left] == labels[right] or rates[(left, right)] >= config.threshold:
                links.add((left, right))

    shared_members = sum(
        1
        for node in range(nodes)
        if sum(labels[other] == labels[node] for other in range(nodes)) > 1
    )
    cross_links = sum(labels[left] != labels[right] for left, right in links)
    carrying_cost = (
        config.shared_scope_member_cost * shared_members
        + config.directed_link_cost * cross_links
    )
    return links, labels, carrying_cost


def run_i12(config: I12Config, policy: str) -> dict[str, float]:
    valid = {
        "global_scope",
        "directed_links",
        "symmetric_links",
        "reciprocity_adaptive",
    }
    if policy not in valid:
        raise ValueError(f"unknown I12 policy: {policy}")

    rng = random.Random(config.seed)
    nodes = 12
    rates = {
        (left, right): 0.05
        for left in range(nodes)
        for right in range(nodes)
        if left != right
    }

    total_utility = 0.0
    missed_events = 0
    false_flows = 0
    represented_links = 0
    segment_utility: dict[str, float] = defaultdict(float)
    segment_steps: dict[str, int] = defaultdict(int)

    regimes = ("sparse_directional", "reciprocal_clusters", "mixed")
    for _ in range(config.cycles):
        for regime in regimes:
            true_edges = _true_edges(regime)
            for _ in range(config.regime_duration):
                events: set[tuple[int, int]] = set()
                for edge in rates:
                    probability = (
                        config.event_probability
                        if edge in true_edges
                        else config.false_event_probability
                    )
                    happened = rng.random() < probability
                    if happened:
                        events.add(edge)
                    rates[edge] = (
                        config.evidence_decay * rates[edge]
                        + (1.0 - config.evidence_decay) * float(happened)
                    )

                represented, labels, cost = _represented(policy, rates, config)
                captured = events & represented
                missed = events - represented
                false = represented - true_edges

                for left, right in captured:
                    internal = (
                        policy == "global_scope"
                        or (
                            policy == "reciprocity_adaptive"
                            and labels[left] == labels[right]
                        )
                    )
                    cost += (
                        config.internal_dispatch_cost
                        if internal
                        else config.directed_dispatch_cost
                    )

                utility = (
                    config.event_value * len(captured)
                    - config.missed_event_penalty * len(missed)
                    - config.false_flow_cost * len(false)
                    - cost
                )
                total_utility += utility
                segment_utility[regime] += utility
                segment_steps[regime] += 1
                missed_events += len(missed)
                false_flows += len(false)
                represented_links += len(represented)

    steps = config.cycles * len(regimes) * config.regime_duration
    result = {
        "net_utility_per_step": total_utility / steps,
        "missed_events_per_step": missed_events / steps,
        "false_flows_per_step": false_flows / steps,
        "represented_links_per_step": represented_links / steps,
    }
    for regime in regimes:
        result[f"{regime}_utility"] = (
            segment_utility[regime] / segment_steps[regime]
        )
    return result
