from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class PredictiveBreadthConfig:
    seed: int = 0
    episodes: int = 1000
    queries_per_episode: int = 80
    state_bits: int = 12
    goal_switch_probability: float = 0.10
    active_rent_per_bit: float = 0.002
    archive_rent_per_bit: float = 0.0003
    retrieval_cost_per_bit: float = 0.025


def _target(bits: tuple[int, ...], goal: str) -> int:
    indexes = (0, 1, 2) if goal == "A" else (6, 7, 8)
    return sum(bits[index] for index in indexes) % 2


def run_predictive_breadth_experiment(
    config: PredictiveBreadthConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    rng = random.Random(config.seed)
    names = ("broad_active", "decision_sufficient", "source_recoverable_hybrid")
    stats = {
        name: {
            "correct": 0,
            "queries": 0,
            "cost": 0.0,
            "retrievals": 0,
            "active_items": 0,
            "archive_items": 0,
        }
        for name in names
    }

    for _ in range(config.episodes):
        bits = tuple(rng.randrange(2) for _ in range(config.state_bits))
        goal = "A"
        previous_goal = goal
        for query_index in range(config.queries_per_episode):
            if query_index > 0 and rng.random() < config.goal_switch_probability:
                goal = "B" if goal == "A" else "A"
            target = _target(bits, goal)

            broad = stats["broad_active"]
            broad["correct"] += 1
            broad["queries"] += 1
            broad["active_items"] += config.state_bits
            broad["cost"] += config.state_bits * config.active_rent_per_bit

            selective = stats["decision_sufficient"]
            selective_prediction = _target(bits, "A") if goal == "A" else 0
            selective["correct"] += int(selective_prediction == target)
            selective["queries"] += 1
            selective["active_items"] += 3
            selective["cost"] += 3 * config.active_rent_per_bit

            hybrid = stats["source_recoverable_hybrid"]
            hybrid["correct"] += 1
            hybrid["queries"] += 1
            hybrid["active_items"] += 3
            hybrid["archive_items"] += config.state_bits
            hybrid["cost"] += (
                3 * config.active_rent_per_bit
                + config.state_bits * config.archive_rent_per_bit
            )
            if query_index > 0 and goal != previous_goal:
                hybrid["retrievals"] += 1
                hybrid["cost"] += 3 * config.retrieval_cost_per_bit

            previous_goal = goal

    results = []
    for name in names:
        row = stats[name]
        queries = row["queries"]
        accuracy = row["correct"] / queries
        cost_per_query = row["cost"] / queries
        results.append(
            (
                name,
                {
                    "accuracy": accuracy,
                    "cost_per_query": cost_per_query,
                    "net_utility": accuracy - cost_per_query,
                    "avg_active_items": row["active_items"] / queries,
                    "avg_archive_items": row["archive_items"] / queries,
                    "retrievals_per_episode": row["retrievals"] / config.episodes,
                },
            )
        )
    return results
