from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .evidence_lineage import EvidenceSummary


EvidenceAction = Literal["use_current", "acquire_independent", "unresolved"]


@dataclass(frozen=True)
class EvidenceAssuranceDecision:
    action: EvidenceAction
    current_expected_harm: float
    independent_expected_harm: float
    unresolved_expected_harm: float
    reason: str


def decide_evidence_assurance(
    summary: EvidenceSummary,
    *,
    current_label: bool | None,
    estimated_current_error: float,
    estimated_independent_error: float,
    consequence: float,
    false_positive_penalty: float,
    false_negative_penalty: float,
    independent_cost: float,
    unresolved_penalty: float,
) -> EvidenceAssuranceDecision:
    """Price whether current evidence is enough or another lineage is worth buying.

    This function intentionally does not estimate source reliability. Those
    estimates are learned/maintained elsewhere. It consumes evidence-structure
    facts (lineage count, resolution and conflict) plus current quality/cost
    estimates, preserving the separation exposed by I05C/I17.
    """

    for name, value in (
        ("estimated_current_error", estimated_current_error),
        ("estimated_independent_error", estimated_independent_error),
    ):
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must lie in [0, 1]")
    for name, value in (
        ("consequence", consequence),
        ("false_positive_penalty", false_positive_penalty),
        ("false_negative_penalty", false_negative_penalty),
        ("independent_cost", independent_cost),
        ("unresolved_penalty", unresolved_penalty),
    ):
        if value < 0.0:
            raise ValueError(f"{name} cannot be negative")

    unresolved_harm = unresolved_penalty * consequence
    average_wrong_penalty = (
        false_positive_penalty + false_negative_penalty
    ) / 2.0
    independent_harm = (
        estimated_independent_error * average_wrong_penalty * consequence
        + independent_cost
    )

    if current_label is None or summary.resolving_lineages == 0:
        current_harm = unresolved_harm
        if independent_harm < unresolved_harm:
            return EvidenceAssuranceDecision(
                "acquire_independent",
                current_harm,
                independent_harm,
                unresolved_harm,
                "current records do not resolve the claim and an independent resolving path is worth its cost",
            )
        return EvidenceAssuranceDecision(
            "unresolved",
            current_harm,
            independent_harm,
            unresolved_harm,
            "current records do not resolve the claim and another lineage is not worth its cost",
        )

    wrong_penalty = (
        false_positive_penalty if current_label else false_negative_penalty
    )
    current_harm = estimated_current_error * wrong_penalty * consequence

    # Contradiction across resolving lineages is itself evidence that a single
    # current conclusion should not be promoted merely by record count.
    if summary.conflict:
        if independent_harm < unresolved_harm:
            return EvidenceAssuranceDecision(
                "acquire_independent",
                current_harm,
                independent_harm,
                unresolved_harm,
                "independent resolving lineages conflict and another failure mode is cheaper than carrying the uncertainty",
            )
        return EvidenceAssuranceDecision(
            "unresolved",
            current_harm,
            independent_harm,
            unresolved_harm,
            "independent resolving lineages conflict and additional resolution is too expensive",
        )

    # Multiple records from one lineage do not reduce this harm estimate.
    # Conversely, two independent resolving lineages are not automatically
    # perfect evidence; reliability remains an explicit learned quantity.
    if independent_harm < current_harm:
        return EvidenceAssuranceDecision(
            "acquire_independent",
            current_harm,
            independent_harm,
            unresolved_harm,
            "expected harm reduction from a new failure lineage exceeds its acquisition cost",
        )

    if unresolved_harm < current_harm:
        return EvidenceAssuranceDecision(
            "unresolved",
            current_harm,
            independent_harm,
            unresolved_harm,
            "retaining uncertainty is cheaper than acting on the current lineage",
        )

    return EvidenceAssuranceDecision(
        "use_current",
        current_harm,
        independent_harm,
        unresolved_harm,
        "current resolving evidence has lower expected harm than another lineage or deferral",
    )
