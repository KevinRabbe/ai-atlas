from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class ArchiveLineageConfig:
    seed: int = 0
    rounds: int = 300
    candidates_per_round: int = 12
    archive_size: int = 6
    archive_cost_per_variant: float = 0.0008
    switching: bool = True


@dataclass(frozen=True)
class Variant:
    a: float
    b: float


def _regime(config: ArchiveLineageConfig, round_index: int) -> str:
    if not config.switching:
        return "A"
    return "A" if (round_index // 50) % 2 == 0 else "B"


def _mutate(rng: random.Random, parent: Variant, regime: str) -> Variant:
    gain = max(0.0, rng.gauss(0.018, 0.018))
    tradeoff = max(0.0, rng.gauss(0.035, 0.018))
    common = rng.gauss(0.001, 0.006)
    if regime == "A":
        return Variant(
            min(1.0, max(0.0, parent.a + gain + common)),
            min(1.0, max(0.0, parent.b - tradeoff + common)),
        )
    return Variant(
        min(1.0, max(0.0, parent.a - tradeoff + common)),
        min(1.0, max(0.0, parent.b + gain + common)),
    )


def _prune_diverse(variants: list[Variant], limit: int) -> list[Variant]:
    unique: list[Variant] = []
    for variant in variants:
        if variant not in unique:
            unique.append(variant)
    if len(unique) <= limit:
        return unique

    seeds = [
        max(unique, key=lambda item: (item.a + item.b) / 2.0),
        max(unique, key=lambda item: item.a),
        max(unique, key=lambda item: item.b),
    ]
    selected: list[Variant] = []
    for item in seeds:
        if item not in selected:
            selected.append(item)

    while len(selected) < limit:
        remaining = [item for item in unique if item not in selected]
        next_item = max(
            remaining,
            key=lambda item: min(
                math.dist((item.a, item.b), (kept.a, kept.b))
                for kept in selected
            ),
        )
        selected.append(next_item)
    return selected


def run_lineage_archive(
    config: ArchiveLineageConfig,
    policy: str,
) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    incumbent = Variant(0.5, 0.5)
    archive = [incumbent]
    performance: list[float] = []
    storage_cost = 0.0
    previous_regime = _regime(config, 0)
    switch_points: list[int] = []

    for round_index in range(config.rounds):
        regime = _regime(config, round_index)
        if regime != previous_regime:
            switch_points.append(round_index)
            previous_regime = regime

        if policy == "greedy_incumbent":
            parent = incumbent
        elif policy == "bounded_archive":
            parent = max(
                archive,
                key=lambda item: item.a if regime == "A" else item.b,
            )
        else:
            raise ValueError(policy)

        candidates = [
            _mutate(rng, parent, regime)
            for _ in range(config.candidates_per_round)
        ]
        best = max(
            candidates,
            key=lambda item: item.a if regime == "A" else item.b,
        )

        if policy == "greedy_incumbent":
            current = incumbent.a if regime == "A" else incumbent.b
            candidate = best.a if regime == "A" else best.b
            if candidate > current:
                incumbent = best
            chosen = incumbent
        else:
            archive = _prune_diverse(
                archive + [best],
                config.archive_size,
            )
            chosen = max(
                archive,
                key=lambda item: item.a if regime == "A" else item.b,
            )
            storage_cost += (
                len(archive)
                * config.archive_cost_per_variant
            )

        performance.append(
            chosen.a if regime == "A" else chosen.b
        )

    switch10 = (
        sum(
            sum(performance[index : index + 10]) / 10.0
            for index in switch_points
        )
        / len(switch_points)
        if switch_points
        else 0.0
    )
    return {
        "net_performance": (
            sum(performance) / len(performance)
            - storage_cost / config.rounds
        ),
        "raw_performance": sum(performance) / len(performance),
        "switch10_performance": switch10,
        "archive_cost_per_round": storage_cost / config.rounds,
        "retained_variants": len(archive) if policy == "bounded_archive" else 1,
        "best_a": (
            max(item.a for item in archive)
            if policy == "bounded_archive"
            else incumbent.a
        ),
        "best_b": (
            max(item.b for item in archive)
            if policy == "bounded_archive"
            else incumbent.b
        ),
    }
