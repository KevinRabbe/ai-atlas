import unittest

from ai_atlas_lab.capability_boundaries_dynamic import (
    BEHAVIOR_ONLY,
    LIVE_HYBRID,
    STATIC_HYBRID,
    VERSIONED_HYBRID,
    DynamicAuthorityConfig,
    run_dynamic_authority,
)


class DynamicAuthorityTests(unittest.TestCase):
    def _mean(self, policy, key):
        values = [
            run_dynamic_authority(DynamicAuthorityConfig(seed=seed), policy)[key]
            for seed in range(12)
        ]
        return sum(values) / len(values)

    def test_static_boundary_becomes_stale(self):
        self.assertGreater(self._mean(STATIC_HYBRID, "invariant_violations"), 500.0)

    def test_live_and_versioned_boundaries_hold_zero_violations(self):
        self.assertEqual(self._mean(LIVE_HYBRID, "invariant_violations"), 0.0)
        self.assertEqual(self._mean(VERSIONED_HYBRID, "invariant_violations"), 0.0)

    def test_versioned_boundary_refreshes_sparsely(self):
        self.assertLess(self._mean(VERSIONED_HYBRID, "refreshes_per_task"), 0.03)
        self.assertEqual(self._mean(VERSIONED_HYBRID, "live_lookups_per_task"), 0.0)

    def test_versioned_boundary_beats_always_live_utility(self):
        self.assertGreater(
            self._mean(VERSIONED_HYBRID, "net_utility_per_task"),
            self._mean(LIVE_HYBRID, "net_utility_per_task"),
        )

    def test_behavior_only_is_worst_on_categorical_authority(self):
        self.assertGreater(
            self._mean(BEHAVIOR_ONLY, "invariant_violations"),
            self._mean(STATIC_HYBRID, "invariant_violations"),
        )


if __name__ == "__main__":
    unittest.main()
