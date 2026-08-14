from __future__ import annotations

from dataclasses import dataclass
import random

from .belief_hypotheses import (
    Observation,
    action_utility,
    hypothesis_bits,
    multiple_hypothesis_action,
    normalize,
    posterior_from_observations,
)


@dataclass(frozen=True)
class ActiveInfoTask:
    true_hypothesis: int
    passive_observations: tuple[Observation, ...]
    probe_outcomes: tuple[int, int]
    task_value: float


@dataclass(frozen=True)
class ActiveInfoConfig:
    seed: int = 0
    task_count: int = 2000
    passive_reliability: float = 0.62
    probe_reliability: float = 0.97
    probe_cost: float = 0.08
    safe_utility: float = 0.10
    correct_commit_utility: float = 1.0
    wrong_commit_utility: float = -1.0


def update_with_observation(
    posterior: tuple[float, ...],
    *,
    bit_index: int,
    observed: int,
    reliability: float,
) -> tuple[float, ...]:
    weights = []
    for hypothesis, prior in enumerate(posterior):
        expected = hypothesis_bits(hypothesis)[bit_index]
        weights.append(prior * (reliability if expected == observed else 1.0 - reliability))
    return normalize(tuple(weights))


def terminal_expected_utility(posterior: tuple[float, ...], config: ActiveInfoConfig) -> float:
    action = multiple_hypothesis_action(
        posterior,
        safe_utility=config.safe_utility,
        correct_commit_utility=config.correct_commit_utility,
        wrong_commit_utility=config.wrong_commit_utility,
    )
    if action is None:
        return config.safe_utility
    p = posterior[action]
    return p * config.correct_commit_utility + (1.0 - p) * config.wrong_commit_utility


def observation_probability(
    posterior: tuple[float, ...],
    *,
    bit_index: int,
    observed: int,
    reliability: float,
) -> float:
    probability = 0.0
    for hypothesis, prior in enumerate(posterior):
        expected = hypothesis_bits(hypothesis)[bit_index]
        probability += prior * (reliability if expected == observed else 1.0 - reliability)
    return probability


def one_probe_value(
    posterior: tuple[float, ...],
    *,
    bit_index: int,
    task_value: float,
    config: ActiveInfoConfig,
) -> float:
    value = -config.probe_cost
    for observed in (0, 1):
        probability = observation_probability(
            posterior,
            bit_index=bit_index,
            observed=observed,
            reliability=config.probe_reliability,
        )
        updated = update_with_observation(
            posterior,
            bit_index=bit_index,
            observed=observed,
            reliability=config.probe_reliability,
        )
        value += probability * terminal_expected_utility(updated, config) * task_value
    return value


def myopic_probe_action(
    posterior: tuple[float, ...],
    *,
    available: tuple[int, ...],
    task_value: float,
    config: ActiveInfoConfig,
) -> int | None:
    terminal = terminal_expected_utility(posterior, config) * task_value
    candidates = [
        (one_probe_value(posterior, bit_index=bit, task_value=task_value, config=config), bit)
        for bit in available
    ]
    if not candidates:
        return None
    value, bit = max(candidates)
    return bit if value > terminal else None


def lookahead_probe_action(
    posterior: tuple[float, ...],
    *,
    available: tuple[int, ...],
    task_value: float,
    config: ActiveInfoConfig,
) -> int | None:
    terminal = terminal_expected_utility(posterior, config) * task_value
    best_value = terminal
    best_bit: int | None = None
    for bit in available:
        remaining = tuple(other for other in available if other != bit)
        value = -config.probe_cost
        for observed in (0, 1):
            probability = observation_probability(
                posterior,
                bit_index=bit,
                observed=observed,
                reliability=config.probe_reliability,
            )
            updated = update_with_observation(
                posterior,
                bit_index=bit,
                observed=observed,
                reliability=config.probe_reliability,
            )
            continuation = terminal_expected_utility(updated, config) * task_value
            for second in remaining:
                continuation = max(
                    continuation,
                    one_probe_value(updated, bit_index=second, task_value=task_value, config=config),
                )
            value += probability * continuation
        if value > best_value:
            best_value = value
            best_bit = bit
    return best_bit


def generate_active_info_tasks(config: ActiveInfoConfig) -> tuple[ActiveInfoTask, ...]:
    rng = random.Random(config.seed)
    tasks: list[ActiveInfoTask] = []
    for _ in range(config.task_count):
        hidden = rng.randrange(4)
        bits = hypothesis_bits(hidden)
        bit_index = rng.randrange(2)
        truth = bits[bit_index]
        passive = truth if rng.random() < config.passive_reliability else 1 - truth
        probe_outcomes = []
        for probe_bit in range(2):
            truth = bits[probe_bit]
            probe_outcomes.append(truth if rng.random() < config.probe_reliability else 1 - truth)
        task_value = 0.5 + 1.5 * rng.random()
        tasks.append(
            ActiveInfoTask(
                true_hypothesis=hidden,
                passive_observations=((bit_index, passive),),
                probe_outcomes=(probe_outcomes[0], probe_outcomes[1]),
                task_value=task_value,
            )
        )
    return tuple(tasks)


def evaluate_active_policy(
    tasks: tuple[ActiveInfoTask, ...],
    config: ActiveInfoConfig,
    *,
    mode: str,
) -> dict[str, float | int]:
    total_net = 0.0
    total_queries = 0
    wrong_commits = 0
    safe_actions = 0
    for task in tasks:
        posterior = posterior_from_observations(
            task.passive_observations,
            reliability=config.passive_reliability,
        )
        query_order: list[int] = []
        available = [0, 1]

        if mode == "fixed_both":
            query_order = [0, 1]
        elif mode == "passive":
            pass
        elif mode in {"voi_myopic", "voi_lookahead"}:
            current_mode = mode
            while available:
                chooser = myopic_probe_action if current_mode == "voi_myopic" else lookahead_probe_action
                bit = chooser(
                    posterior,
                    available=tuple(available),
                    task_value=task.task_value,
                    config=config,
                )
                if bit is None:
                    break
                query_order.append(bit)
                available.remove(bit)
                posterior = update_with_observation(
                    posterior,
                    bit_index=bit,
                    observed=task.probe_outcomes[bit],
                    reliability=config.probe_reliability,
                )
                current_mode = "voi_myopic"
        else:
            raise ValueError(f"unknown mode: {mode}")

        if mode == "fixed_both":
            posterior = posterior_from_observations(
                task.passive_observations,
                reliability=config.passive_reliability,
            )
            for bit in query_order:
                posterior = update_with_observation(
                    posterior,
                    bit_index=bit,
                    observed=task.probe_outcomes[bit],
                    reliability=config.probe_reliability,
                )

        total_queries += len(query_order)
        action = multiple_hypothesis_action(
            posterior,
            safe_utility=config.safe_utility,
            correct_commit_utility=config.correct_commit_utility,
            wrong_commit_utility=config.wrong_commit_utility,
        )
        if action is None:
            safe_actions += 1
        elif action != task.true_hypothesis:
            wrong_commits += 1
        utility = action_utility(
            action,
            task.true_hypothesis,
            safe_utility=config.safe_utility,
            correct_commit_utility=config.correct_commit_utility,
            wrong_commit_utility=config.wrong_commit_utility,
        ) * task.task_value
        total_net += utility - len(query_order) * config.probe_cost

    n = len(tasks)
    return {
        "avg_net_utility": total_net / n,
        "avg_queries": total_queries / n,
        "wrong_commit_rate": wrong_commits / n,
        "safe_action_rate": safe_actions / n,
        "task_count": n,
    }


def run_active_information_experiment(
    config: ActiveInfoConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    tasks = generate_active_info_tasks(config)
    return [
        ("passive", evaluate_active_policy(tasks, config, mode="passive")),
        ("fixed_both", evaluate_active_policy(tasks, config, mode="fixed_both")),
        ("voi_myopic", evaluate_active_policy(tasks, config, mode="voi_myopic")),
        ("value_of_information", evaluate_active_policy(tasks, config, mode="voi_lookahead")),
    ]
