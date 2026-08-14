import unittest

from ai_atlas_lab.noise_volatility import (
    NoiseVolatilityConfig,
    run_noise_volatility_experiment,
)


class NoiseVolatilityTests(unittest.TestCase):
    def test_adaptive_corroboration_reduces_false_updates_in_noisy_stable_world(self):
        rows = dict(
            run_noise_volatility_experiment(
                NoiseVolatilityConfig(
                    seed=3,
                    switch_probability=0.001,
                    sensor_reliability=0.78,
                )
            )
        )
        self.assertLess(
            rows["adaptive_corroboration"]["false_updates"],
            rows["single_sensor_adaptive"]["false_updates"],
        )
        self.assertGreater(
            rows["adaptive_corroboration"]["net_utility"],
            rows["single_sensor_adaptive"]["net_utility"],
        )

    def test_adaptive_policy_samples_secondary_sparsely_in_clean_volatile_world(self):
        rows = dict(
            run_noise_volatility_experiment(
                NoiseVolatilityConfig(
                    seed=4,
                    switch_probability=0.08,
                    sensor_reliability=0.96,
                )
            )
        )
        self.assertLess(rows["adaptive_corroboration"]["secondary_read_rate"], 0.2)

    def test_adaptive_policy_samples_secondary_sparsely_in_clean_stable_world(self):
        rows = dict(
            run_noise_volatility_experiment(
                NoiseVolatilityConfig(
                    seed=5,
                    switch_probability=0.001,
                    sensor_reliability=0.98,
                )
            )
        )
        self.assertLess(rows["adaptive_corroboration"]["secondary_read_rate"], 0.2)

    def test_always_on_corroboration_is_not_free_in_clean_volatile_world(self):
        rows = dict(
            run_noise_volatility_experiment(
                NoiseVolatilityConfig(
                    seed=6,
                    switch_probability=0.08,
                    sensor_reliability=0.96,
                )
            )
        )
        self.assertGreater(
            rows["single_sensor_adaptive"]["net_utility"],
            rows["always_corroborate"]["net_utility"],
        )


if __name__ == "__main__":
    unittest.main()
