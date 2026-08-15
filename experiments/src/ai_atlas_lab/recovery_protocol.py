from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RecoveryState = Literal[
    "already_published",
    "not_published",
    "superseded",
    "conflict",
    "inconsistent",
]
RecoveryAction = Literal[
    "mark_complete",
    "retry_publish",
    "discard",
    "halt",
]


@dataclass(frozen=True)
class RecoveryRecord:
    """Minimum implementation-neutral semantics retained across a crash.

    The record deliberately does not contain an approval bit that can become
    authority after restart. It identifies the transition, the authoritative
    state it expected to replace, and the semantic target it intended to
    produce. `target_version` may be unknown at preparation time when version
    allocation is shared with unrelated publications; in that case exact
    attribution relies on publication provenance in the authoritative state.
    """

    publication_id: str
    kind: str
    expected_base_version: int
    target_version: int | None
    target_ref: str
    validation_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.expected_base_version < 0:
            raise ValueError("base version must be non-negative")
        if self.target_version is not None:
            if self.target_version < 0:
                raise ValueError("target version must be non-negative")
            if self.target_version <= self.expected_base_version:
                raise ValueError("target version must advance the base version")
        if not self.publication_id:
            raise ValueError("publication identity must be stable and non-empty")
        if not self.target_ref:
            raise ValueError("target identity/digest must be stable and non-empty")


@dataclass(frozen=True)
class RecoveryObservation:
    current_version: int
    current_ref: str
    current_publication_id: str | None = None


@dataclass(frozen=True)
class RecoveryDecision:
    state: RecoveryState
    action: RecoveryAction
    reason: str


def classify_recovery(
    record: RecoveryRecord,
    observation: RecoveryObservation,
) -> RecoveryState:
    """Classify authoritative state without trusting a local phase marker."""

    if observation.current_version < record.expected_base_version:
        return "inconsistent"

    # Strongest path: authoritative state records which publication produced
    # it. This remains exact even when the numeric target version could not be
    # known during preparation.
    if observation.current_publication_id == record.publication_id:
        if observation.current_ref != record.target_ref:
            return "conflict"
        if observation.current_version <= record.expected_base_version:
            return "inconsistent"
        if (
            record.target_version is not None
            and observation.current_version != record.target_version
        ):
            return "conflict"
        return "already_published"

    # We are still on the exact base the transition was prepared against. A
    # publication provenance tag on that base belongs to the prior authority
    # state and is not a conflict with this new intent.
    if observation.current_version == record.expected_base_version:
        return "not_published"

    # Backward-compatible weaker path when the target numeric version was known
    # exactly but the authoritative store cannot expose publication provenance.
    # I18 shows why this cannot distinguish a same-target publication collision.
    if (
        record.target_version is not None
        and observation.current_version == record.target_version
    ):
        if observation.current_ref != record.target_ref:
            return "conflict"
        if observation.current_publication_id is None:
            return "already_published"
        return "conflict"

    # Any other version above the expected base means authority moved along a
    # different path. Recovery must not overwrite it merely because an old
    # candidate had previously passed validation or has the same state value.
    if observation.current_version > record.expected_base_version:
        return "superseded"

    return "inconsistent"


def decide_recovery(
    record: RecoveryRecord,
    observation: RecoveryObservation,
    *,
    current_validation_ok: bool,
    current_assurance_ok: bool,
) -> RecoveryDecision:
    """Choose crash recovery action using current evidence/authority.

    `current_validation_ok` represents domain-specific current validity such as
    capability authority or non-retracted evidence. `current_assurance_ok`
    represents any independent assurance required to publish now. Neither is
    inferred from approval that existed before the crash.
    """

    state = classify_recovery(record, observation)

    if state == "already_published":
        return RecoveryDecision(
            state,
            "mark_complete",
            "authoritative publication provenance/target identifies this transition; do not publish twice",
        )

    if state == "not_published":
        if current_validation_ok and current_assurance_ok:
            return RecoveryDecision(
                state,
                "retry_publish",
                "base version is still authoritative and current checks permit retry",
            )
        return RecoveryDecision(
            state,
            "discard",
            "prepared intent has no authority after restart without current checks",
        )

    if state == "superseded":
        return RecoveryDecision(
            state,
            "discard",
            "authoritative state advanced through another publication; old intent must not overwrite it",
        )

    if state == "conflict":
        return RecoveryDecision(
            state,
            "halt",
            "version/target/publication provenance conflict makes automatic recovery unsafe",
        )

    return RecoveryDecision(
        state,
        "halt",
        "authoritative version regressed below the expected base; state requires reconciliation",
    )
