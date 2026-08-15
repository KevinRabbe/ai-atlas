import statistics
import unittest

from ai_atlas_lab.transient_state_recovery import (
    CacheRecoveryConfig,
    CreditRecoveryConfig,
    run_cache_recovery,
    run_credit_recovery,
)


class TransientStateRecoveryTests(unittest.TestCase):
    def cache_mean(self, policy: str, key: str) -> float:
        return statistics.mean(
            run_cache_recovery(CacheRecoveryConfig(seed=seed), policy).get(key, 0.0)
            for seed in range(6)
        )

    def credit_mean(self, policy: str, key: str) -> float:
        return statistics.mean(
            run_credit_recovery(CreditRecoveryConfig(seed=seed), policy).get(key, 0.0)
            for seed in range(6)
        )

    def test_adaptive_cache_recovery_beats_always_rematerialize(self) -> None:
        self.assertGreater(
            self.cache_mean("adaptive", "utility"),
            self.cache_mean("rematerialize", "utility") + 0.003,
        )

    def test_adaptive_cache_recovery_uses_both_persistence_and_rematerialization(self) -> None:
        self.assertGreater(self.cache_mean("adaptive", "persisted_items"), 0.10)
        self.assertGreater(self.cache_mean("adaptive", "rematerialized_items"), 0.20)

    def test_persisting_all_hot_state_exposes_more_stale_reuse(self) -> None:
        self.assertGreater(
            self.cache_mean("persist_all", "stale_reuse"),
            self.cache_mean("adaptive", "stale_reuse") * 5.0,
        )

    def test_discarding_source_backed_cache_loses_future_reuse(self) -> None:
        self.assertGreater(self.cache_mean("discard", "missed_reuse"), 0.35)

    def test_unversioned_credit_trace_creates_false_blame_after_structure_change(self) -> None:
        self.assertGreater(self.credit_mean("unversioned", "false_blame"), 0.10)

    def test_versioned_credit_trace_removes_false_blame_and_beats_unversioned(self) -> None:
        self.assertEqual(self.credit_mean("versioned", "false_blame"), 0.0)
        self.assertGreater(
            self.credit_mean("versioned", "utility"),
            self.credit_mean("unversioned", "utility") + 0.07,
        )

    def test_adaptive_credit_recovery_uses_persistence_and_source_replay(self) -> None:
        self.assertGreater(self.credit_mean("adaptive", "persisted_trace_items"), 0.60)
        self.assertGreater(self.credit_mean("adaptive", "replayed_trace_items"), 0.15)
        self.assertGreater(
            self.credit_mean("adaptive", "utility"),
            self.credit_mean("versioned", "utility") + 0.05,
        )

    def test_discarding_credit_trace_loses_all_delayed_attribution(self) -> None:
        self.assertGreater(self.credit_mean("discard", "missed_credit"), 0.99)


if __name__ == "__main__":
    unittest.main()
