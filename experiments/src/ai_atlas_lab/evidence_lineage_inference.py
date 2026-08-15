from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
import random
from typing import Callable


@dataclass(frozen=True)
class I24Config:
    seed: int = 0
    tasks: int = 12_000
    shift_task: int = 6_000
    shared_error: float = 0.13
    individual_error: float = 0.025
    passive_resolution: float = 0.10
    audit_error: float = 0.02
    audit_unavailable: float = 0.08
    audit_cost: float = 0.18
    probe_cost: float = 0.05
    probe_ttl: int = 500
    decay: float = 0.995
    covariance_threshold: float = 0.025


def _lineage_map(regime: int) -> tuple[int, ...]:
    # Hidden upstream relationships change without changing source identities.
    return (0, 0, 1, 1, 2, 2) if regime == 0 else (0, 1, 1, 2, 2, 0)


def _penalties(family: str) -> tuple[float, float, float]:
    if family == "external":
        return 1.5, 4.0, 0.65
    if family == "metacognitive":
        return 6.0, 1.2, 0.80
    raise ValueError(f"unknown claim family: {family}")


class HiddenLineageEstimator:
    """Infer shared failure ancestry from independently resolved outcomes.

    The estimator is intentionally simple: it tracks exponentially decayed
    source error rates and pairwise co-error rates. Positive excess co-error is
    treated as evidence that two visible sources share a hidden failure lineage.
    A bounded explicit probe can temporarily override that inference.
    """

    def __init__(self, config: I24Config, sources: int = 6) -> None:
        self.config = config
        self.sources = sources
        self.error_rate = [0.12] * sources
        self.joint_error = {
            (left, right): 0.0144
            for left in range(sources)
            for right in range(left + 1, sources)
        }
        self.probe_cache: dict[tuple[int, int], tuple[bool, int]] = {}

    def observe_resolution(self, labels: tuple[bool, ...], truth: bool) -> None:
        if len(labels) != self.sources:
            raise ValueError("label count must match source count")
        decay = self.config.decay
        errors = [int(label != truth) for label in labels]
        for source, error in enumerate(errors):
            self.error_rate[source] = (
                decay * self.error_rate[source] + (1.0 - decay) * error
            )
        for left in range(self.sources):
            for right in range(left + 1, self.sources):
                key = (left, right)
                joint = errors[left] * errors[right]
                self.joint_error[key] = (
                    decay * self.joint_error[key] + (1.0 - decay) * joint
                )

    def covariance(self, left: int, right: int) -> float:
        if left == right:
            return self.error_rate[left] * (1.0 - self.error_rate[left])
        if left > right:
            left, right = right, left
        return (
            self.joint_error[(left, right)]
            - self.error_rate[left] * self.error_rate[right]
        )

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
        distance = abs(
            self.covariance(left, right) - self.config.covariance_threshold
        )
        return min(1.0, distance / 0.035)

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


def _components(
    panel: tuple[int, ...],
    same_lineage: Callable[[int, int], bool],
) -> dict[int, int]:
    parent = {source: source for source in panel}

    def find(source: int) -> int:
        while parent[source] != source:
            parent[source] = parent[parent[source]]
            source = parent[source]
        return source

    def union(left: int, right: int) -> None:
        left_root = find(left)
        right_root = find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    for index, left in enumerate(panel):
        for right in panel[index + 1 :]:
            if same_lineage(left, right):
                union(left, right)
    return {source: find(source) for source in panel}


def _majority_error_estimate(
    panel: tuple[int, ...],
    labels: tuple[bool, ...],
    components: dict[int, int],
    marginal_error: float,
) -> float:
    """Estimate vote error from effective independent lineage structure.

    For unanimous votes, k independent latent lineages agreeing is stronger than
    k copied records. For a split vote where the majority pair shares one hidden
    lineage and the minority is independent, the apparent 2:1 vote is really a
    one-lineage-versus-one-lineage disagreement and remains highly ambiguous.
    """

    error = min(0.45, max(0.03, marginal_error))
    majority = sum(labels[source] for source in panel) >= 2
    unanimous = len({labels[source] for source in panel}) == 1
    independent_lineages = len(set(components.values()))

    if unanimous:
        wrong = error**independent_lineages
        right = (1.0 - error) ** independent_lineages
        return wrong / (wrong + right)

    majority_sources = [
        source for source in panel if labels[source] == majority
    ]
    if independent_lineages == 1:
        return error
    if components[majority_sources[0]] == components[majority_sources[1]]:
        return 0.50
    return error


def run_i24(config: I24Config, policy: str) -> dict[str, float]:
    valid = {
        "record_count",
        "all_correlated",
        "learned",
        "learned_probe",
        "oracle",
    }
    if policy not in valid:
        raise ValueError(f"unknown I24 policy: {policy}")

    rng = random.Random(config.seed)
    estimator = HiddenLineageEstimator(config)
    metrics: dict[str, float] = defaultdict(float)
    pair_accuracy_sum = [0.0, 0.0, 0.0]
    pair_accuracy_count = [0, 0, 0]

    for task in range(config.tasks):
        regime = int(task >= config.shift_task)
        hidden_lineage = _lineage_map(regime)
        truth = rng.random() < 0.5
        family = "external" if rng.random() < 0.5 else "metacognitive"
        consequence = rng.choice((1.0, 2.0, 4.0, 8.0))

        shared_failure = {
            lineage: rng.random() < config.shared_error
            for lineage in set(hidden_lineage)
        }
        labels_list: list[bool] = []
        for source, lineage in enumerate(hidden_lineage):
            label = truth
            if shared_failure[lineage]:
                label = not label
            if rng.random() < config.individual_error:
                label = not label
            labels_list.append(label)
        labels = tuple(labels_list)

        panel = tuple(rng.sample(range(6), 3))
        majority = sum(labels[source] for source in panel) >= 2

        correct_pairs = sum(
            estimator.same_lineage(left, right, step=task)
            == (hidden_lineage[left] == hidden_lineage[right])
            for left in range(6)
            for right in range(left + 1, 6)
        )
        segment = (
            0
            if task < config.shift_task
            else 1
            if task < config.shift_task + 800
            else 2
        )
        pair_accuracy_sum[segment] += correct_pairs / 15.0
        pair_accuracy_count[segment] += 1

        if policy == "oracle":
            components = _components(
                panel,
                lambda left, right: (
                    hidden_lineage[left] == hidden_lineage[right]
                ),
            )
        elif policy == "all_correlated":
            components = {source: 0 for source in panel}
        elif policy == "record_count":
            components = {source: source for source in panel}
        else:
            components = _components(
                panel,
                lambda left, right: estimator.same_lineage(
                    left,
                    right,
                    step=task,
                ),
            )

        marginal_error = sum(
            estimator.error_rate[source] for source in panel
        ) / len(panel)
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

        if policy == "learned_probe":
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
                    metrics["lineage_probes"] += 1.0
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

        query_audit = audit_harm < current_harm
        decision: bool | None = majority
        if query_audit:
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

        # Passive independent outcome resolution is the learning signal. The
        # hidden lineage map itself is never exposed through this path.
        if rng.random() < config.passive_resolution:
            estimator.observe_resolution(labels, truth)
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
