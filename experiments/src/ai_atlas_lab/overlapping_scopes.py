from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I11Config:
    seed: int = 0
    steps: int = 4_000
    cross_probability: float = 0.18
    dense_coupling: bool = False
    membership_cost: float = 0.0025
    overlay_activation_cost: float = 0.10
    overlay_message_cost: float = 0.004
    global_carrying_cost: float = 0.015
    repartition_cost: float = 0.06
    false_pair_cost: float = 0.0025
    missed_pair_penalty: float = 0.020
    captured_pair_benefit: float = 0.008


BASE_GROUPS = (
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (8, 9, 10, 11),
)

CROSS_GROUPS = (
    (0, 4, 8, 9),
    (1, 5, 9, 10),
    (2, 6, 10, 11),
    (3, 7, 8, 11),
)


def _edges(group: tuple[int, ...]) -> set[tuple[int, int]]:
    return {
        (left, right)
        for left in group
        for right in group
        if left < right
    }


def _base_edges() -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    for group in BASE_GROUPS:
        result |= _edges(group)
    return result


def _repartition_edges(active_group: tuple[int, ...]) -> set[tuple[int, int]]:
    active = set(active_group)
    scopes: list[tuple[int, ...]] = [active_group]
    for base in BASE_GROUPS:
        remaining = tuple(node for node in base if node not in active)
        if remaining:
            scopes.append(remaining)
    result: set[tuple[int, int]] = set()
    for scope in scopes:
        result |= _edges(scope)
    return result


def run_i11(config: I11Config, policy: str) -> dict[str, float]:
    valid = {
        "base_partition",
        "forced_repartition",
        "global_scope",
        "persistent_overlap",
        "temporary_overlay",
    }
    if policy not in valid:
        raise ValueError(f"unknown I11 policy: {policy}")

    rng = random.Random(config.seed)
    nodes = 12
    base_edges = _base_edges()
    all_edges = {
        (left, right)
        for left in range(nodes)
        for right in range(left + 1, nodes)
    }
    cross_groups = (tuple(range(nodes)),) if config.dense_coupling else CROSS_GROUPS

    total_utility = 0.0
    missed_pairs = 0
    false_pairs = 0
    memberships = 0
    overlay_activations = 0

    for _ in range(config.steps):
        if config.dense_coupling:
            active_index: int | None = 0
        else:
            active_index = (
                rng.randrange(len(cross_groups))
                if rng.random() < config.cross_probability
                else None
            )

        true_edges = set(base_edges)
        if active_index is not None:
            true_edges |= _edges(cross_groups[active_index])

        extra_cost = 0.0
        active_memberships = 12

        if policy == "base_partition":
            represented = set(base_edges)
        elif policy == "global_scope":
            represented = set(all_edges)
            extra_cost = config.global_carrying_cost
        elif policy == "persistent_overlap":
            represented = set(base_edges)
            extra_memberships = 0
            for group in cross_groups:
                represented |= _edges(group)
                extra_memberships += len(group)
            active_memberships += extra_memberships
            extra_cost = config.membership_cost * extra_memberships
        elif policy == "temporary_overlay":
            represented = set(base_edges)
            if active_index is not None:
                group = cross_groups[active_index]
                represented |= _edges(group)
                active_memberships += len(group)
                extra_cost = (
                    config.overlay_activation_cost
                    + config.overlay_message_cost * len(group)
                )
                overlay_activations += 1
        else:
            represented = set(base_edges)
            if active_index is not None:
                represented = _repartition_edges(cross_groups[active_index])
                extra_cost = config.repartition_cost

        captured = len(true_edges & represented)
        missed = len(true_edges - represented)
        false = len(represented - true_edges)
        total_utility += (
            1.0
            + config.captured_pair_benefit * captured
            - config.missed_pair_penalty * missed
            - config.false_pair_cost * false
            - extra_cost
        )
        missed_pairs += missed
        false_pairs += false
        memberships += active_memberships

    return {
        "net_utility_per_step": total_utility / config.steps,
        "missed_pairs_per_step": missed_pairs / config.steps,
        "false_pairs_per_step": false_pairs / config.steps,
        "mean_memberships": memberships / config.steps,
        "overlay_activation_rate": overlay_activations / config.steps,
    }
