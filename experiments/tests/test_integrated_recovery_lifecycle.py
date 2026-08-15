import statistics
import unittest

from ai_atlas_lab.integrated_recovery_lifecycle import I23Config, run_i23


class IntegratedRecoveryLifecycleTests(unittest.TestCase):
    def mean(self, policy: str, key: str) -> float:
        return statistics.mean(
            run_i23(I23Config(seed=seed, episodes=700), policy).get(key, 0.0)
            for seed in range(5)
        )

    def test_typed_recovery_preserves_runtime_semantic_invariants(self) -> None:
        self.assertEqual(self.mean("typed", "semantic_invariant_failure"), 0.0)
        self.assertEqual(self.mean("typed", "publication_recovery_failure"), 0.0)

    def test_typed_recovery_does_not_reuse_stale_hot_state(self) -> None:
        self.assertEqual(self.mean("typed", "stale_hot_use"), 0.0)
        self.assertGreater(self.mean("opaque_snapshot", "stale_hot_use"), 0.45)

    def test_typed_recovery_does_not_assign_credit_by_stale_position(self) -> None:
        self.assertEqual(self.mean("typed", "false_credit"), 0.0)
        self.assertGreater(self.mean("opaque_snapshot", "false_credit"), 0.20)

    def test_old_epoch_external_events_are_forwarded_and_recheck_current_authority(self) -> None:
        self.assertGreater(self.mean("typed", "event_forwarded"), 0.95)
        self.assertEqual(self.mean("typed", "event_exactly_once_failure"), 0.0)
        self.assertEqual(self.mean("typed", "unauthorized_event"), 0.0)
        self.assertGreater(self.mean("opaque_snapshot", "unauthorized_event"), 0.15)

    def test_publication_provenance_prevents_duplicate_recovery_publish(self) -> None:
        self.assertEqual(self.mean("typed", "duplicate_publication_attempt"), 0.0)
        self.assertGreater(
            self.mean("opaque_snapshot", "duplicate_publication_attempt"),
            0.35,
        )

    def test_lineage_aware_recovery_reduces_external_execution_error(self) -> None:
        typed_error = self.mean("typed", "duplicate_external_effect") + self.mean(
            "typed", "omitted_external_effect"
        )
        opaque_error = self.mean("opaque_snapshot", "duplicate_external_effect") + self.mean(
            "opaque_snapshot", "omitted_external_effect"
        )
        self.assertLess(typed_error, opaque_error * 0.70)

    def test_typed_recovery_beats_safe_but_wasteful_transient_discard(self) -> None:
        self.assertGreater(
            self.mean("typed", "utility"),
            self.mean("discard_transient", "utility") + 0.70,
        )

    def test_typed_recovery_beats_opaque_snapshot_restore(self) -> None:
        self.assertGreater(
            self.mean("typed", "utility"),
            self.mean("opaque_snapshot", "utility") + 2.0,
        )


if __name__ == "__main__":
    unittest.main()
