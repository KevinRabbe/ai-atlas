import statistics
import unittest

from ai_atlas_lab.directional_dependencies import I12Config, run_i12


class DirectionalDependencyTests(unittest.TestCase):
    def mean(self, policy: str, key: str, **overrides) -> float:
        return statistics.mean(
            float(run_i12(I12Config(seed=seed, **overrides), policy)[key])
            for seed in range(6)
        )

    def test_sparse_one_way_dependencies_do_not_justify_reverse_flow(self) -> None:
        directed = self.mean("directed_links", "sparse_directional_utility")
        symmetric = self.mean("symmetric_links", "sparse_directional_utility")
        self.assertGreater(directed, symmetric + 0.02)
        self.assertGreater(
            self.mean("symmetric_links", "false_flows_per_step"),
            self.mean("directed_links", "false_flows_per_step") + 4.0,
        )

    def test_reciprocal_clusters_justify_shared_scope(self) -> None:
        adaptive = self.mean("reciprocity_adaptive", "reciprocal_clusters_utility")
        directed = self.mean("directed_links", "reciprocal_clusters_utility")
        self.assertGreater(adaptive, directed + 0.04)

    def test_mixed_regime_uses_shared_clusters_plus_directional_links(self) -> None:
        adaptive = self.mean("reciprocity_adaptive", "mixed_utility")
        directed = self.mean("directed_links", "mixed_utility")
        symmetric = self.mean("symmetric_links", "mixed_utility")
        self.assertGreater(adaptive, directed + 0.04)
        self.assertGreater(adaptive, symmetric + 0.07)

    def test_adaptive_directionality_wins_default_mixed_lifetime(self) -> None:
        adaptive = self.mean("reciprocity_adaptive", "net_utility_per_step")
        competitors = [
            self.mean("global_scope", "net_utility_per_step"),
            self.mean("directed_links", "net_utility_per_step"),
            self.mean("symmetric_links", "net_utility_per_step"),
        ]
        self.assertGreater(adaptive, max(competitors) + 0.02)

    def test_rapid_dependency_changes_can_make_static_global_better(self) -> None:
        global_scope = self.mean(
            "global_scope",
            "net_utility_per_step",
            regime_duration=20,
        )
        adaptive = self.mean(
            "reciprocity_adaptive",
            "net_utility_per_step",
            regime_duration=20,
        )
        self.assertGreater(global_scope, adaptive + 0.05)

    def test_adaptive_directionality_avoids_symmetric_false_flow(self) -> None:
        self.assertGreater(
            self.mean("symmetric_links", "false_flows_per_step"),
            self.mean("reciprocity_adaptive", "false_flows_per_step") + 4.0,
        )


if __name__ == "__main__":
    unittest.main()
