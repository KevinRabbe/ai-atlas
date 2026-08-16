from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class I30Config:
    seed: int = 0
    candidates: int = 30_000
    frontier_rate: float = 0.30
    ordinary_truth_rate: float = 0.35
    frontier_truth_rate: float = 0.20
    visible_pass_threshold: float = 0.65
    near_threshold: float = 0.45
    rejected_verification_cost: float = 1.20
    passed_verification_cost: float = 0.20
    coverage_rate: float = 0.04
    targeted_rate: float = 0.30
    decay: float = 0.995
    min_samples: int = 15


class RejectedCandidateLearner:
    """Learn truth rates among rejected candidates.

    The experiment keeps both a domain-level estimate and domain/score-bin
    estimates so that sample-selection bias and estimand granularity can be
    separated. This is not a selected discovery-calibration algorithm.
    """

    def __init__(self, config: I30Config) -> None:
        self.config = config
        self.domain = {
            domain: [0.20, 0]
            for domain in ("ordinary", "frontier")
        }
        self.bins = {
            (domain, score_bin): [0.20, 0]
            for domain in ("ordinary", "frontier")
            for score_bin in range(3)
        }

    @staticmethod
    def score_bin(score: float) -> int:
        if score < 0.25:
            return 0
        if score < 0.45:
            return 1
        return 2

    def observe(self, domain: str, score: float, true_candidate: bool) -> None:
        decay = self.config.decay
        domain_state = self.domain[domain]
        domain_state[0] = (
            decay * domain_state[0]
            + (1.0 - decay) * float(true_candidate)
        )
        domain_state[1] += 1

        key = (domain, self.score_bin(score))
        bin_state = self.bins[key]
        bin_state[0] = (
            decay * bin_state[0]
            + (1.0 - decay) * float(true_candidate)
        )
        bin_state[1] += 1


def _beta_pdf(value: float, alpha: float, beta: float) -> float:
    if value <= 0.0 or value >= 1.0:
        return 0.0
    normalization = (
        math.gamma(alpha)
        * math.gamma(beta)
        / math.gamma(alpha + beta)
    )
    return (
        value ** (alpha - 1.0)
        * (1.0 - value) ** (beta - 1.0)
        / normalization
    )


def _oracle_truth_probability(
    domain: str,
    score: float,
    config: I30Config,
) -> float:
    if domain == "frontier":
        prior = config.frontier_truth_rate
        true_shape = (3.0, 3.5)
    else:
        prior = config.ordinary_truth_rate
        true_shape = (5.0, 2.0)
    false_shape = (2.0, 5.0)
    true_likelihood = _beta_pdf(score, *true_shape)
    false_likelihood = _beta_pdf(score, *false_shape)
    denominator = (
        prior * true_likelihood
        + (1.0 - prior) * false_likelihood
    )
    if denominator <= 0.0:
        return prior
    return prior * true_likelihood / denominator


def _generate_candidate(
    rng: random.Random,
    config: I30Config,
) -> tuple[str, bool, float, float]:
    domain = (
        "frontier"
        if rng.random() < config.frontier_rate
        else "ordinary"
    )
    truth_rate = (
        config.frontier_truth_rate
        if domain == "frontier"
        else config.ordinary_truth_rate
    )
    true_candidate = rng.random() < truth_rate

    if true_candidate:
        if domain == "frontier":
            score = rng.betavariate(3.0, 3.5)
        else:
            score = rng.betavariate(5.0, 2.0)
    else:
        score = rng.betavariate(2.0, 5.0)

    discovery_value = 8.0 if domain == "frontier" else 2.0
    return domain, true_candidate, score, discovery_value


def run_i30(config: I30Config, policy: str) -> dict[str, float]:
    valid = {
        "pass_only",
        "near_threshold_global",
        "random_domain",
        "selection_aware_bin",
        "oracle_score",
    }
    if policy not in valid:
        raise ValueError(f"unknown I30 policy: {policy}")

    world_rng = random.Random(config.seed)
    acquisition_rng = random.Random(config.seed + 424_242)
    learner = RejectedCandidateLearner(config)
    metrics: dict[str, float] = defaultdict(float)

    for _ in range(config.candidates):
        domain, true_candidate, score, value = _generate_candidate(
            world_rng,
            config,
        )

        # Candidates that pass the visible gate still require independent
        # verification before they become discoveries. This prevents visible
        # evaluator confidence from manufacturing knowledge.
        if score >= config.visible_pass_threshold:
            metrics["verifications"] += 1.0
            metrics["utility"] -= config.passed_verification_cost
            if true_candidate:
                metrics["discoveries"] += 1.0
                metrics["utility"] += value
            continue

        verify_reject = False
        if policy == "near_threshold_global":
            estimate, samples = learner.domain[domain]
            if (
                samples >= config.min_samples
                and estimate * value > config.rejected_verification_cost
            ):
                verify_reject = True
            elif (
                score >= config.near_threshold
                and acquisition_rng.random() < config.targeted_rate
            ):
                verify_reject = True
        elif policy == "random_domain":
            estimate, samples = learner.domain[domain]
            if (
                samples >= config.min_samples
                and estimate * value > config.rejected_verification_cost
            ):
                verify_reject = True
            elif acquisition_rng.random() < config.coverage_rate:
                verify_reject = True
        elif policy == "selection_aware_bin":
            key = (domain, learner.score_bin(score))
            estimate, samples = learner.bins[key]
            if (
                samples >= config.min_samples
                and estimate * value > config.rejected_verification_cost
            ):
                verify_reject = True
            elif acquisition_rng.random() < config.coverage_rate:
                verify_reject = True
        elif policy == "oracle_score":
            verify_reject = (
                _oracle_truth_probability(domain, score, config) * value
                > config.rejected_verification_cost
            )

        if verify_reject:
            metrics["verifications"] += 1.0
            metrics["rejected_verifications"] += 1.0
            metrics["utility"] -= config.rejected_verification_cost
            if policy != "oracle_score":
                learner.observe(domain, score, true_candidate)
            if true_candidate:
                metrics["discoveries"] += 1.0
                metrics["recovered_discoveries"] += 1.0
                metrics["utility"] += value

            if domain == "ordinary":
                metrics["ordinary_reject_audits"] += 1.0
                metrics["ordinary_reject_true"] += float(true_candidate)
            else:
                metrics["frontier_reject_audits"] += 1.0
                metrics["frontier_reject_true"] += float(true_candidate)
        elif true_candidate:
            metrics["missed_discoveries"] += 1.0

    total = float(config.candidates)
    ordinary_audits = metrics["ordinary_reject_audits"]
    frontier_audits = metrics["frontier_reject_audits"]
    return {
        "net_utility": metrics["utility"] / total,
        "discoveries": metrics["discoveries"] / total,
        "recovered_discoveries": metrics["recovered_discoveries"] / total,
        "missed_discoveries": metrics["missed_discoveries"] / total,
        "verification_rate": metrics["verifications"] / total,
        "rejected_verification_rate": (
            metrics["rejected_verifications"] / total
        ),
        "ordinary_domain_estimate": learner.domain["ordinary"][0],
        "frontier_domain_estimate": learner.domain["frontier"][0],
        "ordinary_reject_audit_precision": (
            metrics["ordinary_reject_true"] / ordinary_audits
            if ordinary_audits
            else 0.0
        ),
        "frontier_reject_audit_precision": (
            metrics["frontier_reject_true"] / frontier_audits
            if frontier_audits
            else 0.0
        ),
    }
