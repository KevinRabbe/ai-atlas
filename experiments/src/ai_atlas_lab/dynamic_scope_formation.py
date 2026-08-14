from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I07Config:
    seed: int = 0
    nodes: int = 12
    cycles: int = 6
    regime_duration: int = 120
    inside_event_probability: float = 0.65
    outside_event_probability: float = 0.04
    evidence_decay: float = 0.94
    coupling_threshold: float = 0.30
    decision_interval: int = 10
    coupled_pair_benefit: float = 0.05
    missed_coupling_penalty: float = 0.07
    false_group_penalty: float = 0.012
    migration_cost: float = 0.025


def _partitions(nodes: int) -> list[list[int]]:
    if nodes != 12:
        raise ValueError("I07 currently pins twelve nodes so its three recurrent partitions stay matched")
    return [
        [index // 4 for index in range(nodes)],
        [index % 3 for index in range(nodes)],
        [(index // 2) % 3 for index in range(nodes)],
    ]


def _components(nodes: int, evidence: dict[tuple[int, int], float], threshold: float) -> list[int]:
    adjacency: list[list[int]] = [[] for _ in range(nodes)]
    for (left, right), value in evidence.items():
        if value >= threshold:
            adjacency[left].append(right)
            adjacency[right].append(left)

    labels = [-1] * nodes
    group = 0
    for start in range(nodes):
        if labels[start] >= 0:
            continue
        stack = [start]
        labels[start] = group
        while stack:
            node = stack.pop()
            for neighbor in adjacency[node]:
                if labels[neighbor] < 0:
                    labels[neighbor] = group
                    stack.append(neighbor)
        group += 1
    return labels


def _partition_utility(true_partition: list[int], proposed: list[int], config: I07Config) -> float:
    utility = 1.0
    for left in range(config.nodes):
        for right in range(left + 1, config.nodes):
            truly_coupled = true_partition[left] == true_partition[right]
            grouped = proposed[left] == proposed[right]
            if truly_coupled and grouped:
                utility += config.coupled_pair_benefit / config.nodes
            elif truly_coupled and not grouped:
                utility -= config.missed_coupling_penalty / config.nodes
            elif not truly_coupled and grouped:
                utility -= config.false_group_penalty / config.nodes
    return utility


def _migration_cost(old: list[int] | None, new: list[int], config: I07Config) -> float:
    if old is None:
        return 0.0
    changed = 0
    for node in range(config.nodes):
        old_scope = {other for other in range(config.nodes) if old[other] == old[node]}
        new_scope = {other for other in range(config.nodes) if new[other] == new[node]}
        changed += int(old_scope != new_scope)
    return config.migration_cost * changed / config.nodes


def _pairwise_agreement(true_partition: list[int], proposed: list[int], nodes: int) -> float:
    correct = 0
    total = 0
    for left in range(nodes):
        for right in range(left + 1, nodes):
            correct += int(
                (true_partition[left] == true_partition[right])
                == (proposed[left] == proposed[right])
            )
            total += 1
    return correct / total


def generate_i07_lifetime(config: I07Config) -> list[tuple[list[int], dict[tuple[int, int], bool]]]:
    rng = random.Random(config.seed)
    regimes = _partitions(config.nodes)
    lifetime: list[tuple[list[int], dict[tuple[int, int], bool]]] = []
    for _ in range(config.cycles):
        for partition in regimes:
            for _ in range(config.regime_duration):
                events: dict[tuple[int, int], bool] = {}
                for left in range(config.nodes):
                    for right in range(left + 1, config.nodes):
                        probability = (
                            config.inside_event_probability
                            if partition[left] == partition[right]
                            else config.outside_event_probability
                        )
                        events[(left, right)] = rng.random() < probability
                lifetime.append((partition, events))
    return lifetime


def run_i07(config: I07Config, policy: str) -> dict[str, float | int]:
    valid = {"global", "local", "fixed_initial", "adaptive", "oracle"}
    if policy not in valid:
        raise ValueError(f"unknown I07 policy: {policy}")

    regimes = _partitions(config.nodes)
    evidence = {
        (left, right): 0.10
        for left in range(config.nodes)
        for right in range(left + 1, config.nodes)
    }
    proposed: list[int] | None = None
    total_utility = 0.0
    migrations = 0
    migration_spend = 0.0
    agreement = 0.0

    for step, (true_partition, events) in enumerate(generate_i07_lifetime(config)):
        for edge, happened in events.items():
            evidence[edge] = (
                config.evidence_decay * evidence[edge]
                + (1.0 - config.evidence_decay) * float(happened)
            )

        if policy == "global":
            candidate = [0] * config.nodes
        elif policy == "local":
            candidate = list(range(config.nodes))
        elif policy == "fixed_initial":
            candidate = regimes[0]
        elif policy == "oracle":
            candidate = true_partition
        else:
            candidate = proposed if proposed is not None else list(range(config.nodes))
            if step % config.decision_interval == 0:
                candidate = _components(
                    config.nodes, evidence, config.coupling_threshold
                )

        if proposed is None or candidate != proposed:
            cost = _migration_cost(proposed, candidate, config)
            if proposed is not None and cost > 0.0:
                migrations += 1
            migration_spend += cost
            proposed = list(candidate)
            total_utility -= cost

        total_utility += _partition_utility(true_partition, proposed, config)
        agreement += _pairwise_agreement(true_partition, proposed, config.nodes)

    steps = len(generate_i07_lifetime(config))
    return {
        "net_utility_per_step": total_utility / steps,
        "pairwise_scope_accuracy": agreement / steps,
        "migrations": migrations,
        "migration_spend_per_step": migration_spend / steps,
    }
