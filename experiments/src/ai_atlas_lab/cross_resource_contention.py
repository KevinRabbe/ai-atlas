from __future__ import annotations

from dataclasses import dataclass
import random

RESOURCES = ("memory", "compute", "observe", "verify")
QUALITY_REGIMES = (
    ((0.92, 0.68, 0.78, 0.72), (0.70, 0.92, 0.80, 0.76), (0.76, 0.77, 0.95, 0.82), (0.67, 0.78, 0.83, 0.90)),
    ((0.58, 0.86, 0.91, 0.74), (0.62, 0.83, 0.93, 0.78), (0.60, 0.70, 0.96, 0.88), (0.56, 0.72, 0.90, 0.93)),
    ((0.78, 0.55, 0.82, 0.94), (0.82, 0.60, 0.78, 0.91), (0.73, 0.58, 0.88, 0.95), (0.76, 0.62, 0.84, 0.96)),
)
PRICE_REGIMES = (
    (0.22, 0.42, 0.72, 1.05),
    (0.48, 0.35, 0.55, 0.72),
    (0.38, 0.58, 0.50, 0.45),
)
CAPACITIES = (3, 3, 2, 2)
VALUES = (0.8, 1.6, 3.2)


@dataclass(frozen=True)
class ContendedTask:
    task_type: int
    value: float
    outcomes: tuple[bool, bool, bool, bool]


@dataclass(frozen=True)
class CrossResourceContentionConfig:
    seed: int = 0
    warmup_rounds: int = 80
    measured_rounds_per_regime: int = 180
    batch_size: int = 12
    alpha: float = 0.06
    epsilon: float = 0.06


def true_expected_utility(task: ContendedTask, regime: int, resource: int) -> float:
    probability = QUALITY_REGIMES[regime][task.task_type][resource]
    return task.value * (2.0 * probability - 1.0) - PRICE_REGIMES[regime][resource]


class QualityModel:
    def __init__(self, config: CrossResourceContentionConfig, seed: int, adaptive: bool) -> None:
        self.q = [list(row) for row in QUALITY_REGIMES[0]]
        self.alpha = config.alpha
        self.epsilon = config.epsilon
        self.adaptive = adaptive
        self.rng = random.Random(seed)

    def score(self, task: ContendedTask, regime: int, resource: int) -> float:
        probability = self.q[task.task_type][resource]
        return task.value * (2.0 * probability - 1.0) - PRICE_REGIMES[regime][resource]

    def update(self, task: ContendedTask, resource: int) -> None:
        if not self.adaptive:
            return
        old = self.q[task.task_type][resource]
        target = 1.0 if task.outcomes[resource] else 0.0
        self.q[task.task_type][resource] = (1.0 - self.alpha) * old + self.alpha * target


def _capacity_greedy(score_rows: list[list[float]]) -> list[int | None]:
    edges = sorted(
        (
            (score_rows[task][resource], task, resource)
            for task in range(len(score_rows))
            for resource in range(len(RESOURCES))
        ),
        reverse=True,
    )
    remaining = list(CAPACITIES)
    used: set[int] = set()
    assignment: list[int | None] = [None] * len(score_rows)
    for score, task, resource in edges:
        if score <= 0.0:
            break
        if task in used or remaining[resource] <= 0:
            continue
        assignment[task] = resource
        used.add(task)
        remaining[resource] -= 1
    return assignment


def _independent_assignment(
    learner: QualityModel,
    tasks: tuple[ContendedTask, ...],
    regime: int,
    *,
    explore: bool,
) -> list[int | None]:
    remaining = list(CAPACITIES)
    assignment: list[int | None] = [None] * len(tasks)
    for index, task in enumerate(tasks):
        if explore and learner.rng.random() < learner.epsilon:
            resource = learner.rng.randrange(len(RESOURCES))
        else:
            resource = max(
                range(len(RESOURCES)),
                key=lambda candidate: learner.score(task, regime, candidate),
            )
        if remaining[resource] > 0 and learner.score(task, regime, resource) > 0.0:
            assignment[index] = resource
            remaining[resource] -= 1
    return assignment


def _joint_assignment(
    learner: QualityModel,
    tasks: tuple[ContendedTask, ...],
    regime: int,
    *,
    explore: bool,
) -> list[int | None]:
    perturb = explore and learner.rng.random() < learner.epsilon
    rows: list[list[float]] = []
    for task in tasks:
        row = []
        for resource in range(len(RESOURCES)):
            value = learner.score(task, regime, resource)
            if perturb:
                value += learner.rng.uniform(-0.35, 0.45)
            row.append(value)
        rows.append(row)
    return _capacity_greedy(rows)


def _generate_batch(
    rng: random.Random,
    regime: int,
    batch_size: int,
) -> tuple[ContendedTask, ...]:
    result = []
    for _ in range(batch_size):
        task_type = rng.randrange(len(QUALITY_REGIMES[regime]))
        value = rng.choice(VALUES)
        outcomes = tuple(
            rng.random() < QUALITY_REGIMES[regime][task_type][resource]
            for resource in range(len(RESOURCES))
        )
        result.append(ContendedTask(task_type, value, outcomes))
    return tuple(result)


def _true_reference(
    tasks: tuple[ContendedTask, ...],
    regime: int,
) -> tuple[list[int | None], float]:
    rows = [
        [true_expected_utility(task, regime, resource) for resource in range(len(RESOURCES))]
        for task in tasks
    ]
    assignment = _capacity_greedy(rows)
    value = sum(
        true_expected_utility(tasks[index], regime, resource)
        for index, resource in enumerate(assignment)
        if resource is not None
    )
    return assignment, value


def run_cross_resource_contention_experiment(
    config: CrossResourceContentionConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    rng = random.Random(config.seed)
    policies = {
        "frozen_independent": (QualityModel(config, config.seed + 1, False), False),
        "adaptive_independent": (QualityModel(config, config.seed + 2, True), False),
        "frozen_joint": (QualityModel(config, config.seed + 3, False), True),
        "adaptive_joint": (QualityModel(config, config.seed + 4, True), True),
    }
    stats = {
        name: [
            {"n": 0, "actual": 0.0, "regret": 0.0, "unserved": 0, "messages": 0}
            for _ in QUALITY_REGIMES
        ]
        for name in policies
    }

    total_rounds = config.warmup_rounds + config.measured_rounds_per_regime * len(QUALITY_REGIMES)
    for round_index in range(total_rounds):
        regime = (
            0
            if round_index < config.warmup_rounds
            else min(
                len(QUALITY_REGIMES) - 1,
                (round_index - config.warmup_rounds) // config.measured_rounds_per_regime,
            )
        )
        tasks = _generate_batch(rng, regime, config.batch_size)
        _, reference_value = _true_reference(tasks, regime)

        for name, (learner, joint) in policies.items():
            adaptive = name.startswith("adaptive")
            assignment = (
                _joint_assignment(learner, tasks, regime, explore=adaptive)
                if joint
                else _independent_assignment(learner, tasks, regime, explore=adaptive)
            )
            expected = 0.0
            actual = 0.0
            for index, resource in enumerate(assignment):
                if resource is None:
                    continue
                task = tasks[index]
                expected += true_expected_utility(task, regime, resource)
                actual += (
                    task.value if task.outcomes[resource] else -task.value
                ) - PRICE_REGIMES[regime][resource]
                learner.update(task, resource)

            if round_index < config.warmup_rounds:
                continue
            row = stats[name][regime]
            row["n"] += len(tasks)
            row["actual"] += actual
            row["regret"] += reference_value - expected
            row["unserved"] += sum(resource is None for resource in assignment)
            if joint:
                row["messages"] += len(tasks) * len(RESOURCES)

    results = []
    for name, rows in stats.items():
        metrics: dict[str, float | int] = {}
        shifted_regret = 0.0
        shifted_n = 0
        for regime, row in enumerate(rows):
            count = row["n"]
            metrics[f"actual_utility_regime_{regime}"] = row["actual"] / count
            metrics[f"reference_regret_regime_{regime}"] = row["regret"] / count
            metrics[f"unserved_rate_regime_{regime}"] = row["unserved"] / count
            metrics[f"messages_per_task_regime_{regime}"] = row["messages"] / count
            if regime > 0:
                shifted_regret += row["regret"]
                shifted_n += count
        metrics["post_shift_mean_regret"] = shifted_regret / shifted_n
        results.append((name, metrics))
    return results
