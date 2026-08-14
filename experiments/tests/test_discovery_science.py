import unittest

from ai_atlas_lab.discovery_science import ScienceDiscoveryConfig, run_science_discovery_experiment


class ScienceDiscoveryTests(unittest.TestCase):
    def test_active_experiments_cross_teacher_frontier(self):
        config = ScienceDiscoveryConfig(seed=11, task_count=3000, experiment_cost=0.05)
        rows = dict(run_science_discovery_experiment(config))
        self.assertLess(rows["teacher_passive"]["theory_accuracy"], 0.38)
        self.assertEqual(rows["active_hypothesis_science"]["theory_accuracy"], 1.0)
        self.assertEqual(rows["active_hypothesis_science"]["beyond_teacher"], 1)

    def test_active_experiments_outperform_one_fixed_experiment(self):
        config = ScienceDiscoveryConfig(seed=12, task_count=3000, experiment_cost=0.03)
        rows = dict(run_science_discovery_experiment(config))
        self.assertGreater(
            rows["active_hypothesis_science"]["theory_accuracy"],
            rows["fixed_experiment"]["theory_accuracy"],
        )
        self.assertGreater(
            rows["active_hypothesis_science"]["avg_net_utility"],
            rows["fixed_experiment"]["avg_net_utility"],
        )

    def test_multiple_theories_avoid_false_claim_cost_under_same_experiment(self):
        config = ScienceDiscoveryConfig(
            seed=15,
            task_count=4000,
            experiment_cost=0.03,
            wrong_theory_utility=-2.0,
        )
        rows = dict(run_science_discovery_experiment(config))
        self.assertGreater(
            rows["fixed_experiment_multi"]["avg_net_utility"],
            rows["fixed_experiment"]["avg_net_utility"],
        )
        self.assertGreater(rows["fixed_experiment_multi"]["unresolved_rate"], 0.5)

    def test_active_science_uses_at_most_two_experiments(self):
        config = ScienceDiscoveryConfig(seed=13, task_count=1000, experiment_cost=0.05)
        rows = dict(run_science_discovery_experiment(config))
        self.assertLessEqual(rows["active_hypothesis_science"]["avg_experiments"], 2.0)

    def test_active_science_leaves_claim_unresolved_when_experiments_cost_too_much(self):
        config = ScienceDiscoveryConfig(seed=14, task_count=1000, experiment_cost=1.0)
        rows = dict(run_science_discovery_experiment(config))
        self.assertEqual(rows["active_hypothesis_science"]["avg_experiments"], 0.0)
        self.assertEqual(rows["active_hypothesis_science"]["unresolved_rate"], 1.0)
        self.assertGreater(
            rows["active_hypothesis_science"]["avg_net_utility"],
            rows["teacher_passive"]["avg_net_utility"],
        )


if __name__ == "__main__":
    unittest.main()
