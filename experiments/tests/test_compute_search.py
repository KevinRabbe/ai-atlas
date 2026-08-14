import unittest

from ai_atlas_lab.compute_search import SearchComputeConfig, run_search_compute_experiment


class ComputeSearchTests(unittest.TestCase):
    def rows(self, cost: float):
        rows = run_search_compute_experiment(SearchComputeConfig(seed=8, task_count=1500, evaluation_cost=cost))
        return {name: metrics for name, metrics, _cost in rows}

    def test_adaptive_spends_more_on_ambiguous_tasks(self):
        adaptive = self.rows(0.08)["adaptive_value_of_search"]
        self.assertGreater(adaptive["avg_evaluations_sigma_0_8"], adaptive["avg_evaluations_sigma_0_15"] + 0.8)

    def test_adaptive_spends_more_on_high_value_tasks_when_cost_matters(self):
        adaptive = self.rows(0.25)["adaptive_value_of_search"]
        self.assertGreater(adaptive["avg_evaluations_value_3_0"], adaptive["avg_evaluations_value_0_8"] + 0.1)

    def test_adaptive_reduces_work_as_evaluation_cost_rises(self):
        cheap = self.rows(0.02)["adaptive_value_of_search"]
        expensive = self.rows(0.60)["adaptive_value_of_search"]
        self.assertGreater(cheap["avg_evaluations"], expensive["avg_evaluations"] + 0.25)

    def test_adaptive_is_near_or_above_best_fixed_utility(self):
        rows = self.rows(0.25)
        adaptive = rows["adaptive_value_of_search"]["net_utility"]
        best_fixed = max(metrics["net_utility"] for name, metrics in rows.items() if name.startswith("fixed_"))
        self.assertGreaterEqual(adaptive, best_fixed - 0.02)


if __name__ == "__main__":
    unittest.main()
