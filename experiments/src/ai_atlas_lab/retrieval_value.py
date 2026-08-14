from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class MemoryRecord:
    topic: int
    family: int
    regime: int
    mechanism: int
    action: int
    outcome: int
    verified: bool
    age: int


@dataclass(frozen=True)
class RetrievalQuery:
    topic: int
    family: int
    regime: int
    mechanism: int
    correct_action: int


@dataclass(frozen=True)
class RetrievalConfig:
    seed: int = 0
    task_count: int = 2000
    check_cost: float = 0.002


def _pick_staleness(
    query: RetrievalQuery,
    memories: list[MemoryRecord],
    mode: str,
) -> tuple[MemoryRecord, int]:
    if mode == "similarity":
        return max(
            memories,
            key=lambda memory: (
                memory.topic == query.topic,
                -abs(memory.topic - query.topic),
            ),
        ), len(memories)
    if mode == "temporal_applicability":
        return max(
            memories,
            key=lambda memory: (
                memory.regime == query.regime,
                memory.family == query.family,
                memory.topic == query.topic,
                -memory.age,
            ),
        ), 3 * len(memories)
    if mode == "decision_value":
        return max(
            memories,
            key=lambda memory: (
                memory.regime == query.regime
                and memory.family == query.family
                and memory.outcome > 0,
                memory.verified,
                memory.topic == query.topic,
                -memory.age,
            ),
        ), 5 * len(memories)
    raise ValueError(mode)


def run_staleness_retrieval(
    config: RetrievalConfig,
    *,
    shifted_fraction: float,
) -> list[tuple[str, dict[str, float | int]]]:
    rng = random.Random(config.seed)
    modes = ("similarity", "temporal_applicability", "decision_value")
    totals = {mode: [0, 0, 0] for mode in modes}
    for _ in range(config.task_count):
        topic = rng.randrange(20)
        family = topic % 2
        regime = 1 if rng.random() < shifted_fraction else 0
        correct = family ^ regime
        memories = [
            MemoryRecord(topic, family, 0, 0, family, 1, True, 50),
            MemoryRecord((topic + 2) % 20, family, regime, 0, correct, 1, True, 1),
            MemoryRecord(
                (topic + 1) % 20,
                1 - family,
                regime,
                0,
                (1 - family) ^ regime,
                1,
                True,
                1,
            ),
        ]
        rng.shuffle(memories)
        query = RetrievalQuery(topic, family, regime, 0, correct)
        for mode in modes:
            memory, checks = _pick_staleness(query, memories, mode)
            totals[mode][0] += int(memory.action == correct)
            totals[mode][1] += checks
            totals[mode][2] += 1

    rows = []
    for mode, (correct, checks, count) in totals.items():
        accuracy = correct / count
        cost = checks / count * config.check_cost
        rows.append(
            (
                mode,
                {
                    "accuracy": accuracy,
                    "checks_per_query": checks / count,
                    "net_utility": accuracy - cost,
                },
            )
        )
    return rows


def _pick_causal(
    query: RetrievalQuery,
    memories: list[MemoryRecord],
    mode: str,
) -> tuple[MemoryRecord, int]:
    if mode == "similarity":
        return max(
            memories,
            key=lambda memory: (
                memory.topic == query.topic,
                -abs(memory.topic - query.topic),
            ),
        ), len(memories)
    if mode == "causal_only":
        return max(
            memories,
            key=lambda memory: (
                memory.mechanism == query.mechanism,
                memory.topic == query.topic,
            ),
        ), 2 * len(memories)
    if mode == "decision_value":
        return max(
            memories,
            key=lambda memory: (
                memory.mechanism == query.mechanism,
                memory.outcome > 0,
                memory.verified,
                memory.topic == query.topic,
            ),
        ), 4 * len(memories)
    if mode == "hybrid":
        return max(
            memories,
            key=lambda memory: (
                3 * int(memory.mechanism == query.mechanism)
                + 2 * int(memory.outcome > 0)
                + int(memory.verified)
                + int(memory.topic == query.topic)
            ),
        ), 4 * len(memories)
    raise ValueError(mode)


def run_causal_retrieval(
    config: RetrievalConfig,
    *,
    conflict_probability: float,
    lure_count: int = 3,
) -> list[tuple[str, dict[str, float | int]]]:
    rng = random.Random(config.seed)
    modes = ("similarity", "causal_only", "decision_value", "hybrid")
    totals = {mode: [0, 0, 0] for mode in modes}
    for _ in range(config.task_count):
        topic = rng.randrange(30)
        mechanism = rng.randrange(2)
        correct = mechanism
        conflict = rng.random() < conflict_probability
        lure_mechanism = 1 - mechanism if conflict else mechanism
        memories = [
            MemoryRecord(topic, 0, 0, lure_mechanism, lure_mechanism, 1, False, 1 + index)
            for index in range(lure_count)
        ]
        memories.append(
            MemoryRecord((topic + 7) % 30, 0, 0, mechanism, correct, 1, True, 2)
        )
        memories.append(
            MemoryRecord((topic + 11) % 30, 0, 0, mechanism, 1 - correct, -1, True, 2)
        )
        rng.shuffle(memories)
        query = RetrievalQuery(topic, 0, 0, mechanism, correct)
        for mode in modes:
            memory, checks = _pick_causal(query, memories, mode)
            totals[mode][0] += int(memory.action == correct)
            totals[mode][1] += checks
            totals[mode][2] += 1

    rows = []
    for mode, (correct, checks, count) in totals.items():
        accuracy = correct / count
        cost = checks / count * config.check_cost
        rows.append(
            (
                mode,
                {
                    "accuracy": accuracy,
                    "checks_per_query": checks / count,
                    "net_utility": accuracy - cost,
                },
            )
        )
    return rows
