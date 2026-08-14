import unittest

from ai_atlas_lab.self_change_regression_long_horizon import (
    ADVERSARIAL_ROTATING,
    FIXED_HIDDEN,
    ROTATING_HIDDEN,
    VISIBLE_ONLY,
    LongHorizonRegressionConfig,
    run_long_horizon_regression,
)


class LongHorizonRegressionTests(unittest.TestCase):
    def _mean(self, policy, key):
        values = [
            run_long_horizon_regression(LongHorizonRegressionConfig(seed=seed), policy)[key]
            for seed in range(12)
        ]
        return sum(values) / len(values)

    def test_visible_short_tests_miss_long_horizon_instability(self):
        self.assertLess(self._mean(VISIBLE_ONLY, "post_shift_true_score"), 0.15)

    def test_fixed_short_hidden_suite_also_misses_long_horizon_instability(self):
        self.assertLess(self._mean(FIXED_HIDDEN, "post_shift_true_score"), 0.20)

    def test_rotating_horizon_preserves_long_session_capability(self):
        self.assertGreater(self._mean(ROTATING_HIDDEN, "post_shift_true_score"), 0.85)

    def test_rotating_horizon_reduces_harmful_accepted_changes(self):
        self.assertLess(
            self._mean(ROTATING_HIDDEN, "harmful_accepted"),
            self._mean(FIXED_HIDDEN, "harmful_accepted") * 0.30,
        )

    def test_adversarial_horizon_is_safer_but_more_conservative(self):
        self.assertLess(self._mean(ADVERSARIAL_ROTATING, "harmful_accepted"), 1.0)
        self.assertGreater(
            self._mean(ADVERSARIAL_ROTATING, "good_rejected"),
            self._mean(ROTATING_HIDDEN, "good_rejected") * 5.0,
        )


if __name__ == "__main__":
    unittest.main()
