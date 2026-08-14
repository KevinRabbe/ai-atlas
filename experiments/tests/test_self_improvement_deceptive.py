import unittest
from ai_atlas_lab.self_improvement_deceptive import DeceptiveLineageConfig, run_deceptive_lineage


class DeceptiveLineageTests(unittest.TestCase):
    def _mean(self, policy, key):
        vals = [
            run_deceptive_lineage(DeceptiveLineageConfig(seed=s), policy)[key]
            for s in range(20)
        ]
        return sum(vals) / len(vals)

    def test_greedy_stays_at_local_optimum(self):
        self.assertEqual(self._mean("greedy_incumbent", "best_score"), 10.0)

    def test_archive_crosses_deceptive_valley(self):
        self.assertGreater(self._mean("bounded_archive", "reached_global"), 0.9)

    def test_archive_reaches_score_above_teacher_local_optimum(self):
        self.assertGreater(self._mean("bounded_archive", "best_score"), 14.0)

    def test_archive_cost_is_explicit(self):
        self.assertGreater(self._mean("bounded_archive", "archive_cost_per_round"), 0.0)

    def test_greedy_retains_only_one_variant(self):
        self.assertEqual(self._mean("greedy_incumbent", "retained_variants"), 1.0)


if __name__ == "__main__":
    unittest.main()
