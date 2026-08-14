import unittest

from ai_atlas_lab.transition_kernel import (
    FLAT_SHARED,
    TYPED_SHARED,
    TYPED_SILOED,
    TransitionKernelConfig,
    run_transition_kernel,
)


class TransitionKernelTests(unittest.TestCase):
    def _mean(self, variant, key):
        values = [
            run_transition_kernel(TransitionKernelConfig(seed=seed), variant)[key]
            for seed in range(12)
        ]
        return sum(values) / len(values)

    def test_typed_shared_beats_flattened_lifetime_utility(self):
        self.assertGreater(
            self._mean(TYPED_SHARED, "net_utility_per_task"),
            self._mean(FLAT_SHARED, "net_utility_per_task") + 0.8,
        )

    def test_flattening_creates_authority_boundary_violations(self):
        self.assertEqual(self._mean(TYPED_SHARED, "boundary_violations"), 0.0)
        self.assertGreater(self._mean(FLAT_SHARED, "boundary_violations"), 100.0)

    def test_typed_shared_prevents_most_false_durable_writes(self):
        self.assertLess(
            self._mean(TYPED_SHARED, "false_durable_writes"),
            self._mean(FLAT_SHARED, "false_durable_writes") * 0.08,
        )

    def test_shared_typed_allocator_beats_fixed_typed_silos(self):
        self.assertGreater(
            self._mean(TYPED_SHARED, "net_utility_per_task"),
            self._mean(TYPED_SILOED, "net_utility_per_task") + 0.10,
        )

    def test_shared_allocator_reallocates_verification_after_mix_shift(self):
        before = self._mean(TYPED_SHARED, "phase0_verify_alloc_per_task")
        after = self._mean(TYPED_SHARED, "phase1_verify_alloc_per_task")
        self.assertGreater(after, before * 1.5)


if __name__ == "__main__":
    unittest.main()
