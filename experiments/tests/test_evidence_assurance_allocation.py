import statistics
import unittest

from ai_atlas_lab.evidence_assurance_allocation import I20Config, run_i20


class EvidenceAssuranceAllocationTests(unittest.TestCase):
    def mean(self, policy: str, key: str, *, cost: float = 0.18) -> float:
        return statistics.mean(
            run_i20(I20Config(seed=seed, independent_cost=cost), policy).get(key, 0.0)
            for seed in range(6)
        )

    def test_lineage_value_beats_record_count_confidence(self) -> None:
        self.assertGreater(
            self.mean("lineage_value", "utility"),
            self.mean("record_count_confidence", "utility") + 0.40,
        )

    def test_lineage_value_beats_uniform_independent_at_default_cost(self) -> None:
        self.assertGreater(
            self.mean("lineage_value", "utility"),
            self.mean("uniform_independent", "utility") + 0.10,
        )

    def test_lineage_value_uses_fewer_queries_than_uniform_checking(self) -> None:
        query_rate = self.mean("lineage_value", "independent_queries")
        self.assertLess(query_rate, 0.80)
        self.assertGreater(query_rate, 0.50)

    def test_shared_policy_reduces_harm_in_both_claim_families(self) -> None:
        for key in (
            "external_harm_per_family_task",
            "metacognitive_harm_per_family_task",
        ):
            self.assertLess(
                self.mean("lineage_value", key),
                self.mean("record_count_confidence", key) * 0.60,
            )

    def test_independent_evidence_usage_falls_as_its_price_rises(self) -> None:
        cheap = self.mean("lineage_value", "independent_queries", cost=0.01)
        expensive = self.mean("lineage_value", "independent_queries", cost=3.0)
        self.assertGreater(cheap, expensive + 0.60)

    def test_value_aware_policy_remains_better_than_check_everything_when_checks_are_expensive(self) -> None:
        self.assertGreater(
            self.mean("lineage_value", "utility", cost=0.80),
            self.mean("uniform_independent", "utility", cost=0.80) + 0.30,
        )


if __name__ == "__main__":
    unittest.main()
