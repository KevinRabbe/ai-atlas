import unittest

from ai_atlas_lab.self_change_regression import (
    ADVERSARIAL_ROTATING,
    FIXED_HIDDEN,
    ROTATING_HIDDEN,
    VISIBLE_ONLY,
    RegressionExposureConfig,
    run_regression_exposure,
)


class RegressionExposureTests(unittest.TestCase):
    def _mean(self, policy, key):
        values = [
            run_regression_exposure(RegressionExposureConfig(seed=seed), policy)[key]
            for seed in range(12)
        ]
        return sum(values) / len(values)

    def test_visible_only_collapses_after_distribution_shift(self):
        self.assertLess(self._mean(VISIBLE_ONLY, "post_shift_true_score"), 0.10)

    def test_fixed_hidden_can_also_become_stale(self):
        self.assertLess(self._mean(FIXED_HIDDEN, "post_shift_true_score"), 0.15)

    def test_rotating_hidden_preserves_shifted_capability(self):
        self.assertGreater(self._mean(ROTATING_HIDDEN, "post_shift_true_score"), 0.95)

    def test_rotating_hidden_rejects_most_harmful_changes(self):
        self.assertLess(
            self._mean(ROTATING_HIDDEN, "harmful_accepted"),
            self._mean(FIXED_HIDDEN, "harmful_accepted") * 0.10,
        )

    def test_adversarial_rotation_is_safer_but_more_conservative(self):
        self.assertLess(self._mean(ADVERSARIAL_ROTATING, "harmful_accepted"), 1.0)
        self.assertGreater(
            self._mean(ADVERSARIAL_ROTATING, "good_rejected"),
            self._mean(ROTATING_HIDDEN, "good_rejected") * 2.0,
        )


if __name__ == "__main__":
    unittest.main()
