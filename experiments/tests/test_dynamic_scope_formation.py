import statistics
import unittest

from ai_atlas_lab.dynamic_scope_formation import I07Config, run_i07


class DynamicScopeFormationTests(unittest.TestCase):
    def mean(self, policy: str, key: str, duration: int = 80) -> float:
        return statistics.mean(
            float(
                run_i07(
                    I07Config(seed=seed, cycles=3, regime_duration=duration),
                    policy,
                )[key]
            )
            for seed in range(6)
        )

    def test_adaptive_scopes_beat_static_topologies_when_structure_persists(self) -> None:
        adaptive = self.mean("adaptive", "net_utility_per_step")
        best_static = max(
            self.mean(policy, "net_utility_per_step")
            for policy in ("global", "local", "fixed_initial")
        )
        self.assertGreater(adaptive, best_static + 0.015)

    def test_adaptive_scope_recovers_most_pairwise_structure(self) -> None:
        self.assertGreater(self.mean("adaptive", "pairwise_scope_accuracy"), 0.86)

    def test_oracle_partition_remains_upper_bound(self) -> None:
        self.assertGreater(
            self.mean("oracle", "net_utility_per_step"),
            self.mean("adaptive", "net_utility_per_step") + 0.01,
        )

    def test_fast_structural_change_can_make_static_topology_better(self) -> None:
        adaptive = self.mean("adaptive", "net_utility_per_step", duration=20)
        global_static = self.mean("global", "net_utility_per_step", duration=20)
        self.assertLess(adaptive, global_static)

    def test_adaptive_topology_actually_splits_and_merges(self) -> None:
        self.assertGreater(self.mean("adaptive", "migrations"), 5.0)
        self.assertGreater(self.mean("adaptive", "migration_spend_per_step"), 0.0)


if __name__ == "__main__":
    unittest.main()
