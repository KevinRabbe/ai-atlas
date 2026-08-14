import unittest

from ai_atlas_lab.representation_interface import RepresentationExperimentConfig, run_representation_experiment


class RepresentationInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows = run_representation_experiment(RepresentationExperimentConfig(seed=13, state_count=240, corruption_trials=120))
        cls.rows = {name: metrics for name, metrics, _cost in rows}

    def test_exact_structured_and_text_round_trip(self):
        self.assertEqual(self.rows["human_readable_json"]["roundtrip_state_accuracy"], 1.0)
        self.assertEqual(self.rows["structured_tagged_binary"]["roundtrip_state_accuracy"], 1.0)

    def test_continuous_is_compact_but_loses_large_exact_identifiers(self):
        vector = self.rows["opaque_float32_vector"]
        text = self.rows["human_readable_json"]
        self.assertLess(vector["avg_payload_bytes"], text["avg_payload_bytes"] / 3)
        self.assertLess(vector["exact_discrete_field_accuracy"], 0.1)
        self.assertEqual(vector["action_accuracy"], 1.0)
        self.assertLess(vector["mean_score_abs_error"], 1e-6)

    def test_tagged_protocol_survives_version_extension_and_detects_corruption(self):
        structured = self.rows["structured_tagged_binary"]
        vector = self.rows["opaque_float32_vector"]
        self.assertEqual(structured["new_producer_old_consumer_compatibility"], 1.0)
        self.assertEqual(vector["new_producer_old_consumer_compatibility"], 0.0)
        self.assertEqual(structured["corruption_detection_rate"], 1.0)

    def test_hybrid_redundancy_can_recover_corrupted_core(self):
        self.assertEqual(self.rows["hybrid_structured_plus_audit"]["corruption_recovery_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
