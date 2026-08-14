from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class I06Config:
    seed: int = 0
    batches: int = 700
    tasks_per_batch: int = 12
    shift_batch: int = 350
    shared_capacity: int = 12
    high_fidelity_cost: float = 0.09
    rematerialize_cost: float = 0.10
    broad_state_cost: float = 0.15
    synchronize_cost: float = 0.10
    intervene_cost: float = 0.16
    exploration: float = 0.18
    decay: float = 0.992


@dataclass(frozen=True)
class RuntimeTask:
    task_id: int
    batch: int
    kind: str
    family: int
    value: float
    consequence: float
    hidden_extra_needed: bool
    outcome_draw: float


@dataclass(frozen=True)
class RuntimeVariant:
    name: str
    policy: str


ORACLE_JOINT = RuntimeVariant("oracle_joint_upper_bound", "oracle_joint")
LEARNED_JOINT = RuntimeVariant("learned_joint_allocator", "learned_joint")
FACTORIZED = RuntimeVariant("factorized_independent_controllers", "factorized")
UNIFORM_SAFE = RuntimeVariant("uniform_safe_bundle", "safe")
UNIFORM_CHEAP = RuntimeVariant("uniform_cheap_bundle", "cheap")
VARIANTS = (ORACLE_JOINT, LEARNED_JOINT, FACTORIZED, UNIFORM_SAFE, UNIFORM_CHEAP)


_OPERATION_UNITS = {"high": 1, "remat": 1, "broad": 2, "sync": 1, "observe": 2}
_ALLOWED = {
    "decision": ("high",),
    "latent": ("high", "remat", "broad"),
    "coupled": ("high", "sync"),
    "intervention": ("high", "remat", "observe"),
}
_BUNDLES = {
    "decision": (frozenset(), frozenset({"high"})),
    "latent": (
        frozenset(),
        frozenset({"high"}),
        frozenset({"remat"}),
        frozenset({"remat", "high"}),
        frozenset({"broad"}),
        frozenset({"broad", "high"}),
    ),
    "coupled": (
        frozenset(),
        frozenset({"high"}),
        frozenset({"sync"}),
        frozenset({"sync", "high"}),
    ),
    "intervention": (
        frozenset(),
        frozenset({"high"}),
        frozenset({"remat"}),
        frozenset({"remat", "high"}),
        frozenset({"observe"}),
        frozenset({"observe", "high"}),
    ),
}


def _operation_cost(operation: str, config: I06Config) -> float:
    return {
        "high": config.high_fidelity_cost,
        "remat": config.rematerialize_cost,
        "broad": config.broad_state_cost,
        "sync": config.synchronize_cost,
        "observe": config.intervene_cost,
    }[operation]


def _bundle_cost(bundle: frozenset[str], config: I06Config) -> float:
    return sum(_operation_cost(operation, config) for operation in bundle)


def _bundle_units(bundle: frozenset[str]) -> int:
    return sum(_OPERATION_UNITS[operation] for operation in bundle)


def _success_probability(task: RuntimeTask, bundle: frozenset[str]) -> float:
    need = task.hidden_extra_needed
    if task.kind == "decision":
        if need:
            return 0.94 if "high" in bundle else 0.62
        return 0.92 if "high" in bundle else 0.90

    if task.kind == "latent":
        has_source = "remat" in bundle or "broad" in bundle
        if need:
            if has_source and "high" in bundle:
                return 0.95
            if has_source:
                return 0.86
            return 0.58 if "high" in bundle else 0.52
        return 0.92 if "high" in bundle else 0.90

    if task.kind == "coupled":
        if need:
            if "sync" in bundle and "high" in bundle:
                return 0.95
            if "sync" in bundle:
                return 0.92
            return 0.60 if "high" in bundle else 0.55
        return 0.92 if "high" in bundle else 0.90

    if need:
        if "observe" in bundle:
            return 0.96 if "high" in bundle else 0.94
        if "remat" in bundle:
            return 0.79 if "high" in bundle else 0.74
        return 0.56 if "high" in bundle else 0.50
    return 0.92 if "high" in bundle else 0.90


def _expected_utility(task: RuntimeTask, probability: float) -> float:
    return (
        probability * task.value
        - (1.0 - probability) * task.consequence * task.value
    )


def generate_i06_tasks(config: I06Config) -> list[list[RuntimeTask]]:
    rng = random.Random(config.seed)
    batches: list[list[RuntimeTask]] = []
    task_id = 0
    for batch_index in range(config.batches):
        regime = int(batch_index >= config.shift_batch)
        batch: list[RuntimeTask] = []
        for _ in range(config.tasks_per_batch):
            kind = rng.choices(
                ("decision", "latent", "coupled", "intervention"),
                weights=(0.28, 0.26, 0.24, 0.22),
            )[0]
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


class _Rate:
    def __init__(self, successes: float = 2.0, total: float = 3.0) -> None:
        self.successes = successes
        self.total = total
        self.last_batch = 0

    def _advance(self, batch: int, config: I06Config) -> None:
        factor = config.decay ** max(0, batch - self.last_batch)
        self.successes *= factor
        self.total *= factor
        self.last_batch = batch

    def mean(self, batch: int, config: I06Config) -> float:
        self._advance(batch, config)
        return self.successes / self.total

    def optimistic(self, batch: int, config: I06Config) -> float:
        self._advance(batch, config)
        return min(
            0.99,
            self.successes / self.total
            + config.exploration / math.sqrt(max(1.0, self.total)),
        )

    def update(self, batch: int, success: bool, config: I06Config) -> None:
        self._advance(batch, config)
        self.successes += float(success)
        self.total += 1.0


class _JointEstimator:
    def __init__(self, config: I06Config) -> None:
        self.config = config
        self.rates: dict[tuple[str, int, tuple[str, ...]], _Rate] = defaultdict(_Rate)

    @staticmethod
    def _key(task: RuntimeTask, bundle: frozenset[str]) -> tuple[str, int, tuple[str, ...]]:
        return task.kind, task.family, tuple(sorted(bundle))

    def estimate(self, task: RuntimeTask, bundle: frozenset[str], oracle: bool) -> float:
        if oracle:
            return _success_probability(task, bundle)
        return self.rates[self._key(task, bundle)].optimistic(task.batch, self.config)

    def update(self, task: RuntimeTask, bundle: frozenset[str], success: bool) -> None:
        self.rates[self._key(task, bundle)].update(task.batch, success, self.config)


class _FactorizedEstimator:
    def __init__(self, config: I06Config) -> None:
        self.config = config
        self.present: dict[tuple[str, int, str], _Rate] = defaultdict(_Rate)
        self.absent: dict[tuple[str, int, str], _Rate] = defaultdict(_Rate)

    def effect(self, task: RuntimeTask, operation: str) -> float:
        key = (task.kind, task.family, operation)
        return (
            self.present[key].mean(task.batch, self.config)
            - self.absent[key].mean(task.batch, self.config)
        )

    def update(self, task: RuntimeTask, bundle: frozenset[str], success: bool) -> None:
        for operation in _OPERATION_UNITS:
            target = self.present if operation in bundle else self.absent
            target[(task.kind, task.family, operation)].update(task.batch, success, self.config)


def _choose_joint(
    batch: list[RuntimeTask],
    estimator: _JointEstimator,
    config: I06Config,
    oracle: bool,
) -> list[tuple[RuntimeTask, frozenset[str]]]:
    # Grouped knapsack: every task gets exactly one typed runtime bundle and all
    # optional operations compete for the same finite capacity.
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
                probability = estimator.estimate(task, bundle, oracle)
                value = _expected_utility(task, probability) - _bundle_cost(bundle, config)
                candidate = (score + value, choices + [(task, bundle)])
                previous = next_dynamic.get(used + units)
                if previous is None or candidate[0] > previous[0]:
                    next_dynamic[used + units] = candidate
        dynamic = next_dynamic
    return max(dynamic.values(), key=lambda item: item[0])[1]


def _choose_factorized(
    batch: list[RuntimeTask],
    estimator: _FactorizedEstimator,
    config: I06Config,
) -> list[tuple[RuntimeTask, frozenset[str]]]:
    # Independent controllers estimate one operation at a time. They share a
    # resource queue, but do not represent bundle synergies or substitutions.
    proposals: list[tuple[float, float, RuntimeTask, str]] = []
    for task in batch:
        for operation in _ALLOWED[task.kind]:
            gain = (
                estimator.effect(task, operation)
                * (1.0 + task.consequence)
                * task.value
                - _operation_cost(operation, config)
            )
            proposals.append(
                (gain / _OPERATION_UNITS[operation], gain, task, operation)
            )

    capacity = config.shared_capacity
    chosen: dict[int, set[str]] = {task.task_id: set() for task in batch}
    for _, gain, task, operation in sorted(proposals, key=lambda item: item[0], reverse=True):
        units = _OPERATION_UNITS[operation]
        if gain <= 0.0 or units > capacity:
            continue
        chosen[task.task_id].add(operation)
        capacity -= units
    return [(task, frozenset(chosen[task.task_id])) for task in batch]


def _choose_fixed(
    batch: list[RuntimeTask], config: I06Config, safe: bool
) -> list[tuple[RuntimeTask, frozenset[str]]]:
    full = {
        "decision": frozenset({"high"}),
        "latent": frozenset({"broad", "high"}),
        "coupled": frozenset({"sync", "high"}),
        "intervention": frozenset({"observe", "high"}),
    }
    capacity = config.shared_capacity
    chosen: list[tuple[RuntimeTask, frozenset[str]]] = []
    for task in sorted(
        batch, key=lambda item: item.value * (1.0 + item.consequence), reverse=True
    ):
        bundle = frozenset()
        if safe:
            units = _bundle_units(full[task.kind])
            if units <= capacity:
                bundle = full[task.kind]
                capacity -= units
        chosen.append((task, bundle))
    return chosen


def run_i06(config: I06Config, variant: RuntimeVariant) -> dict[str, float | int]:
    joint = _JointEstimator(config)
    factorized = _FactorizedEstimator(config)

    total_utility = 0.0
    errors = 0
    capacity_used = 0
    operation_counts: dict[str, int] = defaultdict(int)
    segment_utility: dict[str, float] = defaultdict(float)
    segment_tasks: dict[str, int] = defaultdict(int)
    failure_counts: dict[str, int] = defaultdict(int)
    redundant_source = 0

    for batch_index, batch in enumerate(generate_i06_tasks(config)):
        if variant.policy == "oracle_joint":
            choices = _choose_joint(batch, joint, config, oracle=True)
        elif variant.policy == "learned_joint":
            choices = _choose_joint(batch, joint, config, oracle=False)
        elif variant.policy == "factorized":
            choices = _choose_factorized(batch, factorized, config)
        elif variant.policy == "safe":
            choices = _choose_fixed(batch, config, safe=True)
        else:
            choices = _choose_fixed(batch, config, safe=False)

        used_this_batch = sum(_bundle_units(bundle) for _, bundle in choices)
        if used_this_batch > config.shared_capacity:
            raise AssertionError("runtime allocator exceeded shared capacity")
        capacity_used += used_this_batch

        for task, bundle in choices:
            probability = _success_probability(task, bundle)
            success = task.outcome_draw < probability
            reward = (
                task.value if success else -task.consequence * task.value
            ) - _bundle_cost(bundle, config)
            total_utility += reward
            errors += int(not success)

            for operation in bundle:
                operation_counts[operation] += 1
            if "remat" in bundle and "broad" in bundle:
                redundant_source += 1

            if not success and task.hidden_extra_needed:
                if task.kind == "decision" and "high" not in bundle:
                    failure_counts["sensitivity"] += 1
                elif task.kind == "latent" and not ({"remat", "broad"} & set(bundle)):
                    failure_counts["discarded_state"] += 1
                elif task.kind == "coupled" and "sync" not in bundle:
                    failure_counts["consistency"] += 1
                elif task.kind == "intervention" and "observe" not in bundle:
                    failure_counts["intervention"] += 1

            if variant.policy in {"oracle_joint", "learned_joint"}:
                joint.update(task, bundle, success)
            elif variant.policy == "factorized":
                factorized.update(task, bundle, success)

            if batch_index < config.shift_batch:
                segment = "pre"
            elif batch_index < config.shift_batch + 80:
                segment = "early_post"
            else:
                segment = "late_post"
            segment_utility[segment] += reward
            segment_tasks[segment] += 1

    total_tasks = config.batches * config.tasks_per_batch
    result: dict[str, float | int] = {
        "net_utility_per_task": total_utility / total_tasks,
        "error_rate": errors / total_tasks,
        "capacity_utilization": capacity_used / (config.batches * config.shared_capacity),
        "pre_shift_utility": segment_utility["pre"] / segment_tasks["pre"],
        "early_post_shift_utility": segment_utility["early_post"] / segment_tasks["early_post"],
        "late_post_shift_utility": segment_utility["late_post"] / segment_tasks["late_post"],
        "redundant_source_rate": redundant_source / total_tasks,
        "sensitivity_failure_rate": failure_counts["sensitivity"] / total_tasks,
        "discarded_state_failure_rate": failure_counts["discarded_state"] / total_tasks,
        "consistency_failure_rate": failure_counts["consistency"] / total_tasks,
        "intervention_failure_rate": failure_counts["intervention"] / total_tasks,
    }
    for operation in _OPERATION_UNITS:
        result[f"{operation}_rate"] = operation_counts[operation] / total_tasks
    return result


def run_i06_experiment(config: I06Config) -> list[tuple[str, dict[str, float | int]]]:
    return [(variant.name, run_i06(config, variant)) for variant in VARIANTS]
