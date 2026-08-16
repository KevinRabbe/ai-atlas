import statistics
import unittest
from dataclasses import replace

from ai_atlas_lab.self_change_audit_selection import I29Config, run_i29


class SelfChangeAuditSelectionTests(unittest.TestCase):
    def mean(self, policy: str, key: str, **changes) -> float:
        return statistics.mean(
            run_i29(
                replace(I29Config(seed=seed), **changes),
                policy,
            )[key]
            for seed in range(6)
        )

    def test_flagged_only_scalar_audits_are_not_population_calibration(self) -> None:
        self.assertGreater(
            self.mean("flagged_selected_scalar", "global_calibration_error"),
            0.40,
        )
        self.assertLess(
            self.mean("random_coverage_scalar", "global_calibration_error"),
            0.03,
        )

    def test_flagged_selected_scalar_becomes_overconservative(self) -> None:
        self.assertLess(
            self.mean("flagged_selected_scalar", "safe_promotions"),
            0.01,
        )
        self.assertLess(
            self.mean("flagged_selected_scalar", "net_utility"),
            self.mean("visible_only", "net_utility") - 0.10,
        )

    def test_flagged_only_conditional_cannot_calibrate_safe_path(self) -> None:
        self.assertGreater(
            self.mean("flagged_only_conditional", "safe_path_calibration_error"),
            self.mean("selection_aware_conditional", "safe_path_calibration_error")
            + 0.04,
        )

    def test_small_safe_path_coverage_learns_conditional_risk(self) -> None:
        self.assertLess(
            self.mean("selection_aware_conditional", "safe_path_calibration_error"),
            0.02,
        )
        self.assertLess(
            self.mean("selection_aware_conditional", "flagged_path_calibration_error"),
            0.03,
        )

    def test_selection_aware_conditional_beats_visible_policy(self) -> None:
        self.assertGreater(
            self.mean("selection_aware_conditional", "net_utility"),
            self.mean("visible_only", "net_utility") + 0.05,
        )

    def test_selection_aware_conditional_reduces_harmful_promotions(self) -> None:
        self.assertLess(
            self.mean("selection_aware_conditional", "harmful_promotions"),
            self.mean("visible_only", "harmful_promotions") * 0.65,
        )

    def test_selection_aware_audits_both_output_strata(self) -> None:
        self.assertGreater(
            self.mean("selection_aware_conditional", "safe_audit_rate"),
            0.02,
        )
        self.assertGreater(
            self.mean("selection_aware_conditional", "flagged_audit_rate"),
            0.10,
        )

    def test_auditing_can_stop_paying_when_expensive(self) -> None:
        self.assertGreater(
            self.mean("visible_only", "net_utility"),
            self.mean(
                "selection_aware_conditional",
                "net_utility",
                audit_cost=1.0,
            )
            + 0.03,
        )


if __name__ == "__main__":
    unittest.main()
