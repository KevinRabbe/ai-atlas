import statistics
import unittest

from ai_atlas_lab.evidence_dependence_directional import I26BConfig, run_i26b


class EvidenceDependenceDirectionalTests(unittest.TestCase):
    def mean(self, policy: str, key: str) -> float:
        return statistics.mean(
            run_i26b(I26BConfig(seed=seed), policy).get(key, 0.0)
            for seed in range(6)
        )

    def test_directional_provenance_beats_record_count(self) -> None:
        self.assertLess(
            self.mean("directional_provenance", "error_rate"),
            self.mean("record_count", "error_rate") - 0.004,
        )
        self.assertGreater(
            self.mean("directional_provenance", "utility"),
            self.mean("record_count", "utility") + 0.05,
        )

    def test_symmetric_lineage_collapse_loses_directional_information(self) -> None:
        self.assertGreater(
            self.mean("symmetric_lineage", "error_rate"),
            self.mean("directional_provenance", "error_rate") + 0.04,
        )

    def test_direction_is_most_useful_when_child_departs_from_parent(self) -> None:
        self.assertLess(
            self.mean("directional_provenance", "correction_case_error"),
            self.mean("record_count", "correction_case_error") - 0.025,
        )

    def test_direction_can_be_learned_from_resolved_error_history(self) -> None:
        self.assertGreater(
            self.mean("learned_direction", "learned_parent_b_is_a"),
            0.95,
        )
        self.assertGreater(
            self.mean("learned_direction", "learned_parent_c_is_a"),
            0.95,
        )
        self.assertLess(
            self.mean("learned_direction", "direction_established_step"),
            1600.0,
        )

    def test_learned_direction_nearly_matches_known_provenance(self) -> None:
        learned = self.mean("learned_direction", "error_rate")
        known = self.mean("directional_provenance", "error_rate")
        self.assertLess(learned, self.mean("record_count", "error_rate") - 0.004)
        self.assertLess(abs(learned - known), 0.004)

    def test_independent_comparator_is_not_inferred_as_child_parent(self) -> None:
        self.assertLess(
            self.mean("learned_direction", "d_to_b_score"),
            self.mean("learned_direction", "a_to_b_score") - 0.25,
        )

    def test_bayesian_oracle_remains_a_real_information_ceiling(self) -> None:
        self.assertLess(
            self.mean("oracle", "error_rate"),
            self.mean("learned_direction", "error_rate") - 0.004,
        )


if __name__ == "__main__":
    unittest.main()
