from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class RoutedConfig:
    seed: int = 0
    raw_bits: int = 6
    task_count: int = 3
    sharedness: float = 0.75
    train_examples: int = 480
    test_examples_per_task: int = 400
    primary_task_fraction: float = 0.80
    learning_rate: float = 0.035
    exploration_rate: float = 0.10
    loss_ema: float = 0.08

    @property
    def feature_dim(self) -> int:
        return self.raw_bits * (self.raw_bits - 1) // 2

    @property
    def private_width(self) -> int:
        numerator = self.feature_dim * (self.task_count - 1)
        if numerator % self.task_count:
            raise ValueError("feature/task dimensions do not permit exact parameter matching")
        return numerator // self.task_count


def _pairs(raw: tuple[int, ...]) -> tuple[float, ...]:
    return tuple(float(raw[i] * raw[j]) for i in range(len(raw)) for j in range(i + 1, len(raw)))


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


def _loss(label: int, score: float) -> float:
    z = label * score
    if z > 35:
        return math.exp(-z)
    if z < -35:
        return -z
    return math.log1p(math.exp(-z))


@dataclass(frozen=True)
class Example:
    task_id: int
    features: tuple[float, ...]
    label: int


def _true_weights(config: RoutedConfig) -> tuple[tuple[float, ...], ...]:
    rng = random.Random(config.seed + 3301)
    shared = _unit([rng.gauss(0, 1) for _ in range(config.feature_dim)])
    rho = min(1.0, max(0.0, config.sharedness))
    rows = []
    for _ in range(config.task_count):
        independent = _unit([rng.gauss(0, 1) for _ in range(config.feature_dim)])
        rows.append(tuple(_unit([rho * a + (1.0 - rho) * b for a, b in zip(shared, independent)])))
    return tuple(rows)


def _examples(
    config: RoutedConfig,
    *,
    seed: int,
    count: int,
    task_id: int | None = None,
) -> tuple[Example, ...]:
    rng = random.Random(seed)
    weights = _true_weights(config)
    out: list[Example] = []
    for _ in range(count):
        if task_id is not None:
            tid = task_id
        elif rng.random() < config.primary_task_fraction:
            tid = 0
        else:
            tid = 1 + rng.randrange(config.task_count - 1)
        raw = tuple(1 if rng.random() < 0.5 else -1 for _ in range(config.raw_bits))
        feats = _pairs(raw)
        margin = sum(w * x for w, x in zip(weights[tid], feats))
        out.append(Example(tid, feats, 1 if margin >= 0 else -1))
    return tuple(out)


class Specialists:
    def __init__(self, config: RoutedConfig, rng: random.Random):
        self.config = config
        self.weights = [
            [rng.uniform(-0.02, 0.02) for _ in range(config.feature_dim)]
            for _ in range(config.task_count)
        ]
        self.operations = 0

    @property
    def parameter_count(self) -> int:
        return self.config.feature_dim * self.config.task_count

    def score(self, task_id: int, features: tuple[float, ...]) -> float:
        self.operations += 2 * self.config.feature_dim
        return sum(w * x for w, x in zip(self.weights[task_id], features))

    def update(self, example: Example) -> None:
        score = self.score(example.task_id, example.features)
        g = _grad(example.label, score)
        row = self.weights[example.task_id]
        for i, x in enumerate(example.features):
            row[i] -= self.config.learning_rate * g * x
            self.operations += 3

    def predict(self, example: Example) -> int:
        return 1 if self.score(example.task_id, example.features) >= 0 else -1


class RoutedSharedPrivate:
    def __init__(self, config: RoutedConfig, rng: random.Random):
        self.config = config
        self.shared = [rng.uniform(-0.02, 0.02) for _ in range(config.feature_dim)]
        self.private = [
            [rng.uniform(-0.02, 0.02) for _ in range(config.private_width)]
            for _ in range(config.task_count)
        ]
        self.private_masks = []
        for task in range(config.task_count):
            start = (task * (config.feature_dim // config.task_count)) % config.feature_dim
            self.private_masks.append(
                tuple((start + offset) % config.feature_dim for offset in range(config.private_width))
            )
        self.shared_loss = [0.693] * config.task_count
        self.private_loss = [0.693] * config.task_count
        self.route_counts = {"shared": 0, "private": 0}
        self.operations = 0
        self.rng = rng

    @property
    def parameter_count(self) -> int:
        return self.config.feature_dim + self.config.task_count * self.config.private_width

    def _shared_score(self, features: tuple[float, ...]) -> float:
        self.operations += 2 * self.config.feature_dim
        return sum(w * x for w, x in zip(self.shared, features))

    def _private_score(self, task_id: int, features: tuple[float, ...]) -> float:
        mask = self.private_masks[task_id]
        self.operations += 2 * self.config.private_width
        return sum(w * features[idx] for w, idx in zip(self.private[task_id], mask))

    def _route(self, task_id: int, *, explore: bool) -> str:
        if explore and self.rng.random() < self.config.exploration_rate:
            return "shared" if self.rng.random() < 0.5 else "private"
        return "shared" if self.shared_loss[task_id] <= self.private_loss[task_id] else "private"

    def update(self, example: Example) -> None:
        route = self._route(example.task_id, explore=True)
        alpha = self.config.loss_ema
        if route == "shared":
            score = self._shared_score(example.features)
            g = _grad(example.label, score)
            for i, x in enumerate(example.features):
                self.shared[i] -= self.config.learning_rate * g * x
                self.operations += 3
            self.shared_loss[example.task_id] = (
                (1.0 - alpha) * self.shared_loss[example.task_id]
                + alpha * _loss(example.label, score)
            )
        else:
            score = self._private_score(example.task_id, example.features)
            g = _grad(example.label, score)
            row = self.private[example.task_id]
            for r, feature_idx in enumerate(self.private_masks[example.task_id]):
                row[r] -= self.config.learning_rate * g * example.features[feature_idx]
                self.operations += 3
            self.private_loss[example.task_id] = (
                (1.0 - alpha) * self.private_loss[example.task_id]
                + alpha * _loss(example.label, score)
            )
        self.route_counts[route] += 1

    def predict(self, example: Example) -> int:
        route = self._route(example.task_id, explore=False)
        score = (
            self._shared_score(example.features)
            if route == "shared"
            else self._private_score(example.task_id, example.features)
        )
        return 1 if score >= 0 else -1


def _evaluate(model, tests: tuple[tuple[Example, ...], ...]) -> tuple[float, tuple[float, ...]]:
    per = []
    for examples in tests:
        good = sum(int(model.predict(ex) == ex.label) for ex in examples)
        per.append(good / len(examples))
    return sum(per) / len(per), tuple(per)


def _train(
    model,
    train: tuple[Example, ...],
    tests: tuple[tuple[Example, ...], ...],
) -> dict[str, float | int]:
    start_ops = model.operations
    for ex in train:
        model.update(ex)
    train_ops = model.operations - start_ops
    before_eval = model.operations
    avg, per = _evaluate(model, tests)
    eval_ops = model.operations - before_eval
    metrics: dict[str, float | int] = {
        "accuracy": avg,
        "parameter_count": model.parameter_count,
        "operations_per_train_example": train_ops / len(train),
        "operations_per_test_example": eval_ops / sum(len(x) for x in tests),
    }
    if isinstance(model, RoutedSharedPrivate):
        total = model.route_counts["shared"] + model.route_counts["private"]
        metrics["shared_train_route_rate"] = (
            model.route_counts["shared"] / total if total else 0.0
        )
        for task in range(model.config.task_count):
            metrics[f"task_{task}_route_shared"] = int(
                model.shared_loss[task] <= model.private_loss[task]
            )
    for i, acc in enumerate(per):
        metrics[f"accuracy_task_{i}"] = acc
    return metrics


def run_routed_integration_experiment(
    config: RoutedConfig,
) -> list[tuple[str, dict[str, float | int]]]:
    train = _examples(config, seed=config.seed + 17, count=config.train_examples)
    tests = tuple(
        _examples(
            config,
            seed=config.seed + 900 + task,
            count=config.test_examples_per_task,
            task_id=task,
        )
        for task in range(config.task_count)
    )
    rng_seed = config.seed + 77
    models = [
        Specialists(config, random.Random(rng_seed)),
        RoutedSharedPrivate(config, random.Random(rng_seed)),
    ]
    return [(model.__class__.__name__, _train(model, train, tests)) for model in models]
