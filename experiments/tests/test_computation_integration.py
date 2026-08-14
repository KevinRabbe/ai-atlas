import unittest

from ai_atlas_lab.computation_integration import ComputationIntegrationExperimentConfig, run_computation_integration_experiment


class ComputationIntegrationTests(unittest.TestCase):
    def _run(self, sharedness: float):
        rows = run_computation_integration_experiment(ComputationIntegrationExperimentConfig(seed=7, sharedness=sharedness, train_examples=1200, test_examples_per_task=350, adaptation_examples=260, primary_task_fraction=0.80))
        return {name: metrics for name, metrics, _cost in rows}

    def test_parameter_counts_are_matched(self):
        rows = self._run(0.9)
        self.assertEqual(rows["integrated_shared_low_rank"]["parameter_count"], rows["heterogeneous_specialists"]["parameter_count"])

    def test_shared_structure_can_favor_integrated_transfer(self):
        rows = self._run(0.98)
        self.assertGreaterEqual(rows["integrated_shared_low_rank"]["accuracy"], rows["heterogeneous_specialists"]["accuracy"] - 0.01)

    def test_divergent_structure_favors_specialists(self):
        rows = self._run(0.15)
        self.assertGreater(rows["heterogeneous_specialists"]["accuracy"], rows["integrated_shared_low_rank"]["accuracy"] + 0.06)

    def test_shared_state_exposes_cross_task_update_interference(self):
        rows = self._run(0.90)
        self.assertGreater(rows["integrated_shared_low_rank"]["other_task_absolute_interference_after_task0_shift"], rows["heterogeneous_specialists"]["other_task_absolute_interference_after_task0_shift"] + 0.03)


if __name__ == "__main__":
    unittest.main()
