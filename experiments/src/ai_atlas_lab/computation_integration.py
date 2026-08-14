from __future__ import annotations

from dataclasses import dataclass
import copy
import math
import random
from typing import Protocol

from .core import CostMeter


@dataclass(frozen=True)
class MultiTaskExample:
    task_id: int
    features: tuple[float, ...]
    label: int


@dataclass(frozen=True)
class ComputationIntegrationExperimentConfig:
    seed: int = 0
    input_dim: int = 6
    task_count: int = 3
    integrated_rank: int = 2
    sharedness: float = 0.75
    train_examples: int = 2400
    test_examples_per_task: int = 500
    learning_rate: float = 0.055
    checkpoints: int = 8
    adaptation_examples: int = 350
    primary_task_fraction: float = 0.70


class Learner(Protocol):
    name: str

    @property
    def parameter_count(self) -> int: ...
    def predict_score(self, task_id: int, features: tuple[float, ...], cost: CostMeter | None = None) -> float: ...
    def update(self, example: MultiTaskExample, lr: float, cost: CostMeter) -> None: ...


class SpecialistLearner:
    name = "heterogeneous_specialists"

    def __init__(self, input_dim: int, task_count: int, rng: random.Random):
        self.input_dim = input_dim
        self.task_count = task_count
        self.weights = [[rng.uniform(-0.04, 0.04) for _ in range(input_dim)] for _ in range(task_count)]

    @property
    def parameter_count(self) -> int:
        return self.input_dim * self.task_count

    def predict_score(self, task_id: int, features: tuple[float, ...], cost: CostMeter | None = None) -> float:
        if cost is not None:
            cost.messages += 1
            cost.reads += self.input_dim
            cost.operations += 2 * self.input_dim
        return sum(w * x for w, x in zip(self.weights[task_id], features))

    def update(self, example: MultiTaskExample, lr: float, cost: CostMeter) -> None:
        score = self.predict_score(example.task_id, example.features, cost)
        grad = _logistic_score_gradient(example.label, score)
        row = self.weights[example.task_id]
        for idx, x in enumerate(example.features):
            row[idx] -= lr * grad * x
            cost.writes += 1
            cost.operations += 3


class IntegratedLowRankLearner:
    name = "integrated_shared_low_rank"

    def __init__(self, input_dim: int, task_count: int, rank: int, rng: random.Random):
        self.input_dim = input_dim
        self.task_count = task_count
        self.rank = rank
        self.encoder = [[rng.uniform(-0.04, 0.04) for _ in range(rank)] for _ in range(input_dim)]
        self.task_vectors = [[rng.uniform(-0.04, 0.04) for _ in range(rank)] for _ in range(task_count)]

    @property
    def parameter_count(self) -> int:
        return self.input_dim * self.rank + self.task_count * self.rank

    def _hidden(self, features: tuple[float, ...], cost: CostMeter | None = None) -> list[float]:
        hidden = [0.0] * self.rank
        for i, x in enumerate(features):
            for k in range(self.rank):
                hidden[k] += x * self.encoder[i][k]
        if cost is not None:
            cost.reads += self.input_dim * self.rank
            cost.operations += 2 * self.input_dim * self.rank
        return hidden

    def predict_score(self, task_id: int, features: tuple[float, ...], cost: CostMeter | None = None) -> float:
        hidden = self._hidden(features, cost)
        if cost is not None:
            cost.reads += self.rank
            cost.operations += 2 * self.rank
        return sum(h * v for h, v in zip(hidden, self.task_vectors[task_id]))

    def update(self, example: MultiTaskExample, lr: float, cost: CostMeter) -> None:
        hidden = self._hidden(example.features, cost)
        task_vector = self.task_vectors[example.task_id]
        score = sum(h * v for h, v in zip(hidden, task_vector))
        cost.reads += self.rank
        cost.operations += 2 * self.rank
        grad = _logistic_score_gradient(example.label, score)
        old_task = task_vector.copy()
        for k in range(self.rank):
            task_vector[k] -= lr * grad * hidden[k]
            cost.writes += 1
            cost.operations += 3
        for i, x in enumerate(example.features):
            for k in range(self.rank):
                self.encoder[i][k] -= lr * grad * x * old_task[k]
                cost.writes += 1
                cost.operations += 4


def _logistic_score_gradient(label: int, score: float) -> float:
    z = label * score
    if z > 35.0:
        return 0.0
    if z < -35.0:
        return -float(label)
    return -label / (1.0 + math.exp(z))


def _unit_vector(values: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


def generate_task_weights(config: ComputationIntegrationExperimentConfig) -> tuple[tuple[float, ...], ...]:
    rng = random.Random(config.seed + 991)
    shared = _unit_vector([rng.gauss(0.0, 1.0) for _ in range(config.input_dim)])
    result: list[tuple[float, ...]] = []
    rho = max(0.0, min(1.0, config.sharedness))
    for _ in range(config.task_count):
        independent = _unit_vector([rng.gauss(0.0, 1.0) for _ in range(config.input_dim)])
        mixed = [rho * s + (1.0 - rho) * i for s, i in zip(shared, independent)]
        result.append(tuple(_unit_vector(mixed)))
    return tuple(result)


def _make_examples(*, seed: int, weights: tuple[tuple[float, ...], ...], count: int, task_id: int | None = None, primary_task_fraction: float | None = None) -> tuple[MultiTaskExample, ...]:
    rng = random.Random(seed)
    input_dim = len(weights[0])
    result: list[MultiTaskExample] = []
    for _ in range(count):
        if task_id is not None:
            tid = task_id
        elif primary_task_fraction is None or len(weights) == 1:
            tid = rng.randrange(len(weights))
        elif rng.random() < primary_task_fraction:
            tid = 0
        else:
            tid = 1 + rng.randrange(len(weights) - 1)
        features = tuple(rng.gauss(0.0, 1.0) for _ in range(input_dim))
        margin = sum(w * x for w, x in zip(weights[tid], features))
        result.append(MultiTaskExample(tid, features, 1 if margin >= 0.0 else -1))
    return tuple(result)


def _accuracy_by_task(model: Learner, test_sets: tuple[tuple[MultiTaskExample, ...], ...], cost: CostMeter | None = None) -> tuple[float, tuple[float, ...]]:
    per_task: list[float] = []
    for examples in test_sets:
        correct = 0
        for item in examples:
            score = model.predict_score(item.task_id, item.features, cost)
            correct += int((1 if score >= 0 else -1) == item.label)
        per_task.append(correct / len(examples))
    return sum(per_task) / len(per_task), tuple(per_task)


def _train_and_measure(model: Learner, train: tuple[MultiTaskExample, ...], test_sets: tuple[tuple[MultiTaskExample, ...], ...], config: ComputationIntegrationExperimentConfig) -> tuple[dict[str, float | int], CostMeter]:
    cost = CostMeter()
    checkpoint_every = max(1, len(train) // config.checkpoints)
    checkpoint_accuracies: list[float] = []
    for idx, example in enumerate(train, 1):
        model.update(example, config.learning_rate, cost)
        if idx % checkpoint_every == 0 or idx == len(train):
            avg, _ = _accuracy_by_task(model, test_sets)
            checkpoint_accuracies.append(avg)

    final_avg, final_per_task = _accuracy_by_task(model, test_sets)
    metrics: dict[str, float | int] = {
        "accuracy": final_avg,
        "learning_curve_mean_accuracy": sum(checkpoint_accuracies) / len(checkpoint_accuracies),
        "parameter_count": model.parameter_count,
        "operations_per_train_example": cost.operations / len(train),
        "messages_per_train_example": cost.messages / len(train),
    }
    for task_id, acc in enumerate(final_per_task):
        metrics[f"accuracy_task_{task_id}"] = acc

    before_other = sum(final_per_task[1:]) / max(1, len(final_per_task) - 1)
    adapted = copy.deepcopy(model)
    adapt_cost = CostMeter()
    weights = generate_task_weights(config)
    shift_rng = random.Random(config.seed + 7000)
    repair_direction = _unit_vector([shift_rng.gauss(0.0, 1.0) for _ in range(config.input_dim)])
    shifted_task0 = tuple(_unit_vector([0.72 * base + 0.69 * delta for base, delta in zip(weights[0], repair_direction)]))
    shifted_weights = (shifted_task0,) + weights[1:]
    adaptation = _make_examples(seed=config.seed + 7001, weights=shifted_weights, count=config.adaptation_examples, task_id=0)
    for item in adaptation:
        adapted.update(item, config.learning_rate, adapt_cost)
    _, after_per_task = _accuracy_by_task(adapted, test_sets)
    after_other = sum(after_per_task[1:]) / max(1, len(after_per_task) - 1)
    metrics["other_task_accuracy_delta_after_task0_shift_adaptation"] = after_other - before_other
    metrics["other_task_absolute_interference_after_task0_shift"] = abs(after_other - before_other)

    damaged = copy.deepcopy(model)
    if isinstance(damaged, IntegratedLowRankLearner):
        for i in range(damaged.input_dim):
            damaged.encoder[i][0] = 0.0
    else:
        damaged.weights[0] = [0.0] * damaged.input_dim
    _, damaged_per_task = _accuracy_by_task(damaged, test_sets)
    drops = [base - bad for base, bad in zip(final_per_task, damaged_per_task)]
    metrics["failure_blast_radius_tasks_gt_2pct"] = sum(drop > 0.02 for drop in drops)
    metrics["mean_accuracy_drop_after_targeted_failure"] = sum(drops) / len(drops)
    cost.add(adapt_cost)
    return metrics, cost


def run_computation_integration_experiment(config: ComputationIntegrationExperimentConfig) -> list[tuple[str, dict[str, float | int], CostMeter]]:
    if config.input_dim * config.task_count != config.integrated_rank * (config.input_dim + config.task_count):
        raise ValueError("configuration must match learned parameter count: input_dim*task_count == rank*(input_dim+task_count)")
    weights = generate_task_weights(config)
    train = _make_examples(seed=config.seed + 17, weights=weights, count=config.train_examples, primary_task_fraction=config.primary_task_fraction)
    test_sets = tuple(_make_examples(seed=config.seed + 1000 + task_id, weights=weights, count=config.test_examples_per_task, task_id=task_id) for task_id in range(config.task_count))
    models: list[Learner] = [
        IntegratedLowRankLearner(config.input_dim, config.task_count, config.integrated_rank, random.Random(config.seed + 31)),
        SpecialistLearner(config.input_dim, config.task_count, random.Random(config.seed + 31)),
    ]
    return [(model.name, *_train_and_measure(model, train, test_sets, config)) for model in models]
