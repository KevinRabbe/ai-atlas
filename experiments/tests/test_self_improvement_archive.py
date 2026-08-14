import unittest
from ai_atlas_lab.self_improvement_archive import ArchiveLineageConfig, run_lineage_archive


class ArchiveLineageTests(unittest.TestCase):
    def _mean(self, switching, policy, key):
        vals = [
            run_lineage_archive(ArchiveLineageConfig(seed=s, switching=switching), policy)[key]
            for s in range(12)
        ]
        return sum(vals) / len(vals)

    def test_greedy_wins_stationary_after_archive_cost(self):
        self.assertGreater(
            self._mean(False, "greedy_incumbent", "net_performance"),
            self._mean(False, "bounded_archive", "net_performance"),
        )

    def test_archive_wins_switching_lifetime(self):
        self.assertGreater(
            self._mean(True, "bounded_archive", "net_performance"),
            self._mean(True, "greedy_incumbent", "net_performance") + 0.01,
        )

    def test_archive_improves_post_switch_recovery(self):
        self.assertGreater(
            self._mean(True, "bounded_archive", "switch10_performance"),
            self._mean(True, "greedy_incumbent", "switch10_performance") + 0.10,
        )

    def test_archive_retains_both_specialties(self):
        self.assertGreater(self._mean(True, "bounded_archive", "best_a"), 0.98)
        self.assertGreater(self._mean(True, "bounded_archive", "best_b"), 0.98)

    def test_greedy_tradeoff_prevents_retaining_both_specialties(self):
        a = self._mean(True, "greedy_incumbent", "best_a")
        b = self._mean(True, "greedy_incumbent", "best_b")
        self.assertLess(min(a, b), 0.95)


if __name__ == "__main__":
    unittest.main()
