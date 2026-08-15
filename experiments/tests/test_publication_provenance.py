import unittest

from ai_atlas_lab.publication_provenance import (
    I18Config,
    run_same_target_collision,
    run_unpredictable_target_version,
)


class PublicationProvenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = I18Config(seed=9, trials=30_000)

    def test_precomputed_target_version_fails_when_unrelated_global_versions_advance(self) -> None:
        result = run_unpredictable_target_version(self.config, "predicted_target_version")
        self.assertLess(result["correct_recovery"], 0.65)
        self.assertGreater(result["missed_completion"], 0.30)

    def test_state_identity_handles_unpredictable_numeric_target_version(self) -> None:
        result = run_unpredictable_target_version(self.config, "state_ref_only")
        self.assertGreater(result["correct_recovery"], 0.999)

    def test_publication_provenance_handles_unpredictable_numeric_target_version(self) -> None:
        result = run_unpredictable_target_version(self.config, "publication_provenance")
        self.assertGreater(result["correct_recovery"], 0.999)

    def test_same_state_value_can_be_created_by_another_publication(self) -> None:
        result = run_same_target_collision(self.config, "state_ref_only")
        self.assertGreater(result["false_completion"], 0.06)
        self.assertLess(result["correct_recovery"], 0.95)

    def test_precomputed_version_plus_state_still_misattributed_same_target_collision(self) -> None:
        result = run_same_target_collision(self.config, "predicted_target_version")
        self.assertGreater(result["false_completion"], 0.06)

    def test_publication_identity_removes_same_target_attribution_collision(self) -> None:
        result = run_same_target_collision(self.config, "publication_provenance")
        self.assertGreater(result["correct_recovery"], 0.999)
        self.assertEqual(result["false_completion"], 0.0)


if __name__ == "__main__":
    unittest.main()
