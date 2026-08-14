import unittest

from ai_atlas_lab.adaptive_compute import (
    AdaptiveComputeExperimentConfig,
    AdaptiveComputePolicy,
    evaluate_compute_policy,
    run_adaptive_compute_experiment,
)
from ai_atlas_lab.environments.noisy_evidence import generate_evidence_tasks


class AdaptiveComputeTests(unittest.TestCase):
    def test_adaptive_policy_respects_max_budget(self) -> None:
        tasks = generate_evidence_tasks(seed=4, count=100)
        metrics, _ = evaluate_compute_policy(
            AdaptiveComputePolicy(threshold=1.75, min_samples=2, max_samples=9), tasks
        )
        self.assertLessEqual(metrics["avg_samples"], 9)
        self.assertEqual(metrics["max_samples"], 9)

    def test_easy_tasks_receive_less_compute_than_hard_tasks(self) -> None:
        tasks = generate_evidence_tasks(seed=8, count=3000)
        metrics, _ = evaluate_compute_policy(
            AdaptiveComputePolicy(threshold=1.75, min_samples=2, max_samples=15), tasks
        )
        easy = metrics["avg_samples_signal_1_75"]
        hard = metrics["avg_samples_signal_0_45"]
        self.assertLess(easy, hard)

    def test_experiment_contains_fixed_and_adaptive_variants(self) -> None:
        rows = run_adaptive_compute_experiment(
            AdaptiveComputeExperimentConfig(seed=1, task_count=100, fixed_samples=(2, 5), max_samples=8)
        )
        names = [row[0] for row in rows]
        self.assertEqual(names[:2], ["fixed_2", "fixed_5"])
        self.assertTrue(names[-1].startswith("adaptive_"))


if __name__ == "__main__":
    unittest.main()
