from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class CreditConfig:
    seed: int = 0
    episodes: int = 6000
    contexts: int = 3
    stages: int = 9
    epsilon: float = 0.08
    local_diagnostic_reliability: float = 0.78
    prior_successes: float = 1.0
    prior_trials: float = 2.0
    tail_window: int = 800


@dataclass(frozen=True)
class Episode:
    context: int
    correct_actions: tuple[int, ...]
    diagnostic_draws: tuple[float, ...]
    explore_draws: tuple[float, ...]
    explore_actions: tuple[int, ...]


def _rules(config: CreditConfig) -> tuple[tuple[int, ...], ...]:
    rng = random.Random(config.seed + 911)
    return tuple(
        tuple(rng.randrange(2) for _ in range(config.stages))
        for _ in range(config.contexts)
    )


def generate_episodes(config: CreditConfig) -> tuple[Episode, ...]:
    rng = random.Random(config.seed)
    rules = _rules(config)
    out = []
    for _ in range(config.episodes):
        context = rng.randrange(config.contexts)
        out.append(
            Episode(
                context=context,
                correct_actions=rules[context],
                diagnostic_draws=tuple(rng.random() for _ in range(config.stages)),
                explore_draws=tuple(rng.random() for _ in range(config.stages)),
                explore_actions=tuple(rng.randrange(2) for _ in range(config.stages)),
            )
        )
    return tuple(out)


class Estimates:
    def __init__(self, config: CreditConfig):
        self.s = [
            [
                [config.prior_successes, config.prior_successes]
                for _ in range(config.stages)
            ]
            for _ in range(config.contexts)
        ]
        self.n = [
            [
                [config.prior_trials, config.prior_trials]
                for _ in range(config.stages)
            ]
            for _ in range(config.contexts)
        ]

    def value(self, context: int, stage: int, action: int) -> float:
        return self.s[context][stage][action] / self.n[context][stage][action]

    def update(self, context: int, stage: int, action: int, success: bool) -> None:
        self.n[context][stage][action] += 1.0
        self.s[context][stage][action] += 1.0 if success else 0.0


def _choose_actions(
    estimates: Estimates,
    episode: Episode,
    config: CreditConfig,
) -> tuple[int, ...]:
    actions = []
    for stage in range(config.stages):
        if episode.explore_draws[stage] < config.epsilon:
            actions.append(episode.explore_actions[stage])
        else:
            a0 = estimates.value(episode.context, stage, 0)
            a1 = estimates.value(episode.context, stage, 1)
            actions.append(1 if a1 > a0 else 0)
    return tuple(actions)


def _diagnostics(
    episode: Episode,
    actions: tuple[int, ...],
    config: CreditConfig,
) -> tuple[bool, ...]:
    result = []
    for stage, action in enumerate(actions):
        correct = action == episode.correct_actions[stage]
        reliable = (
            episode.diagnostic_draws[stage]
            < config.local_diagnostic_reliability
        )
        result.append(correct if reliable else not correct)
    return tuple(result)


def _run(config: CreditConfig, policy: str) -> dict[str, float | int]:
    estimates = Estimates(config)
    episodes = generate_episodes(config)
    successes = []
    false_blame = missed_blame = updates = retained_items = 0

    for episode in episodes:
        actions = _choose_actions(estimates, episode, config)
        correct_by_stage = tuple(
            action == episode.correct_actions[stage]
            for stage, action in enumerate(actions)
        )
        final_success = all(correct_by_stage)
        diagnostics = _diagnostics(episode, actions, config)
        successes.append(int(final_success))

        if policy == "global_trajectory":
            retained_items += config.stages
            for stage, action in enumerate(actions):
                update_success = final_success
                estimates.update(
                    episode.context,
                    stage,
                    action,
                    update_success,
                )
                updates += 1
                if not update_success and correct_by_stage[stage]:
                    false_blame += 1
                if (not correct_by_stage[stage]) and update_success:
                    missed_blame += 1

        elif policy == "local_diagnostics":
            for stage, action in enumerate(actions):
                update_success = diagnostics[stage]
                estimates.update(
                    episode.context,
                    stage,
                    action,
                    update_success,
                )
                updates += 1
                if not update_success and correct_by_stage[stage]:
                    false_blame += 1
                if update_success and not correct_by_stage[stage]:
                    missed_blame += 1

        elif policy == "eligibility_hybrid":
            # Positive local evidence is learned immediately. Suspicious stages retain
            # only a compact eligibility item until the delayed outcome arrives.
            suspicious = []
            for stage, action in enumerate(actions):
                if diagnostics[stage]:
                    estimates.update(episode.context, stage, action, True)
                    updates += 1
                    if not correct_by_stage[stage]:
                        missed_blame += 1
                else:
                    suspicious.append((stage, action))
            retained_items += len(suspicious)

            for stage, action in suspicious:
                # If the complete task succeeds, a negative local diagnostic is known
                # to have been a false alarm. Otherwise keep the local negative blame.
                update_success = final_success
                estimates.update(
                    episode.context,
                    stage,
                    action,
                    update_success,
                )
                updates += 1
                if not update_success and correct_by_stage[stage]:
                    false_blame += 1
                if update_success and not correct_by_stage[stage]:
                    missed_blame += 1
        else:
            raise ValueError(policy)

    tail = successes[-config.tail_window :]
    first_half = successes[: config.episodes // 2]
    second_half = successes[config.episodes // 2 :]
    return {
        "success_rate": sum(successes) / len(successes),
        "tail_success_rate": sum(tail) / len(tail),
        "first_half_success_rate": sum(first_half) / len(first_half),
        "second_half_success_rate": sum(second_half) / len(second_half),
        "false_blame_per_episode": false_blame / config.episodes,
        "missed_blame_per_episode": missed_blame / config.episodes,
        "retained_items_per_episode": retained_items / config.episodes,
        "updates_per_episode": updates / config.episodes,
    }


def run_credit_assignment_experiment(
    config: CreditConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    return [
        ("global_trajectory", _run(config, "global_trajectory")),
        ("local_diagnostics", _run(config, "local_diagnostics")),
        ("eligibility_hybrid", _run(config, "eligibility_hybrid")),
    ]
