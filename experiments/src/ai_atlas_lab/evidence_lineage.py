from __future__ import annotations

from dataclasses import dataclass

from .organism_runtime import TypedScopeRuntime


@dataclass(frozen=True)
class EvidenceSource:
    source_id: str
    lineage_id: str
    validity_steps: int | None = None


@dataclass(frozen=True)
class EvidenceMetadata:
    evidence_id: int
    source_id: str
    claim_ref: str
    observed_step: int
    resolves_claim: bool
    value_ref: str | None = None


@dataclass(frozen=True)
class EvidenceSummary:
    record_count: int
    independent_lineages: int
    resolving_lineages: int
    stale_records: int
    unresolved_records: int
    conflict: bool


class EvidenceLineageRegistry:
    """Non-owning provenance/failure-lineage metadata for runtime evidence.

    The registry does not decide truth and does not duplicate evidence payloads.
    It records only the semantic relations needed to avoid treating copied,
    stale or non-resolving observations as independent confirmation.
    """

    def __init__(self, runtime: TypedScopeRuntime) -> None:
        self.runtime = runtime
        self.sources: dict[str, EvidenceSource] = {}
        self.metadata: dict[int, EvidenceMetadata] = {}

    def register_source(
        self,
        source_id: str,
        *,
        lineage_id: str,
        validity_steps: int | None = None,
    ) -> EvidenceSource:
        if not source_id or not lineage_id:
            raise ValueError("source and lineage identities must be non-empty")
        if validity_steps is not None and validity_steps < 0:
            raise ValueError("validity_steps cannot be negative")
        source = EvidenceSource(source_id, lineage_id, validity_steps)
        self.sources[source_id] = source
        self.runtime.costs.writes += 1
        return source

    def annotate(
        self,
        evidence_id: int,
        *,
        source_id: str,
        claim_ref: str,
        observed_step: int,
        resolves_claim: bool,
        value_ref: str | None = None,
    ) -> EvidenceMetadata:
        if evidence_id not in self.runtime.evidence:
            raise KeyError(f"unknown runtime evidence {evidence_id}")
        if source_id not in self.sources:
            raise KeyError(f"unknown evidence source {source_id!r}")
        if observed_step < 0:
            raise ValueError("observed_step cannot be negative")
        if not claim_ref:
            raise ValueError("claim_ref must be non-empty")
        metadata = EvidenceMetadata(
            evidence_id=evidence_id,
            source_id=source_id,
            claim_ref=claim_ref,
            observed_step=observed_step,
            resolves_claim=resolves_claim,
            value_ref=value_ref,
        )
        self.metadata[evidence_id] = metadata
        self.runtime.costs.writes += 1
        return metadata

    def _is_stale(self, metadata: EvidenceMetadata, current_step: int) -> bool:
        source = self.sources[metadata.source_id]
        if source.validity_steps is None:
            return False
        return current_step - metadata.observed_step > source.validity_steps

    def summarize(self, claim_ref: str, *, current_step: int) -> EvidenceSummary:
        records = [
            metadata
            for metadata in self.metadata.values()
            if metadata.claim_ref == claim_ref
        ]
        stale = [record for record in records if self._is_stale(record, current_step)]
        current = [record for record in records if record not in stale]

        lineages = {
            self.sources[record.source_id].lineage_id for record in current
        }
        resolving = [record for record in current if record.resolves_claim]
        resolving_lineages = {
            self.sources[record.source_id].lineage_id for record in resolving
        }

        # Conflict is counted across independent resolving lineages only. Many
        # copied records from one lineage remain one epistemic source.
        values_by_lineage: dict[str, set[str]] = {}
        for record in resolving:
            if record.value_ref is None:
                continue
            lineage = self.sources[record.source_id].lineage_id
            values_by_lineage.setdefault(lineage, set()).add(record.value_ref)

        lineage_values = {
            next(iter(values))
            for values in values_by_lineage.values()
            if len(values) == 1
        }
        internal_lineage_conflict = any(
            len(values) > 1 for values in values_by_lineage.values()
        )
        conflict = internal_lineage_conflict or len(lineage_values) > 1

        self.runtime.costs.reads += len(records)
        return EvidenceSummary(
            record_count=len(records),
            independent_lineages=len(lineages),
            resolving_lineages=len(resolving_lineages),
            stale_records=len(stale),
            unresolved_records=sum(not record.resolves_claim for record in current),
            conflict=conflict,
        )
