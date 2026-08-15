import statistics
import unittest

from ai_atlas_lab.evidence_aggregation_cycles import I28CConfig, run_i28c


class EvidenceAggregationCyclesTests(unittest.TestCase):
    def mean(self, policy: str, key: str) -> float:
        return statistics.mean(
            run_i28c(I28CConfig(seed=seed), policy).get(key, 0.0)
            for seed in range(6)
        )

    def test_final_outputs_share_innovation_root_often_but_not_always(self) -> None:
        rate = self.mean("oracle", "same_root_rate")
        self.assertGreater(rate, 0.55)
        self.assertLess(rate, 0.75)

    def test_static_cycle_collapse_loses_distinct_root_evidence(self) -> None:
        self.assertGreater(
            self.mean("static_cycle_collapse", "distinct_root_error"),
            self.mean("versioned_root_groups", "distinct_root_error") + 0.005,
        )

    def test_final_independence_double_counts_same_root_evidence(self) -> None:
        self.assertGreater(
            self.mean("final_independent", "same_root_error"),
            self.mean("versioned_root_groups", "same_root_error") + 0.005,
        )

    def test_unversioned_history_independence_creates_false_precision(self) -> None:
        self.assertGreater(
            self.mean("history_independent", "brier"),
            self.mean("learned_temporal", "brier") + 0.01,
        )

    def test_temporal_unrolling_improves_calibration_over_dynamic_root_grouping(self) -> None:
        self.assertLess(
            self.mean("learned_temporal", "brier"),
            self.mean("versioned_root_groups", "brier") - 0.005,
        )

    def test_temporal_unrolling_beats_static_cycle_collapse(self) -> None:
        self.assertLess(
            self.mean("learned_temporal", "error_rate"),
            self.mean("static_cycle_collapse", "error_rate") - 0.003,
        )

    def test_learned_temporal_model_nearly_matches_oracle_error(self) -> None:
        learned = self.mean("learned_temporal", "error_rate")
        oracle = self.mean("oracle", "error_rate")
        self.assertLess(abs(learned - oracle), 0.008)

    def test_oracle_remains_calibration_ceiling(self) -> None:
        self.assertLess(
            self.mean("oracle", "brier"),
            self.mean("learned_temporal", "brier") - 0.001,
        )


if __name__ == "__main__":
    unittest.main()
