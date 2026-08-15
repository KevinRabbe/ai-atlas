from __future__ import annotations

from dataclasses import dataclass

from .organism_runtime import TypedScopeRuntime


@dataclass(frozen=True)
class HotStateRecord:
    hot_id: int
    subject_id: int
    state_ref: str
    source_ref: str
    source_version: int
    created_epoch: int
    scope_sensitive: bool


@dataclass(frozen=True)
class HotRecoveryStatus:
    persisted_valid: bool
    rematerializable: bool
    source_changed: bool
    scope_changed: bool


@dataclass(frozen=True)
class CreditEligibilityRecord:
    trace_id: int
    subject_id: int
    transition_ref: str
    created_epoch: int
    replay_source_ref: str | None


@dataclass(frozen=True)
class CreditRecoveryStatus:
    exact_target_valid: bool
    positional_restore_safe: bool
    replayable: bool
    structural_epoch_changed: bool


class TransientStateRegistry:
    """Non-owning transient recovery metadata for the typed organism runtime.

    The registry stores recovery semantics, not opaque process snapshots. Source
    evidence, capability authority and authoritative topology remain owned by
    their existing runtime records.
    """

    def __init__(self, runtime: TypedScopeRuntime) -> None:
        self.runtime = runtime
        self.hot_state: dict[int, HotStateRecord] = {}
        self.credit_traces: dict[int, CreditEligibilityRecord] = {}
        self._next_hot_id = 0
        self._next_trace_id = 0

    def register_hot_state(
        self,
        subject_id: int,
        *,
        state_ref: str,
        source_ref: str,
        source_version: int,
        scope_sensitive: bool,
    ) -> HotStateRecord:
        self.runtime._require_subject(subject_id)
        if not state_ref or not source_ref:
            raise ValueError("hot state and source references must be non-empty")
        if source_version < 0:
            raise ValueError("source_version cannot be negative")
        record = HotStateRecord(
            hot_id=self._next_hot_id,
            subject_id=subject_id,
            state_ref=state_ref,
            source_ref=source_ref,
            source_version=source_version,
            created_epoch=self.runtime.topology_epoch,
            scope_sensitive=scope_sensitive,
        )
        self._next_hot_id += 1
        self.hot_state[record.hot_id] = record
        self.runtime.costs.writes += 1
        return record

    def assess_hot_recovery(
        self,
        hot_id: int,
        *,
        current_source_version: int,
    ) -> HotRecoveryStatus:
        record = self.hot_state[hot_id]
        if current_source_version < 0:
            raise ValueError("current_source_version cannot be negative")
        source_changed = current_source_version != record.source_version
        scope_changed = self.runtime.topology_epoch != record.created_epoch
        persisted_valid = not source_changed and not (
            record.scope_sensitive and scope_changed
        )
        self.runtime.costs.reads += 1
        return HotRecoveryStatus(
            persisted_valid=persisted_valid,
            rematerializable=bool(record.source_ref),
            source_changed=source_changed,
            scope_changed=scope_changed,
        )

    def register_credit_trace(
        self,
        subject_id: int,
        *,
        transition_ref: str,
        replay_source_ref: str | None = None,
    ) -> CreditEligibilityRecord:
        self.runtime._require_subject(subject_id)
        if not transition_ref:
            raise ValueError("transition_ref must be non-empty")
        record = CreditEligibilityRecord(
            trace_id=self._next_trace_id,
            subject_id=subject_id,
            transition_ref=transition_ref,
            created_epoch=self.runtime.topology_epoch,
            replay_source_ref=replay_source_ref,
        )
        self._next_trace_id += 1
        self.credit_traces[record.trace_id] = record
        self.runtime.costs.writes += 1
        return record

    def assess_credit_recovery(
        self,
        trace_id: int,
        *,
        valid_transition_refs: set[str] | frozenset[str],
    ) -> CreditRecoveryStatus:
        record = self.credit_traces[trace_id]
        epoch_changed = self.runtime.topology_epoch != record.created_epoch
        exact_target_valid = record.transition_ref in valid_transition_refs
        self.runtime.costs.reads += 1
        return CreditRecoveryStatus(
            exact_target_valid=exact_target_valid,
            positional_restore_safe=not epoch_changed,
            replayable=record.replay_source_ref is not None,
            structural_epoch_changed=epoch_changed,
        )
