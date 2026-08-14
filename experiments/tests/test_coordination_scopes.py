import unittest

from ai_atlas_lab.coordination_scopes import CoordinationScopeRegistry
from ai_atlas_lab.organism_runtime import TypedScopeRuntime


class CoordinationScopeRegistryTests(unittest.TestCase):
    def test_subject_can_join_multiple_overlapping_coordination_scopes(self) -> None:
        runtime = TypedScopeRuntime(range(4))
        registry = CoordinationScopeRegistry(runtime)
        first = registry.create((0, 1, 2))
        second = registry.create((1, 2, 3), persistent=True)

        subject_scopes = registry.for_subject(1)
        self.assertEqual({scope.scope_id for scope in subject_scopes}, {first.scope_id, second.scope_id})
        self.assertEqual(runtime.topology_labels, (0, 1, 2, 3))

    def test_closing_overlay_cannot_delete_or_transfer_semantic_state(self) -> None:
        runtime = TypedScopeRuntime(range(4))
        evidence = runtime.attach_evidence(1, "source:1")
        runtime.register_predictive_state(1, "latent:1", "raw:1")
        lease = runtime.lease_resource("compute:0", 1)
        runtime.set_authority(1, False)
        registry = CoordinationScopeRegistry(runtime)
        overlay = registry.create((0, 1, 3))

        registry.close(overlay.scope_id)

        self.assertEqual(runtime.evidence[evidence.evidence_id].source_ref, "source:1")
        self.assertEqual(runtime.rematerialize(1), "raw:1")
        self.assertEqual(runtime.leases["compute:0"], lease)
        self.assertFalse(runtime.read_authority(1).allowed)

    def test_overlap_does_not_duplicate_resource_or_capability_authority(self) -> None:
        runtime = TypedScopeRuntime(range(4))
        runtime.lease_resource("verify:0", 1)
        runtime.set_authority(1, False)
        registry = CoordinationScopeRegistry(runtime)
        registry.create((0, 1), persistent=True)
        registry.create((1, 2), persistent=True)
        registry.create((1, 3))

        self.assertEqual(len(runtime.leases), 1)
        self.assertEqual(runtime.leases["verify:0"].holder_id, 1)
        self.assertFalse(runtime.read_authority(1).allowed)
        with self.assertRaises(ValueError):
            runtime.lease_resource("verify:0", 2)


if __name__ == "__main__":
    unittest.main()
