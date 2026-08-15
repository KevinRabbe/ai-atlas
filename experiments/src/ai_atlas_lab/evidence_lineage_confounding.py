from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random

from .evidence_lineage_inference import (
    _components,
    _majority_error_estimate,
    _penalties,
)


@dataclass(frozen=True)
class I25Config:
    seed: int = 0
    tasks: int = 10_000
    shift_task: int = 5_000
    hard_probability: float = 0.30
    difficulty_proxy_accuracy: float = 0.82
    passive_resolution: float = 0.12
    audit_error: float = 0.02
    audit_cost: float = 0.20
    audit_unavailable: float = 0.08
    probe_cost: float = 0.08
    probe_ttl: int = 500
    decay: float = 0.996
    covariance_threshold: float = 0.025


def _lineage_map(regime: int) -> tuple[int, ...]:
    return (
        (0, 0, 1, 1, 2, 2, 3, 3)
        if regime == 0
        else (0, 1, 1, 2, 2, 3, 3, 0)
    )


def _error_parameters(hard: bool) -> tuple[float, float]:
    # Hard tasks raise error rates across all evaluators, creating a global
    # common cause that can mimic shared ancestry in raw co-failure statistics.
    return (0.06, 0.01) if not hard else (0.10, 0.32)


class DifficultyConditionedLineageEstimator:
    """Estimate hidden failure ancestry while conditioning on task difficulty.

    The raw estimator has one error/co-error model for all tasks. The
    conditioned estimator keeps separate statistics for an observable noisy
    difficulty bucket and averages residual covariance across those contexts.
    This tests whether broad task difficulty was creating spurious lineage.
    """

    def __init__(
        self,
        config: I25Config,
        *,
        conditional: bool,
        sources: int = 8,
    ) -> None:
        self.config = config
        self.conditional = conditional
        self.sources = sources
        buckets = 2 if conditional else 1
        self.error_rate = [[0.12] * sources for _ in range(buckets)]
        self.joint_error = [
            {
                (left, right): 0.0144
                for left in range(sources)
                for right in range(left + 1, sources)
            }
            for _ in range(buckets)
        ]
        self.probe_cache: dict[tuple[int, int], tuple[bool, int]] = {}

    def observe_resolution(
        self,
        labels: tuple[bool, ...],
        truth: bool,
        *,
        difficulty_proxy: bool,
    ) -> None:
        bucket = int(difficulty_proxy) if self.conditional else 0
        decay = self.config.decay
        errors = [int(label != truth) for label in labels]
        for source, error in enumerate(errors):
            self.error_rate[bucket][source] = (
                decay * self.error_rate[bucket][source]
                + (1.0 - decay) * error
            )
        for left in range(self.sources):
            for right in range(left + 1, self.sources):
                key = (left, right)
                joint = errors[left] * errors[right]
                self.joint_error[bucket][key] = (
                    decay * self.joint_error[bucket][key]
                    + (1.0 - decay) * joint
                )

    def covariance(self, left: int, right: int) -> float:
        if left > right:
            left, right = right, left
        residuals = [
            self.joint_error[bucket][(left, right)]
            - self.error_rate[bucket][left] * self.error_rate[bucket][right]
            for bucket in range(len(self.error_rate))
        ]
        return sum(residuals) / len(residuals)

    def same_lineage(self, left: int, right: int, *, step: int) -> bool:
        if left == right:
            return True
        if left > right:
            left, right = right, left
        cached = self.probe_cache.get((left, right))
        if cached is not None and cached[1] >= step:
            return cached[0]
        return self.covariance(left, right) > self.config.covariance_threshold

    def relation_confidence(self, left: int, right: int) -> float:
        return min(
            1.0,
            abs(
                self.covariance(left, right)
                - self.config.covariance_threshold
            )
            / 0.03,
        )

    def remember_probe(
        self,
        left: int,
        right: int,
        *,
        same_lineage: bool,
        step: int,
    ) -> None:
        if left > right:
            left, right = right, left
        self.probe_cache[(left, right)] = (
            same_lineage,
            step + self.config.probe_ttl,
        )

    def marginal_error(
        self,
        panel: tuple[int, ...],
        *,
        difficulty_proxy: bool,
    ) -> float:
        bucket = int(difficulty_proxy) if self.conditional else 0
        return sum(
            self.error_rate[bucket][source] for source in panel
        ) / len(panel)


def run_i25(config: I25Config, policy: str) -> dict[str, float]:
    valid = {"raw_cofailure", "difficulty_conditioned", "conditioned_probe", "oracle"}
    if policy not in valid:
        raise ValueError(f"unknown I25 policy: {policy}")

    rng = random.Random(config.seed)
    raw = DifficultyConditionedLineageEstimator(config, conditional=False)
    conditioned = DifficultyConditionedLineageEstimator(config, conditional=True)
    estimator = raw if policy == "raw_cofailure" else conditioned
    metrics: dict[str, float] = defaultdict(float)
    pair_accuracy_sum = [0.0, 0.0, 0.0]
    pair_accuracy_count = [0, 0, 0]

    for task in range(config.tasks):
        regime = int(task >= config.shift_task)
        hidden_lineage = _lineage_map(regime)
        truth = rng.random() < 0.5
        hard = rng.random() < config.hard_probability
        difficulty_proxy = (
            hard
            if rng.random() < config.difficulty_proxy_accuracy
            else not hard
        )
        family = "external" if rng.random() < 0.5 else "metacognitive"
        consequence = rng.choice((1.0, 2.0, 4.0, 8.0))

        shared_error, individual_error = _error_parameters(hard)
        shared_failure = {
            lineage: rng.random() < shared_error
            for lineage in set(hidden_lineage)
        }
        labels_list: list[bool] = []
        for source, lineage in enumerate(hidden_lineage):
            label = truth
            if shared_failure[lineage]:
                label = not label
            if rng.random() < individual_error:
                label = not label
            labels_list.append(label)
        labels = tuple(labels_list)

        panel = tuple(rng.sample(range(8), 3))
        majority = sum(labels[source] for source in panel) >= 2

        correct_pairs = sum(
            estimator.same_lineage(left, right, step=task)
            == (hidden_lineage[left] == hidden_lineage[right])
            for left in range(8)
            for right in range(left + 1, 8)
        )
        segment = (
            0
            if task < config.shift_task
            else 1
            if task < config.shift_task + 800
            else 2
        )
        pair_accuracy_sum[segment] += correct_pairs / 28.0
        pair_accuracy_count[segment] += 1

        if policy == "oracle":
            components = _components(
                panel,
                lambda left, right: (
                    hidden_lineage[left] == hidden_lineage[right]
                ),
            )
        else:
            components = _components(
                panel,
                lambda left, right: estimator.same_lineage(
                    left,
                    right,
                    step=task,
                ),
            )

        marginal_error = estimator.marginal_error(
            panel,
            difficulty_proxy=difficulty_proxy,
        )
        current_error = _majority_error_estimate(
            panel,
            labels,
            components,
            marginal_error,
        )
        false_positive, false_negative, unresolved_penalty = _penalties(family)
        wrong_penalty = false_positive if majority else false_negative
        average_wrong_penalty = (false_positive + false_negative) / 2.0
        current_harm = current_error * wrong_penalty * consequence
        audit_harm = (
            config.audit_error * average_wrong_penalty * consequence
            + config.audit_cost
        )

        if policy == "conditioned_probe":
            majority_sources = [
                source for source in panel if labels[source] == majority
            ]
            left, right = majority_sources[:2]
            confidence = estimator.relation_confidence(left, right)

            def forced_components(force_same: bool) -> dict[int, int]:
                def relation(source_a: int, source_b: int) -> bool:
                    if {source_a, source_b} == {left, right}:
                        return force_same
                    return estimator.same_lineage(
                        source_a,
                        source_b,
                        step=task,
                    )

                return _components(panel, relation)

            error_if_same = _majority_error_estimate(
                panel,
                labels,
                forced_components(True),
                marginal_error,
            )
            error_if_different = _majority_error_estimate(
                panel,
                labels,
                forced_components(False),
                marginal_error,
            )
            audit_if_same = audit_harm < (
                error_if_same * wrong_penalty * consequence
            )
            audit_if_different = audit_harm < (
                error_if_different * wrong_penalty * consequence
            )
            if audit_if_same != audit_if_different:
                probe_value = (
                    (1.0 - confidence)
                    * abs(error_if_same - error_if_different)
                    * wrong_penalty
                    * consequence
                )
                if probe_value > config.probe_cost:
                    estimator.remember_probe(
                        left,
                        right,
                        same_lineage=(
                            hidden_lineage[left] == hidden_lineage[right]
                        ),
                        step=task,
                    )
                    metrics["dependency_probes"] += 1.0
                    metrics["utility"] -= config.probe_cost
                    components = _components(
                        panel,
                        lambda source_a, source_b: estimator.same_lineage(
                            source_a,
                            source_b,
                            step=task,
                        ),
                    )
                    current_error = _majority_error_estimate(
                        panel,
                        labels,
                        components,
                        marginal_error,
                    )
                    current_harm = (
                        current_error * wrong_penalty * consequence
                    )

        decision: bool | None = majority
        if audit_harm < current_harm:
            metrics["independent_audits"] += 1.0
            metrics["utility"] -= config.audit_cost
            if rng.random() < config.audit_unavailable:
                if unresolved_penalty * consequence < current_harm:
                    decision = None
            else:
                decision = (
                    not truth if rng.random() < config.audit_error else truth
                )

        if decision is None:
            harm = unresolved_penalty * consequence
            metrics["unresolved"] += 1.0
        elif decision == truth:
            harm = 0.0
        elif decision:
            harm = false_positive * consequence
            metrics["false_positive"] += 1.0
        else:
            harm = false_negative * consequence
            metrics["false_negative"] += 1.0

        metrics["weighted_harm"] += harm
        metrics["utility"] += 1.2 * consequence - harm

        if rng.random() < config.passive_resolution:
            raw.observe_resolution(
                labels,
                truth,
                difficulty_proxy=difficulty_proxy,
            )
            conditioned.observe_resolution(
                labels,
                truth,
                difficulty_proxy=difficulty_proxy,
            )
            metrics["passive_resolutions"] += 1.0

    result = {
        key: value / config.tasks for key, value in metrics.items()
    }
    result["pair_accuracy_pre_shift"] = (
        pair_accuracy_sum[0] / pair_accuracy_count[0]
    )
    result["pair_accuracy_early_post_shift"] = (
        pair_accuracy_sum[1] / pair_accuracy_count[1]
    )
    result["pair_accuracy_late_post_shift"] = (
        pair_accuracy_sum[2] / pair_accuracy_count[2]
    )
    return result
