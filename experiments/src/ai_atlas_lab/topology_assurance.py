from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I09Config:
    seed: int = 0
    nodes: int = 12
    cycles: int = 5
    regime_duration: int = 120
    inside_event_probability: float = 0.65
    outside_event_probability: float = 0.04
    evidence_decay: float = 0.94
    coupling_threshold: float = 0.30
    high_threshold: float = 0.48
    decision_interval: int = 10
    attack_fraction: float = 0.22
    attack_false_edge_probability: float = 0.78
    audit_inside_probability: float = 0.78
    audit_outside_probability: float = 0.03
    audit_samples: int = 5
    audit_acceptance: float = 0.55
    audit_cost: float = 0.00045
    migration_cost: float = 0.025
    coupled_pair_benefit: float = 0.05
    missed_coupling_penalty: float = 0.10
    false_group_penalty: float = 0.03


def _partitions(nodes: int) -> list[list[int]]:
    if nodes != 12:
        raise ValueError("I09 currently pins twelve nodes to the matched topology family")
    return [
        [index // 4 for index in range(nodes)],
        [index % 3 for index in range(nodes)],
        [(index // 2) % 3 for index in range(nodes)],
    ]


def _components(
    nodes: int,
    evidence: dict[tuple[int, int], float],
    threshold: float,
) -> list[int]:
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


def _pairwise_accuracy(true_partition: list[int], proposed: list[int], nodes: int) -> float:
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


def _partition_utility(true_partition: list[int], proposed: list[int], config: I09Config) -> float:
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


def _changed_pairs(old: list[int], new: list[int], nodes: int) -> list[tuple[int, int]]:
    return [
        (left, right)
        for left in range(nodes)
        for right in range(left + 1, nodes)
        if (old[left] == old[right]) != (new[left] == new[right])
    ]


def _changed_nodes(old: list[int], new: list[int], nodes: int) -> int:
    changed = 0
    for node in range(nodes):
        old_scope = {other for other in range(nodes) if old[other] == old[node]}
        new_scope = {other for other in range(nodes) if new[other] == new[node]}
        changed += int(old_scope != new_scope)
    return changed


def _audit_edge(
    rng: random.Random,
    truly_coupled: bool,
    config: I09Config,
) -> tuple[bool, int]:
    positives = sum(
        rng.random()
        < (
            config.audit_inside_probability
            if truly_coupled
            else config.audit_outside_probability
        )
        for _ in range(config.audit_samples)
    )
    return positives / config.audit_samples >= 0.40, config.audit_samples


def _audit_candidate(
    rng: random.Random,
    true_partition: list[int],
    current: list[int],
    candidate: list[int],
    config: I09Config,
) -> tuple[bool, int]:
    changed = _changed_pairs(current, candidate, config.nodes)
    if not changed:
        return True, 0

    agreements = 0
    samples = 0
    for left, right in changed:
        predicted_same, used = _audit_edge(
            rng,
            true_partition[left] == true_partition[right],
            config,
        )
        samples += used
        agreements += int(predicted_same == (candidate[left] == candidate[right]))
    return agreements / len(changed) >= config.audit_acceptance, samples


def run_i09(
    config: I09Config,
    policy: str,
    adversarial: bool = True,
) -> dict[str, float | int]:
    valid = {"raw", "high_threshold", "uniform_independent", "selective_independent"}
    if policy not in valid:
        raise ValueError(f"unknown I09 policy: {policy}")

    rng = random.Random(config.seed)
    audit_rng = random.Random(config.seed + 55_555)
    evidence = {
        (left, right): 0.10
        for left in range(config.nodes)
        for right in range(left + 1, config.nodes)
    }
    current = list(range(config.nodes))

    total_utility = 0.0
    pairwise_accuracy = 0.0
    migrations = 0
    harmful_migrations = 0
    audit_samples = 0
    steps = 0

    for _ in range(config.cycles):
        for true_partition in _partitions(config.nodes):
            groups: dict[int, list[int]] = {}
            for node, group in enumerate(true_partition):
                groups.setdefault(group, []).append(node)
            first, second = sorted(groups)[:2]
            attacked_edges = {
                (min(left, right), max(left, right))
                for left in groups[first]
                for right in groups[second]
            }
            attack_steps = int(config.regime_duration * config.attack_fraction)
            attack_start = config.regime_duration // 2 - attack_steps // 2

            for regime_step in range(config.regime_duration):
                attacked = (
                    adversarial
                    and attack_start <= regime_step < attack_start + attack_steps
                )
                for edge in evidence:
                    left, right = edge
                    if attacked and edge in attacked_edges:
                        probability = config.attack_false_edge_probability
                    else:
                        probability = (
                            config.inside_event_probability
                            if true_partition[left] == true_partition[right]
                            else config.outside_event_probability
                        )
                    happened = rng.random() < probability
                    evidence[edge] = (
                        config.evidence_decay * evidence[edge]
                        + (1.0 - config.evidence_decay) * float(happened)
                    )

                if steps % config.decision_interval == 0:
                    threshold = (
                        config.high_threshold
                        if policy == "high_threshold"
                        else config.coupling_threshold
                    )
                    candidate = _components(config.nodes, evidence, threshold)
                    approved = True
                    used_samples = 0

                    if policy == "uniform_independent":
                        audited_evidence: dict[tuple[int, int], float] = {}
                        for edge in evidence:
                            left, right = edge
                            predicted_same, used = _audit_edge(
                                audit_rng,
                                true_partition[left] == true_partition[right],
                                config,
                            )
                            audited_evidence[edge] = float(predicted_same)
                            used_samples += used
                        candidate = _components(
                            config.nodes,
                            audited_evidence,
                            config.coupling_threshold,
                        )
                    elif policy == "selective_independent" and candidate != current:
                        approved, used_samples = _audit_candidate(
                            audit_rng,
                            true_partition,
                            current,
                            candidate,
                            config,
                        )

                    audit_samples += used_samples
                    total_utility -= config.audit_cost * used_samples

                    if approved and candidate != current:
                        before = _pairwise_accuracy(
                            true_partition, current, config.nodes
                        )
                        after = _pairwise_accuracy(
                            true_partition, candidate, config.nodes
                        )
                        harmful_migrations += int(after < before)
                        moved = _changed_nodes(current, candidate, config.nodes)
                        total_utility -= (
                            config.migration_cost * moved / config.nodes
                        )
                        current = list(candidate)
                        migrations += 1

                total_utility += _partition_utility(
                    true_partition, current, config
                )
                pairwise_accuracy += _pairwise_accuracy(
                    true_partition, current, config.nodes
                )
                steps += 1

    return {
        "net_utility_per_step": total_utility / steps,
        "pairwise_scope_accuracy": pairwise_accuracy / steps,
        "migrations": migrations,
        "harmful_migrations": harmful_migrations,
        "audit_samples_per_step": audit_samples / steps,
    }
