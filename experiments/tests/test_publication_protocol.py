import unittest

from ai_atlas_lab.organism_runtime import TypedScopeRuntime
from ai_atlas_lab.publication_protocol import PublicationProtocol


class PublicationProtocolTests(unittest.TestCase):
    def runtime(self) -> TypedScopeRuntime:
        runtime = TypedScopeRuntime(range(4), structural_assurance_threshold=4.0)
        runtime.lease_resource("compute:0", 0)
        return runtime

    def independent_token(self, runtime: TypedScopeRuntime, proposal_id: int):
        return runtime.request_assurance(
            proposal_id,
            independent=True,
            approved=True,
            evidence_ref="independent-publication-check",
        )

    def test_preparation_does_not_change_live_resource_ownership(self) -> None:
        runtime = self.runtime()
        protocol = PublicationProtocol(runtime)
        publication = protocol.prepare_resource_handoff(
            "compute:0",
            1,
            consequence=5.0,
        )
        self.assertEqual(runtime.leases["compute:0"].holder_id, 0)
        self.assertEqual(publication.status, "prepared")

    def test_revocation_after_prepare_blocks_resource_publication(self) -> None:
        runtime = self.runtime()
        protocol = PublicationProtocol(runtime)
        publication = protocol.prepare_resource_handoff(
            "compute:0",
            1,
            consequence=5.0,
        )
        token = self.independent_token(runtime, publication.proposal_id)
        runtime.set_authority(1, False)

        with self.assertRaises(PermissionError):
            protocol.publish(
                publication.publication_id,
                assurance_token_id=token.token_id,
            )
        self.assertEqual(runtime.leases["compute:0"].holder_id, 0)

    def test_stale_lease_version_rejects_prepared_handoff(self) -> None:
        runtime = self.runtime()
        protocol = PublicationProtocol(runtime)
        publication = protocol.prepare_resource_handoff(
            "compute:0",
            1,
            consequence=5.0,
        )
        token = self.independent_token(runtime, publication.proposal_id)
        runtime.transfer_resource("compute:0", 2)

        with self.assertRaises(RuntimeError):
            protocol.publish(
                publication.publication_id,
                assurance_token_id=token.token_id,
            )
        self.assertEqual(runtime.leases["compute:0"].holder_id, 2)

    def test_second_topology_plan_from_old_epoch_cannot_overwrite_new_commit(self) -> None:
        runtime = self.runtime()
        protocol = PublicationProtocol(runtime)
        first = protocol.prepare_topology((0, 0, 1, 1), consequence=2.0)
        second = protocol.prepare_topology((0, 1, 1, 0), consequence=2.0)
        first_token = self.independent_token(runtime, first.proposal_id)
        second_token = self.independent_token(runtime, second.proposal_id)

        protocol.publish(
            first.publication_id,
            assurance_token_id=first_token.token_id,
        )
        with self.assertRaises(RuntimeError):
            protocol.publish(
                second.publication_id,
                assurance_token_id=second_token.token_id,
            )
        self.assertEqual(runtime.topology_labels, (0, 0, 1, 1))
        self.assertEqual(runtime.topology_epoch, 1)

    def test_non_independent_assurance_cannot_publish_consequential_change(self) -> None:
        runtime = self.runtime()
        protocol = PublicationProtocol(runtime)
        publication = protocol.prepare_resource_handoff(
            "compute:0",
            1,
            consequence=5.0,
        )
        self_token = runtime.request_assurance(
            publication.proposal_id,
            independent=False,
            approved=True,
            evidence_ref="same-path-self-check",
        )
        with self.assertRaises(PermissionError):
            protocol.publish(
                publication.publication_id,
                assurance_token_id=self_token.token_id,
            )

    def test_discard_keeps_live_state_unchanged(self) -> None:
        runtime = self.runtime()
        protocol = PublicationProtocol(runtime)
        topology = protocol.prepare_topology((0, 0, 1, 1), consequence=0.2)
        handoff = protocol.prepare_resource_handoff(
            "compute:0",
            1,
            consequence=0.2,
        )

        protocol.discard(topology.publication_id)
        protocol.discard(handoff.publication_id)

        self.assertEqual(runtime.topology_labels, (0, 1, 2, 3))
        self.assertEqual(runtime.topology_epoch, 0)
        self.assertEqual(runtime.leases["compute:0"].holder_id, 0)
        self.assertEqual(topology.status, "discarded")
        self.assertEqual(handoff.status, "discarded")


if __name__ == "__main__":
    unittest.main()
