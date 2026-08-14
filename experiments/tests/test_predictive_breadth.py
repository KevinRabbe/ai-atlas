import unittest

from ai_atlas_lab.predictive_breadth import (
    PredictiveBreadthConfig,
    run_predictive_breadth_experiment,
)


class PredictiveBreadthTests(unittest.TestCase):
    def rows(self, seed: int, switch_probability: float):
        return dict(
            run_predictive_breadth_experiment(
                PredictiveBreadthConfig(
                    seed=seed,
                    episodes=600,
                    goal_switch_probability=switch_probability,
                )
            )
        )

    def test_decision_sufficient_wins_when_objective_never_changes(self):
        rows = self.rows(2, 0.0)
        self.assertGreater(
            rows["decision_sufficient"]["net_utility"],
            rows["source_recoverable_hybrid"]["net_utility"],
        )
        self.assertGreater(
            rows["source_recoverable_hybrid"]["net_utility"],
            rows["broad_active"]["net_utility"],
        )

    def test_hybrid_wins_under_moderate_goal_switching(self):
        rows = self.rows(4, 0.10)
        self.assertGreater(
            rows["source_recoverable_hybrid"]["net_utility"],
            rows["broad_active"]["net_utility"],
        )
        self.assertGreater(
            rows["broad_active"]["net_utility"],
            rows["decision_sufficient"]["net_utility"],
        )

    def test_broad_hot_state_wins_when_goals_switch_rapidly(self):
        rows = self.rows(7, 0.80)
        self.assertGreater(
            rows["broad_active"]["net_utility"],
            rows["source_recoverable_hybrid"]["net_utility"],
        )

    def test_hybrid_preserves_accuracy_without_broad_hot_state(self):
        rows = self.rows(9, 0.10)
        self.assertEqual(rows["source_recoverable_hybrid"]["accuracy"], 1.0)
        self.assertEqual(rows["source_recoverable_hybrid"]["avg_active_items"], 3.0)
        self.assertEqual(rows["broad_active"]["avg_active_items"], 12.0)


if __name__ == "__main__":
    unittest.main()
