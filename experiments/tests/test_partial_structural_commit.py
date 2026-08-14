import statistics
import unittest

from ai_atlas_lab.partial_structural_commit import I13Config, run_i13


class PartialStructuralCommitTests(unittest.TestCase):
    def mean(self, policy: str, key: str, **overrides) -> float:
        return statistics.mean(
            float(run_i13(I13Config(seed=seed, **overrides), policy)[key])
            for seed in range(6)
        )

    def test_naive_partial_failure_exposes_live_corruption(self) -> None:
        self.assertGreater(
            self.mean("naive_in_place", "corrupt_migration_rate"),
            0.15,
        )
        self.assertGreater(
            self.mean("naive_in_place", "lost_events_per_migration"),
            2.0,
        )
        self.assertGreater(
            self.mean("naive_in_place", "duplicate_events_per_migration"),
            0.2,
        )

    def test_isolated_commit_mechanisms_avoid_partial_live_corruption(self) -> None:
        for policy in (
            "stop_world_replace",
            "staged_transaction",
            "dual_version_handoff",
        ):
            self.assertEqual(self.mean(policy, "corrupt_migration_rate"), 0.0)
            self.assertEqual(self.mean(policy, "lost_events_per_migration"), 0.0)
            self.assertEqual(self.mean(policy, "duplicate_events_per_migration"), 0.0)
            self.assertEqual(
                self.mean(policy, "ambiguous_resource_exposure_per_migration"),
                0.0,
            )

    def test_default_failure_load_favors_staged_transaction_over_naive(self) -> None:
        transaction = self.mean(
            "staged_transaction",
            "net_utility_per_migration",
        )
        naive = self.mean(
            "naive_in_place",
            "net_utility_per_migration",
        )
        self.assertGreater(transaction, naive + 0.30)

    def test_low_failure_low_traffic_can_make_naive_live_change_cheapest(self) -> None:
        naive = self.mean(
            "naive_in_place",
            "net_utility_per_migration",
            failure_probability=0.0,
            event_rate=0.2,
        )
        competitors = [
            self.mean(
                policy,
                "net_utility_per_migration",
                failure_probability=0.0,
                event_rate=0.2,
            )
            for policy in (
                "stop_world_replace",
                "staged_transaction",
                "dual_version_handoff",
            )
        ]
        self.assertGreater(naive, max(competitors))

    def test_high_failure_low_traffic_can_make_stop_world_isolation_rational(self) -> None:
        stop_world = self.mean(
            "stop_world_replace",
            "net_utility_per_migration",
            failure_probability=0.50,
            event_rate=0.2,
        )
        transaction = self.mean(
            "staged_transaction",
            "net_utility_per_migration",
            failure_probability=0.50,
            event_rate=0.2,
        )
        self.assertGreater(stop_world, transaction + 0.05)

    def test_high_live_traffic_can_make_dual_version_handoff_worth_it(self) -> None:
        dual = self.mean(
            "dual_version_handoff",
            "net_utility_per_migration",
            failure_probability=0.50,
            event_rate=80.0,
        )
        transaction = self.mean(
            "staged_transaction",
            "net_utility_per_migration",
            failure_probability=0.50,
            event_rate=80.0,
        )
        stop_world = self.mean(
            "stop_world_replace",
            "net_utility_per_migration",
            failure_probability=0.50,
            event_rate=80.0,
        )
        self.assertGreater(dual, transaction + 0.10)
        self.assertGreater(dual, stop_world + 0.70)


if __name__ == "__main__":
    unittest.main()
