import unittest

from ai_atlas_lab.computation_compositional import CompositionalExperimentConfig, run_compositional_integration_experiment


class CompositionalIntegrationTests(unittest.TestCase):
    def _rows(self, sharedness: float):
        rows = run_compositional_integration_experiment(
            CompositionalExperimentConfig(
                seed=7,
                sharedness=sharedness,
                train_examples=300,
                test_examples_per_task=300,
                primary_task_fraction=0.85,
                learning_rate=0.04,
            )
        )
        return {name: metrics for name, metrics, _cost in rows}

    def test_partial_and_specialist_parameter_counts_match(self):
        rows = self._rows(0.65)
        self.assertEqual(rows["shared_plus_isolated_residual"]["parameter_count"], rows["compositional_specialists"]["parameter_count"])

    def test_high_sharedness_rewards_shared_learning_with_scarce_data(self):
        rows = self._rows(0.95)
        self.assertGreater(rows["shared_only_reference"]["accuracy"], rows["compositional_specialists"]["accuracy"] + 0.08)

    def test_low_sharedness_rewards_isolation(self):
        rows = self._rows(0.25)
        self.assertGreater(rows["compositional_specialists"]["accuracy"], rows["shared_plus_isolated_residual"]["accuracy"] + 0.05)

    def test_partial_sharing_can_beat_shared_only_at_intermediate_structure(self):
        rows = self._rows(0.65)
        self.assertGreater(rows["shared_plus_isolated_residual"]["accuracy"], rows["shared_only_reference"]["accuracy"] + 0.015)


if __name__ == "__main__":
    unittest.main()
