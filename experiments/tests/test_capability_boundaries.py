import unittest

from ai_atlas_lab.capability_boundaries import (
    BEHAVIOR_ONLY,
    BROAD_HARD,
    HYBRID,
    NARROW_HARD_ONLY,
    CapabilityBoundaryConfig,
    run_capability_boundary,
)


class CapabilityBoundaryTests(unittest.TestCase):
    def _mean(self, policy, key):
        values = [
            run_capability_boundary(CapabilityBoundaryConfig(seed=seed), policy)[key]
            for seed in range(12)
        ]
        return sum(values) / len(values)

    def test_hard_boundary_eliminates_categorical_violations(self):
        self.assertEqual(self._mean(HYBRID, "invariant_violations"), 0.0)
        self.assertGreater(self._mean(BEHAVIOR_ONLY, "invariant_violations"), 100.0)

    def test_behavioral_control_degrades_after_spoof_shift(self):
        self.assertGreater(
            self._mean(BEHAVIOR_ONLY, "phase1_invariant_violations"),
            self._mean(BEHAVIOR_ONLY, "phase0_invariant_violations") * 1.20,
        )

    def test_hard_only_misses_contextual_risk(self):
        self.assertGreater(
            self._mean(NARROW_HARD_ONLY, "contextual_harms"),
            self._mean(HYBRID, "contextual_harms") * 2.5,
        )

    def test_broad_hard_boundary_blocks_more_useful_work_than_hybrid(self):
        self.assertLess(
            self._mean(BROAD_HARD, "useful_success_rate"),
            self._mean(NARROW_HARD_ONLY, "useful_success_rate"),
        )

    def test_hybrid_has_best_lifetime_utility(self):
        hybrid = self._mean(HYBRID, "net_utility_per_task")
        for policy in (BEHAVIOR_ONLY, NARROW_HARD_ONLY, BROAD_HARD):
            self.assertGreater(hybrid, self._mean(policy, "net_utility_per_task") + 1.0)


if __name__ == "__main__":
    unittest.main()
