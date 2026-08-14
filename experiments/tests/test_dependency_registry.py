import unittest

from ai_atlas_lab.dependency_registry import DependencyRegistry
from ai_atlas_lab.organism_runtime import TypedScopeRuntime


class DependencyRegistryTests(unittest.TestCase):
    def test_one_way_dependency_does_not_create_reverse_flow(self) -> None:
        runtime = TypedScopeRuntime(range(3))
        registry = DependencyRegistry(runtime)
        dependency = registry.add(0, 1, kind="information")

        self.assertEqual(registry.outgoing(0), (dependency,))
        self.assertEqual(registry.incoming(1), (dependency,))
        self.assertEqual(registry.outgoing(1), ())
        self.assertEqual(registry.incoming(0), ())
        self.assertEqual(registry.reciprocal_pairs(), frozenset())

    def test_reciprocity_is_detected_but_does_not_create_shared_authority_or_ownership(self) -> None:
        runtime = TypedScopeRuntime(range(3))
        runtime.lease_resource("compute:0", 0)
        runtime.set_authority(1, False)
        registry = DependencyRegistry(runtime)
        registry.add(0, 1, kind="information")
        registry.add(1, 0, kind="information")

        self.assertEqual(
            registry.reciprocal_pairs(kind="information"),
            frozenset((frozenset((0, 1)),)),
        )
        self.assertEqual(runtime.topology_labels, (0, 1, 2))
        self.assertEqual(runtime.leases["compute:0"].holder_id, 0)
        self.assertFalse(runtime.read_authority(1).allowed)

    def test_dependency_identity_survives_ownership_topology_change(self) -> None:
        runtime = TypedScopeRuntime(range(4), structural_assurance_threshold=4.0)
        registry = DependencyRegistry(runtime)
        dependency = registry.add(0, 3, persistent=True)

        change = runtime.stage_scope_change((0, 0, 1, 1), consequence=2.0)
        token = runtime.request_assurance(
            change.proposal_id,
            independent=True,
            approved=True,
            evidence_ref="topology-check",
        )
        runtime.commit_scope_change(
            change.change_id,
            assurance_token_id=token.token_id,
        )

        self.assertEqual(registry.outgoing(0), (dependency,))
        self.assertEqual(registry.incoming(3), (dependency,))
        self.assertEqual(dependency.source_id, 0)
        self.assertEqual(dependency.target_id, 3)
        self.assertEqual(dependency.created_epoch, 0)
        self.assertEqual(runtime.topology_epoch, 1)


if __name__ == "__main__":
    unittest.main()
