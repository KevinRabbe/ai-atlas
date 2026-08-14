import unittest

from ai_atlas_lab.structural_development import (
    StructuralDevelopmentConfig,
    run_structural_development,
)


def mean_metric(family, variant, metric, seeds=12):
    values = [
        run_structural_development(
            StructuralDevelopmentConfig(seed=seed),
            family,
            variant,
        )[metric]
        for seed in range(seeds)
    ]
    return sum(values) / len(values)


class StructuralDevelopmentTests(unittest.TestCase):
    def test_indirect_structure_wins_on_repeated_regular_structure(self):
        indirect = mean_metric("regular_repeated", "adaptive_indirect", "net_utility_per_round")
        direct = mean_metric("regular_repeated", "direct", "net_utility_per_round")
        self.assertGreater(indirect, direct + 0.08)

    def test_direct_beats_always_generative_on_irregular_local_change(self):
        direct = mean_metric("irregular_local", "direct", "net_utility_per_round")
        generative = mean_metric("irregular_local", "generative", "net_utility_per_round")
        self.assertGreater(direct, generative + 0.004)

    def test_adaptive_indirect_matches_direct_when_global_rule_has_no_value(self):
        adaptive = mean_metric("irregular_local", "adaptive_indirect", "net_utility_per_round")
        direct = mean_metric("irregular_local", "direct", "net_utility_per_round")
        self.assertGreaterEqual(adaptive, direct - 0.002)

    def test_adaptive_indirect_recovers_coherent_shift_quickly(self):
        adaptive = mean_metric("regular_repeated", "adaptive_indirect", "first10_after_shift")
        direct = mean_metric("regular_repeated", "direct", "first10_after_shift")
        self.assertGreater(adaptive, 0.95)
        self.assertGreater(adaptive, direct + 0.70)

    def test_regular_indirect_encoding_is_compact(self):
        indirect = mean_metric("regular_repeated", "adaptive_indirect", "final_parameters")
        direct = mean_metric("regular_repeated", "direct", "final_parameters")
        self.assertLess(indirect, direct * 0.2)


if __name__ == "__main__":
    unittest.main()
