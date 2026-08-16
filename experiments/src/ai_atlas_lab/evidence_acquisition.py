from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .organism_runtime import TypedScopeRuntime


AcquisitionMode = Literal[
    "passive",
    "randomized",
    "targeted",
    "interventional",
    "unknown",
]


@dataclass(frozen=True)
class EvidenceAcquisitionMetadata:
    evidence_id: int
    acquisition_ref: str
    mode: AcquisitionMode
    inclusion_probability: float | None = None
    selection_scope_ref: str | None = None


@dataclass(frozen=True)
class EvidenceSelectionSummary:
    record_count: int
    targeted_records: int
    randomized_records: int
    unknown_mode_records: int
    known_probability_records: int
    unmodeled_selection_records: int


class EvidenceAcquisitionRegistry:
    """Non-owning metadata for how evidence became observable.

    PS-027 requires acquisition/selection semantics to remain distinguishable
    from the evidence value itself. This registry deliberately does not decide
    whether an observation is representative, true, independent or sufficient.

    `inclusion_probability` is optional. When it is genuinely known, callers
    may use the inverse weight as one possible correction. The architecture does
    not assume inverse-propensity weighting is universally appropriate.
    """

    def __init__(self, runtime: TypedScopeRuntime) -> None:
        self.runtime = runtime
        self.metadata: dict[int, EvidenceAcquisitionMetadata] = {}

    def record(
        self,
        evidence_id: int,
        *,
        acquisition_ref: str,
        mode: AcquisitionMode,
        inclusion_probability: float | None = None,
        selection_scope_ref: str | None = None,
    ) -> EvidenceAcquisitionMetadata:
        if evidence_id not in self.runtime.evidence:
            raise KeyError(f"unknown runtime evidence {evidence_id}")
        if not acquisition_ref:
            raise ValueError("acquisition_ref must be non-empty")
        if mode not in {
            "passive",
            "randomized",
            "targeted",
            "interventional",
            "unknown",
        }:
            raise ValueError(f"unsupported acquisition mode {mode!r}")
        if inclusion_probability is not None and not (
            0.0 < inclusion_probability <= 1.0
        ):
            raise ValueError("inclusion_probability must lie in (0, 1]")
        if selection_scope_ref is not None and not selection_scope_ref:
            raise ValueError("selection_scope_ref must be non-empty when supplied")

        metadata = EvidenceAcquisitionMetadata(
            evidence_id=evidence_id,
            acquisition_ref=acquisition_ref,
            mode=mode,
            inclusion_probability=inclusion_probability,
            selection_scope_ref=selection_scope_ref,
        )
        self.metadata[evidence_id] = metadata
        self.runtime.costs.writes += 1
        return metadata

    def inverse_inclusion_weight(self, evidence_id: int) -> float | None:
        metadata = self.metadata[evidence_id]
        if metadata.inclusion_probability is None:
            return None
        self.runtime.costs.reads += 1
        return 1.0 / metadata.inclusion_probability

    def summarize(
        self,
        evidence_ids: tuple[int, ...],
    ) -> EvidenceSelectionSummary:
        records = [
            self.metadata[evidence_id]
            for evidence_id in evidence_ids
            if evidence_id in self.metadata
        ]
        targeted = sum(record.mode == "targeted" for record in records)
        randomized = sum(record.mode == "randomized" for record in records)
        unknown = sum(record.mode == "unknown" for record in records)
        known_probability = sum(
            record.inclusion_probability is not None for record in records
        )
        unmodeled_selection = sum(
            record.mode in {"targeted", "unknown"}
            and record.inclusion_probability is None
            for record in records
        )
        self.runtime.costs.reads += len(records)
        return EvidenceSelectionSummary(
            record_count=len(records),
            targeted_records=targeted,
            randomized_records=randomized,
            unknown_mode_records=unknown,
            known_probability_records=known_probability,
            unmodeled_selection_records=unmodeled_selection,
        )
