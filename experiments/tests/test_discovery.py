import unittest

from ai_atlas_lab.discovery import (
    DiscoveryExperimentConfig,
    DiscoveryLandscape,
    run_discovery_experiment,
    run_diverse_archive,
    run_epistemic_lifecycle,
    run_greedy_visible,
)


class DiscoveryTests(unittest.TestCase):
    def test_teacher_is_deceptive_local_optimum(self):
        landscape = DiscoveryLandscape()
        self.assertEqual(landscape.hidden_score(landscape.teacher), 10)
        self.assertEqual(landscape.hidden_score(landscape.optimum), 15)
        for bit in range(landscape.width):
            candidate = list(landscape.teacher)
            candidate[bit] = 1
            self.assertLess(landscape.hidden_score(tuple(candidate)), 10)

    def test_greedy_stays_at_teacher_frontier_but_diversity_crosses_it(self):
        landscape = DiscoveryLandscape()
        greedy, _ = run_greedy_visible(landscape, seed=0, proposal_budget=1000)
        diverse, _ = run_diverse_archive(landscape, seed=0, proposal_budget=1000)
        self.assertEqual(greedy["selected_hidden_score"], 10)
        self.assertGreater(diverse["selected_hidden_score"], 10)

    def test_visible_evaluator_can_be_exploited(self):
        landscape = DiscoveryLandscape(evaluator_defect_bonus=8)
        diverse, _ = run_diverse_archive(landscape, seed=0, proposal_budget=1500)
        self.assertGreater(diverse["selected_visible_score"], 10)
        self.assertLessEqual(diverse["selected_hidden_score"], 10)
        self.assertEqual(diverse["false_discovery"], 1)

    def test_hidden_verification_blocks_false_promotion_and_still_exceeds_teacher(self):
        landscape = DiscoveryLandscape(evaluator_defect_bonus=8)
        lifecycle, _ = run_epistemic_lifecycle(
            landscape,
            seed=0,
            proposal_budget=1500,
            verification_budget=100,
            remember_rejections=True,
        )
        self.assertGreater(lifecycle["selected_hidden_score"], 10)
        self.assertEqual(lifecycle["false_discovery"], 0)
        self.assertGreater(lifecycle["rejected_candidates"], 0)

    def test_negative_memory_avoids_repeat_failed_verification(self):
        landscape = DiscoveryLandscape(evaluator_defect_bonus=8)
        remembered, remembered_cost = run_epistemic_lifecycle(
            landscape,
            seed=0,
            proposal_budget=1500,
            verification_budget=100,
            remember_rejections=True,
        )
        forgotten, forgotten_cost = run_epistemic_lifecycle(
            landscape,
            seed=0,
            proposal_budget=1500,
            verification_budget=100,
            remember_rejections=False,
        )
        self.assertEqual(remembered["duplicate_failed_verifications"], 0)
        self.assertGreater(forgotten["duplicate_failed_verifications"], 0)
        self.assertLess(remembered_cost.verifications, forgotten_cost.verifications)

    def test_experiment_runner_has_all_variants(self):
        rows = run_discovery_experiment(
            DiscoveryExperimentConfig(seed=0, proposal_budget=300, evaluator_defect_bonus=0)
        )
        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[0][0], "teacher_imitation")


if __name__ == "__main__":
    unittest.main()
