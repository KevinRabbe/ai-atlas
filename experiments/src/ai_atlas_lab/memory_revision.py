from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Protocol

from .core import CostMeter


@dataclass(frozen=True)
class Evidence:
    event_id: int
    entity: int
    value: int


@dataclass(frozen=True)
class Retraction:
    target_id: int


@dataclass(frozen=True)
class RevisionQuery:
    entity: int
    kind: str
    expected: object


Operation = Evidence | Retraction | RevisionQuery


@dataclass(frozen=True)
class RevisionExperimentConfig:
    seed: int = 0
    entities: int = 20
    mutations: int = 1200
    retraction_probability: float = 0.10
    query_probability: float = 0.45
    provenance_fraction: float = 0.25


def generate_revision_stream(config: RevisionExperimentConfig) -> tuple[Operation, ...]:
    rng = random.Random(config.seed)
    operations: list[Operation] = []
    active: dict[int, Evidence] = {}
    next_id = 0
    for _ in range(config.mutations):
        if active and rng.random() < config.retraction_probability:
            target = rng.choice(list(active))
            operations.append(Retraction(target))
            active.pop(target, None)
        else:
            evidence = Evidence(next_id, rng.randrange(config.entities), 1 if rng.random() < 0.5 else -1)
            next_id += 1
            operations.append(evidence)
            active[evidence.event_id] = evidence

        if rng.random() < config.query_probability:
            entity = rng.randrange(config.entities)
            support = [evidence for evidence in active.values() if evidence.entity == entity]
            total = sum(evidence.value for evidence in support)
            belief = 1 if total > 0 else -1 if total < 0 else 0
            if rng.random() < config.provenance_fraction:
                operations.append(RevisionQuery(entity, "provenance", tuple(sorted(evidence.event_id for evidence in support))))
            else:
                operations.append(RevisionQuery(entity, "current", belief))
    return tuple(operations)


class RevisionPolicy(Protocol):
    name: str
    def apply(self, operation: Operation, cost: CostMeter) -> object | None: ...
    def storage_metrics(self) -> dict[str, int]: ...


class DirectEvidenceReplay:
    name = "direct_evidence_replay"

    def __init__(self) -> None:
        self.log: list[Evidence | Retraction] = []

    def apply(self, operation: Operation, cost: CostMeter) -> object | None:
        if not isinstance(operation, RevisionQuery):
            self.log.append(operation)
            cost.writes += 1
            return None
        evidence: dict[int, Evidence] = {}
        retracted: set[int] = set()
        for item in self.log:
            cost.reads += 1
            cost.operations += 1
            if isinstance(item, Evidence):
                evidence[item.event_id] = item
            else:
                retracted.add(item.target_id)
        support = [item for event_id, item in evidence.items() if event_id not in retracted and item.entity == operation.entity]
        if operation.kind == "provenance":
            return tuple(sorted(item.event_id for item in support))
        total = sum(item.value for item in support)
        return 1 if total > 0 else -1 if total < 0 else 0

    def storage_metrics(self) -> dict[str, int]:
        return {"archive_items": len(self.log), "active_items": 0, "index_items": 0}


class CompressedCurrentOnly:
    name = "compressed_current_only"

    def __init__(self) -> None:
        self.sums: dict[int, int] = {}

    def apply(self, operation: Operation, cost: CostMeter) -> object | None:
        if isinstance(operation, Evidence):
            self.sums[operation.entity] = self.sums.get(operation.entity, 0) + operation.value
            cost.writes += 1
            cost.operations += 1
            return None
        if isinstance(operation, Retraction):
            # Source semantics needed to reverse this update were intentionally discarded.
            cost.operations += 1
            return None
        cost.reads += 1
        if operation.kind == "provenance":
            return None
        total = self.sums.get(operation.entity, 0)
        return 1 if total > 0 else -1 if total < 0 else 0

    def storage_metrics(self) -> dict[str, int]:
        return {"archive_items": 0, "active_items": len(self.sums), "index_items": 0}


class EvidenceLinkedCurrent:
    name = "evidence_linked_current"

    def __init__(self) -> None:
        self.sums: dict[int, int] = {}
        self.by_id: dict[int, Evidence] = {}
        self.active: set[int] = set()
        self.by_entity: dict[int, set[int]] = {}

    def apply(self, operation: Operation, cost: CostMeter) -> object | None:
        if isinstance(operation, Evidence):
            self.by_id[operation.event_id] = operation
            self.active.add(operation.event_id)
            self.by_entity.setdefault(operation.entity, set()).add(operation.event_id)
            self.sums[operation.entity] = self.sums.get(operation.entity, 0) + operation.value
            cost.writes += 4
            cost.operations += 4
            return None
        if isinstance(operation, Retraction):
            cost.reads += 1
            evidence = self.by_id.get(operation.target_id)
            if evidence is not None and operation.target_id in self.active:
                self.active.remove(operation.target_id)
                self.by_entity[evidence.entity].discard(operation.target_id)
                self.sums[evidence.entity] -= evidence.value
                cost.writes += 3
                cost.operations += 3
            return None
        cost.reads += 1
        if operation.kind == "provenance":
            return tuple(sorted(self.by_entity.get(operation.entity, set()) & self.active))
        total = self.sums.get(operation.entity, 0)
        return 1 if total > 0 else -1 if total < 0 else 0

    def storage_metrics(self) -> dict[str, int]:
        return {
            "archive_items": len(self.by_id),
            "active_items": len(self.sums),
            "index_items": len(self.active) + sum(len(values) for values in self.by_entity.values()),
        }


def evaluate_revision_policy(policy: RevisionPolicy, operations: tuple[Operation, ...]) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    current_correct = current_total = provenance_correct = provenance_total = mutations = 0
    for operation in operations:
        answer = policy.apply(operation, cost)
        if isinstance(operation, RevisionQuery):
            if operation.kind == "current":
                current_total += 1
                current_correct += int(answer == operation.expected)
            else:
                provenance_total += 1
                provenance_correct += int(answer == operation.expected)
        else:
            mutations += 1
    query_count = current_total + provenance_total
    metrics: dict[str, float | int] = {
        "current_accuracy": current_correct / current_total if current_total else 0.0,
        "provenance_accuracy": provenance_correct / provenance_total if provenance_total else 0.0,
        "queries": query_count,
        "reads_per_query": cost.reads / query_count if query_count else 0.0,
        "writes_per_mutation": cost.writes / mutations if mutations else 0.0,
    }
    metrics.update(policy.storage_metrics())
    return metrics, cost


def run_revision_memory_experiment(config: RevisionExperimentConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    operations = generate_revision_stream(config)
    policies: list[RevisionPolicy] = [DirectEvidenceReplay(), CompressedCurrentOnly(), EvidenceLinkedCurrent()]
    return [(policy.name, *evaluate_revision_policy(policy, operations)) for policy in policies]
