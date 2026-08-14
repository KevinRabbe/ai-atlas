import statistics
import unittest

from ai_atlas_lab.typed_scope_runtime import I08Config, run_i08


class TypedScopeRuntimeTests(unittest.TestCase):
    def configs(self, **overrides):
        return [I08Config(seed=seed, **overrides) for seed in range(6)]

    def mean(self, variant: str, key: str, **overrides) -> float:
        return statistics.mean(
            float(run_i08(config, variant)[key])
            for config in self.configs(**overrides)
        )

    def test_typed_epoch_preserves_migration_invariants(self) -> None:
        for config in self.configs():
            result = run_i08(config, "typed_epoch")
            self.assertEqual(result["authority_violations"], 0)
            self.assertEqual(result["event_misroutes"], 0)
            self.assertEqual(result["provenance_failures"], 0)
            self.assertEqual(result["rematerialization_failures"], 0)
            self.assertEqual(result["duplicate_resource_exposure_per_step"], 0.0)
            self.assertGreater(result["forwarded_events"], 5)

    def test_scope_snapshot_exposes_state_that_should_not_be_scope_relative(self) -> None:
        self.assertGreater(self.mean("scope_snapshot", "authority_violations"), 1.0)
        self.assertGreater(self.mean("scope_snapshot", "event_misroutes"), 10.0)
        self.assertGreater(self.mean("scope_snapshot", "provenance_failures"), 20.0)
        self.assertGreater(self.mean("scope_snapshot", "rematerialization_failures"), 20.0)
        self.assertGreater(
            self.mean("scope_snapshot", "duplicate_resource_exposure_per_step"),
            1.0,
        )

    def test_stale_route_ablation_isolates_in_flight_event_failure(self) -> None:
        self.assertGreater(self.mean("typed_stale_route", "event_misroutes"), 10.0)
        for key in (
            "authority_violations",
            "provenance_failures",
            "rematerialization_failures",
            "duplicate_resource_exposure_per_step",
        ):
            self.assertEqual(self.mean("typed_stale_route", key), 0.0)

    def test_safe_dynamic_runtime_beats_static_topology_when_structure_persists(self) -> None:
        dynamic = self.mean("typed_epoch", "net_utility_per_step")
        static = self.mean("static_typed", "net_utility_per_step")
        self.assertGreater(dynamic, static + 0.04)

    def test_epoch_forwarding_beats_typed_state_with_stale_scope_routes(self) -> None:
        safe = self.mean("typed_epoch", "net_utility_per_step")
        stale = self.mean("typed_stale_route", "net_utility_per_step")
        self.assertGreater(safe, stale + 0.005)

    def test_fast_expensive_migration_can_make_static_topology_better(self) -> None:
        static = self.mean(
            "static_typed",
            "net_utility_per_step",
            regime_duration=20,
            safe_migration_cost=0.20,
        )
        dynamic = self.mean(
            "typed_epoch",
            "net_utility_per_step",
            regime_duration=20,
            safe_migration_cost=0.20,
        )
        self.assertGreater(static, dynamic + 0.003)


if __name__ == "__main__":
    unittest.main()
