import statistics
import unittest

from ai_atlas_lab.evidence_lineage_inference import I24Config, run_i24


class EvidenceLineageInferenceTests(unittest.TestCase):
    def mean(
        self,
        policy: str,
        key: str,
        *,
        probe_cost: float = 0.05,
    ) -> float:
        return statistics.mean(
            run_i24(
                I24Config(seed=seed, probe_cost=probe_cost),
                policy,
            ).get(key, 0.0)
            for seed in range(6)
        )

    def test_learned_lineage_beats_record_count_confidence(self) -> None:
        self.assertGreater(
            self.mean("learned", "utility"),
            self.mean("record_count", "utility") + 0.015,
        )
        self.assertLess(
            self.mean("learned", "weighted_harm"),
            self.mean("record_count", "weighted_harm") * 0.85,
        )

    def test_learned_lineage_beats_assume_everything_correlated(self) -> None:
        self.assertGreater(
            self.mean("learned", "utility"),
            self.mean("all_correlated", "utility") + 0.10,
        )
        self.assertLess(
            self.mean("learned", "independent_audits"),
            self.mean("all_correlated", "independent_audits") * 0.65,
        )

    def test_hidden_lineages_are_learned_from_resolved_outcomes(self) -> None:
        self.assertGreater(
            self.mean("learned", "pair_accuracy_pre_shift"),
            0.90,
        )
        self.assertGreater(
            self.mean("learned", "pair_accuracy_late_post_shift"),
            0.88,
        )

    def test_hidden_upstream_change_temporarily_breaks_old_lineage_model(self) -> None:
        pre = self.mean("learned", "pair_accuracy_pre_shift")
        early = self.mean("learned", "pair_accuracy_early_post_shift")
        late = self.mean("learned", "pair_accuracy_late_post_shift")
        self.assertGreater(pre, early + 0.20)
        self.assertGreater(late, early + 0.20)

    def test_active_dependency_probe_accelerates_post_shift_recovery(self) -> None:
        learned_early = self.mean(
            "learned",
            "pair_accuracy_early_post_shift",
        )
        probed_early = self.mean(
            "learned_probe",
            "pair_accuracy_early_post_shift",
        )
        self.assertGreater(probed_early, learned_early + 0.10)
        self.assertLess(
            self.mean("learned_probe", "weighted_harm"),
            self.mean("learned", "weighted_harm"),
        )

    def test_dependency_probe_is_value_priced(self) -> None:
        cheap = self.mean(
            "learned_probe",
            "lineage_probes",
            probe_cost=0.01,
        )
        expensive = self.mean(
            "learned_probe",
            "lineage_probes",
            probe_cost=0.50,
        )
        self.assertGreater(cheap, expensive + 0.15)

    def test_oracle_lineage_is_still_a_real_ceiling(self) -> None:
        self.assertLessEqual(
            self.mean("oracle", "weighted_harm"),
            self.mean("learned", "weighted_harm") + 0.01,
        )


if __name__ == "__main__":
    unittest.main()
