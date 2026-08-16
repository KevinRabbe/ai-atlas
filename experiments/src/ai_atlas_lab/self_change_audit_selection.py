from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class I29Config:
    seed: int = 0
    candidates: int = 20_000
    harmful_change_rate: float = 0.10
    evaluator_true_positive: float = 0.80
    evaluator_false_positive: float = 0.15
    safe_gain: float = 1.0
    harmful_cost: float = 8.0
    audit_cost: float = 0.20
    flagged_audit_rate: float = 0.60
    coverage_audit_rate: float = 0.04
    decay: float = 0.995
    prior_global_error: float = 0.15
    prior_harm_if_safe: float = 0.08
    prior_harm_if_flagged: float = 0.30


class AuditCalibration:
    """Tiny experimental evaluator-calibration state.

    It intentionally exposes two estimands:

    - one global evaluator error rate;
    - conditional hidden-harm rates given the evaluator output.

    The point of I29 is not to select this estimator. It is to test whether a
    selectively audited sample can safely be reused as if it represented the
    population or an unobserved evaluator-output stratum.
    """

    def __init__(self, config: I29Config) -> None:
        self.config = config
        self.global_error = config.prior_global_error
        self.harm_if_safe = config.prior_harm_if_safe
        self.harm_if_flagged = config.prior_harm_if_flagged
        self.safe_audits = 0
        self.flagged_audits = 0

    def observe(self, flagged: bool, harmful: bool) -> None:
        decay = self.config.decay
        evaluator_wrong = flagged != harmful
        self.global_error = (
            decay * self.global_error
            + (1.0 - decay) * float(evaluator_wrong)
        )
        if flagged:
            self.harm_if_flagged = (
                decay * self.harm_if_flagged
                + (1.0 - decay) * float(harmful)
            )
            self.flagged_audits += 1
        else:
            self.harm_if_safe = (
                decay * self.harm_if_safe
                + (1.0 - decay) * float(harmful)
            )
            self.safe_audits += 1


def _generate_candidate(
    rng: random.Random,
    config: I29Config,
) -> tuple[bool, bool, float]:
    harmful = rng.random() < config.harmful_change_rate
    if harmful:
        flagged = rng.random() < config.evaluator_true_positive
    else:
        flagged = rng.random() < config.evaluator_false_positive
    consequence = rng.choice((1.0, 2.0, 4.0, 8.0))
    return harmful, flagged, consequence


def _promote(
    risk: float,
    consequence: float,
    config: I29Config,
) -> bool:
    expected = (
        (1.0 - risk) * config.safe_gain
        - risk * config.harmful_cost * consequence
    )
    return expected > 0.0


def _oracle_conditional_risks(config: I29Config) -> tuple[float, float]:
    harmful = config.harmful_change_rate
    flagged_probability = (
        harmful * config.evaluator_true_positive
        + (1.0 - harmful) * config.evaluator_false_positive
    )
    safe_probability = 1.0 - flagged_probability
    harm_if_flagged = (
        harmful * config.evaluator_true_positive / flagged_probability
    )
    harm_if_safe = (
        harmful * (1.0 - config.evaluator_true_positive) / safe_probability
    )
    return harm_if_safe, harm_if_flagged


def run_i29(config: I29Config, policy: str) -> dict[str, float]:
    valid = {
        "visible_only",
        "flagged_selected_scalar",
        "random_coverage_scalar",
        "flagged_only_conditional",
        "selection_aware_conditional",
        "oracle_conditional",
    }
    if policy not in valid:
        raise ValueError(f"unknown I29 policy: {policy}")

    # Audit scheduling must not perturb the hidden candidate stream.
    world_rng = random.Random(config.seed)
    audit_rng = random.Random(config.seed + 77_777)
    calibration = AuditCalibration(config)
    metrics: dict[str, float] = defaultdict(float)
    oracle_safe, oracle_flagged = _oracle_conditional_risks(config)

    for _ in range(config.candidates):
        harmful, flagged, consequence = _generate_candidate(
            world_rng,
            config,
        )

        if policy == "visible_only":
            risk = 1.0 if flagged else 0.0
        elif policy in {"flagged_selected_scalar", "random_coverage_scalar"}:
            # A single error rate assumes symmetric evaluator errors. This is a
            # deliberately weaker estimator used to separate sample selection
            # from the later conditional-calibration result.
            risk = (
                1.0 - calibration.global_error
                if flagged
                else calibration.global_error
            )
        elif policy in {
            "flagged_only_conditional",
            "selection_aware_conditional",
        }:
            risk = (
                calibration.harm_if_flagged
                if flagged
                else calibration.harm_if_safe
            )
        else:
            risk = oracle_flagged if flagged else oracle_safe

        promote = _promote(risk, consequence, config)
        if promote:
            if harmful:
                metrics["harmful_promotions"] += 1.0
                metrics["utility"] -= config.harmful_cost * consequence
            else:
                metrics["safe_promotions"] += 1.0
                metrics["utility"] += config.safe_gain
        elif not harmful:
            metrics["safe_rejections"] += 1.0

        # Audit happens after the promotion decision. Its purpose in this
        # experiment is future calibration, not oracle rescue of this candidate.
        audit = False
        if policy in {"flagged_selected_scalar", "flagged_only_conditional"}:
            audit = (
                flagged
                and audit_rng.random() < config.flagged_audit_rate
            )
        elif policy == "random_coverage_scalar":
            audit = audit_rng.random() < config.coverage_audit_rate
        elif policy == "selection_aware_conditional":
            audit = (
                flagged
                and audit_rng.random() < config.flagged_audit_rate
            ) or (
                not flagged
                and audit_rng.random() < config.coverage_audit_rate
            )

        if audit:
            calibration.observe(flagged, harmful)
            metrics["audits"] += 1.0
            metrics["utility"] -= config.audit_cost

    total = float(config.candidates)
    true_global_error = (
        config.harmful_change_rate
        * (1.0 - config.evaluator_true_positive)
        + (1.0 - config.harmful_change_rate)
        * config.evaluator_false_positive
    )
    return {
        "net_utility": metrics["utility"] / total,
        "harmful_promotions": metrics["harmful_promotions"] / total,
        "safe_promotions": metrics["safe_promotions"] / total,
        "safe_rejections": metrics["safe_rejections"] / total,
        "audit_rate": metrics["audits"] / total,
        "final_global_error": calibration.global_error,
        "true_global_error": true_global_error,
        "global_calibration_error": abs(
            calibration.global_error - true_global_error
        ),
        "final_harm_if_safe": calibration.harm_if_safe,
        "final_harm_if_flagged": calibration.harm_if_flagged,
        "oracle_harm_if_safe": oracle_safe,
        "oracle_harm_if_flagged": oracle_flagged,
        "safe_path_calibration_error": abs(
            calibration.harm_if_safe - oracle_safe
        ),
        "flagged_path_calibration_error": abs(
            calibration.harm_if_flagged - oracle_flagged
        ),
        "safe_audit_rate": calibration.safe_audits / total,
        "flagged_audit_rate": calibration.flagged_audits / total,
    }
