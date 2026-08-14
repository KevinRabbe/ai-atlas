from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random

from .adaptive_organization import CONTEXTS, MODES, organizational_value


_PROTOTYPES = {
    "local": (0.12, 0.30, 0.15),
    "coupled": (0.82, 0.35, 0.25),
    "shared": (0.30, 0.88, 0.30),
    "recurrent": (0.45, 0.35, 0.90),
}


@dataclass(frozen=True)
class AF03Config:
    seed: int = 0
    domains: int = 4
    cycles: int = 6
    regime_duration: int = 80
    heterogeneous_domains: bool = True
    cross_domain_coupling: float = 0.12
    domain_switch_cost: float = 0.08
    global_switch_cost: float = 0.18
    scoped_carrying_cost: float = 0.006
    global_carrying_cost: float = 0.01
    boundary_mismatch_cost: float = 0.05
    reward_noise: float = 0.10
    cue_noise: float = 0.08
    structural_jitter: float = 0.05
    decision_interval: int = 10
    exploration: float = 0.22


@dataclass(frozen=True)
class DomainState:
    context: str
    coupling: float
    sharedness: float
    recurrence: float
    observed_coupling: float
    observed_sharedness: float
    observed_recurrence: float
    rewards: tuple[float, float, float, float]


@dataclass
class _Estimate:
    samples: int = 0
    mean: float = 1.45

    def optimistic(self, exploration: float) -> float:
        return self.mean + exploration / math.sqrt(self.samples + 1.0)

    def update(self, value: float) -> None:
        self.samples += 1
        alpha = 1.0 / min(self.samples, 30)
        self.mean += alpha * (value - self.mean)


def _clip(value: float) -> float:
    return max(0.0, min(1.0, value))


def _bucket(coupling: float, sharedness: float, recurrence: float) -> tuple[bool, bool, bool, bool]:
    return (
        coupling >= 0.55,
        (1.0 - sharedness) >= 0.45,
        recurrence >= 0.60,
        sharedness >= 0.60,
    )


def generate_af03_lifetime(config: AF03Config) -> list[list[DomainState]]:
    rng = random.Random(config.seed)
    lifetime: list[list[DomainState]] = []
    for cycle in range(config.cycles):
        for block in range(len(CONTEXTS)):
            base_index = block % len(CONTEXTS)
            contexts = []
            for domain in range(config.domains):
                index = (
                    (base_index + domain) % len(CONTEXTS)
                    if config.heterogeneous_domains
                    else base_index
                )
                contexts.append(CONTEXTS[index])

            for _ in range(config.regime_duration):
                states: list[DomainState] = []
                for context in contexts:
                    prototype = _PROTOTYPES[context]
                    coupling, sharedness, recurrence = (
                        _clip(value + rng.gauss(0.0, config.structural_jitter))
                        for value in prototype
                    )
                    rewards = tuple(
                        organizational_value(mode, coupling, sharedness, recurrence)
                        + rng.gauss(0.0, config.reward_noise)
                        for mode in MODES
                    )
                    states.append(
                        DomainState(
                            context=context,
                            coupling=coupling,
                            sharedness=sharedness,
                            recurrence=recurrence,
                            observed_coupling=_clip(coupling + rng.gauss(0.0, config.cue_noise)),
                            observed_sharedness=_clip(sharedness + rng.gauss(0.0, config.cue_noise)),
                            observed_recurrence=_clip(recurrence + rng.gauss(0.0, config.cue_noise)),
                            rewards=rewards,
                        )
                    )
                lifetime.append(states)
    return lifetime


def _choose(estimates, key, exploration: float) -> str:
    return max(MODES, key=lambda mode: estimates[key][mode].optimistic(exploration))


def _hidden_best(state: DomainState) -> str:
    return max(
        MODES,
        key=lambda mode: organizational_value(
            mode, state.coupling, state.sharedness, state.recurrence
        ),
    )


def run_af03(config: AF03Config, policy: str) -> dict[str, float | int]:
    valid = (*MODES, "global_adaptive", "scoped_adaptive", "oracle_global", "oracle_scoped")
    if policy not in valid:
        raise ValueError(f"unknown AF03 policy: {policy}")

    global_estimates = defaultdict(lambda: {mode: _Estimate() for mode in MODES})
    scoped_estimates = [
        defaultdict(lambda: {mode: _Estimate() for mode in MODES})
        for _ in range(config.domains)
    ]

    current_global: str | None = None
    current_scoped: list[str | None] = [None] * config.domains
    block_global: str | None = None
    block_scoped: list[str | None] = [None] * config.domains
    global_key = None
    scoped_keys = [None] * config.domains
    global_rewards: list[float] = []
    scoped_rewards: list[list[float]] = [[] for _ in range(config.domains)]

    total_utility = 0.0
    switches = 0
    mismatch_cost_total = 0.0
    correct_domain_modes = 0
    total_domain_decisions = 0

    lifetime = generate_af03_lifetime(config)
    for step, states in enumerate(lifetime):
        if step % config.decision_interval == 0:
            if block_global is not None and global_key is not None and global_rewards:
                global_estimates[global_key][block_global].update(
                    sum(global_rewards) / len(global_rewards)
                )
            for domain in range(config.domains):
                if block_scoped[domain] is not None and scoped_keys[domain] is not None and scoped_rewards[domain]:
                    scoped_estimates[domain][scoped_keys[domain]][block_scoped[domain]].update(
                        sum(scoped_rewards[domain]) / len(scoped_rewards[domain])
                    )
            global_rewards = []
            scoped_rewards = [[] for _ in range(config.domains)]

            mean_coupling = sum(state.observed_coupling for state in states) / config.domains
            mean_sharedness = sum(state.observed_sharedness for state in states) / config.domains
            mean_recurrence = sum(state.observed_recurrence for state in states) / config.domains
            global_key = _bucket(mean_coupling, mean_sharedness, mean_recurrence)
            block_global = _choose(global_estimates, global_key, config.exploration)

            for domain, state in enumerate(states):
                scoped_keys[domain] = _bucket(
                    state.observed_coupling,
                    state.observed_sharedness,
                    state.observed_recurrence,
                )
                block_scoped[domain] = _choose(
                    scoped_estimates[domain], scoped_keys[domain], config.exploration
                )

        if policy in MODES:
            modes = [policy] * config.domains
        elif policy == "global_adaptive":
            if block_global is None:
                raise AssertionError("global selector has no mode")
            modes = [block_global] * config.domains
        elif policy == "scoped_adaptive":
            if any(mode is None for mode in block_scoped):
                raise AssertionError("scoped selector has an uninitialized mode")
            modes = [str(mode) for mode in block_scoped]
        elif policy == "oracle_global":
            best = max(
                MODES,
                key=lambda mode: sum(
                    organizational_value(mode, state.coupling, state.sharedness, state.recurrence)
                    for state in states
                ),
            )
            modes = [best] * config.domains
        else:
            modes = [_hidden_best(state) for state in states]

        cost = 0.0
        if policy in {"global_adaptive", "oracle_global"}:
            chosen = modes[0]
            if current_global is not None and chosen != current_global:
                cost += config.global_switch_cost
                switches += 1
            current_global = chosen
            cost += config.global_carrying_cost
        elif policy in {"scoped_adaptive", "oracle_scoped"}:
            for domain, chosen in enumerate(modes):
                if current_scoped[domain] is not None and chosen != current_scoped[domain]:
                    cost += config.domain_switch_cost
                    switches += 1
                current_scoped[domain] = chosen
            cost += config.scoped_carrying_cost * config.domains

            mismatched_pairs = 0
            for left in range(config.domains):
                for right in range(left + 1, config.domains):
                    mismatched_pairs += int(modes[left] != modes[right])
            mismatch_cost = (
                config.cross_domain_coupling
                * config.boundary_mismatch_cost
                * mismatched_pairs
            )
            mismatch_cost_total += mismatch_cost
            cost += mismatch_cost

        rewards = [
            state.rewards[MODES.index(mode)] for state, mode in zip(states, modes)
        ]
        total_utility += sum(rewards) / config.domains - cost / config.domains

        if policy == "global_adaptive":
            global_rewards.append(sum(rewards) / config.domains)
        elif policy == "scoped_adaptive":
            for domain, reward in enumerate(rewards):
                scoped_rewards[domain].append(reward)

        for state, mode in zip(states, modes):
            correct_domain_modes += int(mode == _hidden_best(state))
            total_domain_decisions += 1

    return {
        "net_utility_per_domain_step": total_utility / len(lifetime),
        "switches": switches,
        "mismatch_cost_per_step": mismatch_cost_total / len(lifetime),
        "best_domain_mode_fraction": correct_domain_modes / total_domain_decisions,
    }
