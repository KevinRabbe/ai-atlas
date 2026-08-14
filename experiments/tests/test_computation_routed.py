import unittest

from ai_atlas_lab.computation_routed import RoutedConfig, run_routed_integration_experiment


class RoutedIntegrationTests(unittest.TestCase):
    def test_parameter_count_is_matched(self):
        rows = dict(run_routed_integration_experiment(RoutedConfig(seed=1, train_examples=300)))
        self.assertEqual(
            rows["Specialists"]["parameter_count"],
            rows["RoutedSharedPrivate"]["parameter_count"],
        )

    def test_routed_training_compute_does_not_exceed_specialists(self):
        rows = dict(run_routed_integration_experiment(RoutedConfig(seed=2, train_examples=500)))
        self.assertLessEqual(
            rows["RoutedSharedPrivate"]["operations_per_train_example"],
            rows["Specialists"]["operations_per_train_example"],
        )
        self.assertLessEqual(
            rows["RoutedSharedPrivate"]["operations_per_test_example"],
            rows["Specialists"]["operations_per_test_example"],
        )

    def test_high_sharedness_can_route_to_shared_path(self):
        rows = dict(
            run_routed_integration_experiment(
                RoutedConfig(seed=3, sharedness=0.98, train_examples=600)
            )
        )
        self.assertGreater(rows["RoutedSharedPrivate"]["shared_train_route_rate"], 0.15)

    def test_low_sharedness_retains_private_route(self):
        rows = dict(
            run_routed_integration_experiment(
                RoutedConfig(seed=4, sharedness=0.15, train_examples=800)
            )
        )
        private_tasks = sum(
            1 - rows["RoutedSharedPrivate"][f"task_{task}_route_shared"]
            for task in range(3)
        )
        self.assertGreaterEqual(private_tasks, 1)


if __name__ == "__main__":
    unittest.main()
