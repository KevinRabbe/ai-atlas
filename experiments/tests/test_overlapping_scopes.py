import statistics
import unittest

from ai_atlas_lab.overlapping_scopes import I11Config, run_i11


class OverlappingScopeTests(unittest.TestCase):
    def mean(self, policy: str, key: str = "net_utility_per_step", **overrides) -> float:
        return statistics.mean(
            float(run_i11(I11Config(seed=seed, **overrides), policy)[key])
            for seed in range(6)
        )

    def test_sparse_cross_cutting_work_favors_temporary_overlay(self) -> None:
        overlay = self.mean("temporary_overlay", cross_probability=0.18)
        base = self.mean("base_partition", cross_probability=0.18)
        persistent = self.mean("persistent_overlap", cross_probability=0.18)
        self.assertGreater(overlay, base + 0.002)
        self.assertGreater(overlay, persistent + 0.05)

    def test_forcing_disjoint_repartition_loses_base_structure(self) -> None:
        repartition = self.mean("forced_repartition", cross_probability=0.18)
        overlay = self.mean("temporary_overlay", cross_probability=0.18)
        self.assertGreater(overlay, repartition + 0.03)
        self.assertGreater(
            self.mean("forced_repartition", "missed_pairs_per_step", cross_probability=0.18),
            self.mean("temporary_overlay", "missed_pairs_per_step", cross_probability=0.18),
        )

    def test_frequent_cross_cutting_work_can_make_persistent_overlap_worth_it(self) -> None:
        persistent = self.mean("persistent_overlap", cross_probability=0.90)
        overlay = self.mean("temporary_overlay", cross_probability=0.90)
        base = self.mean("base_partition", cross_probability=0.90)
        self.assertGreater(persistent, overlay + 0.015)
        self.assertGreater(persistent, base + 0.03)

    def test_dense_coupling_can_make_one_global_scope_cheapest(self) -> None:
        global_scope = self.mean("global_scope", dense_coupling=True, cross_probability=1.0)
        persistent = self.mean("persistent_overlap", dense_coupling=True, cross_probability=1.0)
        overlay = self.mean("temporary_overlay", dense_coupling=True, cross_probability=1.0)
        self.assertGreater(global_scope, persistent + 0.01)
        self.assertGreater(global_scope, overlay + 0.10)

    def test_overlap_strategy_has_a_recurrence_crossover(self) -> None:
        sparse_delta = (
            self.mean("persistent_overlap", cross_probability=0.20)
            - self.mean("temporary_overlay", cross_probability=0.20)
        )
        frequent_delta = (
            self.mean("persistent_overlap", cross_probability=0.80)
            - self.mean("temporary_overlay", cross_probability=0.80)
        )
        self.assertLess(sparse_delta, -0.04)
        self.assertGreater(frequent_delta, 0.005)

    def test_temporary_overlay_pays_state_only_when_cross_scope_work_is_active(self) -> None:
        sparse = self.mean("temporary_overlay", "mean_memberships", cross_probability=0.10)
        frequent = self.mean("temporary_overlay", "mean_memberships", cross_probability=0.90)
        self.assertLess(sparse, frequent - 2.5)


if __name__ == "__main__":
    unittest.main()
