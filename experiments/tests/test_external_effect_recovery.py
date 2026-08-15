import unittest

from ai_atlas_lab.external_effect_recovery import (
    ExternalLedgerConfig,
    PhysicalEffectConfig,
    run_external_ledger,
    run_physical_effect,
)


class ExternalEffectRecoveryTests(unittest.TestCase):
    def test_blind_retry_duplicates_effects_when_remote_outcome_is_unknown(self) -> None:
        result = run_external_ledger(ExternalLedgerConfig(seed=3), "blind_retry")
        self.assertGreater(result["duplicate_effect"], 0.45)

    def test_externally_recognized_stable_identity_removes_retry_ambiguity(self) -> None:
        result = run_external_ledger(ExternalLedgerConfig(seed=4), "stable_identity")
        self.assertEqual(result["duplicate_effect"], 0.0)
        self.assertEqual(result["missed_effect"], 0.0)
        self.assertGreater(result["utility"], 0.95)

    def test_exact_external_reconciliation_also_removes_retry_ambiguity(self) -> None:
        result = run_external_ledger(ExternalLedgerConfig(seed=5), "reconcile")
        self.assertEqual(result["duplicate_effect"], 0.0)
        self.assertEqual(result["missed_effect"], 0.0)

    def test_noisy_world_sensor_cannot_reconstruct_exact_effect_history(self) -> None:
        result = run_physical_effect(PhysicalEffectConfig(seed=6), "sensor_reconcile")
        self.assertGreater(result["duplicate_effect"], 0.03)
        self.assertGreater(result["missed_effect"], 0.02)

    def test_duplicate_dominated_risk_can_make_abstention_rational(self) -> None:
        config = PhysicalEffectConfig(
            seed=7,
            duplicate_penalty=8.0,
            missed_penalty=1.0,
        )
        risk = run_physical_effect(config, "risk_sensitive")
        blind = run_physical_effect(config, "blind_retry")
        self.assertEqual(risk["duplicate_effect"], 0.0)
        self.assertGreater(risk["utility"], blind["utility"] + 2.0)

    def test_omission_dominated_risk_can_make_retry_after_sensor_rational(self) -> None:
        config = PhysicalEffectConfig(
            seed=8,
            duplicate_penalty=1.0,
            missed_penalty=4.0,
        )
        risk = run_physical_effect(config, "risk_sensitive")
        abstain = run_physical_effect(config, "abstain")
        self.assertGreater(risk["duplicate_effect"], 0.03)
        self.assertLess(risk["missed_effect"], 0.08)
        self.assertGreater(risk["utility"], abstain["utility"] + 0.4)


if __name__ == "__main__":
    unittest.main()
