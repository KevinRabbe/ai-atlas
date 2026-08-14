from __future__ import annotations

from bisect import bisect_right
from collections import defaultdict
from dataclasses import dataclass
from typing import Protocol

from .core import CostMeter
from .environments.temporal_state import Event, Query, TemporalStateDataset, generate_temporal_state_dataset


class StatePolicy(Protocol):
    name: str

    def write(self, event: Event, cost: CostMeter) -> None: ...
    def answer(self, query: Query, cost: CostMeter) -> int | str | None: ...
    def storage_metrics(self) -> dict[str, int]: ...


class DirectAddressState:
    name = "direct_address"

    def __init__(self) -> None:
        self.events: list[Event] = []

    def write(self, event: Event, cost: CostMeter) -> None:
        self.events.append(event)
        cost.writes += 1
        cost.operations += 1

    def answer(self, query: Query, cost: CostMeter) -> int | str | None:
        if query.kind == "exact" and query.event_id is not None:
            # Deliberately scan: retained addressable history without a derived index.
            for event in self.events:
                cost.reads += 1
                cost.comparisons += 1
                if event.event_id == query.event_id:
                    return event.payload
            return None

        if query.entity is None:
            return None
        for event in reversed(self.events):
            cost.reads += 1
            cost.comparisons += 1
            if event.entity != query.entity:
                continue
            if query.kind == "current":
                return event.value
            if query.kind == "historical" and query.time is not None and event.time <= query.time:
                return event.value
        return None

    def storage_metrics(self) -> dict[str, int]:
        return {"active_items": 0, "archive_items": len(self.events), "index_items": 0}


class CompressedState:
    name = "compressed_state"

    def __init__(self) -> None:
        self.current: dict[str, int] = {}

    def write(self, event: Event, cost: CostMeter) -> None:
        self.current[event.entity] = event.value
        cost.writes += 1
        cost.operations += 1

    def answer(self, query: Query, cost: CostMeter) -> int | str | None:
        cost.reads += 1
        cost.operations += 1
        if query.kind == "current" and query.entity is not None:
            return self.current.get(query.entity)
        # History/exact event detail was intentionally discarded.
        return None

    def storage_metrics(self) -> dict[str, int]:
        return {"active_items": len(self.current), "archive_items": 0, "index_items": 0}


class HybridState:
    name = "hybrid_state"

    def __init__(self) -> None:
        self.current: dict[str, int] = {}
        self.events_by_id: dict[int, Event] = {}
        self.history: dict[str, list[Event]] = defaultdict(list)
        self.times: dict[str, list[int]] = defaultdict(list)

    def write(self, event: Event, cost: CostMeter) -> None:
        self.current[event.entity] = event.value
        self.events_by_id[event.event_id] = event
        self.history[event.entity].append(event)
        self.times[event.entity].append(event.time)
        cost.writes += 4
        cost.operations += 4

    def answer(self, query: Query, cost: CostMeter) -> int | str | None:
        if query.kind == "current" and query.entity is not None:
            cost.reads += 1
            cost.operations += 1
            return self.current.get(query.entity)

        if query.kind == "exact" and query.event_id is not None:
            cost.reads += 1
            cost.operations += 1
            event = self.events_by_id.get(query.event_id)
            return None if event is None else event.payload

        if query.kind == "historical" and query.entity is not None and query.time is not None:
            times = self.times.get(query.entity, [])
            cost.reads += 1
            depth = max(1, (len(times) + 1).bit_length()) if times else 1
            cost.comparisons += depth
            idx = bisect_right(times, query.time) - 1
            if idx < 0:
                return None
            cost.reads += 1
            return self.history[query.entity][idx].value
        return None

    def storage_metrics(self) -> dict[str, int]:
        # Events are retained once semantically; indexes are counted separately.
        return {
            "active_items": len(self.current),
            "archive_items": len(self.events_by_id),
            "index_items": len(self.events_by_id) + sum(len(v) for v in self.times.values()),
        }


@dataclass(frozen=True)
class MemoryExperimentConfig:
    seed: int = 0
    num_entities: int = 12
    num_events: int = 240
    current_queries: int = 60
    historical_queries: int = 60
    exact_queries: int = 60


def evaluate_state_policy(
    policy: StatePolicy,
    dataset: TemporalStateDataset,
) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    for event in dataset.events:
        policy.write(event, cost)

    correct_by_kind = {"current": 0, "historical": 0, "exact": 0}
    total_by_kind = {"current": 0, "historical": 0, "exact": 0}

    for query in dataset.queries:
        total_by_kind[query.kind] += 1
        answer = policy.answer(query, cost)
        if answer == query.expected:
            correct_by_kind[query.kind] += 1

    metrics: dict[str, float | int] = {}
    total_correct = 0
    total_queries = len(dataset.queries)
    for kind in ("current", "historical", "exact"):
        total = total_by_kind[kind]
        correct = correct_by_kind[kind]
        total_correct += correct
        metrics[f"{kind}_accuracy"] = correct / total if total else 0.0
    metrics["overall_accuracy"] = total_correct / total_queries if total_queries else 0.0
    metrics["query_count"] = total_queries
    metrics.update(policy.storage_metrics())
    return metrics, cost


def run_memory_experiment(config: MemoryExperimentConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    dataset = generate_temporal_state_dataset(
        seed=config.seed,
        num_entities=config.num_entities,
        num_events=config.num_events,
        current_queries=config.current_queries,
        historical_queries=config.historical_queries,
        exact_queries=config.exact_queries,
    )
    variants: list[StatePolicy] = [DirectAddressState(), CompressedState(), HybridState()]
    return [(variant.name, *evaluate_state_policy(variant, dataset)) for variant in variants]
