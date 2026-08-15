import unittest

from ai_atlas_lab.recovery_protocol import (
    RecoveryObservation,
    RecoveryRecord,
    classify_recovery,
    decide_recovery,
)


class RecoveryProtocolProvenanceTests(unittest.TestCase):
    def test_publication_identity_recovers_unknown_numeric_target_version(self) -> None:
        record = RecoveryRecord(
            publication_id="pub-42",
            kind="resource_handoff",
            expected_base_version=10,
            target_version=None,
            target_ref="holder:B",
        )
        observation = RecoveryObservation(
            current_version=17,
            current_ref="holder:B",
            current_publication_id="pub-42",
        )
        self.assertEqual(classify_recovery(record, observation), "already_published")

    def test_same_target_from_other_publication_is_not_ours(self) -> None:
        record = RecoveryRecord(
            publication_id="pub-42",
            kind="resource_handoff",
            expected_base_version=10,
            target_version=11,
            target_ref="holder:B",
        )
        observation = RecoveryObservation(
            current_version=11,
            current_ref="holder:B",
            current_publication_id="pub-99",
        )
        decision = decide_recovery(
            record,
            observation,
            current_validation_ok=True,
            current_assurance_ok=True,
        )
        self.assertEqual(decision.state, "conflict")
        self.assertEqual(decision.action, "halt")

    def test_unknown_target_version_without_publication_provenance_is_not_attributed(self) -> None:
        record = RecoveryRecord(
            publication_id="pub-42",
            kind="resource_handoff",
            expected_base_version=10,
            target_version=None,
            target_ref="holder:B",
        )
        observation = RecoveryObservation(
            current_version=17,
            current_ref="holder:B",
            current_publication_id=None,
        )
        self.assertEqual(classify_recovery(record, observation), "superseded")

    def test_base_state_can_have_prior_publication_provenance_without_conflict(self) -> None:
        record = RecoveryRecord(
            publication_id="pub-42",
            kind="knowledge",
            expected_base_version=10,
            target_version=None,
            target_ref="claim:new",
        )
        observation = RecoveryObservation(
            current_version=10,
            current_ref="claim:old",
            current_publication_id="pub-base",
        )
        decision = decide_recovery(
            record,
            observation,
            current_validation_ok=True,
            current_assurance_ok=True,
        )
        self.assertEqual(decision.state, "not_published")
        self.assertEqual(decision.action, "retry_publish")


if __name__ == "__main__":
    unittest.main()
