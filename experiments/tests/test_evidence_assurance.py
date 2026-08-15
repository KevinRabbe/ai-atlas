import unittest

from ai_atlas_lab.evidence_assurance import decide_evidence_assurance
from ai_atlas_lab.evidence_lineage import EvidenceSummary


def summary(*, records=3, lineages=1, resolving=1, stale=0, unresolved=0, conflict=False):
    return EvidenceSummary(
        record_count=records,
        independent_lineages=lineages,
        resolving_lineages=resolving,
        stale_records=stale,
        unresolved_records=unresolved,
        conflict=conflict,
    )


class EvidenceAssuranceTests(unittest.TestCase):
    def decide(self, evidence, **kwargs):
        defaults = dict(
            current_label=True,
            estimated_current_error=0.15,
            estimated_independent_error=0.03,
            consequence=4.0,
            false_positive_penalty=4.0,
            false_negative_penalty=2.0,
            independent_cost=0.10,
            unresolved_penalty=0.8,
        )
        defaults.update(kwargs)
        return decide_evidence_assurance(evidence, **defaults)

    def test_record_count_does_not_change_decision_when_lineage_structure_is_same(self) -> None:
        one = self.decide(summary(records=1))
        many = self.decide(summary(records=100))
        self.assertEqual(one.action, many.action)
        self.assertEqual(one.current_expected_harm, many.current_expected_harm)

    def test_stale_nonresolving_lineage_can_trigger_independent_acquisition(self) -> None:
        decision = self.decide(
            summary(records=3, lineages=0, resolving=0, stale=3)
        )
        self.assertEqual(decision.action, "acquire_independent")

    def test_nonresolving_evidence_can_remain_unresolved_when_resolution_is_too_expensive(self) -> None:
        decision = self.decide(
            summary(records=3, lineages=0, resolving=0, stale=3),
            independent_cost=20.0,
        )
        self.assertEqual(decision.action, "unresolved")

    def test_independent_conflict_can_trigger_another_failure_lineage(self) -> None:
        decision = self.decide(
            summary(records=2, lineages=2, resolving=2, conflict=True)
        )
        self.assertEqual(decision.action, "acquire_independent")

    def test_conflict_can_remain_unresolved_when_another_check_costs_too_much(self) -> None:
        decision = self.decide(
            summary(records=2, lineages=2, resolving=2, conflict=True),
            independent_cost=20.0,
        )
        self.assertEqual(decision.action, "unresolved")

    def test_current_lineage_is_used_when_its_expected_harm_is_lowest(self) -> None:
        decision = self.decide(
            summary(),
            estimated_current_error=0.01,
            independent_cost=1.0,
        )
        self.assertEqual(decision.action, "use_current")


if __name__ == "__main__":
    unittest.main()
