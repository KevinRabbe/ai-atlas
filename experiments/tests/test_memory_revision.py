import unittest

from ai_atlas_lab.memory_revision import RevisionExperimentConfig, run_revision_memory_experiment


class MemoryRevisionTests(unittest.TestCase):
    def rows(self, retraction_probability: float):
        rows = run_revision_memory_experiment(RevisionExperimentConfig(seed=5, mutations=800, retraction_probability=retraction_probability, query_probability=0.5))
        return {name: metrics for name, metrics, _cost in rows}

    def test_without_retractions_compressed_current_is_correct(self):
        self.assertEqual(self.rows(0.0)["compressed_current_only"]["current_accuracy"], 1.0)

    def test_retractions_break_unlinked_compressed_belief(self):
        rows = self.rows(0.20)
        self.assertGreater(rows["evidence_linked_current"]["current_accuracy"], rows["compressed_current_only"]["current_accuracy"] + 0.10)

    def test_direct_and_linked_state_preserve_provenance(self):
        rows = self.rows(0.15)
        self.assertEqual(rows["direct_evidence_replay"]["provenance_accuracy"], 1.0)
        self.assertEqual(rows["evidence_linked_current"]["provenance_accuracy"], 1.0)

    def test_linked_current_avoids_full_history_replay_per_query(self):
        rows = self.rows(0.15)
        self.assertLess(rows["evidence_linked_current"]["reads_per_query"], rows["direct_evidence_replay"]["reads_per_query"] * 0.05)


if __name__ == "__main__":
    unittest.main()
