import unittest

from ai_atlas_lab.belief_hypotheses import BeliefExperimentConfig, run_belief_experiment


class BeliefHypothesisTests(unittest.TestCase):
    def test_multiple_hypotheses_reduce_bad_commitments_when_ambiguous(self):
        config = BeliefExperimentConfig(seed=3, task_count=4000, reliability=0.56)
        rows = dict(run_belief_experiment(config))
        self.assertLess(
            rows["multiple_hypotheses"]["wrong_commit_rate"],
            rows["single_belief"]["wrong_commit_rate"],
        )
        self.assertGreater(
            rows["multiple_hypotheses"]["avg_utility"],
            rows["single_belief"]["avg_utility"],
        )

    def test_single_belief_recovers_when_evidence_is_clear(self):
        config = BeliefExperimentConfig(seed=4, task_count=4000, reliability=0.97)
        rows = dict(run_belief_experiment(config))
        self.assertGreater(rows["single_belief"]["avg_utility"], 0.85)
        self.assertGreater(rows["multiple_hypotheses"]["avg_utility"], 0.85)

    def test_multiple_hypotheses_pay_more_active_state(self):
        config = BeliefExperimentConfig(seed=1, task_count=100, reliability=0.7)
        rows = dict(run_belief_experiment(config))
        self.assertEqual(rows["single_belief"]["avg_active_hypothesis_items"], 1.0)
        self.assertEqual(rows["multiple_hypotheses"]["avg_active_hypothesis_items"], 4.0)


if __name__ == "__main__":
    unittest.main()
