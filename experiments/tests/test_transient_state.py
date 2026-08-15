import unittest

from ai_atlas_lab.organism_runtime import TypedScopeRuntime
from ai_atlas_lab.transient_state import TransientStateRegistry


class TransientStateRegistryTests(unittest.TestCase):
    def setup(self):
        runtime = TypedScopeRuntime((0, 1, 2))
        registry = TransientStateRegistry(runtime)
        return runtime, registry

    def test_registry_is_nonowning_over_source_authority_and_resources(self) -> None:
        runtime, registry = self.setup()
        runtime.lease_resource("compute", 0)
        before_evidence = len(runtime.evidence)
        before_authority = dict((key, (value.allowed, value.version)) for key, value in runtime.authority.items())
        registry.register_hot_state(
            0,
            state_ref="hot:0",
            source_ref="source:0",
            source_version=1,
            scope_sensitive=True,
        )
        registry.register_credit_trace(0, transition_ref="transition:0", replay_source_ref="trace-source:0")
        self.assertEqual(len(runtime.evidence), before_evidence)
        self.assertEqual(runtime.leases["compute"].holder_id, 0)
        self.assertEqual(
            dict((key, (value.allowed, value.version)) for key, value in runtime.authority.items()),
            before_authority,
        )

    def test_scope_sensitive_hot_state_invalidates_after_topology_epoch_change(self) -> None:
        runtime, registry = self.setup()
        record = registry.register_hot_state(
            0,
            state_ref="hot:0",
            source_ref="source:0",
            source_version=1,
            scope_sensitive=True,
        )
        change = runtime.stage_scope_change((0, 0, 1), consequence=0.1)
        runtime.commit_scope_change(change.change_id)
        status = registry.assess_hot_recovery(record.hot_id, current_source_version=1)
        self.assertFalse(status.persisted_valid)
        self.assertTrue(status.rematerializable)
        self.assertTrue(status.scope_changed)

    def test_scope_insensitive_hot_state_can_survive_topology_change(self) -> None:
        runtime, registry = self.setup()
        record = registry.register_hot_state(
            0,
            state_ref="hot:0",
            source_ref="source:0",
            source_version=1,
            scope_sensitive=False,
        )
        change = runtime.stage_scope_change((0, 0, 1), consequence=0.1)
        runtime.commit_scope_change(change.change_id)
        status = registry.assess_hot_recovery(record.hot_id, current_source_version=1)
        self.assertTrue(status.persisted_valid)

    def test_source_version_change_invalidates_persisted_hot_state(self) -> None:
        _, registry = self.setup()
        record = registry.register_hot_state(
            0,
            state_ref="hot:0",
            source_ref="source:0",
            source_version=1,
            scope_sensitive=False,
        )
        status = registry.assess_hot_recovery(record.hot_id, current_source_version=2)
        self.assertFalse(status.persisted_valid)
        self.assertTrue(status.source_changed)
        self.assertTrue(status.rematerializable)

    def test_stable_transition_identity_can_remain_credit_target_after_topology_change(self) -> None:
        runtime, registry = self.setup()
        trace = registry.register_credit_trace(
            0,
            transition_ref="transition:stable",
            replay_source_ref="history:stable",
        )
        change = runtime.stage_scope_change((0, 0, 1), consequence=0.1)
        runtime.commit_scope_change(change.change_id)
        status = registry.assess_credit_recovery(
            trace.trace_id,
            valid_transition_refs={"transition:stable"},
        )
        self.assertTrue(status.exact_target_valid)
        self.assertFalse(status.positional_restore_safe)
        self.assertTrue(status.structural_epoch_changed)

    def test_retired_transition_is_not_credited_by_position_after_topology_change(self) -> None:
        runtime, registry = self.setup()
        trace = registry.register_credit_trace(
            0,
            transition_ref="transition:retired",
            replay_source_ref="history:retired",
        )
        change = runtime.stage_scope_change((0, 0, 1), consequence=0.1)
        runtime.commit_scope_change(change.change_id)
        status = registry.assess_credit_recovery(
            trace.trace_id,
            valid_transition_refs={"transition:new"},
        )
        self.assertFalse(status.exact_target_valid)
        self.assertFalse(status.positional_restore_safe)
        self.assertTrue(status.replayable)

    def test_trace_without_source_is_not_replayable(self) -> None:
        _, registry = self.setup()
        trace = registry.register_credit_trace(0, transition_ref="transition:0")
        status = registry.assess_credit_recovery(
            trace.trace_id,
            valid_transition_refs=set(),
        )
        self.assertFalse(status.replayable)


if __name__ == "__main__":
    unittest.main()
