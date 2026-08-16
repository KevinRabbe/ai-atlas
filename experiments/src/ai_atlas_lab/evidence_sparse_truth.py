from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class I28DConfig:
    seed: int = 0
    tasks: int = 12_000
    parent_error: float = 0.25
    derived_check_rate: float = 0.35
    derived_check_error: float = 0.03
    independent_b_error: float = 0.11
    independent_c_error: float = 0.18
    independent_d_error: float = 0.22
    passive_resolution_rate: float = 0.012
    passive_delay_min: int = 80
    passive_delay_max: int = 240
    active_resolution_rate: float = 0.04
    active_resolution_delay: int = 10
    active_resolution_cost: float = 0.35
    provenance_probe_cost: float = 0.18
    provenance_probe_ttl: int = 220
    relation_decay: float = 0.92
    relation_min_resolutions: int = 12
    relation_threshold: float = 0.12
    relation_confidence_margin: float = 0.05
    inherited_agreement_weight: float = 0.12


class SparseRelationLearner:
    """Learn whether B currently inherits failures from A from resolved outcomes.

    The hidden relation is never supplied to the behavioral learner. The model
    deliberately receives only delayed resolved labels. An optional provenance
    probe is represented outside this learner so that direct structural evidence
    and behavioral learning remain separate epistemic channels.
    """

    def __init__(self, config: I28DConfig) -> None:
        self.config = config
        self.parent_error = 0.20
        self.child_error = 0.15
        self.joint_error = 0.03
        self.resolution_count = 0

    def observe_resolution(self, labels: dict[str, bool], truth: bool) -> None:
        decay = self.config.relation_decay
        parent_error = float(labels["A"] != truth)
        child_error = float(labels["B"] != truth)
        self.parent_error = (
            decay * self.parent_error + (1.0 - decay) * parent_error
        )
        self.child_error = (
            decay * self.child_error + (1.0 - decay) * child_error
        )
        self.joint_error = (
            decay * self.joint_error
            + (1.0 - decay) * parent_error * child_error
        )
        self.resolution_count += 1

    def dependence_score(self) -> float:
        if self.child_error <= 1e-9:
            return -1.0
        return self.joint_error / self.child_error - self.parent_error

    def estimate(self) -> tuple[bool | None, float]:
        if self.resolution_count < self.config.relation_min_resolutions:
            return None, 0.0
        score = self.dependence_score()
        confidence = min(
            1.0,
            abs(score - self.config.relation_threshold)
            / self.config.relation_confidence_margin,
        )
        if confidence < 0.35:
            return None, confidence
        return score > self.config.relation_threshold, confidence


def _weight(error: float) -> float:
    bounded = min(0.499, max(0.001, error))
    return math.log((1.0 - bounded) / bounded)


def _posterior(
    labels: dict[str, bool],
    relation: bool | None,
    config: I28DConfig,
) -> float:
    # Fixed quality estimates isolate the experiment's target: how scarce truth
    # changes learning of the A->B relation rather than source-quality learning.
    errors = {
        "A": config.parent_error,
        "B": 0.15,
        "C": config.independent_c_error,
        "D": config.independent_d_error,
    }
    log_odds = 0.0

    if relation is True:
        for source in ("A", "C", "D"):
            weight = _weight(errors[source])
            log_odds += weight if labels[source] else -weight
        factor = (
            1.0
            if labels["B"] != labels["A"]
            else config.inherited_agreement_weight
        )
        child_weight = _weight(errors["B"]) * factor
        log_odds += child_weight if labels["B"] else -child_weight
    elif relation is False:
        for source in ("A", "B", "C", "D"):
            weight = _weight(errors[source])
            log_odds += weight if labels[source] else -weight
    else:
        # Unknown relation does not manufacture independence. B is retained as
        # the representative of the uncertain A/B path; C/D remain independent.
        for source in ("B", "C", "D"):
            weight = _weight(errors[source])
            log_odds += weight if labels[source] else -weight

    return 1.0 / (1.0 + math.exp(-log_odds))


def _generate_task(
    rng: random.Random,
    config: I28DConfig,
    step: int,
) -> tuple[bool, dict[str, bool], float, bool]:
    # One unannounced structural shift: B is derived from A during the first
    # half, then becomes an independent evaluator while visible identities stay
    # unchanged.
    derived = step < config.tasks // 2
    truth = rng.random() < 0.5
    parent = (
        not truth if rng.random() < config.parent_error else truth
    )

    if derived:
        if rng.random() < config.derived_check_rate:
            child = (
                not truth
                if rng.random() < config.derived_check_error
                else truth
            )
        else:
            child = parent
    else:
        child = (
            not truth
            if rng.random() < config.independent_b_error
            else truth
        )

    labels = {
        "A": parent,
        "B": child,
        "C": (
            not truth
            if rng.random() < config.independent_c_error
            else truth
        ),
        "D": (
            not truth
            if rng.random() < config.independent_d_error
            else truth
        ),
    }
    consequence = rng.choice((1.0, 2.0, 4.0, 8.0))
    return truth, labels, consequence, derived


def run_i28d(config: I28DConfig, policy: str) -> dict[str, float]:
    valid = {
        "conservative",
        "passive_behavioral",
        "disagreement_targeted_truth",
        "coverage_targeted_truth",
        "provenance_probe",
        "oracle_relation",
    }
    if policy not in valid:
        raise ValueError(f"unknown I28D policy: {policy}")

    rng = random.Random(config.seed)
    learner = SparseRelationLearner(config)
    pending: list[tuple[int, dict[str, bool], bool, str]] = []
    probe: tuple[bool, int] | None = None
    metrics: dict[str, float] = defaultdict(float)

    for step in range(config.tasks):
        future: list[tuple[int, dict[str, bool], bool, str]] = []
        for due, labels, truth, kind in pending:
            if due <= step:
                learner.observe_resolution(labels, truth)
                metrics["feedback"] += 1.0
                metrics[f"feedback_{kind}"] += 1.0
            else:
                future.append((due, labels, truth, kind))
        pending = future

        truth, labels, consequence, true_relation = _generate_task(
            rng,
            config,
            step,
        )
        behavioral_relation, relation_confidence = learner.estimate()

        if policy == "oracle_relation":
            relation = true_relation
        elif policy == "conservative":
            relation = None
        elif (
            policy == "provenance_probe"
            and probe is not None
            and probe[1] >= step
        ):
            relation = probe[0]
        else:
            relation = behavioral_relation

        posterior = _posterior(labels, relation, config)
        decision = posterior >= 0.5
        incorrect = decision != truth
        outcome = 1.0 if truth else 0.0

        metrics["errors"] += float(incorrect)
        metrics["brier"] += (posterior - outcome) ** 2
        metrics["reward"] += (
            consequence if not incorrect else -3.0 * consequence
        )

        if relation is not None:
            metrics["relation_known"] += 1.0
            metrics["relation_correct"] += float(relation == true_relation)

        shift = config.tasks // 2
        if shift <= step < shift + 600:
            metrics["post_shift_cases"] += 1.0
            metrics["post_shift_errors"] += float(incorrect)
            if relation is not None:
                metrics["post_shift_relation_known"] += 1.0
                metrics["post_shift_relation_correct"] += float(
                    relation == true_relation
                )

        # Passive truth is sparse and delayed.
        if rng.random() < config.passive_resolution_rate:
            delay = rng.randint(
                config.passive_delay_min,
                config.passive_delay_max,
            )
            pending.append((step + delay, labels, truth, "passive"))

        # This intentionally demonstrates a bad active-learning design. Sampling
        # only disagreements makes the resolved set non-representative of the
        # joint A/B failure process, so an otherwise sensible dependence
        # estimator can become confidently biased.
        if policy == "disagreement_targeted_truth":
            if (
                labels["A"] != labels["B"]
                and (
                    behavioral_relation is None
                    or relation_confidence < 0.75
                    or consequence >= 8.0
                )
            ):
                pending.append(
                    (
                        step + config.active_resolution_delay,
                        labels,
                        truth,
                        "active",
                    )
                )
                metrics["active_resolutions"] += 1.0
                metrics["acquisition_cost"] += config.active_resolution_cost

        # Output-independent acquisition is less sample-efficient per query but
        # does not condition the training distribution on A/B disagreement.
        if policy == "coverage_targeted_truth":
            active_rate = (
                config.active_resolution_rate
                if behavioral_relation is None or relation_confidence < 0.80
                else config.active_resolution_rate / 2.0
            )
            if rng.random() < active_rate:
                pending.append(
                    (
                        step + config.active_resolution_delay,
                        labels,
                        truth,
                        "active",
                    )
                )
                metrics["active_resolutions"] += 1.0
                metrics["acquisition_cost"] += config.active_resolution_cost

        # A provenance probe answers only the relation question and carries a
        # bounded lifetime. It cannot reveal task truth.
        if policy == "provenance_probe":
            probe_active = probe is not None and probe[1] >= step
            if (
                not probe_active
                and (
                    behavioral_relation is None
                    or labels["A"] != labels["B"]
                    or consequence >= 8.0
                )
            ):
                probe = (
                    true_relation,
                    step + config.provenance_probe_ttl,
                )
                metrics["provenance_probes"] += 1.0
                metrics["acquisition_cost"] += config.provenance_probe_cost

    tasks = float(config.tasks)
    relation_known = metrics["relation_known"]
    post_known = metrics["post_shift_relation_known"]
    return {
        "error_rate": metrics["errors"] / tasks,
        "brier": metrics["brier"] / tasks,
        "net_utility": (
            metrics["reward"] - metrics["acquisition_cost"]
        ) / tasks,
        "relation_accuracy": (
            metrics["relation_correct"] / relation_known
            if relation_known
            else 0.0
        ),
        "relation_coverage": relation_known / tasks,
        "post_shift_error": (
            metrics["post_shift_errors"] / metrics["post_shift_cases"]
        ),
        "post_shift_relation_accuracy": (
            metrics["post_shift_relation_correct"] / post_known
            if post_known
            else 0.0
        ),
        "feedback_rate": metrics["feedback"] / tasks,
        "active_resolution_rate": metrics["active_resolutions"] / tasks,
        "provenance_probe_rate": metrics["provenance_probes"] / tasks,
    }
