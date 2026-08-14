from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random

from .integrated_resource_kernel import (
    I06Config,
    RuntimeTask,
    _BUNDLES,
    _JointEstimator,
    _Rate,
    _bundle_cost,
    _bundle_units,
    _expected_utility,
    _success_probability,
)


@dataclass(frozen=True)
class ArchitectureScenario:
    name: str
    seed: int = 0
    batches: int = 360
    tasks_per_batch: int = 10
    shared_capacity: int = 12
    regime_length: int = 90
    kind_weights: tuple[float, float, float, float] = (0.28, 0.26, 0.24, 0.22)
    central_batch_cost: float = 0.36
    bid_cost: float = 0.002
    sync_message_cost: float = 0.008
    archive_batch_cost: float = 0.24
    archive_switch_cost: float = 0.35


@dataclass(frozen=True)
class ArchitectureVariant:
    name: str
    family: str


HIERARCHICAL_A = ArchitectureVariant("A_hierarchical_adaptive", "A")
DISTRIBUTED_B = ArchitectureVariant("B_distributed_event_ecology", "B")
INTEGRATED_C = ArchitectureVariant("C_integrated_predictive_core", "C")
DEVELOPMENTAL_D = ArchitectureVariant("D_developmental_variants", "D")
ARCHITECTURES = (HIERARCHICAL_A, DISTRIBUTED_B, INTEGRATED_C, DEVELOPMENTAL_D)


def sparse_stationary(seed: int = 0) -> ArchitectureScenario:
    return ArchitectureScenario(
        name="sparse_stationary",
        seed=seed,
        shared_capacity=18,
        regime_length=10_000,
        kind_weights=(0.40, 0.30, 0.20, 0.10),
    )


def coupled_switching(seed: int = 0) -> ArchitectureScenario:
    return ArchitectureScenario(
        name="coupled_switching",
        seed=seed,
        shared_capacity=9,
        regime_length=90,
        kind_weights=(0.18, 0.18, 0.42, 0.22),
    )


def recurring_mixed(seed: int = 0) -> ArchitectureScenario:
    return ArchitectureScenario(
        name="recurring_mixed",
        seed=seed,
        shared_capacity=12,
        regime_length=72,
        kind_weights=(0.25, 0.30, 0.20, 0.25),
    )


SCENARIO_BUILDERS = (sparse_stationary, coupled_switching, recurring_mixed)


def _runtime_config(scenario: ArchitectureScenario) -> I06Config:
    return I06Config(
        seed=scenario.seed,
        batches=scenario.batches,
        tasks_per_batch=scenario.tasks_per_batch,
        shift_batch=scenario.regime_length,
        shared_capacity=scenario.shared_capacity,
    )


def generate_architecture_tasks(scenario: ArchitectureScenario) -> list[list[RuntimeTask]]:
    rng = random.Random(scenario.seed)
    kinds = ("decision", "latent", "coupled", "intervention")
    batches: list[list[RuntimeTask]] = []
    task_id = 0
    for batch_index in range(scenario.batches):
        regime = (batch_index // scenario.regime_length) % 2
        batch: list[RuntimeTask] = []
        for _ in range(scenario.tasks_per_batch):
            kind = rng.choices(kinds, weights=scenario.kind_weights)[0]
            family = rng.randrange(2)
            batch.append(
                RuntimeTask(
                    task_id=task_id,
                    batch=batch_index,
                    kind=kind,
                    family=family,
                    value=rng.choice((1.0, 2.0, 4.0)),
                    consequence=rng.choice((0.5, 1.0, 2.0, 4.0)),
                    hidden_extra_needed=(family == regime),
                    outcome_draw=rng.random(),
                )
            )
            task_id += 1
        batches.append(batch)
    return batches


class _PooledEstimator:
    """Integrated core deliberately pools family-specific evidence."""

    def __init__(self, config: I06Config) -> None:
        self.config = config
        self.rates: dict[tuple[str, tuple[str, ...]], _Rate] = defaultdict(_Rate)

    @staticmethod
    def _key(task: RuntimeTask, bundle: frozenset[str]) -> tuple[str, tuple[str, ...]]:
        return task.kind, tuple(sorted(bundle))

    def estimate(self, task: RuntimeTask, bundle: frozenset[str]) -> float:
        return self.rates[self._key(task, bundle)].optimistic(task.batch, self.config)

    def update(self, task: RuntimeTask, bundle: frozenset[str], success: bool) -> None:
        self.rates[self._key(task, bundle)].update(task.batch, success, self.config)


def _choose_joint(
    batch: list[RuntimeTask], estimator, config: I06Config, pooled: bool = False
) -> list[tuple[RuntimeTask, frozenset[str]]]:
    dynamic: dict[int, tuple[float, list[tuple[RuntimeTask, frozenset[str]]]]] = {
        0: (0.0, [])
    }
    for task in batch:
        next_dynamic: dict[int, tuple[float, list[tuple[RuntimeTask, frozenset[str]]]]] = {}
        for used, (score, choices) in dynamic.items():
            for bundle in _BUNDLES[task.kind]:
                units = _bundle_units(bundle)
                if used + units > config.shared_capacity:
                    continue
                probability = (
                    estimator.estimate(task, bundle)
                    if pooled
                    else estimator.estimate(task, bundle, False)
                )
                value = _expected_utility(task, probability) - _bundle_cost(bundle, config)
                candidate = (score + value, choices + [(task, bundle)])
                previous = next_dynamic.get(used + units)
                if previous is None or candidate[0] > previous[0]:
                    next_dynamic[used + units] = candidate
        dynamic = next_dynamic
    return max(dynamic.values(), key=lambda item: item[0])[1]


def _choose_distributed(
    batch: list[RuntimeTask], estimator: _JointEstimator, config: I06Config
) -> tuple[list[tuple[RuntimeTask, frozenset[str]]], int]:
    # Each local task submits only its locally best upgrade. A resource-local
    # auction handles scarcity but cannot reconsider the global bundle frontier.
    bids: list[tuple[float, float, RuntimeTask, frozenset[str]]] = []
    chosen = {task.task_id: (task, frozenset()) for task in batch}
    for task in batch:
        baseline_probability = estimator.estimate(task, frozenset(), False)
        baseline_value = _expected_utility(task, baseline_probability)
        best = None
        for bundle in _BUNDLES[task.kind]:
            if not bundle:
                continue
            probability = estimator.estimate(task, bundle, False)
            value = _expected_utility(task, probability) - _bundle_cost(bundle, config)
            gain = value - baseline_value
            units = _bundle_units(bundle)
            candidate = (gain / max(1, units), gain, task, bundle)
            if best is None or candidate[0] > best[0]:
                best = candidate
        if best is not None and best[1] > 0.0:
            bids.append(best)

    capacity = config.shared_capacity
    for _, _, task, bundle in sorted(bids, key=lambda item: item[0], reverse=True):
        units = _bundle_units(bundle)
        if units <= capacity:
            chosen[task.task_id] = (task, bundle)
            capacity -= units
    return list(chosen.values()), len(bids)


def _score_choices(
    choices: list[tuple[RuntimeTask, frozenset[str]]], config: I06Config
) -> tuple[float, int, int, int]:
    utility = 0.0
    errors = 0
    syncs = 0
    units = 0
    for task, bundle in choices:
        success = task.outcome_draw < _success_probability(task, bundle)
        utility += (
            task.value if success else -task.consequence * task.value
        ) - _bundle_cost(bundle, config)
        errors += int(not success)
        syncs += int("sync" in bundle)
        units += _bundle_units(bundle)
    return utility, errors, syncs, units


def run_architecture_family(
    scenario: ArchitectureScenario, architecture: ArchitectureVariant
) -> dict[str, float | int]:
    config = _runtime_config(scenario)
    tasks = generate_architecture_tasks(scenario)
    conditional = _JointEstimator(config)
    pooled = _PooledEstimator(config)
    archive = (_JointEstimator(config), _JointEstimator(config))
    active_archive = 0
    archive_losses = [0.45, 0.45]
    archive_switches = 0
    archive_cooldown = 0

    total_utility = 0.0
    total_errors = 0
    total_units = 0
    control_messages = 0
    explicit_overhead = 0.0

    for batch in tasks:
        if architecture.family == "A":
            choices = _choose_joint(batch, conditional, config)
            overhead = scenario.central_batch_cost
            control_messages += 2 * len(batch)
        elif architecture.family == "B":
            choices, bids = _choose_distributed(batch, conditional, config)
            overhead = scenario.bid_cost * bids
            control_messages += bids
        elif architecture.family == "C":
            choices = _choose_joint(batch, pooled, config, pooled=True)
            overhead = 0.0
        else:
            if archive_cooldown > 0:
                archive_cooldown -= 1
            choices = _choose_joint(batch, archive[active_archive], config)
            overhead = scenario.archive_batch_cost

        batch_utility, batch_errors, syncs, units = _score_choices(choices, config)
        if architecture.family == "B":
            overhead += scenario.sync_message_cost * syncs
            control_messages += syncs
        total_utility += batch_utility - overhead
        explicit_overhead += overhead
        total_errors += batch_errors
        total_units += units

        if architecture.family == "D":
            losses = [0.0, 0.0]
            for task, bundle in choices:
                success = task.outcome_draw < _success_probability(task, bundle)
                for model_index in (0, 1):
                    probability = max(
                        0.02,
                        min(
                            0.98,
                            archive[model_index].estimate(task, bundle, False),
                        ),
                    )
                    losses[model_index] += -(
                        math.log(probability)
                        if success
                        else math.log(1.0 - probability)
                    )
                archive[active_archive].update(task, bundle, success)
            for model_index in (0, 1):
                batch_loss = losses[model_index] / len(choices)
                archive_losses[model_index] = (
                    0.88 * archive_losses[model_index] + 0.12 * batch_loss
                )
            alternate = 1 - active_archive
            if (
                archive_cooldown == 0
                and batch[0].batch > 25
                and archive_losses[alternate] + 0.06 < archive_losses[active_archive]
            ):
                active_archive = alternate
                archive_switches += 1
                archive_cooldown = 18
                total_utility -= scenario.archive_switch_cost
                explicit_overhead += scenario.archive_switch_cost
        else:
            for task, bundle in choices:
                success = task.outcome_draw < _success_probability(task, bundle)
                if architecture.family in {"A", "B"}:
                    conditional.update(task, bundle, success)
                else:
                    pooled.update(task, bundle, success)

    total_tasks = scenario.batches * scenario.tasks_per_batch
    return {
        "net_utility_per_task": total_utility / total_tasks,
        "error_rate": total_errors / total_tasks,
        "capacity_utilization": total_units / (scenario.batches * scenario.shared_capacity),
        "control_messages_per_task": control_messages / total_tasks,
        "explicit_overhead_per_task": explicit_overhead / total_tasks,
        "archive_switches": archive_switches,
    }


def run_architecture_scenario(
    scenario: ArchitectureScenario,
) -> list[tuple[str, dict[str, float | int]]]:
    return [
        (architecture.name, run_architecture_family(scenario, architecture))
        for architecture in ARCHITECTURES
    ]
