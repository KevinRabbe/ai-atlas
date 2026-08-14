import unittest

from ai_atlas_lab.representation_search import SearchRepresentationConfig, run_search_representation_experiment


class SearchRepresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = run_search_representation_experiment(SearchRepresentationConfig(seed=9, test_count=500, calibration_count=700, corruption_trials=150))
        cls.rows = {name: metrics for name, metrics, _cost in rows}

    def test_structured_is_exact_compatible_and_integrity_checked(self):
        structured = self.rows["search_structured_binary"]
        self.assertEqual(structured["exact_structural_accuracy"], 1.0)
        self.assertEqual(structured["version_compatibility"], 1.0)
        self.assertEqual(structured["corruption_detection_rate"], 1.0)

    def test_float_vector_loses_large_exact_identity(self):
        vector = self.rows["search_float32_vector"]
        self.assertLess(vector["exact_structural_accuracy"], 0.1)
        self.assertEqual(vector["version_compatibility"], 0.0)

    def test_learned_continuous_plus_exact_side_is_compact_and_exact_where_required(self):
        hybrid = self.rows["learned_quantized_exact_side"]
        structured = self.rows["search_structured_binary"]
        self.assertEqual(hybrid["exact_structural_accuracy"], 1.0)
        self.assertLess(hybrid["avg_payload_bytes"], structured["avg_payload_bytes"] - 8)

    def test_learned_hybrid_preserves_search_decisions(self):
        self.assertGreater(self.rows["learned_quantized_exact_side"]["decision_accuracy"], 0.96)


if __name__ == "__main__":
    unittest.main()
