from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class PredictiveRepresentationConfig:
    seed: int = 0
    features_a: int = 24
    samples_a: int = 6000
    train_a: int = 3500
    features_b: int = 16
    episodes_b: int = 400
    episode_len_b: int = 15
    train_b: int = 4000
    coarse_width: int = 4
    dense_width: int = 10
    hot_state_cost: float = 0.003
    cold_source_cost: float = 0.0005


POLICIES = (
    "raw_reconstruction",
    "task_sufficient",
    "coarse_latent_target",
    "dense_latent_target",
    "latent_recoverable_source",
)


def _mutual_information(xs: list[int], ys: list[int]) -> float:
    n = len(xs)
    x_counts = Counter(xs)
    y_counts = Counter(ys)
    joint = Counter(zip(xs, ys))
    result = 0.0
    for (x_value, y_value), count in joint.items():
        p_xy = count / n
        p_x = x_counts[x_value] / n
        p_y = y_counts[y_value] / n
        result += p_xy * math.log2(p_xy / (p_x * p_y))
    return result


def _fit_single_feature_predictor(
    rows: list[tuple[int, ...]],
    labels: list[int],
    mask: list[int],
) -> tuple[int | None, dict[int, float]]:
    overall = sum(labels) / len(labels)
    if not mask:
        return None, {0: overall, 1: overall}

    best_feature = max(
        mask,
        key=lambda feature: _mutual_information(
            [row[feature] for row in rows],
            labels,
        ),
    )
    conditional: dict[int, float] = {}
    for value in (0, 1):
        matching = [
            label
            for row, label in zip(rows, labels)
            if row[best_feature] == value
        ]
        conditional[value] = sum(matching) / len(matching) if matching else overall
    return best_feature, conditional


def _predict(
    model: tuple[int | None, dict[int, float]],
    rows: list[tuple[int, ...]],
) -> list[int]:
    feature, conditional = model
    if feature is None:
        prediction = int(conditional[0] >= 0.5)
        return [prediction] * len(rows)
    return [int(conditional[row[feature]] >= 0.5) for row in rows]


def _balanced_accuracy(labels: list[int], predictions: list[int]) -> float:
    positives = sum(labels)
    negatives = len(labels) - positives
    true_positive = sum(
        label == 1 and prediction == 1
        for label, prediction in zip(labels, predictions)
    )
    true_negative = sum(
        label == 0 and prediction == 0
        for label, prediction in zip(labels, predictions)
    )
    return 0.5 * (
        true_positive / max(1, positives)
        + true_negative / max(1, negatives)
    )


def _predictive_order(
    rows: list[tuple[int, ...]],
    next_rows: list[tuple[int, ...]],
) -> list[int]:
    width = len(rows[0])
    scores = [
        _mutual_information(
            [row[feature] for row in rows],
            [row[feature] for row in next_rows],
        )
        for feature in range(width)
    ]
    return sorted(range(width), key=lambda feature: scores[feature], reverse=True)


def _task_order(
    rows: list[tuple[int, ...]],
    labels: list[int],
) -> list[int]:
    width = len(rows[0])
    scores = [
        _mutual_information([row[feature] for row in rows], labels)
        for feature in range(width)
    ]
    return sorted(range(width), key=lambda feature: scores[feature], reverse=True)


def _generate_objective_shift_stream(
    config: PredictiveRepresentationConfig,
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    rng = random.Random(config.seed + 10_000)
    current = [rng.randrange(2) for _ in range(config.features_a)]
    rows: list[tuple[int, ...]] = []
    next_rows: list[tuple[int, ...]] = []

    for _ in range(config.samples_a):
        next_state: list[int] = []
        for feature, value in enumerate(current):
            if feature < 4:
                probability_one = 0.96 if value else 0.04
            elif feature < 8:
                probability_one = 0.82 if value else 0.18
            elif feature == 8:
                # Lower-frequency but still predictive future-relevant state.
                probability_one = 0.75 if value else 0.05
            elif feature == 9:
                probability_one = 0.68 if value else 0.32
            else:
                probability_one = 0.50
            next_state.append(int(rng.random() < probability_one))

        rows.append(tuple(current))
        next_rows.append(tuple(next_state))
        current = next_state

    return rows, next_rows


def _objective_shift_masks(
    config: PredictiveRepresentationConfig,
    train_rows: list[tuple[int, ...]],
    train_next: list[tuple[int, ...]],
) -> dict[str, tuple[list[int], list[int], int]]:
    predictive = _predictive_order(train_rows, train_next)
    initial_labels = [row[0] for row in train_next]
    initial_task = _task_order(train_rows, initial_labels)[: config.coarse_width]
    future_labels = [row[8] for row in train_next]
    future_feature = _task_order(train_rows, future_labels)[0]
    coarse = predictive[: config.coarse_width]
    dense = predictive[: config.dense_width]

    source_future = list(dict.fromkeys(coarse + [future_feature]))
    return {
        "raw_reconstruction": (
            list(range(config.features_a)),
            list(range(config.features_a)),
            0,
        ),
        "task_sufficient": (initial_task, initial_task, 0),
        "coarse_latent_target": (coarse, coarse, 0),
        "dense_latent_target": (dense, dense, 0),
        # Cold source lets the system re-score the historical raw transition pairs
        # once the new prediction target is named, then materialize only the newly
        # relevant feature into hot state.
        "latent_recoverable_source": (coarse, source_future, config.features_a),
    }


def run_objective_shift_representation(
    config: PredictiveRepresentationConfig,
    policy: str,
) -> dict[str, float | int]:
    if policy not in POLICIES:
        raise ValueError(f"unknown policy: {policy}")

    rows, next_rows = _generate_objective_shift_stream(config)
    train_rows = rows[: config.train_a]
    train_next = next_rows[: config.train_a]
    eval_rows = rows[config.train_a :]
    eval_next = next_rows[config.train_a :]
    initial_mask, future_mask, cold_width = _objective_shift_masks(
        config,
        train_rows,
        train_next,
    )[policy]

    initial_train_labels = [row[0] for row in train_next]
    initial_eval_labels = [row[0] for row in eval_next]
    future_train_labels = [row[8] for row in train_next]
    future_eval_labels = [row[8] for row in eval_next]

    initial_model = _fit_single_feature_predictor(
        train_rows,
        initial_train_labels,
        initial_mask,
    )
    future_model = _fit_single_feature_predictor(
        train_rows,
        future_train_labels,
        future_mask,
    )
    initial_accuracy = _balanced_accuracy(
        initial_eval_labels,
        _predict(initial_model, eval_rows),
    )
    future_accuracy = _balanced_accuracy(
        future_eval_labels,
        _predict(future_model, eval_rows),
    )

    cold_cost = cold_width * config.cold_source_cost
    initial_net = (
        initial_accuracy
        - len(initial_mask) * config.hot_state_cost
        - cold_cost
    )
    future_net = (
        future_accuracy
        - len(future_mask) * config.hot_state_cost
        - cold_cost
    )
    return {
        "initial_balanced_accuracy": initial_accuracy,
        "future_balanced_accuracy": future_accuracy,
        "initial_net_utility": initial_net,
        "future_net_utility": future_net,
        "lifetime_net_utility": 0.5 * (initial_net + future_net),
        "initial_hot_width": len(initial_mask),
        "future_hot_width": len(future_mask),
        "cold_source_width": cold_width,
    }


def _generate_intervention_stream(
    config: PredictiveRepresentationConfig,
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], list[int]]:
    rng = random.Random(config.seed + 20_000)
    rows: list[tuple[int, ...]] = []
    next_rows: list[tuple[int, ...]] = []
    mechanisms: list[int] = []

    for _ in range(config.episodes_b):
        mechanism = rng.randrange(2)
        current = [rng.randrange(2) for _ in range(config.features_b)]
        for _ in range(config.episode_len_b):
            # Feature 8 is a noisy observable cue of the hidden mechanism. It is
            # not needed by the passive target, but it becomes action-relevant.
            current[8] = mechanism if rng.random() < 0.90 else 1 - mechanism
            next_state: list[int] = []
            for feature, value in enumerate(current):
                if feature < 4:
                    probability_one = 0.95 if value else 0.05
                elif feature < 8:
                    probability_one = 0.80 if value else 0.20
                elif feature == 8:
                    probability_one = 0.90 if mechanism else 0.10
                else:
                    probability_one = 0.50
                next_state.append(int(rng.random() < probability_one))

            rows.append(tuple(current))
            next_rows.append(tuple(next_state))
            mechanisms.append(mechanism)
            current = next_state

    return rows, next_rows, mechanisms


def _intervention_masks(
    config: PredictiveRepresentationConfig,
    train_rows: list[tuple[int, ...]],
    train_next: list[tuple[int, ...]],
    intervention_labels: list[int],
) -> dict[str, tuple[list[int], list[int], int]]:
    predictive = _predictive_order(train_rows, train_next)
    passive_labels = [row[0] for row in train_next]
    task_mask = _task_order(train_rows, passive_labels)[: config.coarse_width]
    coarse = predictive[: config.coarse_width]
    dense = predictive[: min(config.dense_width, config.features_b)]
    intervention_feature = _task_order(train_rows, intervention_labels)[0]
    source_future = list(dict.fromkeys(coarse + [intervention_feature]))

    return {
        "raw_reconstruction": (
            list(range(config.features_b)),
            list(range(config.features_b)),
            0,
        ),
        "task_sufficient": (task_mask, task_mask, 0),
        "coarse_latent_target": (coarse, coarse, 0),
        "dense_latent_target": (dense, dense, 0),
        "latent_recoverable_source": (coarse, source_future, config.features_b),
    }


def run_intervention_representation(
    config: PredictiveRepresentationConfig,
    policy: str,
) -> dict[str, float | int]:
    if policy not in POLICIES:
        raise ValueError(f"unknown policy: {policy}")

    rows, next_rows, mechanisms = _generate_intervention_stream(config)
    train_rows = rows[: config.train_b]
    train_next = next_rows[: config.train_b]
    train_mechanisms = mechanisms[: config.train_b]
    eval_rows = rows[config.train_b :]
    eval_next = next_rows[config.train_b :]
    eval_mechanisms = mechanisms[config.train_b :]

    passive_mask, intervention_mask, cold_width = _intervention_masks(
        config,
        train_rows,
        train_next,
        train_mechanisms,
    )[policy]

    passive_train_labels = [row[0] for row in train_next]
    passive_eval_labels = [row[0] for row in eval_next]
    passive_model = _fit_single_feature_predictor(
        train_rows,
        passive_train_labels,
        passive_mask,
    )
    intervention_model = _fit_single_feature_predictor(
        train_rows,
        train_mechanisms,
        intervention_mask,
    )

    passive_accuracy = _balanced_accuracy(
        passive_eval_labels,
        _predict(passive_model, eval_rows),
    )
    intervention_accuracy = _balanced_accuracy(
        eval_mechanisms,
        _predict(intervention_model, eval_rows),
    )

    cold_cost = cold_width * config.cold_source_cost
    passive_net = (
        passive_accuracy
        - len(passive_mask) * config.hot_state_cost
        - cold_cost
    )
    intervention_net = (
        intervention_accuracy
        - len(intervention_mask) * config.hot_state_cost
        - cold_cost
    )
    return {
        "passive_balanced_accuracy": passive_accuracy,
        "intervention_balanced_accuracy": intervention_accuracy,
        "passive_net_utility": passive_net,
        "intervention_net_utility": intervention_net,
        "lifetime_net_utility": 0.5 * (passive_net + intervention_net),
        "passive_hot_width": len(passive_mask),
        "intervention_hot_width": len(intervention_mask),
        "cold_source_width": cold_width,
    }


def run_predictive_representation_experiment(
    config: PredictiveRepresentationConfig,
) -> dict[str, list[tuple[str, dict[str, float | int]]]]:
    return {
        "objective_shift": [
            (policy, run_objective_shift_representation(config, policy))
            for policy in POLICIES
        ],
        "passive_vs_intervention": [
            (policy, run_intervention_representation(config, policy))
            for policy in POLICIES
        ],
    }
