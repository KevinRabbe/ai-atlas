from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Event:
    event_id: int
    time: int
    entity: str
    value: int
    payload: str


@dataclass(frozen=True)
class Query:
    kind: str  # current | historical | exact
    entity: str | None = None
    time: int | None = None
    event_id: int | None = None
    expected: int | str | None = None


@dataclass(frozen=True)
class TemporalStateDataset:
    events: tuple[Event, ...]
    queries: tuple[Query, ...]


def generate_temporal_state_dataset(
    *,
    seed: int,
    num_entities: int = 12,
    num_events: int = 240,
    current_queries: int = 60,
    historical_queries: int = 60,
    exact_queries: int = 60,
) -> TemporalStateDataset:
    rng = random.Random(seed)
    entities = [f"entity_{i}" for i in range(num_entities)]
    current: dict[str, int] = {entity: 0 for entity in entities}
    events: list[Event] = []

    for t in range(num_events):
        entity = rng.choice(entities)
        value = rng.randint(-10_000, 10_000)
        current[entity] = value
        events.append(
            Event(
                event_id=t,
                time=t,
                entity=entity,
                value=value,
                payload=f"event:{t}:entity:{entity}:nonce:{rng.getrandbits(48):012x}",
            )
        )

    by_entity: dict[str, list[Event]] = {entity: [] for entity in entities}
    for event in events:
        by_entity[event.entity].append(event)

    queries: list[Query] = []
    for _ in range(current_queries):
        entity = rng.choice(entities)
        queries.append(Query(kind="current", entity=entity, expected=current[entity]))

    eligible = [entity for entity, items in by_entity.items() if items]
    for _ in range(historical_queries):
        entity = rng.choice(eligible)
        event = rng.choice(by_entity[entity])
        queries.append(
            Query(
                kind="historical",
                entity=entity,
                time=event.time,
                expected=event.value,
            )
        )

    for _ in range(exact_queries):
        event = rng.choice(events)
        queries.append(Query(kind="exact", event_id=event.event_id, expected=event.payload))

    rng.shuffle(queries)
    return TemporalStateDataset(events=tuple(events), queries=tuple(queries))
