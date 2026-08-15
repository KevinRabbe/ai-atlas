import statistics
import unittest

from ai_atlas_lab.metacognitive_audit_corruption import I05CConfig, run_i05c


class MetacognitiveAuditCorruptionTests(unittest.TestCase):
    def results(self, policy: str):
        return [run_i05c(I05CConfig(seed=seed), policy) for seed in range(6)]

    def mean(self, policy: str, key: str) -> float:
        return statistics.mean(result.get(key, 0.0) for result in self.results(policy))

    def test_correlated_majority_is_worse_calibrated_than_independent_audit(self) -> None:
        self.assertGreater(
            self.mean("correlated_majority", "estimate_error"),
            self.mean("uniform_independent", "estimate_error") + 0.02,
        )

    def test_raw_majority_can_pay_for_independent_audit_without_using_its_information(self) -> None:
        self.assertGreater(self.mean("majority_plus_independent", "audit_queries"), 0.99)
        self.assertGreater(
            self.mean("majority_plus_independent", "estimate_error"),
            self.mean("uniform_independent", "estimate_error") + 0.02,
        )

    def test_selective_independent_audit_preserves_calibration_with_fewer_queries(self) -> None:
        self.assertLess(self.mean("selective_independent", "audit_queries"), 0.75)
        self.assertLess(self.mean("selective_independent", "estimate_error"), 0.06)

    def test_unavailable_outcomes_can_remain_explicitly_unresolved(self) -> None:
        self.assertGreater(
            self.mean("uniform_independent", "unresolved_feedback"),
            0.18,
        )

    def test_treating_missing_audit_as_success_worsens_calibration(self) -> None:
        self.assertGreater(
            self.mean("missing_as_success", "estimate_error"),
            self.mean("uniform_independent", "estimate_error") + 0.01,
        )

    def test_treating_missing_audit_as_success_increases_false_durable_writes(self) -> None:
        self.assertGreater(
            self.mean("missing_as_success", "false_durable_writes"),
            self.mean("uniform_independent", "false_durable_writes") + 0.002,
        )


if __name__ == "__main__":
    unittest.main()
