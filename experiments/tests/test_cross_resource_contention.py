import unittest

from ai_atlas_lab.cross_resource_contention import (
    CrossResourceContentionConfig,
    run_cross_resource_contention_experiment,
)


class CrossResourceContentionTests(unittest.TestCase):
    def test_capacity_coordination_reduces_initial_contention_regret(self):
        rows = dict(
            run_cross_resource_contention_experiment(
                CrossResourceContentionConfig(seed=2, measured_rounds_per_regime=120)
            )
        )
        self.assertLess(
            rows["frozen_joint"]["reference_regret_regime_0"],
            rows["frozen_independent"]["reference_regret_regime_0"],
        )

    def test_quality_adaptation_improves_joint_post_shift_regret(self):
        rows = dict(
            run_cross_resource_contention_experiment(
                CrossResourceContentionConfig(seed=7, measured_rounds_per_regime=120)
            )
        )
        self.assertLess(
            rows["adaptive_joint"]["post_shift_mean_regret"],
            rows["frozen_joint"]["post_shift_mean_regret"],
        )

    def test_joint_adaptation_beats_capacity_blind_local_adaptation(self):
        rows = dict(
            run_cross_resource_contention_experiment(
                CrossResourceContentionConfig(seed=11, measured_rounds_per_regime=120)
            )
        )
        self.assertLess(
            rows["adaptive_joint"]["post_shift_mean_regret"],
            rows["adaptive_independent"]["post_shift_mean_regret"],
        )

    def test_joint_coordination_cost_is_explicit(self):
        rows = dict(
            run_cross_resource_contention_experiment(
                CrossResourceContentionConfig(seed=3, measured_rounds_per_regime=60)
            )
        )
        self.assertEqual(rows["adaptive_joint"]["messages_per_task_regime_1"], 4.0)
        self.assertEqual(rows["adaptive_independent"]["messages_per_task_regime_1"], 0.0)


if __name__ == "__main__":
    unittest.main()
