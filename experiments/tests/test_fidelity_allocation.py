import unittest

from ai_atlas_lab.fidelity_allocation import (
    FidelityConfig,
    run_threshold_fidelity,
    run_trajectory_fidelity,
)


def mean_metric(fn, variant, metric, seeds=12):
    values = [fn(FidelityConfig(seed=seed), variant)[metric] for seed in range(seeds)]
    return sum(values) / len(values)


class FidelityAllocationTests(unittest.TestCase):
    def test_threshold_adaptive_beats_uniform_high_utility(self):
        adaptive = mean_metric(run_threshold_fidelity, "adaptive", "net_utility_per_task")
        high = mean_metric(run_threshold_fidelity, "high", "net_utility_per_task")
        self.assertGreater(adaptive, high + 0.03)

    def test_threshold_adaptive_preserves_exact_decision_quality(self):
        error = mean_metric(run_threshold_fidelity, "adaptive", "error_rate")
        high_rate = mean_metric(run_threshold_fidelity, "adaptive", "high_fidelity_rate")
        self.assertEqual(error, 0.0)
        self.assertLess(high_rate, 0.25)

    def test_threshold_consequence_increases_fidelity(self):
        low = mean_metric(run_threshold_fidelity, "adaptive", "high_rate_consequence_1")
        high = mean_metric(run_threshold_fidelity, "adaptive", "high_rate_consequence_6")
        self.assertGreater(high, low + 0.20)

    def test_trajectory_adaptive_beats_uniform_high(self):
        adaptive = mean_metric(run_trajectory_fidelity, "adaptive", "net_utility_per_episode")
        high = mean_metric(run_trajectory_fidelity, "high", "net_utility_per_episode")
        self.assertGreater(adaptive, high + 0.03)

    def test_trajectory_adaptive_controls_compounding_error(self):
        adaptive_error = mean_metric(run_trajectory_fidelity, "adaptive", "error_rate")
        low_error = mean_metric(run_trajectory_fidelity, "low", "error_rate")
        self.assertLess(adaptive_error, 0.01)
        self.assertLess(adaptive_error, low_error * 0.10)

    def test_trajectory_high_consequence_gets_more_exact_replay(self):
        low = mean_metric(run_trajectory_fidelity, "adaptive", "high_rate_consequence_4")
        high = mean_metric(run_trajectory_fidelity, "adaptive", "high_rate_consequence_12")
        self.assertGreater(high, low + 0.15)


if __name__ == "__main__":
    unittest.main()
