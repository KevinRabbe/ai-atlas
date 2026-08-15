import statistics
import unittest

from ai_atlas_lab.evidence_aggregation_directional import I28AConfig, run_i28a


class EvidenceAggregationDirectionalTests(unittest.TestCase):
    def mean(self, policy: str, key: str) -> float:
        return statistics.mean(
            run_i28a(I28AConfig(seed=seed), policy).get(key, 0.0)
            for seed in range(6)
        )

    def test_symmetric_group_beats_naive_independent_counting(self) -> None:
        self.assertLess(
            self.mean("symmetric_group", "error_rate"),
            self.mean("independent_quality", "error_rate") - 0.03,
        )

    def test_static_child_discount_is_not_enough(self) -> None:
        self.assertGreater(
            self.mean("inheritance_discount", "departure_error"),
            self.mean("novelty_weighted", "departure_error") + 0.10,
        )

    def test_direction_aware_novelty_beats_symmetric_collapse(self) -> None:
        self.assertLess(
            self.mean("novelty_weighted", "error_rate"),
            self.mean("symmetric_group", "error_rate") - 0.005,
        )
        self.assertLess(
            self.mean("novelty_weighted", "departure_error"),
            self.mean("symmetric_group", "departure_error") - 0.03,
        )

    def test_learned_directional_model_improves_late_calibration(self) -> None:
        self.assertLess(
            self.mean("learned_directional", "late_brier"),
            self.mean("novelty_weighted", "late_brier") - 0.002,
        )

    def test_learned_directional_model_nearly_matches_oracle_on_late_departures(self) -> None:
        learned = self.mean("learned_directional", "late_departure_error")
        oracle = self.mean("oracle", "late_departure_error")
        self.assertLess(abs(learned - oracle), 0.015)

    def test_direction_is_learned_from_passive_resolution(self) -> None:
        self.assertGreater(
            self.mean("learned_directional", "learned_parent_b_is_a"),
            0.95,
        )
        self.assertGreater(
            self.mean("learned_directional", "learned_parent_c_is_a"),
            0.95,
        )
        self.assertLess(
            self.mean("learned_directional", "direction_established_step"),
            1100.0,
        )

    def test_learned_directional_lifetime_brier_beats_symmetric_group(self) -> None:
        self.assertLess(
            self.mean("learned_directional", "brier"),
            self.mean("symmetric_group", "brier") - 0.003,
        )

    def test_oracle_remains_a_real_ceiling(self) -> None:
        self.assertLess(
            self.mean("oracle", "error_rate"),
            self.mean("novelty_weighted", "error_rate") - 0.004,
        )
        self.assertLess(
            self.mean("oracle", "late_brier"),
            self.mean("learned_directional", "late_brier") - 0.001,
        )


if __name__ == "__main__":
    unittest.main()
