import statistics
import unittest

from ai_atlas_lab.resource_handoff_failure import I13BConfig, run_i13b


class ResourceHandoffFailureTests(unittest.TestCase):
    def mean(self, policy: str, key: str, **overrides) -> float:
        return statistics.mean(
            float(run_i13b(I13BConfig(seed=seed, **overrides), policy)[key])
            for seed in range(6)
        )

    def test_make_before_break_can_expose_duplicate_ownership_and_writes(self) -> None:
        self.assertGreater(
            self.mean("make_before_break", "ownership_violation_rate"),
            0.04,
        )
        self.assertGreater(
            self.mean("make_before_break", "duplicate_writes_per_handoff"),
            0.30,
        )

    def test_break_before_make_can_expose_zero_owner_and_lost_work(self) -> None:
        self.assertGreater(
            self.mean("break_before_make", "ownership_violation_rate"),
            0.04,
        )
        self.assertGreater(
            self.mean("break_before_make", "lost_requests_per_handoff"),
            2.0,
        )

    def test_failure_isolated_handoffs_preserve_singular_ownership(self) -> None:
        for policy in (
            "stop_world_transfer",
            "staged_lease_fence",
            "dual_read_single_write",
        ):
            self.assertEqual(self.mean(policy, "ownership_violation_rate"), 0.0)
            self.assertEqual(self.mean(policy, "duplicate_writes_per_handoff"), 0.0)
            self.assertEqual(self.mean(policy, "lost_requests_per_handoff"), 0.0)

    def test_default_load_favors_failure_isolated_publication(self) -> None:
        safe = max(
            self.mean("staged_lease_fence", "net_utility_per_handoff"),
            self.mean("dual_read_single_write", "net_utility_per_handoff"),
        )
        naive = max(
            self.mean("make_before_break", "net_utility_per_handoff"),
            self.mean("break_before_make", "net_utility_per_handoff"),
        )
        self.assertGreater(safe, naive + 0.15)

    def test_no_failure_low_traffic_can_make_direct_handoff_cheapest(self) -> None:
        direct = self.mean(
            "make_before_break",
            "net_utility_per_handoff",
            failure_probability=0.0,
            request_rate=0.2,
        )
        safe = max(
            self.mean(
                policy,
                "net_utility_per_handoff",
                failure_probability=0.0,
                request_rate=0.2,
            )
            for policy in (
                "stop_world_transfer",
                "staged_lease_fence",
                "dual_read_single_write",
            )
        )
        self.assertGreater(direct, safe)

    def test_high_live_read_traffic_can_make_dual_handoff_best(self) -> None:
        dual = self.mean(
            "dual_read_single_write",
            "net_utility_per_handoff",
            failure_probability=0.50,
            request_rate=80.0,
        )
        fence = self.mean(
            "staged_lease_fence",
            "net_utility_per_handoff",
            failure_probability=0.50,
            request_rate=80.0,
        )
        stop_world = self.mean(
            "stop_world_transfer",
            "net_utility_per_handoff",
            failure_probability=0.50,
            request_rate=80.0,
        )
        self.assertGreater(dual, fence + 0.02)
        self.assertGreater(dual, stop_world + 0.60)


if __name__ == "__main__":
    unittest.main()
