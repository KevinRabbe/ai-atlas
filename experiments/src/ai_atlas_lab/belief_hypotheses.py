from __future__ import annotations

from dataclasses import dataclass
import math
import random

Hypothesis = int
Observation = tuple[int, int]


def hypothesis_bits(hypothesis: Hypothesis) -> tuple[int, int]:
    return ((hypothesis >> 1) & 1, hypothesis & 1)


def normalize(weights: tuple[float, ...]) -> tuple[float, ...]:
    total = sum(weights)
    if total <= 0:
        return tuple(1.0 / len(weights) for _ in weights)
    return tuple(value / total for value in weights)


def posterior_from_observations(
    observations: tuple[Observation, ...],
    *,
    reliability: float,
) -> tuple[float, ...]:
    weights = [0.25] * 4
    for bit_index, observed in observations:
        for hypothesis in range(4):
            expected = hypothesis_bits(hypothesis)[bit_index]
            weights[hypothesis] *= reliability if expected == observed else (1.0 - reliability)
        weights[:] = normalize(tuple(weights))
    return tuple(weights)


def posterior_entropy(posterior: tuple[float, ...]) -> float:
    return -sum(p * math.log2(p) for p in posterior if p > 0)


@dataclass(frozen=True)
class BeliefTask:
    true_hypothesis: Hypothesis
    observations: tuple[Observation, ...]


@dataclass(frozen=True)
class BeliefExperimentConfig:
    seed: int = 0
    task_count: int = 2000
    observation_count: int = 4
    reliability: float = 0.70
    safe_utility: float = 0.10
    correct_commit_utility: float = 1.0
    wrong_commit_utility: float = -1.0


def generate_belief_tasks(config: BeliefExperimentConfig) -> tuple[BeliefTask, ...]:
    rng = random.Random(config.seed)
    tasks: list[BeliefTask] = []
    for _ in range(config.task_count):
        hidden = rng.randrange(4)
        bits = hypothesis_bits(hidden)
        observations: list[Observation] = []
        for step in range(config.observation_count):
            bit_index = step % 2
            truth = bits[bit_index]
            observed = truth if rng.random() < config.reliability else 1 - truth
            observations.append((bit_index, observed))
        tasks.append(BeliefTask(hidden, tuple(observations)))
    return tuple(tasks)


def action_utility(
    action: int | None,
    true_hypothesis: int,
    *,
    safe_utility: float,
    correct_commit_utility: float,
    wrong_commit_utility: float,
) -> float:
    if action is None:
        return safe_utility
    return correct_commit_utility if action == true_hypothesis else wrong_commit_utility


def single_belief_action(posterior: tuple[float, ...]) -> int:
    return max(range(4), key=lambda idx: (posterior[idx], -idx))


def multiple_hypothesis_action(
    posterior: tuple[float, ...],
    *,
    safe_utility: float,
    correct_commit_utility: float,
    wrong_commit_utility: float,
) -> int | None:
    best_action: int | None = None
    best_value = safe_utility
    for action in range(4):
        p_correct = posterior[action]
        expected = p_correct * correct_commit_utility + (1.0 - p_correct) * wrong_commit_utility
        if expected > best_value:
            best_value = expected
            best_action = action
    return best_action


def evaluate_belief_policy(
    tasks: tuple[BeliefTask, ...],
    *,
    reliability: float,
    mode: str,
    safe_utility: float,
    correct_commit_utility: float,
    wrong_commit_utility: float,
) -> dict[str, float | int]:
    utility = 0.0
    wrong_commits = 0
    safe_actions = 0
    entropy = 0.0
    posterior_items = 0
    for task in tasks:
        posterior = posterior_from_observations(task.observations, reliability=reliability)
        entropy += posterior_entropy(posterior)
        if mode == "single":
            action: int | None = single_belief_action(posterior)
            posterior_items += 1
        elif mode == "multiple":
            action = multiple_hypothesis_action(
                posterior,
                safe_utility=safe_utility,
                correct_commit_utility=correct_commit_utility,
                wrong_commit_utility=wrong_commit_utility,
            )
            posterior_items += 4
        else:
            raise ValueError(f"unknown mode: {mode}")
        if action is None:
            safe_actions += 1
        elif action != task.true_hypothesis:
            wrong_commits += 1
        utility += action_utility(
            action,
            task.true_hypothesis,
            safe_utility=safe_utility,
            correct_commit_utility=correct_commit_utility,
            wrong_commit_utility=wrong_commit_utility,
        )
    n = len(tasks)
    return {
        "avg_utility": utility / n,
        "wrong_commit_rate": wrong_commits / n,
        "safe_action_rate": safe_actions / n,
        "avg_posterior_entropy": entropy / n,
        "avg_active_hypothesis_items": posterior_items / n,
        "task_count": n,
    }


def run_belief_experiment(config: BeliefExperimentConfig) -> list[tuple[str, dict[str, float | int]]]:
    tasks = generate_belief_tasks(config)
    common = dict(
        reliability=config.reliability,
        safe_utility=config.safe_utility,
        correct_commit_utility=config.correct_commit_utility,
        wrong_commit_utility=config.wrong_commit_utility,
    )
    return [
        ("single_belief", evaluate_belief_policy(tasks, mode="single", **common)),
        ("multiple_hypotheses", evaluate_belief_policy(tasks, mode="multiple", **common)),
    ]
