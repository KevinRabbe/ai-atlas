from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Protocol

from .core import CostMeter


def _pairs(raw: tuple[int, ...]) -> tuple[float, ...]:
    out: list[float] = []
    for i in range(len(raw)):
        for j in range(i + 1, len(raw)):
            out.append(float(raw[i] * raw[j]))
    return tuple(out)


def _unit(values: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


def _grad(label: int, score: float) -> float:
    z = label * score
    if z > 35:
        return 0.0
    if z < -35:
        return -float(label)
    return -label / (1.0 + math.exp(z))


@dataclass(frozen=True)
class Example:
    task_id: int
    features: tuple[float, ...]
    label: int


@dataclass(frozen=True)
class CompositionalExperimentConfig:
    seed: int = 0
    raw_bits: int = 6
    task_count: int = 3
    sharedness: float = 0.65
    train_examples: int = 1800
    test_examples_per_task: int = 400
    primary_task_fraction: float = 0.80
    learning_rate: float = 0.035
    shared_lr_scale: float = 0.45

    @property
    def feature_dim(self) -> int:
        return self.raw_bits * (self.raw_bits - 1) // 2

    @property
    def residual_width(self) -> int:
        numerator = self.feature_dim * (self.task_count - 1)
        if numerator % self.task_count:
            raise ValueError("feature/task dimensions do not permit exact parameter matching")
        return numerator // self.task_count


class Learner(Protocol):
    name: str
    @property
    def parameter_count(self) -> int: ...
    def score(self, task_id: int, features: tuple[float, ...], cost: CostMeter | None = None) -> float: ...
    def update(self, example: Example, config: CompositionalExperimentConfig, cost: CostMeter) -> None: ...


class Specialists:
    name = "compositional_specialists"

    def __init__(self, dim: int, tasks: int, rng: random.Random):
        self.dim = dim
        self.tasks = tasks
        self.weights = [[rng.uniform(-0.02, 0.02) for _ in range(dim)] for _ in range(tasks)]

    @property
    def parameter_count(self) -> int:
        return self.dim * self.tasks

    def score(self, task_id: int, features: tuple[float, ...], cost: CostMeter | None = None) -> float:
        if cost:
            cost.messages += 1
            cost.reads += self.dim
            cost.operations += 2 * self.dim
        return sum(w * x for w, x in zip(self.weights[task_id], features))

    def update(self, example: Example, config: CompositionalExperimentConfig, cost: CostMeter) -> None:
        score = self.score(example.task_id, example.features, cost)
        g = _grad(example.label, score)
        row = self.weights[example.task_id]
        for i, x in enumerate(example.features):
            row[i] -= config.learning_rate * g * x
            cost.writes += 1
            cost.operations += 3


class SharedPlusResidual:
    name = "shared_plus_isolated_residual"

    def __init__(self, dim: int, tasks: int, residual_width: int, rng: random.Random):
        self.dim = dim
        self.tasks = tasks
        self.residual_width = residual_width
        self.shared = [rng.uniform(-0.02, 0.02) for _ in range(dim)]
        self.masks: list[tuple[int, ...]] = []
        for task in range(tasks):
            start = (task * (dim // tasks)) % dim
            self.masks.append(tuple((start + offset) % dim for offset in range(residual_width)))
        self.residuals = [[0.0 for _ in range(residual_width)] for _ in range(tasks)]

    @property
    def parameter_count(self) -> int:
        return self.dim + self.tasks * self.residual_width

    def score(self, task_id: int, features: tuple[float, ...], cost: CostMeter | None = None) -> float:
        shared_score = sum(w * x for w, x in zip(self.shared, features))
        residual_score = sum(w * features[i] for w, i in zip(self.residuals[task_id], self.masks[task_id]))
        if cost:
            cost.reads += self.dim + self.residual_width
            cost.operations += 2 * (self.dim + self.residual_width)
        return shared_score + residual_score

    def update(self, example: Example, config: CompositionalExperimentConfig, cost: CostMeter) -> None:
        score = self.score(example.task_id, example.features, cost)
        g = _grad(example.label, score)
        for i, x in enumerate(example.features):
            self.shared[i] -= config.learning_rate * config.shared_lr_scale * g * x
            cost.writes += 1
            cost.operations += 4
        residual = self.residuals[example.task_id]
        for r, feature_idx in enumerate(self.masks[example.task_id]):
            residual[r] -= config.learning_rate * g * example.features[feature_idx]
            cost.writes += 1
            cost.operations += 3


class SharedOnly:
    name = "shared_only_reference"

    def __init__(self, dim: int, rng: random.Random):
        self.dim = dim
        self.weights = [rng.uniform(-0.02, 0.02) for _ in range(dim)]

    @property
    def parameter_count(self) -> int:
        return self.dim

    def score(self, task_id: int, features: tuple[float, ...], cost: CostMeter | None = None) -> float:
        if cost:
            cost.reads += self.dim
            cost.operations += 2 * self.dim
        return sum(w * x for w, x in zip(self.weights, features))

    def update(self, example: Example, config: CompositionalExperimentConfig, cost: CostMeter) -> None:
        score = self.score(example.task_id, example.features, cost)
        g = _grad(example.label, score)
        for i, x in enumerate(example.features):
            self.weights[i] -= config.learning_rate * g * x
            cost.writes += 1
            cost.operations += 3


def _true_weights(config: CompositionalExperimentConfig) -> tuple[tuple[float, ...], ...]:
    rng = random.Random(config.seed + 3301)
    shared = _unit([rng.gauss(0, 1) for _ in range(config.feature_dim)])
    rho = min(1.0, max(0.0, config.sharedness))
    rows = []
    for _ in range(config.task_count):
        independent = _unit([rng.gauss(0, 1) for _ in range(config.feature_dim)])
        rows.append(tuple(_unit([rho * a + (1-rho) * b for a,b in zip(shared, independent)])))
    return tuple(rows)


def _examples(config: CompositionalExperimentConfig, *, seed: int, count: int, task_id: int | None = None) -> tuple[Example, ...]:
    rng = random.Random(seed)
    weights = _true_weights(config)
    out=[]
    for _ in range(count):
        if task_id is not None:
            tid=task_id
        elif rng.random() < config.primary_task_fraction:
            tid=0
        else:
            tid=1+rng.randrange(config.task_count-1)
        raw=tuple(1 if rng.random()<0.5 else -1 for _ in range(config.raw_bits))
        feats=_pairs(raw)
        margin=sum(w*x for w,x in zip(weights[tid],feats))
        out.append(Example(tid,feats,1 if margin>=0 else -1))
    return tuple(out)


def _accuracy(model: Learner, tests: tuple[tuple[Example,...],...]) -> tuple[float, tuple[float,...]]:
    per=[]
    for examples in tests:
        good=0
        for ex in examples:
            good += int((1 if model.score(ex.task_id,ex.features)>=0 else -1)==ex.label)
        per.append(good/len(examples))
    return sum(per)/len(per), tuple(per)


def _train(model: Learner, config: CompositionalExperimentConfig, train: tuple[Example,...], tests: tuple[tuple[Example,...],...]) -> tuple[dict[str,float|int],CostMeter]:
    cost=CostMeter()
    for ex in train:
        model.update(ex,config,cost)
    avg, per=_accuracy(model,tests)
    metrics: dict[str,float|int]={
        "accuracy":avg,
        "parameter_count":model.parameter_count,
        "operations_per_train_example":cost.operations/len(train),
        "messages_per_train_example":cost.messages/len(train),
    }
    for i,a in enumerate(per):
        metrics[f"accuracy_task_{i}"]=a
    return metrics,cost


def run_compositional_integration_experiment(config: CompositionalExperimentConfig) -> list[tuple[str,dict[str,float|int],CostMeter]]:
    train=_examples(config,seed=config.seed+17,count=config.train_examples)
    tests=tuple(_examples(config,seed=config.seed+900+i,count=config.test_examples_per_task,task_id=i) for i in range(config.task_count))
    rng_seed=config.seed+77
    models: list[Learner]=[
        SharedOnly(config.feature_dim, random.Random(rng_seed)),
        SharedPlusResidual(config.feature_dim,config.task_count,config.residual_width,random.Random(rng_seed)),
        Specialists(config.feature_dim,config.task_count,random.Random(rng_seed)),
    ]
    return [(m.name,*_train(m,config,train,tests)) for m in models]
