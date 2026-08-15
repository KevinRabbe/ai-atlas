import statistics
import unittest

from ai_atlas_lab.evidence_lineage_confounding import I25Config, run_i25


class EvidenceLineageConfoundingTests(unittest.TestCase):
    def mean(
        self,
        policy: str,
        key: str,
        *,
        probe_cost: float = 0.08,
    ) -> float:
        return statistics.mean(
            run_i25(
                I25Config(seed=seed, probe_cost=probe_cost),
                policy,
            ).get(key, 0.0)
            for seed in range(6)
        )

    def test_conditioning_on_difficulty_beats_raw_cofailure(self) -> None:
        self.assertGreater(
            self.mean("difficulty_conditioned", "utility"),
            self.mean("raw_cofailure", "utility") + 0.02,
        )

    def test_raw_cofailure_overbuys_audits_under_global_difficulty(self) -> None:
        self.assertLess(
            self.mean("difficulty_conditioned", "independent_audits"),
            self.mean("raw_cofailure", "independent_audits") * 0.90,
        )

    def test_conditioned_lineage_recovers_better_after_hidden_shift(self) -> None:
        self.assertGreater(
            self.mean("difficulty_conditioned", "pair_accuracy_early_post_shift"),
            self.mean("raw_cofailure", "pair_accuracy_early_post_shift") + 0.04,
        )
        self.assertGreater(
            self.mean("difficulty_conditioned", "pair_accuracy_late_post_shift"),
            self.mean("raw_cofailure", "pair_accuracy_late_post_shift") + 0.02,
        )

    def test_active_controlled_probe_reduces_harm(self) -> None:
        self.assertLess(
            self.mean("conditioned_probe", "weighted_harm"),
            self.mean("difficulty_conditioned", "weighted_harm") - 0.005,
        )

    def test_active_probe_nearly_closes_lineage_identification_gap(self) -> None:
        self.assertGreater(
            self.mean("conditioned_probe", "pair_accuracy_pre_shift"),
            0.97,
        )
        self.assertGreater(
            self.mean("conditioned_probe", "pair_accuracy_early_post_shift"),
            0.90,
        )
        self.assertGreater(
            self.mean("conditioned_probe", "pair_accuracy_late_post_shift"),
            0.97,
        )

    def test_dependency_probe_usage_falls_when_probe_is_expensive(self) -> None:
        cheap = self.mean(
            "conditioned_probe",
            "dependency_probes",
            probe_cost=0.02,
        )
        expensive = self.mean(
            "conditioned_probe",
            "dependency_probes",
            probe_cost=0.60,
        )
        self.assertGreater(cheap, expensive + 0.10)

    def test_oracle_remains_the_information_ceiling_on_utility(self) -> None:
        self.assertGreaterEqual(
            self.mean("oracle", "utility") + 0.02,
            self.mean("difficulty_conditioned", "utility"),
        )


if __name__ == "__main__":
    unittest.main()
