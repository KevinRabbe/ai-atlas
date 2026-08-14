import unittest

from ai_atlas_lab.predictive_representation import (
    PredictiveRepresentationConfig,
    run_intervention_representation,
    run_objective_shift_representation,
)


def mean_metric(fn, policy, metric, seeds=10):
    values = [
        fn(PredictiveRepresentationConfig(seed=seed), policy)[metric]
        for seed in range(seeds)
    ]
    return sum(values) / len(values)


class PredictiveRepresentationTests(unittest.TestCase):
    def test_coarse_latent_is_cheaper_on_original_objective(self):
        coarse = mean_metric(
            run_objective_shift_representation,
            "coarse_latent_target",
            "initial_net_utility",
        )
        raw = mean_metric(
            run_objective_shift_representation,
            "raw_reconstruction",
            "initial_net_utility",
        )
        self.assertGreater(coarse, raw + 0.04)

    def test_coarse_latent_loses_future_objective_factor(self):
        coarse = mean_metric(
            run_objective_shift_representation,
            "coarse_latent_target",
            "future_balanced_accuracy",
        )
        dense = mean_metric(
            run_objective_shift_representation,
            "dense_latent_target",
            "future_balanced_accuracy",
        )
        self.assertLess(coarse, 0.55)
        self.assertGreater(dense, coarse + 0.25)

    def test_recoverable_source_restores_future_factor_compactly(self):
        source_accuracy = mean_metric(
            run_objective_shift_representation,
            "latent_recoverable_source",
            "future_balanced_accuracy",
        )
        source_width = mean_metric(
            run_objective_shift_representation,
            "latent_recoverable_source",
            "future_hot_width",
        )
        dense_width = mean_metric(
            run_objective_shift_representation,
            "dense_latent_target",
            "future_hot_width",
        )
        self.assertGreater(source_accuracy, 0.80)
        self.assertLess(source_width, dense_width)

    def test_passive_coarse_latent_is_not_intervention_sufficient(self):
        coarse = mean_metric(
            run_intervention_representation,
            "coarse_latent_target",
            "intervention_balanced_accuracy",
        )
        dense = mean_metric(
            run_intervention_representation,
            "dense_latent_target",
            "intervention_balanced_accuracy",
        )
        self.assertLess(coarse, 0.55)
        self.assertGreater(dense, 0.85)

    def test_all_predictive_policies_solve_passive_target(self):
        coarse = mean_metric(
            run_intervention_representation,
            "coarse_latent_target",
            "passive_balanced_accuracy",
        )
        dense = mean_metric(
            run_intervention_representation,
            "dense_latent_target",
            "passive_balanced_accuracy",
        )
        self.assertGreater(coarse, 0.90)
        self.assertAlmostEqual(coarse, dense, delta=0.01)

    def test_source_hybrid_beats_raw_lifetime_cost(self):
        source = mean_metric(
            run_intervention_representation,
            "latent_recoverable_source",
            "lifetime_net_utility",
        )
        raw = mean_metric(
            run_intervention_representation,
            "raw_reconstruction",
            "lifetime_net_utility",
        )
        self.assertGreater(source, raw + 0.015)


if __name__ == "__main__":
    unittest.main()
