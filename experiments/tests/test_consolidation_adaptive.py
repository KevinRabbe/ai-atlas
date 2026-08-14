import unittest

from ai_atlas_lab.consolidation_adaptive import VolatilityExperimentConfig, run_adaptive_volatility_experiment


class AdaptiveVolatilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = run_adaptive_volatility_experiment(VolatilityExperimentConfig(seed=17))
        cls.rows = {name: metrics for name, metrics, _cost in rows}

    def test_threshold_tracks_volatility_without_hidden_labels(self):
        adaptive = self.rows["adaptive_volatility_threshold"]
        self.assertGreater(adaptive["avg_threshold_segment_0"], adaptive["avg_threshold_segment_1"] + 1.0)
        self.assertGreater(adaptive["avg_threshold_segment_2"], adaptive["avg_threshold_segment_3"] + 1.0)

    def test_adaptive_beats_high_fixed_threshold_on_volatile_segments(self):
        adaptive = self.rows["adaptive_volatility_threshold"]
        high = self.rows["evidence_t4.4"]
        self.assertGreater(adaptive["accuracy_segment_1"], high["accuracy_segment_1"] + 0.08)
        self.assertGreater(adaptive["accuracy_segment_3"], high["accuracy_segment_3"] + 0.08)

    def test_adaptive_reduces_false_updates_vs_low_threshold(self):
        adaptive = self.rows["adaptive_volatility_threshold"]
        low = self.rows["evidence_t1.8"]
        self.assertLess(adaptive["false_updates"], low["false_updates"] * 0.5)

    def test_adaptive_has_shorter_delay_than_conservative_fixed_policy(self):
        adaptive = self.rows["adaptive_volatility_threshold"]
        conservative = self.rows["evidence_t3.4"]
        self.assertLess(adaptive["avg_switch_delay"], conservative["avg_switch_delay"])


if __name__ == "__main__":
    unittest.main()
