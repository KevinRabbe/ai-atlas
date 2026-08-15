from __future__ import annotations

from dataclasses import dataclass

from .evidence_dependence import EvidenceDependenceModel
from .organism_runtime import TypedScopeRuntime


@dataclass(frozen=True)
class EvidenceSource:
    source_id: str
    lineage_id: str | None = None
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
    unknown_dependence_sources: int = 0
    unresolved_dependence_sources: int = 0
    learned_dependence_used: bool = False


class EvidenceLineageRegistry:
    """Non-owning provenance/dependence metadata for runtime evidence.

    Exact source lineage may be supplied when genuinely known. It is no longer
    required. Unknown sources are never silently treated as independent merely
    because their names differ. A learned EvidenceDependenceModel can supply
    additional effective relation structure for the current claim/context.

    Crucially, a below-threshold learned score is counted as evidence of
    independence only when that estimate has enough observation support.

    The registry does not decide truth or source reliability and does not
    duplicate evidence payloads.
    """

    def __init__(self, runtime: TypedScopeRuntime) -> None:
        self.runtime = runtime
        self.sources: dict[str, EvidenceSource] = {}
        self.metadata: dict[int, EvidenceMetadata] = {}

    def register_source(
        self,
        source_id: str,
        *,
        lineage_id: str | None = None,
        validity_steps: int | None = None,
    ) -> EvidenceSource:
        if not source_id:
            raise ValueError("source identity must be non-empty")
        if lineage_id is not None and not lineage_id:
            raise ValueError("lineage identity must be non-empty when supplied")
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

    def _effective_groups(
        self,
        records: list[EvidenceMetadata],
        *,
        current_step: int,
        dependence_model: EvidenceDependenceModel | None,
        dependence_context: str | None,
        minimum_independence_confidence: float,
    ) -> tuple[dict[str, str], set[str]]:
        if not 0.0 <= minimum_independence_confidence <= 1.0:
            raise ValueError("minimum_independence_confidence must lie in [0, 1]")

        source_ids = tuple(sorted({record.source_id for record in records}))
        parent = {source_id: source_id for source_id in source_ids}
        unresolved_dependence: set[str] = set()

        def find(source_id: str) -> str:
            while parent[source_id] != source_id:
                parent[source_id] = parent[parent[source_id]]
                source_id = parent[source_id]
            return source_id

        def union(left: str, right: str) -> None:
            left_root = find(left)
            right_root = find(right)
            if left_root != right_root:
                parent[right_root] = left_root

        # Exact shared lineage is strong positive provenance: two records known
        # to share it cannot be split into independent evidence by a learned
        # behavioral model.
        for index, left in enumerate(source_ids):
            left_lineage = self.sources[left].lineage_id
            for right in source_ids[index + 1 :]:
                right_lineage = self.sources[right].lineage_id
                if (
                    left_lineage is not None
                    and left_lineage == right_lineage
                ):
                    union(left, right)

        modeled_sources = (
            dependence_model.sources if dependence_model is not None else set()
        )
        uncertain_unknown_sources: set[str] = set()

        # Learned dependence may additionally collapse sources whose exact
        # lineage is unknown or whose distinct provenance still exhibits a
        # shared relevant failure mode/common cause.
        if dependence_model is not None:
            for index, left in enumerate(source_ids):
                for right in source_ids[index + 1 :]:
                    if left not in modeled_sources or right not in modeled_sources:
                        continue
                    estimate = dependence_model.estimate(
                        left,
                        right,
                        step=current_step,
                        context_key=dependence_context,
                    )
                    if estimate.same_failure_lineage:
                        union(left, right)
                    elif estimate.confidence < minimum_independence_confidence:
                        # Lack of positive dependence is not established
                        # independence. Mark unknown-lineage participants as
                        # unresolved and conservatively keep multiple uncertain
                        # unknown sources in one effective failure component.
                        if self.sources[left].lineage_id is None:
                            uncertain_unknown_sources.add(left)
                        if self.sources[right].lineage_id is None:
                            uncertain_unknown_sources.add(right)

        # Unknown sources absent from the learned model also have unresolved
        # dependence. Different names do not grant independent-lineage status.
        for source_id in source_ids:
            if (
                self.sources[source_id].lineage_id is None
                and source_id not in modeled_sources
            ):
                uncertain_unknown_sources.add(source_id)

        if uncertain_unknown_sources:
            ordered_unknown = sorted(uncertain_unknown_sources)
            anchor = ordered_unknown[0]
            for source_id in ordered_unknown[1:]:
                union(anchor, source_id)
            unresolved_dependence.update(uncertain_unknown_sources)

        return (
            {source_id: find(source_id) for source_id in source_ids},
            unresolved_dependence,
        )

    def summarize_effective(
        self,
        claim_ref: str,
        *,
        current_step: int,
        dependence_model: EvidenceDependenceModel | None = None,
        dependence_context: str | None = None,
        minimum_independence_confidence: float = 0.50,
    ) -> EvidenceSummary:
        records = [
            metadata
            for metadata in self.metadata.values()
            if metadata.claim_ref == claim_ref
        ]
        stale = [record for record in records if self._is_stale(record, current_step)]
        current = [record for record in records if record not in stale]
        groups, unresolved_dependence = self._effective_groups(
            current,
            current_step=current_step,
            dependence_model=dependence_model,
            dependence_context=dependence_context,
            minimum_independence_confidence=minimum_independence_confidence,
        )

        current_groups = {groups[record.source_id] for record in current}
        resolving = [record for record in current if record.resolves_claim]
        resolving_groups = {groups[record.source_id] for record in resolving}

        # Conflict is counted across effective independent resolving groups.
        # Multiple records inside one effective group remain one failure path,
        # but internal contradictory values are also a conflict signal.
        values_by_group: dict[str, set[str]] = {}
        for record in resolving:
            if record.value_ref is None:
                continue
            group = groups[record.source_id]
            values_by_group.setdefault(group, set()).add(record.value_ref)

        group_values = {
            next(iter(values))
            for values in values_by_group.values()
            if len(values) == 1
        }
        internal_group_conflict = any(
            len(values) > 1 for values in values_by_group.values()
        )
        conflict = internal_group_conflict or len(group_values) > 1

        unknown_sources = {
            record.source_id
            for record in current
            if self.sources[record.source_id].lineage_id is None
        }

        self.runtime.costs.reads += len(records)
        return EvidenceSummary(
            record_count=len(records),
            independent_lineages=len(current_groups),
            resolving_lineages=len(resolving_groups),
            stale_records=len(stale),
            unresolved_records=sum(not record.resolves_claim for record in current),
            conflict=conflict,
            unknown_dependence_sources=len(unknown_sources),
            unresolved_dependence_sources=len(unresolved_dependence),
            learned_dependence_used=dependence_model is not None,
        )

    def summarize(self, claim_ref: str, *, current_step: int) -> EvidenceSummary:
        """Backward-compatible exact/conservative summary.

        Known lineage metadata behaves as before. Unknown/unmodeled sources are
        conservatively grouped rather than silently counted as independent.
        """

        return self.summarize_effective(
            claim_ref,
            current_step=current_step,
        )
