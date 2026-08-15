import statistics
import unittest

from ai_atlas_lab.evidence_dependence_scale import I26DConfig, run_i26d


class EvidenceDependenceScaleTests(unittest.TestCase):
    def mean(
        self,
        policy: str,
        key: str,
        *,
        storage_cost: float = 0.00002,
    ) -> float:
        return statistics.mean(
            run_i26d(
                I26DConfig(seed=seed, relation_storage_cost=storage_cost),
                policy,
            ).get(key, 0.0)
            for seed in range(6)
        )

    def test_dense_full_graph_is_not_required_for_sparse_decisions(self) -> None:
        self.assertGreater(
            self.mean("scoped_ttl", "utility"),
            self.mean("dense_exact", "utility") + 0.10,
        )

    def test_scoped_cache_beats_querying_every_active_pair_repeatedly(self) -> None:
        self.assertGreater(
            self.mean("scoped_ttl", "utility"),
            self.mean("query_every_time", "utility") + 0.05,
        )

    def test_scoped_cache_beats_assuming_independence(self) -> None:
        self.assertGreater(
            self.mean("scoped_ttl", "utility"),
            self.mean("assume_independent", "utility") + 0.20,
        )

    def test_scoped_cache_materializes_small_fraction_of_possible_relations(self) -> None:
        active = self.mean("scoped_ttl", "final_relation_state")
        possible = self.mean("scoped_ttl", "possible_pair_relations")
        self.assertLess(active, possible * 0.10)

    def test_ttl_releases_relations_from_inactive_source_pool(self) -> None:
        self.assertLess(
            self.mean("scoped_ttl", "final_relation_state"),
            self.mean("cache_forever", "final_relation_state") * 0.70,
        )

    def test_permanent_cache_can_win_when_relation_storage_is_nearly_free(self) -> None:
        forever = self.mean(
            "cache_forever",
            "utility",
            storage_cost=0.0,
        )
        ttl = self.mean(
            "scoped_ttl",
            "utility",
            storage_cost=0.0,
        )
        self.assertGreater(forever, ttl)

    def test_dense_graph_cost_grows_with_full_source_population(self) -> None:
        dense = run_i26d(I26DConfig(seed=1), "dense_exact")
        self.assertEqual(dense["possible_pair_relations"], 8128.0)
        self.assertEqual(dense["final_relation_state"], 8128.0)


if __name__ == "__main__":
    unittest.main()
