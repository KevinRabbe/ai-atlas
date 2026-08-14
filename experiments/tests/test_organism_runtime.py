import unittest

from ai_atlas_lab.organism_runtime import TypedScopeRuntime


class OrganismRuntimeTests(unittest.TestCase):
    def runtime(self) -> TypedScopeRuntime:
        return TypedScopeRuntime(range(4), structural_assurance_threshold=4.0)

    def commit_grouping(self, runtime: TypedScopeRuntime) -> None:
        change = runtime.stage_scope_change((0, 0, 1, 1), consequence=2.0)
        token = runtime.request_assurance(
            change.proposal_id,
            independent=True,
            approved=True,
            evidence_ref="independent-topology-audit",
        )
        runtime.commit_scope_change(
            change.change_id,
            assurance_token_id=token.token_id,
        )

    def test_semantic_records_survive_topology_change(self) -> None:
        runtime = self.runtime()
        evidence = runtime.attach_evidence(0, "source:evidence")
        runtime.register_predictive_state(0, "latent:0", "source:predictive")
        lease = runtime.lease_resource("gpu:0", 0)

        self.commit_grouping(runtime)

        self.assertEqual(
            runtime.evidence[evidence.evidence_id].source_ref,
            "source:evidence",
        )
        self.assertEqual(runtime.rematerialize(0), "source:predictive")
        self.assertEqual(runtime.leases["gpu:0"], lease)
        self.assertTrue(all(runtime.semantic_invariants().values()))

    def test_resource_lease_is_singular_and_explicitly_transferable(self) -> None:
        runtime = self.runtime()
        runtime.lease_resource("verify:0", 0)
        with self.assertRaises(ValueError):
            runtime.lease_resource("verify:0", 1)

        transferred = runtime.transfer_resource("verify:0", 1)
        self.assertEqual(transferred.holder_id, 1)
        self.assertEqual(runtime.leases["verify:0"].holder_id, 1)

    def test_high_value_proposal_cannot_manufacture_external_authority(self) -> None:
        runtime = self.runtime()
        proposal = runtime.propose_transition(
            "external-effect",
            target_id=0,
            expected_value=1_000.0,
            cost=0.0,
            uncertainty=0.0,
            consequence=1.0,
            reversible=False,
            authority_class="external_effect",
        )
        runtime.set_authority(0, False)

        with self.assertRaises(PermissionError):
            runtime.execute_transition(proposal.proposal_id)
        self.assertNotIn(proposal.proposal_id, runtime.executed_proposals)

    def test_durable_promotion_requires_independent_assurance(self) -> None:
        runtime = self.runtime()
        proposal = runtime.propose_transition(
            "persist-claim",
            target_id=None,
            expected_value=10.0,
            cost=0.0,
            uncertainty=0.1,
            consequence=1.0,
            reversible=True,
            authority_class="durable_knowledge",
        )
        self_token = runtime.request_assurance(
            proposal.proposal_id,
            independent=False,
            approved=True,
            evidence_ref="proposal-path-self-check",
        )
        with self.assertRaises(PermissionError):
            runtime.execute_transition(
                proposal.proposal_id,
                assurance_token_id=self_token.token_id,
            )

        independent = runtime.request_assurance(
            proposal.proposal_id,
            independent=True,
            approved=True,
            evidence_ref="independent-check",
        )
        runtime.execute_transition(
            proposal.proposal_id,
            assurance_token_id=independent.token_id,
        )
        self.assertIn(proposal.proposal_id, runtime.executed_proposals)

    def test_structural_commit_requires_independent_assurance_when_blast_radius_is_large(self) -> None:
        runtime = self.runtime()
        change = runtime.stage_scope_change((0, 0, 1, 1), consequence=2.0)
        self.assertTrue(change.requires_assurance)

        with self.assertRaises(PermissionError):
            runtime.commit_scope_change(change.change_id)

        self_token = runtime.request_assurance(
            change.proposal_id,
            independent=False,
            approved=True,
            evidence_ref="same-path-check",
        )
        with self.assertRaises(PermissionError):
            runtime.commit_scope_change(
                change.change_id,
                assurance_token_id=self_token.token_id,
            )

        independent = runtime.request_assurance(
            change.proposal_id,
            independent=True,
            approved=True,
            evidence_ref="independent-topology-check",
        )
        epoch = runtime.commit_scope_change(
            change.change_id,
            assurance_token_id=independent.token_id,
        )
        self.assertEqual(epoch, 1)

    def test_rollback_leaves_topology_unchanged(self) -> None:
        runtime = self.runtime()
        original = runtime.topology_labels
        change = runtime.stage_scope_change((0, 0, 1, 1), consequence=0.2)
        runtime.rollback_scope_change(change.change_id)

        self.assertEqual(runtime.topology_labels, original)
        self.assertEqual(runtime.topology_epoch, 0)
        with self.assertRaises(ValueError):
            runtime.commit_scope_change(change.change_id)

    def test_old_epoch_event_is_forwarded_and_processed_exactly_once(self) -> None:
        runtime = self.runtime()
        event = runtime.enqueue_event(0, due_step=10)
        self.commit_grouping(runtime)

        self.assertEqual(runtime.process_due_events(10), (event.event_id,))
        self.assertEqual(runtime.forwarded_events, 1)
        self.assertEqual(runtime.process_due_events(11), ())
        self.assertEqual(runtime.forwarded_events, 1)

    def test_bundle_allocator_can_price_complementarity(self) -> None:
        runtime = self.runtime()
        left = runtime.propose_transition(
            "left",
            target_id=0,
            expected_value=3.0,
            cost=1.0,
            uncertainty=0.0,
            consequence=1.0,
            reversible=True,
        )
        right = runtime.propose_transition(
            "right",
            target_id=1,
            expected_value=3.0,
            cost=1.0,
            uncertainty=0.0,
            consequence=1.0,
            reversible=True,
        )
        standalone = runtime.propose_transition(
            "standalone",
            target_id=2,
            expected_value=5.0,
            cost=1.0,
            uncertainty=0.0,
            consequence=1.0,
            reversible=True,
            resource_units=2,
        )

        result = runtime.allocate_bundle(
            (left, right, standalone),
            capacity=2,
            interactions={
                frozenset((left.proposal_id, right.proposal_id)): 2.0,
            },
        )
        self.assertEqual(
            result.proposal_ids,
            (left.proposal_id, right.proposal_id),
        )
        self.assertAlmostEqual(result.net_value, 6.0)


if __name__ == "__main__":
    unittest.main()
