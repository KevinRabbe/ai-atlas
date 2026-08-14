from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random


MODES = ("A", "B", "C", "D")
CONTEXTS = ("local", "coupled", "shared", "recurrent")


@dataclass(frozen=True)
class AF02Config:
    seed: int = 0
    cycles: int = 8
    regime_duration: int = 100
    switch_cost: float = 0.18
    carrying_cost: float = 0.01
    reward_noise: float = 0.10
    cue_noise: float = 0.08
    structural_jitter: float = 0.06
    exploration: float = 0.22
    decision_interval: int = 10
    minimum_hold_blocks: int = 2


@dataclass(frozen=True)
class StructuralState:
    context: str
    coupling: float
    sharedness: float
    recurrence: float
    observed_coupling: float
    observed_conflict: float
    observed_recurrence: float
    observed_transfer: float
    rewards: tuple[float, float, float, float]


@dataclass
class _Estimate:
    samples: int = 0
    mean: float = 1.45

    def optimistic(self, exploration: float) -> float:
        return self.mean + exploration / math.sqrt(self.samples + 1.0)

    def update(self, value: float) -> None:
        self.samples += 1
        # Deliberately cap the effective memory so obsolete organizational
        # economics do not become permanent constants.
        alpha = 1.0 / min(self.samples, 30)
        self.mean += alpha * (value - self.mean)


_PROTOTYPES = {
    "local": (0.12, 0.30, 0.15),
    "coupled": (0.82, 0.35, 0.25),
    "shared": (0.30, 0.88, 0.30),
    "recurrent": (0.45, 0.35, 0.90),
}


def _clip(value: float) -> float:
    return max(0.0, min(1.0, value))


def organizational_value(mode: str, coupling: float, sharedness: float, recurrence: float) -> float:
    """Continuous synthetic organization economics, not a hidden mode label.

    The terms encode the distinct costs already exposed by AF01: central
    arbitration earns value from coupling, local organization from locality,
    pooling from shared structure, and preserved variants from recurrence.
    """
    base = 1.42
    if mode == "A":
        return base + 0.18 * coupling - 0.05 * (1.0 - coupling) + 0.03 * (1.0 - sharedness)
    if mode == "B":
        return base + 0.16 * (1.0 - coupling) - 0.12 * coupling - 0.01
    if mode == "C":
        return base + 0.22 * sharedness - 0.18 * (1.0 - sharedness) + 0.03 * recurrence
    if mode == "D":
        return base + 0.19 * recurrence + 0.08 * (1.0 - sharedness) - 0.05 * (1.0 - recurrence)
    raise ValueError(f"unknown organizational mode: {mode}")


def generate_af02_lifetime(config: AF02Config) -> list[StructuralState]:
    rng = random.Random(config.seed)
    lifetime: list[StructuralState] = []
    for _ in range(config.cycles):
        for context in CONTEXTS:
            prototype = _PROTOTYPES[context]
            for _ in range(config.regime_duration):
                coupling, sharedness, recurrence = (
                    _clip(value + rng.gauss(0.0, config.structural_jitter))
                    for value in prototype
                )
                observed_coupling = _clip(coupling + rng.gauss(0.0, config.cue_noise))
                observed_conflict = _clip((1.0 - sharedness) + rng.gauss(0.0, config.cue_noise))
                observed_recurrence = _clip(recurrence + rng.gauss(0.0, config.cue_noise))
                observed_transfer = _clip(sharedness + rng.gauss(0.0, config.cue_noise))
                rewards = tuple(
                    organizational_value(mode, coupling, sharedness, recurrence)
                    + rng.gauss(0.0, config.reward_noise)
                    for mode in MODES
                )
                lifetime.append(
                    StructuralState(
                        context=context,
                        coupling=coupling,
                        sharedness=sharedness,
                        recurrence=recurrence,
                        observed_coupling=observed_coupling,
                        observed_conflict=observed_conflict,
                        observed_recurrence=observed_recurrence,
                        observed_transfer=observed_transfer,
                        rewards=rewards,
                    )
                )
    return lifetime


def _observable_bucket(state: StructuralState) -> tuple[bool, bool, bool, bool]:
    # The selector receives noisy observable proxies, never context or the
    # hidden structural variables themselves.
    return (
        state.observed_coupling >= 0.55,
        state.observed_conflict >= 0.45,
        state.observed_recurrence >= 0.60,
        state.observed_transfer >= 0.60,
    )


def _best_hidden_mode(state: StructuralState) -> str:
    return max(
        MODES,
        key=lambda mode: organizational_value(
            mode, state.coupling, state.sharedness, state.recurrence
        ),
    )


def run_af02(config: AF02Config, policy: str) -> dict[str, float | int | dict[str, float]]:
    if policy not in (*MODES, "adaptive", "oracle"):
        raise ValueError(f"unknown policy: {policy}")

    estimates: dict[tuple[bool, bool, bool, bool], dict[str, _Estimate]] = defaultdict(
        lambda: {mode: _Estimate() for mode in MODES}
    )
    lifetime = generate_af02_lifetime(config)

    current_mode: str | None = None
    block_mode: str | None = None
    block_bucket: tuple[bool, bool, bool, bool] | None = None
    block_rewards: list[float] = []
    held_blocks = config.minimum_hold_blocks + 1

    total_utility = 0.0
    switches = 0
    correct_mode_steps = 0
    mode_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for step, state in enumerate(lifetime):
        if policy in MODES:
            chosen = policy
        elif policy == "oracle":
            chosen = _best_hidden_mode(state)
        else:
            if step % config.decision_interval == 0:
                if block_mode is not None and block_bucket is not None and block_rewards:
                    estimates[block_bucket][block_mode].update(
                        sum(block_rewards) / len(block_rewards)
                    )
                block_rewards = []
                block_bucket = _observable_bucket(state)
                values = {
                    mode: estimates[block_bucket][mode].optimistic(config.exploration)
                    for mode in MODES
                }
                candidate = max(values, key=values.get)

                if current_mode is None:
                    block_mode = candidate
                    held_blocks = 0
                elif held_blocks < config.minimum_hold_blocks:
                    block_mode = current_mode
                elif (
                    candidate != current_mode
                    and values[candidate]
                    > values[current_mode]
                    + config.switch_cost / (config.decision_interval * 2.0)
                ):
                    block_mode = candidate
                    held_blocks = 0
                else:
                    block_mode = current_mode
                held_blocks += 1
            if block_mode is None:
                raise AssertionError("adaptive selector failed to choose an initial mode")
            chosen = block_mode

        cost = 0.0
        if current_mode is not None and chosen != current_mode:
            cost += config.switch_cost
            switches += 1
        if policy in {"adaptive", "oracle"}:
            # Keeping enough alternate organizational state available to switch
            # is not free. Fixed organizations do not pay this hybrid carrying cost.
            cost += config.carrying_cost

        reward = state.rewards[MODES.index(chosen)]
        total_utility += reward - cost
        if policy == "adaptive":
            block_rewards.append(reward)

        correct_mode_steps += int(chosen == _best_hidden_mode(state))
        mode_counts[state.context][chosen] += 1
        current_mode = chosen

    total_steps = len(lifetime)
    context_fractions: dict[str, float] = {}
    for context in CONTEXTS:
        count = sum(mode_counts[context].values())
        for mode in MODES:
            context_fractions[f"{context}_{mode}"] = mode_counts[context][mode] / max(1, count)

    return {
        "net_utility_per_step": total_utility / total_steps,
        "switches": switches,
        "best_mode_fraction": correct_mode_steps / total_steps,
        "context_mode_fractions": context_fractions,
    }


def run_af02_experiment(config: AF02Config) -> list[tuple[str, dict[str, float | int | dict[str, float]]]]:
    return [(policy, run_af02(config, policy)) for policy in (*MODES, "adaptive", "oracle")]
