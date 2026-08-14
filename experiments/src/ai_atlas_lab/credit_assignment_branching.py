from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class BranchCreditConfig:
    seed: int = 0
    episodes: int = 6000
    branches: int = 2
    stages_per_branch: int = 5
    epsilon: float = 0.08
    local_diagnostic_reliability: float = 0.80
    prior_successes: float = 1.0
    prior_trials: float = 2.0
    tail_window: int = 800


@dataclass(frozen=True)
class BranchEpisode:
    selected_branch: int
    rules: tuple[tuple[int, ...], ...]
    explore_draws: tuple[tuple[float, ...], ...]
    explore_actions: tuple[tuple[int, ...], ...]
    diagnostic_draws: tuple[float, ...]


class Estimates:
    def __init__(self, config: BranchCreditConfig):
        self.s = [
            [
                [config.prior_successes, config.prior_successes]
                for _ in range(config.stages_per_branch)
            ]
            for _ in range(config.branches)
        ]
        self.n = [
            [
                [config.prior_trials, config.prior_trials]
                for _ in range(config.stages_per_branch)
            ]
            for _ in range(config.branches)
        ]

    def value(self, branch: int, stage: int, action: int) -> float:
        return self.s[branch][stage][action] / self.n[branch][stage][action]

    def update(self, branch: int, stage: int, action: int, success: bool) -> None:
        self.n[branch][stage][action] += 1.0
        self.s[branch][stage][action] += 1.0 if success else 0.0


def _rules(config: BranchCreditConfig) -> tuple[tuple[int, ...], ...]:
    rng = random.Random(config.seed + 7123)
    return tuple(
        tuple(rng.randrange(2) for _ in range(config.stages_per_branch))
        for _ in range(config.branches)
    )


def generate_episodes(config: BranchCreditConfig) -> tuple[BranchEpisode, ...]:
    rng = random.Random(config.seed)
    rules = _rules(config)
    episodes = []
    for _ in range(config.episodes):
        episodes.append(
            BranchEpisode(
                selected_branch=rng.randrange(config.branches),
                rules=rules,
                explore_draws=tuple(
                    tuple(
                        rng.random()
                        for _ in range(config.stages_per_branch)
                    )
                    for _ in range(config.branches)
                ),
                explore_actions=tuple(
                    tuple(
                        rng.randrange(2)
                        for _ in range(config.stages_per_branch)
                    )
                    for _ in range(config.branches)
                ),
                diagnostic_draws=tuple(
                    rng.random()
                    for _ in range(config.stages_per_branch)
                ),
            )
        )
    return tuple(episodes)


def _choose(
    estimates: Estimates,
    episode: BranchEpisode,
    config: BranchCreditConfig,
) -> tuple[tuple[int, ...], ...]:
    result = []
    for branch in range(config.branches):
        row = []
        for stage in range(config.stages_per_branch):
            if episode.explore_draws[branch][stage] < config.epsilon:
                row.append(episode.explore_actions[branch][stage])
            else:
                a0 = estimates.value(branch, stage, 0)
                a1 = estimates.value(branch, stage, 1)
                row.append(1 if a1 > a0 else 0)
        result.append(tuple(row))
    return tuple(result)


def _run(config: BranchCreditConfig, policy: str) -> dict[str, float | int]:
    estimates = Estimates(config)
    episodes = generate_episodes(config)
    success_history = []
    cross_branch_updates = false_blame = retained = 0

    for episode in episodes:
        actions = _choose(estimates, episode, config)
        selected = episode.selected_branch
        selected_correct = tuple(
            actions[selected][stage] == episode.rules[selected][stage]
            for stage in range(config.stages_per_branch)
        )
        final_success = all(selected_correct)
        success_history.append(int(final_success))

        if policy == "global_all_branches":
            retained += config.branches * config.stages_per_branch
            for branch in range(config.branches):
                for stage in range(config.stages_per_branch):
                    action = actions[branch][stage]
                    estimates.update(
                        branch,
                        stage,
                        action,
                        final_success,
                    )
                    if branch != selected:
                        cross_branch_updates += 1
                    elif (not final_success) and selected_correct[stage]:
                        false_blame += 1

        elif policy == "branch_factorized":
            retained += config.stages_per_branch
            for stage in range(config.stages_per_branch):
                action = actions[selected][stage]
                estimates.update(
                    selected,
                    stage,
                    action,
                    final_success,
                )
                if (not final_success) and selected_correct[stage]:
                    false_blame += 1

        elif policy == "branch_eligibility":
            suspicious = []
            for stage in range(config.stages_per_branch):
                action = actions[selected][stage]
                correct = selected_correct[stage]
                reliable = (
                    episode.diagnostic_draws[stage]
                    < config.local_diagnostic_reliability
                )
                local_positive = correct if reliable else not correct
                if local_positive:
                    estimates.update(selected, stage, action, True)
                else:
                    suspicious.append((stage, action, correct))
            retained += len(suspicious)
            for stage, action, correct in suspicious:
                estimates.update(
                    selected,
                    stage,
                    action,
                    final_success,
                )
                if (not final_success) and correct:
                    false_blame += 1
        else:
            raise ValueError(policy)

    tail = success_history[-config.tail_window :]
    return {
        "success_rate": sum(success_history) / len(success_history),
        "tail_success_rate": sum(tail) / len(tail),
        "cross_branch_updates_per_episode": (
            cross_branch_updates / config.episodes
        ),
        "false_blame_per_episode": false_blame / config.episodes,
        "retained_items_per_episode": retained / config.episodes,
    }


def run_branch_credit_experiment(
    config: BranchCreditConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    return [
        ("global_all_branches", _run(config, "global_all_branches")),
        ("branch_factorized", _run(config, "branch_factorized")),
        ("branch_eligibility", _run(config, "branch_eligibility")),
    ]
