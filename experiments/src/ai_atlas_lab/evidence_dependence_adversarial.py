from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random

from .evidence_dependence import EvidenceDependenceModel


@dataclass(frozen=True)
class I26CConfig:
    seed: int = 0
    tasks: int = 12_000
    frontier_probability: float = 0.08
    ordinary_error: float = 0.10
    frontier_shared_error: float = 0.38
    independent_error: float = 0.12
    passive_resolution: float = 0.15
    probe_cost: float = 0.40
    probe_ttl: int = 80
    estimated_frontier_dependency_risk: float = 0.10
    decay: float = 0.995
    covariance_threshold: float = 0.025


def _model(config: I26CConfig) -> EvidenceDependenceModel:
    model = EvidenceDependenceModel(
        decay=config.decay,
        covariance_threshold=config.covariance_threshold,
        confidence_scale=0.035,
    )
    for source in ("B", "C", "D"):
        model.register_source(source)
    return model


def _record_count(labels: dict[str, bool]) -> bool:
    return sum(labels.values()) >= 2


def _collapse_bc(labels: dict[str, bool]) -> bool:
    # B/C count as one shared failure path. D is the other path, so if the
    # lineages disagree D resolves the tie. If B/C disagree, D is also the
    # only source not implicated in their uncertain relation.
    if labels["B"] == labels["C"]:
        return labels["B"] if labels["B"] == labels["D"] else labels["D"]
    return labels["D"]


def run_i26c(config: I26CConfig, policy: str) -> dict[str, float]:
    valid = {
        "record_count",
        "passive_history",
        "always_dependent",
        "stress_probe",
        "oracle",
    }
    if policy not in valid:
        raise ValueError(f"unknown I26C policy: {policy}")

    rng = random.Random(config.seed)
    model = _model(config)
    metrics: dict[str, float] = defaultdict(float)
    probe_valid_until = -1

    for step in range(config.tasks):
        truth = rng.random() < 0.5
        frontier = rng.random() < config.frontier_probability

        if frontier:
            # Adversarial/selective regime: B/C route through one hidden failure
            # mechanism precisely on the consequential frontier where ordinary
            # resolved-history statistics are least informative.
            shared_failure = rng.random() < config.frontier_shared_error
            labels = {
                "B": not truth if shared_failure else truth,
                "C": not truth if shared_failure else truth,
            }
            consequence = 8.0
        else:
            # Resolved ordinary history deliberately looks independent. B/C
            # have separate errors here, so passive co-failure learning is not
            # merely noisy—it is observing a different relation regime.
            labels = {
                "B": not truth if rng.random() < config.ordinary_error else truth,
                "C": not truth if rng.random() < config.ordinary_error else truth,
            }
            consequence = rng.choice((1.0, 2.0))

        labels["D"] = (
            not truth
            if rng.random() < config.independent_error
            else truth
        )

        learned_dependence = model.estimate(
            "B",
            "C",
            step=step,
            context_key="resolved-history",
        ).same_failure_lineage

        if policy == "stress_probe" and frontier and step > probe_valid_until:
            # The policy cannot see hidden truth. It prices a bounded diagnostic
            # from an explicit prior/risk estimate and the expected number of
            # consequential frontier decisions covered by its lifetime.
            expected_covered_frontier = (
                config.frontier_probability * config.probe_ttl
            )
            expected_probe_value = (
                config.estimated_frontier_dependency_risk
                * consequence
                * expected_covered_frontier
            )
            if expected_probe_value > config.probe_cost:
                probe_valid_until = step + config.probe_ttl
                metrics["dependency_probes"] += 1.0
                metrics["utility"] -= config.probe_cost

        if policy == "record_count":
            decision = _record_count(labels)
        elif policy == "passive_history":
            decision = (
                _collapse_bc(labels)
                if learned_dependence
                else _record_count(labels)
            )
        elif policy == "always_dependent":
            decision = _collapse_bc(labels)
        elif policy == "stress_probe":
            relation_known_for_frontier = frontier and step <= probe_valid_until
            decision = (
                _collapse_bc(labels)
                if relation_known_for_frontier
                else _record_count(labels)
            )
        else:
            decision = _collapse_bc(labels) if frontier else _record_count(labels)

        incorrect = decision != truth
        metrics["errors"] += float(incorrect)
        metrics["weighted_harm"] += float(incorrect) * consequence
        metrics["utility"] += (
            consequence if not incorrect else -3.0 * consequence
        )
        if frontier:
            metrics["frontier_cases"] += 1.0
            metrics["frontier_errors"] += float(incorrect)
        else:
            metrics["ordinary_cases"] += 1.0
            metrics["ordinary_errors"] += float(incorrect)

        # Passive resolution is deliberately unavailable on frontier cases in
        # this stress family: the selective attack targets the unresolved/new
        # distribution. This is the distribution-shift condition under test.
        if not frontier and rng.random() < config.passive_resolution:
            model.observe_resolution(
                labels,
                truth,
                context_key="resolved-history",
            )
            metrics["passive_resolutions"] += 1.0

    dependence_score = model.dependence_score(
        "B",
        "C",
        context_key="resolved-history",
    )
    return {
        "error_rate": metrics["errors"] / config.tasks,
        "weighted_harm": metrics["weighted_harm"] / config.tasks,
        "utility": metrics["utility"] / config.tasks,
        "frontier_error": (
            metrics["frontier_errors"] / metrics["frontier_cases"]
        ),
        "ordinary_error": (
            metrics["ordinary_errors"] / metrics["ordinary_cases"]
        ),
        "dependency_probes": metrics["dependency_probes"] / config.tasks,
        "passive_resolutions": metrics["passive_resolutions"] / config.tasks,
        "resolved_history_dependence_score": dependence_score,
        "passive_marks_bc_dependent": float(
            model.estimate(
                "B",
                "C",
                step=config.tasks,
                context_key="resolved-history",
            ).same_failure_lineage
        ),
    }
