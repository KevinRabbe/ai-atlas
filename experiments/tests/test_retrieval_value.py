import unittest

from ai_atlas_lab.retrieval_value import (
    RetrievalConfig,
    run_causal_retrieval,
    run_staleness_retrieval,
)


class RetrievalValueTests(unittest.TestCase):
    def test_similarity_is_cheapest_when_semantics_stay_applicable(self):
        rows = dict(
            run_staleness_retrieval(
                RetrievalConfig(seed=1), shifted_fraction=0.0
            )
        )
        self.assertGreater(
            rows["similarity"]["net_utility"],
            rows["temporal_applicability"]["net_utility"],
        )

    def test_applicability_beats_similarity_after_regime_change(self):
        rows = dict(
            run_staleness_retrieval(
                RetrievalConfig(seed=2), shifted_fraction=0.5
            )
        )
        self.assertGreater(
            rows["temporal_applicability"]["net_utility"],
            rows["similarity"]["net_utility"],
        )

    def test_similarity_is_cheapest_when_surface_and_mechanism_agree(self):
        rows = dict(
            run_causal_retrieval(
                RetrievalConfig(seed=3), conflict_probability=0.0
            )
        )
        self.assertGreater(
            rows["similarity"]["net_utility"],
            rows["decision_value"]["net_utility"],
        )

    def test_decision_value_wins_when_surface_and_cause_diverge(self):
        rows = dict(
            run_causal_retrieval(
                RetrievalConfig(seed=4), conflict_probability=0.8
            )
        )
        self.assertEqual(rows["decision_value"]["accuracy"], 1.0)
        self.assertGreater(
            rows["decision_value"]["net_utility"],
            rows["similarity"]["net_utility"],
        )


if __name__ == "__main__":
    unittest.main()
