import unittest

from ai_atlas_lab.external_effect_authority import I16Config, run_i16


class ExternalEffectAuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = I16Config(seed=13, trials=25_000)

    def test_authority_only_duplicates_unknown_prior_effects(self) -> None:
        result = run_i16(self.config, "authority_only")
        self.assertGreater(result["duplicate_effect"], 0.25)

    def test_execution_evidence_without_current_authority_can_retry_after_revocation(self) -> None:
        result = run_i16(self.config, "evidence_only")
        self.assertGreater(result["unauthorized_retry"], 0.07)

    def test_revocation_must_not_erase_historical_execution(self) -> None:
        result = run_i16(self.config, "revocation_erases_history")
        self.assertGreater(result["history_error"], 0.14)

    def test_separated_policy_has_no_duplicate_or_unauthorized_retry(self) -> None:
        result = run_i16(self.config, "separated")
        self.assertEqual(result["duplicate_effect"], 0.0)
        self.assertEqual(result["unauthorized_retry"], 0.0)

    def test_separated_policy_preserves_execution_history_after_revocation(self) -> None:
        result = run_i16(self.config, "separated")
        self.assertEqual(result["history_error"], 0.0)

    def test_separation_beats_each_conflated_policy(self) -> None:
        separated = run_i16(self.config, "separated")["utility"]
        for policy in ("authority_only", "evidence_only", "revocation_erases_history"):
            self.assertGreater(separated, run_i16(self.config, policy)["utility"] + 0.15)


if __name__ == "__main__":
    unittest.main()
