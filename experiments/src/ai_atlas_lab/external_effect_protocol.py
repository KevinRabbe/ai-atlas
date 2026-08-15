from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


ExecutionStatus = Literal["applied", "absent", "unknown"]
EffectRecoveryAction = Literal[
    "mark_complete",
    "retry",
    "retry_same_identity",
    "blocked",
    "abstain",
    "unresolved",
]


@dataclass(frozen=True)
class ExternalEffectIntent:
    effect_id: str
    target_ref: str
    consequence: float

    def __post_init__(self) -> None:
        if not self.effect_id:
            raise ValueError("external effect identity must be non-empty")
        if not self.target_ref:
            raise ValueError("external target reference must be non-empty")
        if self.consequence < 0.0:
            raise ValueError("consequence cannot be negative")


@dataclass(frozen=True)
class ExternalExecutionObservation:
    status: ExecutionStatus
    effect_specific: bool
    evidence_ref: str | None = None
    probability_applied: float | None = None

    def __post_init__(self) -> None:
        if self.probability_applied is not None and not 0.0 <= self.probability_applied <= 1.0:
            raise ValueError("probability_applied must lie in [0, 1]")


@dataclass(frozen=True)
class ExternalRecoveryDecision:
    action: EffectRecoveryAction
    reason: str


def decide_external_effect_recovery(
    intent: ExternalEffectIntent,
    observation: ExternalExecutionObservation,
    *,
    current_authority: bool,
    receiver_recognizes_identity: bool,
    duplicate_penalty: float,
    missed_penalty: float,
    retry_cost: float = 0.0,
) -> ExternalRecoveryDecision:
    """Recover an external effect without conflating history and permission.

    Exact external evidence can establish that the effect already happened even
    when capability authority is currently revoked. A new attempt, however,
    always requires current authority. If exact execution identity is absent,
    recovery remains unresolved unless consequence economics justify an
    explicitly risky retry/abstention decision.
    """

    if duplicate_penalty < 0.0 or missed_penalty < 0.0 or retry_cost < 0.0:
        raise ValueError("recovery costs/penalties cannot be negative")

    if observation.effect_specific and observation.status == "applied":
        return ExternalRecoveryDecision(
            "mark_complete",
            "effect-specific external evidence establishes historical execution",
        )

    if observation.effect_specific and observation.status == "absent":
        if current_authority:
            return ExternalRecoveryDecision(
                "retry",
                "exact external evidence says absent and current authority permits a new attempt",
            )
        return ExternalRecoveryDecision(
            "blocked",
            "effect is absent but current capability authority denies a new attempt",
        )

    # If the receiver participates in the stable identity semantics, replaying
    # the same identity can be safe even when execution status is locally
    # unknown. Permission to issue that replay is still current authority.
    if receiver_recognizes_identity:
        if current_authority:
            return ExternalRecoveryDecision(
                "retry_same_identity",
                "receiver can deduplicate the stable effect identity and current authority permits replay",
            )
        return ExternalRecoveryDecision(
            "blocked",
            "stable external identity exists but current authority denies replay",
        )

    if not current_authority:
        return ExternalRecoveryDecision(
            "unresolved",
            "execution is ambiguous and authority denies any new attempt; preserve uncertainty",
        )

    probability = observation.probability_applied
    if probability is None:
        return ExternalRecoveryDecision(
            "unresolved",
            "no effect-specific external evidence exists; local intent cannot determine execution",
        )

    retry_harm = probability * duplicate_penalty + retry_cost
    abstain_harm = (1.0 - probability) * missed_penalty
    if retry_harm < abstain_harm:
        return ExternalRecoveryDecision(
            "retry",
            "effect history is unresolved but omission risk exceeds duplicate/retry risk",
        )
    return ExternalRecoveryDecision(
        "abstain",
        "effect history is unresolved and duplicate/retry risk exceeds omission risk",
    )
