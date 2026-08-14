import unittest

from ai_atlas_lab.cross_resource import CrossResourceConfig, run_cross_resource_experiment


class CrossResourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = run_cross_resource_experiment(CrossResourceConfig(seed=21))
        cls.rows = {name: metrics for name, metrics, _cost in rows}

    def test_adaptive_controller_reduces_post_shift_regret(self):
        adaptive = self.rows["adaptive_cross_resource"]
        frozen = self.rows["frozen_initial_economics"]
        self.assertLess(adaptive["post_shift_mean_regret"], frozen["post_shift_mean_regret"] * 0.2)

    def test_resource_substitution_changes_with_prices(self):
        adaptive = self.rows["adaptive_cross_resource"]
        self.assertGreater(adaptive["choice_observe_regime_1"], adaptive["choice_observe_regime_0"] + 0.5)
        self.assertGreater(adaptive["choice_verify_regime_2"], adaptive["choice_verify_regime_0"] + 0.2)

    def test_local_bids_match_adaptive_choice_quality_but_cost_messages(self):
        adaptive = self.rows["adaptive_cross_resource"]
        local = self.rows["resource_local_bids"]
        self.assertLess(abs(adaptive["post_shift_mean_regret"] - local["post_shift_mean_regret"]), 1e-9)
        self.assertGreater(local["messages_per_measured_task"], adaptive["messages_per_measured_task"] + 4)

    def test_pre_shift_adaptive_and_frozen_economics_match(self):
        adaptive = self.rows["adaptive_cross_resource"]
        frozen = self.rows["frozen_initial_economics"]
        self.assertLess(abs(adaptive["expected_utility_regime_0"] - frozen["expected_utility_regime_0"]), 1e-9)


if __name__ == "__main__":
    unittest.main()
