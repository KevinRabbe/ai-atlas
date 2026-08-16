import statistics
import unittest
from dataclasses import replace

from ai_atlas_lab.discovery_verification_selection import I30Config, run_i30


class DiscoveryVerificationSelectionTests(unittest.TestCase):
    def mean(self, policy: str, key: str, **changes) -> float:
        return statistics.mean(
            run_i30(
                replace(I30Config(seed=seed), **changes),
                policy,
            )[key]
            for seed in range(6)
        )

    def test_near_threshold_rejects_are_not_representative_of_all_rejects(self) -> None:
        self.assertGreater(
            self.mean(
                "near_threshold_global",
                "ordinary_reject_audit_precision",
            ),
            self.mean(
                "random_domain",
                "ordinary_reject_audit_precision",
            )
            + 0.25,
        )

    def test_targeted_sample_inflates_global_reject_truth_estimate(self) -> None:
        self.assertGreater(
            self.mean(
                "near_threshold_global",
                "ordinary_domain_estimate",
            ),
            0.35,
        )
        self.assertLess(
            self.mean("random_domain", "ordinary_domain_estimate"),
            0.25,
        )

    def test_selection_aware_bins_beat_targeted_global_generalization(self) -> None:
        self.assertGreater(
            self.mean("selection_aware_bin", "net_utility"),
            self.mean("near_threshold_global", "net_utility") + 0.02,
        )

    def test_selection_aware_discovery_beats_pass_only(self) -> None:
        self.assertGreater(
            self.mean("selection_aware_bin", "net_utility"),
            self.mean("pass_only", "net_utility") + 0.05,
        )

    def test_selection_aware_policy_uses_fewer_reject_verifications_than_biased_global_policy(self) -> None:
        self.assertLess(
            self.mean(
                "selection_aware_bin",
                "rejected_verification_rate",
            ),
            self.mean(
                "near_threshold_global",
                "rejected_verification_rate",
            )
            * 0.75,
        )

    def test_selection_aware_policy_recovers_real_discoveries(self) -> None:
        self.assertGreater(
            self.mean("selection_aware_bin", "recovered_discoveries"),
            self.mean("pass_only", "recovered_discoveries") + 0.03,
        )

    def test_learned_selection_aware_policy_remains_below_but_near_oracle(self) -> None:
        learned = self.mean("selection_aware_bin", "net_utility")
        oracle = self.mean("oracle_score", "net_utility")
        self.assertLess(learned, oracle)
        self.assertGreater(learned, oracle - 0.10)

    def test_reject_verification_stops_paying_when_expensive(self) -> None:
        self.assertGreater(
            self.mean("pass_only", "net_utility", rejected_verification_cost=2.0),
            self.mean(
                "selection_aware_bin",
                "net_utility",
                rejected_verification_cost=2.0,
            )
            + 0.02,
        )


if __name__ == "__main__":
    unittest.main()
