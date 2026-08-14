from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class DeceptiveLineageConfig:
    seed: int = 0
    rounds: int = 180
    candidates_per_round: int = 8
    bits: int = 8
    archive_size: int = 12
    archive_cost_per_variant: float = 0.001


def score(genotype: tuple[int, ...]) -> float:
    ones = sum(genotype)
    if ones == 0:
        return 10.0
    if ones == len(genotype):
        return 15.0
    return 10.0 - 0.7 * ones


def _neighbors(
    rng: random.Random,
    genotype: tuple[int, ...],
    count: int,
) -> list[tuple[int, ...]]:
    result = []
    for _ in range(count):
        index = rng.randrange(len(genotype))
        child = list(genotype)
        child[index] = 1 - child[index]
        result.append(tuple(child))
    return result


def _archive_prune(
    archive: list[tuple[int, ...]],
    limit: int,
) -> list[tuple[int, ...]]:
    unique = list(dict.fromkeys(archive))
    if len(unique) <= limit:
        return unique
    best = max(unique, key=score)
    selected = [best]
    for radius in range(1, len(best) + 1):
        same_radius = [
            item for item in unique
            if sum(item) == radius and item not in selected
        ]
        if same_radius:
            selected.append(max(same_radius, key=score))
            if len(selected) >= limit:
                return selected
    for item in sorted(unique, key=score, reverse=True):
        if item not in selected:
            selected.append(item)
            if len(selected) >= limit:
                break
    return selected


def run_deceptive_lineage(
    config: DeceptiveLineageConfig,
    policy: str,
) -> dict[str, float | int]:
    rng = random.Random(config.seed)
    start = tuple(0 for _ in range(config.bits))
    incumbent = start
    archive = [start]
    storage_cost = 0.0
    reached_global = False
    first_global_round = -1

    for round_index in range(config.rounds):
        if policy == "greedy_incumbent":
            parents = [incumbent]
        elif policy == "bounded_archive":
            parents = [rng.choice(archive)]
        else:
            raise ValueError(policy)

        candidates: list[tuple[int, ...]] = []
        for parent in parents:
            candidates.extend(
                _neighbors(
                    rng,
                    parent,
                    config.candidates_per_round,
                )
            )

        if policy == "greedy_incumbent":
            best = max(candidates, key=score)
            if score(best) > score(incumbent):
                incumbent = best
            current_best = score(incumbent)
        else:
            archive = _archive_prune(
                archive + candidates,
                config.archive_size,
            )
            storage_cost += (
                len(archive)
                * config.archive_cost_per_variant
            )
            current_best = max(score(item) for item in archive)

        if current_best >= 15.0 and not reached_global:
            reached_global = True
            first_global_round = round_index

    return {
        "best_score": (
            score(incumbent)
            if policy == "greedy_incumbent"
            else max(score(item) for item in archive)
        ),
        "reached_global": int(reached_global),
        "first_global_round": first_global_round,
        "archive_cost_per_round": storage_cost / config.rounds,
        "retained_variants": len(archive) if policy == "bounded_archive" else 1,
    }
