import statistics
import unittest

from ai_atlas_lab.topology_assurance import I09Config, run_i09


class TopologyAssuranceTests(unittest.TestCase):
    def configs(self, **overrides):
        return [I09Config(seed=seed, **overrides) for seed in range(6)]

    def mean(self, policy: str, key: str, adversarial: bool = True, **overrides) -> float:
        return statistics.mean(
            float(run_i09(config, policy, adversarial=adversarial)[key])
            for config in self.configs(**overrides)
        )

    def test_correlated_spoofing_degrades_raw_topology(self) -> None:
        honest = self.mean("raw", "pairwise_scope_accuracy", adversarial=False)
        attacked = self.mean("raw", "pairwise_scope_accuracy", adversarial=True)
        self.assertGreater(honest, attacked + 0.06)

    def test_high_threshold_does_not_remove_correlated_spoof_failure(self) -> None:
        self.assertGreater(
            self.mean("high_threshold", "harmful_migrations"),
            5.0,
        )

    def test_selective_independent_assurance_blocks_harmful_migrations(self) -> None:
        self.assertEqual(
            self.mean("selective_independent", "harmful_migrations"),
            0.0,
        )
        self.assertGreater(
            self.mean("selective_independent", "pairwise_scope_accuracy"),
            self.mean("raw", "pairwise_scope_accuracy") + 0.07,
        )

    def test_selective_assurance_beats_raw_under_attack_at_default_prices(self) -> None:
        self.assertGreater(
            self.mean("selective_independent", "net_utility_per_step"),
            self.mean("raw", "net_utility_per_step") + 0.003,
        )

    def test_assurance_is_not_free_when_primary_evidence_is_honest(self) -> None:
        self.assertGreater(
            self.mean("raw", "net_utility_per_step", adversarial=False),
            self.mean("selective_independent", "net_utility_per_step", adversarial=False) + 0.003,
        )

    def test_uniform_vs_selective_assurance_crosses_over_with_audit_price(self) -> None:
        cheap_uniform = self.mean(
            "uniform_independent",
            "net_utility_per_step",
            audit_cost=0.00025,
        )
        cheap_selective = self.mean(
            "selective_independent",
            "net_utility_per_step",
            audit_cost=0.00025,
        )
        expensive_uniform = self.mean(
            "uniform_independent",
            "net_utility_per_step",
            audit_cost=0.00080,
        )
        expensive_selective = self.mean(
            "selective_independent",
            "net_utility_per_step",
            audit_cost=0.00080,
        )
        self.assertGreater(cheap_uniform, cheap_selective)
        self.assertGreater(expensive_selective, expensive_uniform + 0.003)
        self.assertLess(
            self.mean("selective_independent", "audit_samples_per_step"),
            self.mean("uniform_independent", "audit_samples_per_step") * 0.30,
        )


if __name__ == "__main__":
    unittest.main()
