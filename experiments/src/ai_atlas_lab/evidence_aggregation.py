from __future__ import annotations

from dataclasses import dataclass
import math

from .evidence_dependence import EvidenceDependenceModel
from .evidence_lineage import EvidenceLineageRegistry


@dataclass(frozen=True)
class BinaryEvidenceEstimate:
    label: bool | None
    estimated_error: float
    resolving_groups: int
    used_groups: int
    ambiguous_groups: int
    unresolved_dependence_sources: int
    used_source_ids: tuple[str, ...]


def aggregate_binary_evidence(
    registry: EvidenceLineageRegistry,
    claim_ref: str,
    *,
    current_step: int,
    source_error_estimates: dict[str, float],
    positive_value_ref: str,
    negative_value_ref: str,
    dependence_model: EvidenceDependenceModel | None = None,
    dependence_context: str | None = None,
    minimum_independence_confidence: float = 0.50,
    prior_positive: float = 0.50,
) -> BinaryEvidenceEstimate:
    """Aggregate a binary claim once per effective failure group.

    The function consumes source-quality estimates but does not learn them.
    Exact lineage and learned dependence determine effective groups. Within one
    group, repeated/copy records do not multiply evidence; the lowest-error
    resolving source represents the group. Equal-quality contradictory records
    inside one group make that group ambiguous rather than becoming two votes.

    Across effective independent groups, source error estimates are converted to
    log-likelihood weights. This is intentionally a small experimental
    aggregator, not a claim that mature evidence combination must use Naive
    Bayes/log-odds.
    """

    if positive_value_ref == negative_value_ref:
        raise ValueError("positive and negative value refs must differ")
    if not 0.0 < prior_positive < 1.0:
        raise ValueError("prior_positive must lie strictly between 0 and 1")
    for source_id, error in source_error_estimates.items():
        if not 0.0 < error < 0.5:
            raise ValueError(
                f"source error estimate for {source_id!r} must lie in (0, 0.5)"
            )

    view = registry.effective_view(
        claim_ref,
        current_step=current_step,
        dependence_model=dependence_model,
        dependence_context=dependence_context,
        minimum_independence_confidence=minimum_independence_confidence,
    )

    records_by_group: dict[str, list[tuple[str, bool, float]]] = {}
    resolving_groups: set[str] = set()
    for record in view.current_records:
        if not record.resolves_claim or record.value_ref is None:
            continue
        if record.value_ref == positive_value_ref:
            label = True
        elif record.value_ref == negative_value_ref:
            label = False
        else:
            continue
        group = view.group_by_source[record.source_id]
        resolving_groups.add(group)
        error = source_error_estimates.get(record.source_id, 0.499999)
        records_by_group.setdefault(group, []).append(
            (record.source_id, label, error)
        )

    prior_log_odds = math.log(prior_positive / (1.0 - prior_positive))
    total_log_odds = prior_log_odds
    used_sources: list[str] = []
    ambiguous_groups = 0
    used_groups = 0

    for records in records_by_group.values():
        best_error = min(error for _, _, error in records)
        best = [record for record in records if abs(record[2] - best_error) < 1e-12]
        best_labels = {label for _, label, _ in best}
        if len(best_labels) != 1:
            ambiguous_groups += 1
            continue

        source_id, label, error = min(best, key=lambda item: item[0])
        weight = math.log((1.0 - error) / error)
        total_log_odds += weight if label else -weight
        used_groups += 1
        used_sources.append(source_id)

    if used_groups == 0 or abs(total_log_odds) < 1e-12:
        return BinaryEvidenceEstimate(
            label=None,
            estimated_error=0.5,
            resolving_groups=len(resolving_groups),
            used_groups=used_groups,
            ambiguous_groups=ambiguous_groups,
            unresolved_dependence_sources=view.unresolved_dependence_sources,
            used_source_ids=tuple(sorted(used_sources)),
        )

    if total_log_odds >= 0.0:
        label = True
        posterior_positive = 1.0 / (1.0 + math.exp(-total_log_odds))
        estimated_error = 1.0 - posterior_positive
    else:
        label = False
        posterior_positive = 1.0 / (1.0 + math.exp(-total_log_odds))
        estimated_error = posterior_positive

    return BinaryEvidenceEstimate(
        label=label,
        estimated_error=estimated_error,
        resolving_groups=len(resolving_groups),
        used_groups=used_groups,
        ambiguous_groups=ambiguous_groups,
        unresolved_dependence_sources=view.unresolved_dependence_sources,
        used_source_ids=tuple(sorted(used_sources)),
    )
