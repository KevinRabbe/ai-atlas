import unittest

from ai_atlas_lab.recovery_protocol import (
    RecoveryObservation,
    RecoveryRecord,
    classify_recovery,
    decide_recovery,
)


class RecoveryProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = RecoveryRecord(
            publication_id="pub-17",
            kind="resource_handoff",
            expected_base_version=10,
            target_version=11,
            target_ref="holder:2",
            validation_refs=("authority:holder:2",),
        )

    def test_target_identity_recovers_publish_with_lost_completion_marker(self) -> None:
        observation = RecoveryObservation(11, "holder:2")
        self.assertEqual(classify_recovery(self.record, observation), "already_published")
        decision = decide_recovery(
            self.record,
            observation,
            current_validation_ok=False,
            current_assurance_ok=False,
        )
        self.assertEqual(decision.action, "mark_complete")

    def test_matching_base_can_retry_only_after_current_checks(self) -> None:
        observation = RecoveryObservation(10, "holder:1")
        decision = decide_recovery(
            self.record,
            observation,
            current_validation_ok=True,
            current_assurance_ok=True,
        )
        self.assertEqual(decision.state, "not_published")
        self.assertEqual(decision.action, "retry_publish")

    def test_old_approval_does_not_survive_revocation_as_authority(self) -> None:
        observation = RecoveryObservation(10, "holder:1")
        decision = decide_recovery(
            self.record,
            observation,
            current_validation_ok=False,
            current_assurance_ok=True,
        )
        self.assertEqual(decision.action, "discard")

    def test_newer_authoritative_version_supersedes_prepared_transition(self) -> None:
        observation = RecoveryObservation(12, "holder:3")
        decision = decide_recovery(
            self.record,
            observation,
            current_validation_ok=True,
            current_assurance_ok=True,
        )
        self.assertEqual(decision.state, "superseded")
        self.assertEqual(decision.action, "discard")

    def test_same_target_version_with_other_identity_is_conflict(self) -> None:
        observation = RecoveryObservation(11, "holder:99")
        decision = decide_recovery(
            self.record,
            observation,
            current_validation_ok=True,
            current_assurance_ok=True,
        )
        self.assertEqual(decision.state, "conflict")
        self.assertEqual(decision.action, "halt")

    def test_authoritative_version_below_expected_base_requires_reconciliation(self) -> None:
        observation = RecoveryObservation(9, "holder:0")
        decision = decide_recovery(
            self.record,
            observation,
            current_validation_ok=True,
            current_assurance_ok=True,
        )
        self.assertEqual(decision.state, "inconsistent")
        self.assertEqual(decision.action, "halt")


if __name__ == "__main__":
    unittest.main()
