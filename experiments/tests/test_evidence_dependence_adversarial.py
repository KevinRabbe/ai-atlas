import statistics
import unittest

from ai_atlas_lab.evidence_dependence_adversarial import I26CConfig, run_i26c


class EvidenceDependenceAdversarialTests(unittest.TestCase):
    def mean(
        self,
        policy: str,
        key: str,
        *,
        probe_cost: float = 0.40,
    ) -> float:
        return statistics.mean(
            run_i26c(
                I26CConfig(seed=seed, probe_cost=probe_cost),
                policy,
            ).get(key, 0.0)
            for seed in range(6)
        )

    def test_resolved_history_can_look_independent_despite_frontier_dependence(self) -> None:
        self.assertLess(
            abs(self.mean("passive_history", "resolved_history_dependence_score")),
            0.02,
        )
        self.assertLess(
            self.mean("passive_history", "passive_marks_bc_dependent"),
            0.20,
        )

    def test_passive_history_fails_to_protect_selective_frontier(self) -> None:
        self.assertGreater(
            self.mean("passive_history", "frontier_error"),
            0.30,
        )
        self.assertLess(
            abs(
                self.mean("passive_history", "frontier_error")
                - self.mean("record_count", "frontier_error")
            ),
            0.03,
        )

    def test_always_assuming_dependence_damages_ordinary_diversity(self) -> None:
        self.assertGreater(
            self.mean("always_dependent", "ordinary_error"),
            self.mean("record_count", "ordinary_error") + 0.06,
        )

    def test_stress_probe_reduces_frontier_error(self) -> None:
        self.assertLess(
            self.mean("stress_probe", "frontier_error"),
            self.mean("record_count", "frontier_error") - 0.20,
        )
        self.assertLess(
            self.mean("stress_probe", "weighted_harm"),
            self.mean("record_count", "weighted_harm") * 0.60,
        )

    def test_stress_probe_preserves_ordinary_independent_value(self) -> None:
        self.assertLess(
            abs(
                self.mean("stress_probe", "ordinary_error")
                - self.mean("record_count", "ordinary_error")
            ),
            0.01,
        )

    def test_stress_probe_nearly_matches_oracle(self) -> None:
        self.assertLess(
            abs(
                self.mean("stress_probe", "weighted_harm")
                - self.mean("oracle", "weighted_harm")
            ),
            0.01,
        )

    def test_stress_probe_is_value_priced(self) -> None:
        cheap = self.mean(
            "stress_probe",
            "dependency_probes",
            probe_cost=0.10,
        )
        expensive = self.mean(
            "stress_probe",
            "dependency_probes",
            probe_cost=10.0,
        )
        self.assertGreater(cheap, expensive + 0.005)


if __name__ == "__main__":
    unittest.main()
