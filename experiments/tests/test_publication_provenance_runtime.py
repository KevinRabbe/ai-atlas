import unittest

from ai_atlas_lab.organism_runtime import TypedScopeRuntime
from ai_atlas_lab.publication_protocol import PublicationProtocol
from ai_atlas_lab.recovery_protocol import (
    RecoveryObservation,
    RecoveryRecord,
    decide_recovery,
)


class PublicationProvenanceRuntimeTests(unittest.TestCase):
    def runtime(self):
        runtime = TypedScopeRuntime((0, 1, 2))
        runtime.lease_resource("primary", 0)
        runtime.lease_resource("other", 1)
        return runtime, PublicationProtocol(runtime)

    def test_resource_publication_stamps_authoritative_provenance(self) -> None:
        runtime, protocol = self.runtime()
        publication = protocol.prepare_resource_handoff("primary", 1, consequence=1.0)
        protocol.publish(publication.publication_id)
        lease = runtime.leases["primary"]
        self.assertEqual(lease.holder_id, 1)
        self.assertEqual(lease.publication_ref, publication.publication_ref)

    def test_topology_publication_stamps_authoritative_provenance(self) -> None:
        runtime, protocol = self.runtime()
        publication = protocol.prepare_topology((0, 0, 1), consequence=0.2)
        protocol.publish(publication.publication_id)
        self.assertEqual(runtime.topology_publication_ref, publication.publication_ref)

    def test_direct_nonpublication_transfer_does_not_invent_provenance(self) -> None:
        runtime, _ = self.runtime()
        lease = runtime.transfer_resource("primary", 1)
        self.assertIsNone(lease.publication_ref)

    def test_unrelated_global_versions_need_not_be_known_at_prepare_time(self) -> None:
        runtime, protocol = self.runtime()
        publication = protocol.prepare_resource_handoff("primary", 1, consequence=1.0)
        base_version = runtime.leases["primary"].version

        # This advances the runtime-wide lease counter without changing the
        # prepared resource's own current version/fence.
        runtime.transfer_resource("other", 2)
        protocol.publish(publication.publication_id)

        lease = runtime.leases["primary"]
        self.assertGreater(lease.version, base_version + 1)
        self.assertEqual(lease.publication_ref, publication.publication_ref)

    def test_recovery_can_recognize_publication_with_unknown_target_version(self) -> None:
        runtime, protocol = self.runtime()
        publication = protocol.prepare_resource_handoff("primary", 1, consequence=1.0)
        base_version = runtime.leases["primary"].version
        runtime.transfer_resource("other", 2)
        protocol.publish(publication.publication_id)
        lease = runtime.leases["primary"]

        record = RecoveryRecord(
            publication_id=publication.publication_ref,
            kind="resource_handoff",
            expected_base_version=base_version,
            target_version=None,
            target_ref="holder:1",
        )
        observation = RecoveryObservation(
            current_version=lease.version,
            current_ref=f"holder:{lease.holder_id}",
            current_publication_id=lease.publication_ref,
        )
        decision = decide_recovery(
            record,
            observation,
            current_validation_ok=False,
            current_assurance_ok=False,
        )
        self.assertEqual(decision.action, "mark_complete")

    def test_runtime_invariants_include_publication_provenance_integrity(self) -> None:
        runtime, protocol = self.runtime()
        publication = protocol.prepare_resource_handoff("primary", 1, consequence=1.0)
        protocol.publish(publication.publication_id)
        self.assertTrue(runtime.semantic_invariants()["publication_provenance"])


if __name__ == "__main__":
    unittest.main()
