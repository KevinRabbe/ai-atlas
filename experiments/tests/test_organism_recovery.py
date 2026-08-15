import unittest

from ai_atlas_lab.external_effect_protocol import (
    ExternalEffectIntent,
    ExternalExecutionObservation,
)
from ai_atlas_lab.organism_recovery import OrganismRecoveryCoordinator
from ai_atlas_lab.organism_runtime import TypedScopeRuntime
from ai_atlas_lab.publication_protocol import PublicationProtocol


class OrganismRecoveryCoordinatorTests(unittest.TestCase):
    def setup_runtime(self):
        runtime = TypedScopeRuntime((0, 1, 2))
        runtime.lease_resource("primary", 0)
        runtime.lease_resource("other", 1)
        protocol = PublicationProtocol(runtime)
        return runtime, protocol, OrganismRecoveryCoordinator(runtime)

    def test_prepared_resource_handoff_can_retry_only_from_current_base(self) -> None:
        _, protocol, recovery = self.setup_runtime()
        publication = protocol.prepare_resource_handoff("primary", 1, consequence=1.0)
        decision = recovery.recover_publication(
            publication,
            current_assurance_ok=True,
        )
        self.assertEqual(decision.state, "not_published")
        self.assertEqual(decision.action, "retry_publish")

    def test_published_resource_is_completed_even_if_holder_is_later_revoked(self) -> None:
        runtime, protocol, recovery = self.setup_runtime()
        publication = protocol.prepare_resource_handoff("primary", 1, consequence=1.0)
        protocol.publish(publication.publication_id)
        runtime.set_authority(1, False)
        decision = recovery.recover_publication(
            publication,
            current_assurance_ok=False,
        )
        self.assertEqual(decision.state, "already_published")
        self.assertEqual(decision.action, "mark_complete")

    def test_superseding_resource_change_discards_old_prepared_handoff(self) -> None:
        runtime, protocol, recovery = self.setup_runtime()
        publication = protocol.prepare_resource_handoff("primary", 1, consequence=1.0)
        runtime.transfer_resource("primary", 2)
        decision = recovery.recover_publication(
            publication,
            current_assurance_ok=True,
        )
        self.assertEqual(decision.state, "superseded")
        self.assertEqual(decision.action, "discard")

    def test_unrelated_lease_versions_do_not_break_published_recovery(self) -> None:
        runtime, protocol, recovery = self.setup_runtime()
        publication = protocol.prepare_resource_handoff("primary", 1, consequence=1.0)
        runtime.transfer_resource("other", 2)
        protocol.publish(publication.publication_id)
        decision = recovery.recover_publication(
            publication,
            current_assurance_ok=False,
        )
        self.assertEqual(decision.action, "mark_complete")

    def test_prepared_topology_is_retryable_from_same_epoch(self) -> None:
        _, protocol, recovery = self.setup_runtime()
        publication = protocol.prepare_topology((0, 0, 1), consequence=0.2)
        decision = recovery.recover_publication(
            publication,
            current_assurance_ok=True,
            current_validation_ok=True,
        )
        self.assertEqual(decision.action, "retry_publish")

    def test_published_topology_is_recognized_by_publication_provenance(self) -> None:
        _, protocol, recovery = self.setup_runtime()
        publication = protocol.prepare_topology((0, 0, 1), consequence=0.2)
        protocol.publish(publication.publication_id)
        decision = recovery.recover_publication(
            publication,
            current_assurance_ok=False,
            current_validation_ok=False,
        )
        self.assertEqual(decision.action, "mark_complete")

    def test_applied_external_effect_is_historical_even_after_revocation(self) -> None:
        runtime, _, recovery = self.setup_runtime()
        runtime.set_authority(1, False)
        decision = recovery.recover_external_effect(
            ExternalEffectIntent("effect-1", "remote:x", consequence=4.0),
            target_id=1,
            observation=ExternalExecutionObservation(
                "applied", effect_specific=True, evidence_ref="receipt:1"
            ),
            receiver_recognizes_identity=False,
            duplicate_penalty=4.0,
            missed_penalty=1.0,
        )
        self.assertEqual(decision.action, "mark_complete")

    def test_absent_external_effect_is_blocked_after_revocation(self) -> None:
        runtime, _, recovery = self.setup_runtime()
        runtime.set_authority(1, False)
        decision = recovery.recover_external_effect(
            ExternalEffectIntent("effect-2", "remote:x", consequence=4.0),
            target_id=1,
            observation=ExternalExecutionObservation(
                "absent", effect_specific=True, evidence_ref="receipt:2"
            ),
            receiver_recognizes_identity=False,
            duplicate_penalty=4.0,
            missed_penalty=1.0,
        )
        self.assertEqual(decision.action, "blocked")

    def test_nonidentifiable_external_effect_can_remain_unresolved(self) -> None:
        _, _, recovery = self.setup_runtime()
        decision = recovery.recover_external_effect(
            ExternalEffectIntent("effect-3", "physical:x", consequence=4.0),
            target_id=1,
            observation=ExternalExecutionObservation("unknown", effect_specific=False),
            receiver_recognizes_identity=False,
            duplicate_penalty=4.0,
            missed_penalty=1.0,
        )
        self.assertEqual(decision.action, "unresolved")


if __name__ == "__main__":
    unittest.main()
