import unittest

from ai_atlas_lab.active_information import ActiveInfoConfig, run_active_information_experiment


class ActiveInformationTests(unittest.TestCase):
    def test_lookahead_beats_passive_when_probes_are_cheap(self):
        config = ActiveInfoConfig(seed=7, task_count=1200, probe_cost=0.04)
        rows = dict(run_active_information_experiment(config))
        self.assertGreater(
            rows["value_of_information"]["avg_net_utility"],
            rows["passive"]["avg_net_utility"],
        )
        self.assertGreater(rows["value_of_information"]["avg_queries"], 0.0)

    def test_lookahead_stops_querying_when_probes_are_expensive(self):
        config = ActiveInfoConfig(seed=8, task_count=800, probe_cost=2.0)
        rows = dict(run_active_information_experiment(config))
        self.assertEqual(rows["value_of_information"]["avg_queries"], 0.0)

    def test_lookahead_can_value_complementary_probe_pair(self):
        config = ActiveInfoConfig(seed=9, task_count=1200, probe_cost=0.08)
        rows = dict(run_active_information_experiment(config))
        self.assertGreater(
            rows["value_of_information"]["avg_queries"],
            rows["voi_myopic"]["avg_queries"],
        )
        self.assertGreater(
            rows["value_of_information"]["avg_net_utility"],
            rows["voi_myopic"]["avg_net_utility"],
        )

    def test_lookahead_avoids_fixed_cost_when_probes_are_not_worth_it(self):
        config = ActiveInfoConfig(seed=10, task_count=1200, probe_cost=0.60)
        rows = dict(run_active_information_experiment(config))
        self.assertLess(
            rows["value_of_information"]["avg_queries"],
            rows["fixed_both"]["avg_queries"],
        )
        self.assertGreater(
            rows["value_of_information"]["avg_net_utility"],
            rows["fixed_both"]["avg_net_utility"],
        )


if __name__ == "__main__":
    unittest.main()
