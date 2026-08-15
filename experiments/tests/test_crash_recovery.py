import unittest

from ai_atlas_lab.crash_recovery import I14Config, run_knowledge_recovery, run_resource_recovery


class CrashRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = I14Config(seed=11, trials=20_000)

    def test_version_fenced_resource_recovery_is_exact(self) -> None:
        result = run_resource_recovery(self.config, "version_fenced")
        self.assertGreater(result["correct_recovery"], 0.999)
        self.assertEqual(result["duplicate_publication"], 0.0)
        self.assertEqual(result["superseded_overwrite"], 0.0)

    def test_phase_marker_cannot_distinguish_lost_publish_marker(self) -> None:
        result = run_resource_recovery(self.config, "phase_recheck")
        self.assertGreater(result["duplicate_publication"], 0.15)
        self.assertLess(result["correct_recovery"], 0.75)

    def test_missing_base_version_can_overwrite_superseding_state(self) -> None:
        result = run_resource_recovery(self.config, "phase_recheck")
        self.assertGreater(result["superseded_overwrite"], 0.10)

    def test_old_assurance_cannot_override_current_revocation(self) -> None:
        replay = run_resource_recovery(self.config, "assurance_replay")
        fenced = run_resource_recovery(self.config, "version_fenced")
        self.assertGreater(replay["revoked_publication"], 0.01)
        self.assertEqual(fenced["revoked_publication"], 0.0)

    def test_version_fenced_knowledge_recovery_is_exact(self) -> None:
        result = run_knowledge_recovery(self.config, "version_fenced")
        self.assertGreater(result["correct_recovery"], 0.999)
        self.assertEqual(result["duplicate_publication"], 0.0)
        self.assertEqual(result["superseded_overwrite"], 0.0)

    def test_old_assurance_can_promote_retracted_knowledge(self) -> None:
        replay = run_knowledge_recovery(self.config, "assurance_replay")
        fenced = run_knowledge_recovery(self.config, "version_fenced")
        self.assertGreater(replay["retracted_promotion"], 0.015)
        self.assertEqual(fenced["retracted_promotion"], 0.0)


if __name__ == "__main__":
    unittest.main()
