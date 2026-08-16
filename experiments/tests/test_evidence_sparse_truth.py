import statistics
import unittest
from dataclasses import replace

from ai_atlas_lab.evidence_sparse_truth import I28DConfig, run_i28d


class SparseDelayedTruthTests(unittest.TestCase):
    def mean(self, policy: str, key: str, **changes) -> float:
        return statistics.mean(
            run_i28d(
                replace(I28DConfig(seed=seed), **changes),
                policy,
            )[key]
            for seed in range(6)
        )

    def test_sparse_delayed_feedback_leaves_post_shift_relation_stale(self) -> None:
        self.assertLess(
            self.mean("passive_behavioral", "feedback_rate"),
            0.02,
        )
        self.assertLess(
            self.mean("passive_behavioral", "post_shift_relation_accuracy"),
            0.20,
        )

    def test_provenance_probe_nearly_recovers_oracle_relation(self) -> None:
        self.assertGreater(
            self.mean("provenance_probe", "relation_accuracy"),
            0.95,
        )
        self.assertLess(
            abs(
                self.mean("provenance_probe", "error_rate")
                - self.mean("oracle_relation", "error_rate")
            ),
            0.003,
        )

    def test_provenance_probe_reduces_immediate_post_shift_error(self) -> None:
        self.assertLess(
            self.mean("provenance_probe", "post_shift_error"),
            self.mean("passive_behavioral", "post_shift_error") - 0.003,
        )

    def test_disagreement_only_truth_sampling_biases_relation_learning(self) -> None:
        self.assertGreater(
            self.mean("disagreement_targeted_truth", "error_rate"),
            self.mean("passive_behavioral", "error_rate") + 0.02,
        )
        self.assertLess(
            self.mean("disagreement_targeted_truth", "relation_accuracy"),
            self.mean("passive_behavioral", "relation_accuracy"),
        )

    def test_output_independent_truth_sampling_avoids_disagreement_bias(self) -> None:
        self.assertLess(
            self.mean("coverage_targeted_truth", "error_rate"),
            self.mean("disagreement_targeted_truth", "error_rate") - 0.02,
        )
        self.assertGreater(
            self.mean("coverage_targeted_truth", "relation_accuracy"),
            self.mean("disagreement_targeted_truth", "relation_accuracy") + 0.15,
        )

    def test_output_independent_truth_uses_fewer_queries_than_disagreement_sampling(self) -> None:
        self.assertLess(
            self.mean("coverage_targeted_truth", "active_resolution_rate"),
            self.mean("disagreement_targeted_truth", "active_resolution_rate") * 0.60,
        )

    def test_direct_relation_evidence_can_be_sparse(self) -> None:
        self.assertLess(
            self.mean("provenance_probe", "provenance_probe_rate"),
            0.01,
        )

    def test_expensive_provenance_can_lose_to_active_truth_learning(self) -> None:
        self.assertGreater(
            self.mean("coverage_targeted_truth", "net_utility"),
            self.mean(
                "provenance_probe",
                "net_utility",
                provenance_probe_cost=15.0,
            )
            + 0.02,
        )


if __name__ == "__main__":
    unittest.main()
