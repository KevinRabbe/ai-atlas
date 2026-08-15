from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random

from .evidence_dependence import EvidenceDependenceModel


@dataclass(frozen=True)
class I26AConfig:
    seed: int = 0
    tasks: int = 12_000
    passive_resolution: float = 0.10
    shared_error: float = 0.13
    individual_error: float = 0.025
    audit_error: float = 0.02
    audit_cost: float = 0.18
    audit_unavailable: float = 0.08
    probe_cost: float = 0.06
    probe_ttl: int = 500
    decay: float = 0.995
    covariance_threshold: float = 0.025


def _hidden_lineage(domain: str) -> tuple[int, ...]:
    if domain == "external":
        return (0, 0, 1, 1, 2, 2)
    if domain == "metacognitive":
        return (0, 1, 0, 2, 1, 2)
    raise ValueError(f"unknown domain: {domain}")


def _penalties(domain: str) -> tuple[float, float, float]:
    if domain == "external":
        return 1.5, 4.0, 0.65
    if domain == "metacognitive":
        return 6.0, 1.2, 0.80
    raise ValueError(f"unknown domain: {domain}")


def _majority_error(
    panel: tuple[str, ...],
    labels: dict[str, bool],
    components: dict[str, str],
    marginal_error: float,
) -> float:
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


def _model(config: I26AConfig) -> EvidenceDependenceModel:
    model = EvidenceDependenceModel(
        decay=config.decay,
        covariance_threshold=config.covariance_threshold,
        confidence_scale=0.035,
    )
    for source in range(6):
        model.register_source(f"s{source}")
    return model


def _marginal_error(
    model: EvidenceDependenceModel,
    panel: tuple[str, ...],
    context_key: str,
) -> float:
    if context_key not in model.error_rate:
        return model.prior_error
    return sum(
        model.error_rate[context_key][source] for source in panel
    ) / len(panel)


def _oracle_components(
    panel: tuple[str, ...],
    lineage: tuple[int, ...],
) -> dict[str, str]:
    return {
        source: f"lineage:{lineage[int(source[1:])]}"
        for source in panel
    }


def run_i26a(config: I26AConfig, policy: str) -> dict[str, float]:
    valid = {"global", "domain", "domain_probe", "oracle"}
    if policy not in valid:
        raise ValueError(f"unknown I26A policy: {policy}")

    rng = random.Random(config.seed)
    global_model = _model(config)
    domain_model = _model(config)
    metrics: dict[str, float] = defaultdict(float)
    pair_accuracy_sum: dict[str, float] = defaultdict(float)
    pair_accuracy_count: dict[str, int] = defaultdict(int)

    for step in range(config.tasks):
        domain = "external" if rng.random() < 0.5 else "metacognitive"
        lineage = _hidden_lineage(domain)
        truth = rng.random() < 0.5
        consequence = rng.choice((1.0, 2.0, 4.0, 8.0))

        shared_failure = {
            group: rng.random() < config.shared_error
            for group in set(lineage)
        }
        labels: dict[str, bool] = {}
        for source_index, group in enumerate(lineage):
            label = truth
            if shared_failure[group]:
                label = not label
            if rng.random() < config.individual_error:
                label = not label
            labels[f"s{source_index}"] = label

        panel = tuple(rng.sample(tuple(labels), 3))
        majority = sum(labels[source] for source in panel) >= 2

        model = global_model if policy == "global" else domain_model
        context_key = None if policy == "global" else domain
        correct_pairs = 0
        pair_count = 0
        for left in range(6):
            for right in range(left + 1, 6):
                inferred = model.estimate(
                    f"s{left}",
                    f"s{right}",
                    step=step,
                    context_key=context_key,
                ).same_failure_lineage
                correct_pairs += int(inferred == (lineage[left] == lineage[right]))
                pair_count += 1
        pair_accuracy_sum[domain] += correct_pairs / pair_count
        pair_accuracy_count[domain] += 1

        if policy == "oracle":
            components = _oracle_components(panel, lineage)
            marginal_error = _marginal_error(domain_model, panel, domain)
        elif policy == "global":
            components = global_model.components(panel, step=step)
            marginal_error = _marginal_error(global_model, panel, "all")
        else:
            components = domain_model.components(
                panel,
                step=step,
                context_key=domain,
            )
            marginal_error = _marginal_error(domain_model, panel, domain)

        current_error = _majority_error(
            panel,
            labels,
            components,
            marginal_error,
        )
        false_positive, false_negative, unresolved_penalty = _penalties(domain)
        wrong_penalty = false_positive if majority else false_negative
        average_wrong_penalty = (false_positive + false_negative) / 2.0
        current_harm = current_error * wrong_penalty * consequence
        audit_harm = (
            config.audit_error * average_wrong_penalty * consequence
            + config.audit_cost
        )

        if policy == "domain_probe":
            majority_sources = [
                source for source in panel if labels[source] == majority
            ]
            left, right = majority_sources[:2]
            estimate = domain_model.estimate(
                left,
                right,
                step=step,
                context_key=domain,
            )

            def forced_components(force_same: bool) -> dict[str, str]:
                base = domain_model.components(
                    panel,
                    step=step,
                    context_key=domain,
                )
                if force_same:
                    target = base[left]
                    old = base[right]
                    return {
                        source: target if component == old else component
                        for source, component in base.items()
                    }
                if base[left] != base[right]:
                    return base
                # Split only the queried right source for the counterfactual.
                split = dict(base)
                split[right] = f"forced:{right}"
                return split

            error_if_same = _majority_error(
                panel,
                labels,
                forced_components(True),
                marginal_error,
            )
            error_if_different = _majority_error(
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
                    (1.0 - estimate.confidence)
                    * abs(error_if_same - error_if_different)
                    * wrong_penalty
                    * consequence
                )
                if probe_value > config.probe_cost:
                    left_index = int(left[1:])
                    right_index = int(right[1:])
                    domain_model.remember_probe(
                        left,
                        right,
                        same_failure_lineage=(
                            lineage[left_index] == lineage[right_index]
                        ),
                        step=step,
                        ttl=config.probe_ttl,
                        context_key=domain,
                    )
                    metrics["domain_probes"] += 1.0
                    metrics["utility"] -= config.probe_cost
                    components = domain_model.components(
                        panel,
                        step=step,
                        context_key=domain,
                    )
                    current_error = _majority_error(
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
        else:
            harm = false_negative * consequence

        metrics["weighted_harm"] += harm
        metrics["utility"] += 1.2 * consequence - harm

        if rng.random() < config.passive_resolution:
            global_model.observe_resolution(
                labels,
                truth,
                context_key="all",
            )
            domain_model.observe_resolution(
                labels,
                truth,
                context_key=domain,
            )
            metrics["passive_resolutions"] += 1.0

    result = {
        key: value / config.tasks for key, value in metrics.items()
    }
    for domain in ("external", "metacognitive"):
        result[f"{domain}_pair_accuracy"] = (
            pair_accuracy_sum[domain] / pair_accuracy_count[domain]
        )
    return result
