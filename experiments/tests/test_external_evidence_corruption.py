import unittest

from ai_atlas_lab.external_evidence_corruption import I17Config, run_i17


class ExternalEvidenceCorruptionTests(unittest.TestCase):
    def test_correlated_majority_does_not_create_independent_evidence(self) -> None:
        result = run_i17(I17Config(seed=3), "correlated_majority")
        self.assertGreater(result["duplicate_effect"], 0.06)
        self.assertGreater(result["omitted_effect"], 0.035)

    def test_raw_majority_can_waste_an_independent_check(self) -> None:
        result = run_i17(I17Config(seed=4), "majority_plus_independent")
        self.assertGreater(result["independent_queries"], 0.99)
        self.assertGreater(result["duplicate_effect"], 0.06)

    def test_independent_reconciliation_reduces_correlated_failure_harm(self) -> None:
        config = I17Config(seed=5)
        primary = run_i17(config, "trust_primary")
        independent = run_i17(config, "uniform_independent")
        self.assertLess(independent["weighted_harm"], primary["weighted_harm"] * 0.25)

    def test_selective_reconciliation_saves_queries_at_default_cost(self) -> None:
        config = I17Config(seed=6)
        selective = run_i17(config, "selective_independent")
        uniform = run_i17(config, "uniform_independent")
        self.assertLess(selective["independent_queries"], 0.75)
        self.assertLess(selective["weighted_harm"], 0.25)
        self.assertLess(uniform["weighted_harm"], selective["weighted_harm"])

    def test_uniform_checking_can_win_when_independent_evidence_is_cheap(self) -> None:
        config = I17Config(seed=7, independent_cost=0.01)
        uniform = run_i17(config, "uniform_independent")
        selective = run_i17(config, "selective_independent")
        self.assertGreater(uniform["utility"], selective["utility"])

    def test_selective_checking_wins_when_independent_evidence_is_expensive(self) -> None:
        config = I17Config(seed=8, independent_cost=0.70)
        uniform = run_i17(config, "uniform_independent")
        selective = run_i17(config, "selective_independent")
        self.assertGreater(selective["utility"], uniform["utility"] + 0.10)


if __name__ == "__main__":
    unittest.main()
