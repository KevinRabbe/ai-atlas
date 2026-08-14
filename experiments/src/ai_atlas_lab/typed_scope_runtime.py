from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random

from .core import CostMeter


@dataclass(frozen=True)
class I08Config:
    seed: int = 0
    nodes: int = 12
    cycles: int = 4
    regime_duration: int = 100
    inside_event_probability: float = 0.65
    outside_event_probability: float = 0.04
    evidence_decay: float = 0.94
    coupling_threshold: float = 0.30
    decision_interval: int = 10
    safe_migration_cost: float = 0.035
    stale_route_migration_cost: float = 0.025
    snapshot_migration_cost: float = 0.015
    event_probability: float = 0.45
    external_event_probability: float = 0.28
    max_event_delay: int = 5
    authority_change_probability: float = 0.015
    evidence_generation_probability: float = 0.12
    provenance_query_probability: float = 0.10
    rematerialization_query_probability: float = 0.08
    authority_violation_penalty: float = 3.0
    event_misroute_penalty: float = 0.25
    provenance_failure_penalty: float = 0.18
    rematerialization_failure_penalty: float = 0.24
    duplicate_resource_penalty: float = 0.35
    event_value: float = 0.04
    coupled_pair_benefit: float = 0.05
    missed_coupling_penalty: float = 0.07
    false_group_penalty: float = 0.012


@dataclass
class EvidenceRecord:
    evidence_id: int
    node_id: int
    source_ref: str
    source_intact: bool = True


@dataclass
class PredictiveRecord:
    node_id: int
    source_ref: str
    source_intact: bool = True


@dataclass
class AuthorityRecord:
    allowed: bool = True
    version: int = 0


@dataclass(frozen=True)
class ResourceLease:
    resource_id: int
    holder_node: int


@dataclass
class RuntimeEvent:
    event_id: int
    node_id: int
    due_step: int
    external: bool
    created_epoch: int
    captured_scope: tuple[int, ...]
    captured_authority: bool
    processed: bool = False


def _partitions(nodes: int) -> list[list[int]]:
    if nodes != 12:
        raise ValueError("I08 currently pins twelve nodes to the matched I07 topology family")
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


def _scope_map(labels: list[int]) -> dict[int, tuple[int, ...]]:
    groups: dict[int, list[int]] = defaultdict(list)
    for node, label in enumerate(labels):
        groups[label].append(node)
    return {node: tuple(groups[labels[node]]) for node in range(len(labels))}


def _partition_utility(true_partition: list[int], proposed: list[int], config: I08Config) -> float:
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


def _generate_lifetime(
    config: I08Config,
) -> list[tuple[list[int], dict[tuple[int, int], bool]]]:
    rng = random.Random(config.seed)
    lifetime: list[tuple[list[int], dict[tuple[int, int], bool]]] = []
    for _ in range(config.cycles):
        for partition in _partitions(config.nodes):
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


def run_i08(config: I08Config, variant: str) -> dict[str, float | int | dict[str, int]]:
    valid = {"static_typed", "scope_snapshot", "typed_stale_route", "typed_epoch"}
    if variant not in valid:
        raise ValueError(f"unknown I08 variant: {variant}")

    rng = random.Random(config.seed + 9_999)
    costs = CostMeter()
    pair_evidence = {
        (left, right): 0.10
        for left in range(config.nodes)
        for right in range(left + 1, config.nodes)
    }

    initial_partition = _partitions(config.nodes)[0]
    current_partition = list(initial_partition)
    topology_epoch = 0

    authority = {node: AuthorityRecord() for node in range(config.nodes)}
    evidence_records = [
        EvidenceRecord(node, node, f"source:{node}:0")
        for node in range(config.nodes)
    ]
    predictive = {
        node: PredictiveRecord(node, f"predictive-source:{node}:0")
        for node in range(config.nodes)
    }
    leases = [ResourceLease(resource, resource) for resource in range(config.nodes // 2)]
    scope_map = _scope_map(current_partition)
    snapshot_resource_copies: dict[int, set[tuple[int, ...]]] = {
        lease.resource_id: {scope_map[lease.holder_node]} for lease in leases
    }
    cached_authority: dict[tuple[int, ...], dict[int, bool]] = {
        scope: {node: authority[node].allowed for node in scope}
        for scope in set(scope_map.values())
    }

    queued_events: list[RuntimeEvent] = []
    next_event_id = 0
    next_evidence_id = config.nodes

    total_utility = 0.0
    migrations = 0
    moved_nodes = 0
    authority_violations = 0
    stale_authority_prevented = 0
    event_misroutes = 0
    forwarded_events = 0
    provenance_failures = 0
    rematerialization_failures = 0
    duplicate_resource_exposure = 0
    processed_events = 0

    lifetime = _generate_lifetime(config)
    for step, (true_partition, interactions) in enumerate(lifetime):
        for edge, happened in interactions.items():
            pair_evidence[edge] = (
                config.evidence_decay * pair_evidence[edge]
                + (1.0 - config.evidence_decay) * float(happened)
            )
            costs.samples += 1

        if rng.random() < config.authority_change_probability:
            node = rng.randrange(config.nodes)
            authority[node].allowed = not authority[node].allowed
            authority[node].version += 1
            costs.writes += 1

        if rng.random() < config.evidence_generation_probability:
            node = rng.randrange(config.nodes)
            evidence_records.append(
                EvidenceRecord(
                    next_evidence_id,
                    node,
                    f"source:{node}:{next_evidence_id}",
                )
            )
            next_evidence_id += 1
            costs.writes += 1

        if rng.random() < config.event_probability:
            node = rng.randrange(config.nodes)
            current_scope_map = _scope_map(current_partition)
            queued_events.append(
                RuntimeEvent(
                    event_id=next_event_id,
                    node_id=node,
                    due_step=step + rng.randint(1, config.max_event_delay),
                    external=rng.random() < config.external_event_probability,
                    created_epoch=topology_epoch,
                    captured_scope=current_scope_map[node],
                    captured_authority=authority[node].allowed,
                )
            )
            next_event_id += 1
            costs.writes += 1

        candidate = current_partition
        if variant != "static_typed" and step % config.decision_interval == 0:
            candidate = _components(
                config.nodes,
                pair_evidence,
                config.coupling_threshold,
            )
            costs.comparisons += len(pair_evidence)

        if candidate != current_partition:
            old_scope_map = _scope_map(current_partition)
            new_scope_map = _scope_map(candidate)
            moved = sum(
                old_scope_map[node] != new_scope_map[node]
                for node in range(config.nodes)
            )
            migrations += 1
            moved_nodes += moved
            topology_epoch += 1

            if variant == "typed_epoch":
                migration_price = config.safe_migration_cost
            elif variant == "typed_stale_route":
                migration_price = config.stale_route_migration_cost
            else:
                migration_price = config.snapshot_migration_cost
            total_utility -= migration_price * moved / config.nodes
            costs.messages += moved
            costs.writes += moved

            if variant == "scope_snapshot":
                # A deliberately cheaper scope-addressed migration ablation.
                # Identity stays known, but exact source/provenance and lease
                # ownership were not represented independently of scope state.
                for record in evidence_records:
                    if old_scope_map[record.node_id] != new_scope_map[record.node_id]:
                        record.source_intact = False
                for node, record in predictive.items():
                    if old_scope_map[node] != new_scope_map[node]:
                        record.source_intact = False

                refreshed_cache: dict[tuple[int, ...], dict[int, bool]] = {}
                for scope in set(new_scope_map.values()):
                    refreshed_cache[scope] = {}
                    for node in scope:
                        if old_scope_map[node] != new_scope_map[node]:
                            refreshed_cache[scope][node] = authority[node].allowed
                        else:
                            old_scope = old_scope_map[node]
                            refreshed_cache[scope][node] = cached_authority.get(
                                old_scope, {}
                            ).get(node, authority[node].allowed)
                cached_authority = refreshed_cache

                for lease in leases:
                    old_scope = old_scope_map[lease.holder_node]
                    descendant_scopes = {
                        new_scope_map[node] for node in old_scope
                    }
                    snapshot_resource_copies[lease.resource_id] = set(descendant_scopes)

            current_partition = list(candidate)

        current_scope_map = _scope_map(current_partition)
        for event in queued_events:
            if event.processed or event.due_step > step:
                continue

            if variant in {"scope_snapshot", "typed_stale_route"}:
                if event.captured_scope != current_scope_map[event.node_id]:
                    event_misroutes += 1
                    total_utility -= config.event_misroute_penalty
                    event.processed = True
                    costs.reads += 1
                    continue
            elif variant == "typed_epoch" and event.created_epoch != topology_epoch:
                # Stable node identity allows the old event to be forwarded to
                # the node's current scope rather than dropped or replayed.
                forwarded_events += 1
                costs.messages += 1

            if variant == "scope_snapshot":
                allowed = cached_authority.get(
                    current_scope_map[event.node_id], {}
                ).get(event.node_id, event.captured_authority)
            else:
                allowed = authority[event.node_id].allowed

            if event.external and allowed and not authority[event.node_id].allowed:
                authority_violations += 1
                total_utility -= config.authority_violation_penalty
            elif event.external and not allowed:
                if event.captured_authority and not authority[event.node_id].allowed:
                    stale_authority_prevented += 1
            else:
                total_utility += config.event_value

            if event.external and allowed and authority[event.node_id].allowed:
                total_utility += config.event_value

            event.processed = True
            processed_events += 1
            costs.reads += 1
            costs.operations += 1

        if rng.random() < config.provenance_query_probability and evidence_records:
            record = rng.choice(evidence_records)
            costs.reads += 1
            if not record.source_intact:
                provenance_failures += 1
                total_utility -= config.provenance_failure_penalty

        if rng.random() < config.rematerialization_query_probability:
            node = rng.randrange(config.nodes)
            costs.reads += 1
            if not predictive[node].source_intact:
                rematerialization_failures += 1
                total_utility -= config.rematerialization_failure_penalty

        if variant == "scope_snapshot":
            duplicates = sum(
                max(0, len(copies) - 1)
                for copies in snapshot_resource_copies.values()
            )
            if duplicates:
                duplicate_resource_exposure += duplicates
                total_utility -= (
                    config.duplicate_resource_penalty * duplicates / config.nodes
                )

        total_utility += _partition_utility(
            true_partition,
            current_partition,
            config,
        )

    steps = len(lifetime)
    return {
        "net_utility_per_step": total_utility / steps,
        "migrations": migrations,
        "moved_nodes": moved_nodes,
        "authority_violations": authority_violations,
        "stale_authority_prevented": stale_authority_prevented,
        "event_misroutes": event_misroutes,
        "forwarded_events": forwarded_events,
        "provenance_failures": provenance_failures,
        "rematerialization_failures": rematerialization_failures,
        "duplicate_resource_exposure_per_step": duplicate_resource_exposure / steps,
        "processed_events": processed_events,
        "costs": costs.snapshot(),
    }


def run_i08_experiment(config: I08Config) -> list[tuple[str, dict[str, float | int | dict[str, int]]]]:
    variants = ("static_typed", "scope_snapshot", "typed_stale_route", "typed_epoch")
    return [(variant, run_i08(config, variant)) for variant in variants]
