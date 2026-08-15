import statistics
import unittest

from ai_atlas_lab.evidence_aggregation_multihop import I28BConfig, run_i28b


class EvidenceAggregationMultiHopTests(unittest.TestCase):
    def mean(
        self,
        policy: str,
        key: str,
        *,
        root_shortcut: float = 0.20,
    ) -> float:
        return statistics.mean(
            run_i28b(
                I28BConfig(
                    seed=seed,
                    c_local_copy_rate=0.70 - root_shortcut,
                    c_root_shortcut_rate=root_shortcut,
                ),
                policy,
            ).get(key, 0.0)
            for seed in range(6)
        )

    def test_root_provenance_beats_local_edge_novelty_on_bypass_pattern(self) -> None:
        self.assertLess(
            self.mean("root_provenance_novelty", "bypass_error"),
            self.mean("local_edge_novelty", "bypass_error") - 0.08,
        )

    def test_path_conditioning_beats_local_conditioning_on_late_bypass_pattern(self) -> None:
        self.assertLess(
            self.mean("learned_path_conditional", "late_bypass_error"),
            self.mean("learned_local_conditional", "late_bypass_error") - 0.10,
        )

    def test_path_conditioning_improves_late_calibration_when_root_shortcut_exists(self) -> None:
        self.assertLess(
            self.mean("learned_path_conditional", "late_brier"),
            self.mean("learned_local_conditional", "late_brier") - 0.0005,
        )

    def test_root_provenance_novelty_improves_over_symmetric_group_on_bypass(self) -> None:
        self.assertLess(
            self.mean("root_provenance_novelty", "bypass_error"),
            self.mean("symmetric_group", "bypass_error") - 0.08,
        )

    def test_bypass_pattern_is_not_vanishingly_rare(self) -> None:
        rate = self.mean("oracle", "bypass_case_rate")
        self.assertGreater(rate, 0.05)
        self.assertLess(rate, 0.20)

    def test_extra_path_state_is_not_free_when_chain_is_strictly_local(self) -> None:
        local = self.mean(
            "learned_local_conditional",
            "late_brier",
            root_shortcut=0.0,
        )
        path = self.mean(
            "learned_path_conditional",
            "late_brier",
            root_shortcut=0.0,
        )
        self.assertLess(local, path)

    def test_oracle_remains_a_real_ceiling(self) -> None:
        self.assertLess(
            self.mean("oracle", "brier"),
            self.mean("root_provenance_novelty", "brier") - 0.002,
        )
        self.assertLess(
            self.mean("oracle", "late_bypass_error"),
            self.mean("learned_path_conditional", "late_bypass_error") + 0.01,
        )


if __name__ == "__main__":
    unittest.main()
