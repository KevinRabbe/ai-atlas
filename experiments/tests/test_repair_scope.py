import unittest

from ai_atlas_lab.repair_scope import RepairScopeConfig, run_repair_scope


class RepairScopeTests(unittest.TestCase):
    def _mean(self, family, policy, key):
        vals = [
            run_repair_scope(RepairScopeConfig(seed=s, family=family), policy)[key]
            for s in range(12)
        ]
        return sum(vals) / len(vals)

    def test_local_repair_wins_sparse_isolated_faults(self):
        local = self._mean("isolated", "local_only", "net_utility_per_step")
        component = self._mean("isolated", "component_only", "net_utility_per_step")
        structural = self._mean("isolated", "structural_only", "net_utility_per_step")
        self.assertGreater(local, component)
        self.assertGreater(local, structural + 0.03)

    def test_adaptive_scope_stays_near_local_on_isolated_faults(self):
        local = self._mean("isolated", "local_only", "net_utility_per_step")
        adaptive = self._mean("isolated", "adaptive_scope", "net_utility_per_step")
        self.assertGreater(adaptive, local - 0.01)

    def test_component_scope_resolves_recurring_component_root(self):
        self.assertGreater(
            self._mean("component", "component_only", "net_utility_per_step"),
            self._mean("component", "local_only", "net_utility_per_step") + 0.30,
        )

    def test_adaptive_scope_matches_component_regime_without_always_broad_change(self):
        self.assertGreater(
            self._mean("component", "adaptive_scope", "net_utility_per_step"),
            self._mean("component", "component_only", "net_utility_per_step") - 0.01,
        )

    def test_structural_scope_beats_local_on_systemic_fault(self):
        self.assertGreater(
            self._mean("systemic", "structural_only", "net_utility_per_step"),
            self._mean("systemic", "local_only", "net_utility_per_step") + 0.40,
        )

    def test_adaptive_scope_beats_always_structural_and_uses_fewer_broad_changes(self):
        self.assertGreater(
            self._mean("systemic", "adaptive_scope", "net_utility_per_step"),
            self._mean("systemic", "structural_only", "net_utility_per_step") + 0.02,
        )
        self.assertLess(
            self._mean("systemic", "adaptive_scope", "structural_changes"),
            self._mean("systemic", "structural_only", "structural_changes") * 0.10,
        )


if __name__ == "__main__":
    unittest.main()
