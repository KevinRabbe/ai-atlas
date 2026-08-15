import unittest

from ai_atlas_lab.external_effect_protocol import (
    ExternalEffectIntent,
    ExternalExecutionObservation,
    decide_external_effect_recovery,
)


class ExternalEffectProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.intent = ExternalEffectIntent("effect-42", "remote:door", consequence=4.0)

    def decide(self, observation, **kwargs):
        defaults = dict(
            current_authority=True,
            receiver_recognizes_identity=False,
            duplicate_penalty=4.0,
            missed_penalty=1.0,
        )
        defaults.update(kwargs)
        return decide_external_effect_recovery(self.intent, observation, **defaults)

    def test_exact_applied_evidence_marks_history_complete_even_after_revocation(self) -> None:
        decision = self.decide(
            ExternalExecutionObservation("applied", effect_specific=True, evidence_ref="receipt:42"),
            current_authority=False,
        )
        self.assertEqual(decision.action, "mark_complete")

    def test_exact_absence_still_requires_current_authority_for_retry(self) -> None:
        decision = self.decide(
            ExternalExecutionObservation("absent", effect_specific=True, evidence_ref="receipt:42"),
            current_authority=False,
        )
        self.assertEqual(decision.action, "blocked")

    def test_exact_absence_retries_when_currently_authorized(self) -> None:
        decision = self.decide(
            ExternalExecutionObservation("absent", effect_specific=True, evidence_ref="receipt:42")
        )
        self.assertEqual(decision.action, "retry")

    def test_receiver_recognized_identity_allows_deduplicated_replay(self) -> None:
        decision = self.decide(
            ExternalExecutionObservation("unknown", effect_specific=False),
            receiver_recognizes_identity=True,
        )
        self.assertEqual(decision.action, "retry_same_identity")

    def test_non_identifiable_unknown_effect_remains_unresolved_without_probability(self) -> None:
        decision = self.decide(
            ExternalExecutionObservation("unknown", effect_specific=False)
        )
        self.assertEqual(decision.action, "unresolved")

    def test_unresolved_effect_uses_explicit_duplicate_vs_omission_tradeoff(self) -> None:
        observation = ExternalExecutionObservation(
            "unknown",
            effect_specific=False,
            probability_applied=0.6,
        )
        duplicate_dominated = self.decide(
            observation,
            duplicate_penalty=8.0,
            missed_penalty=1.0,
        )
        omission_dominated = self.decide(
            observation,
            duplicate_penalty=1.0,
            missed_penalty=8.0,
        )
        self.assertEqual(duplicate_dominated.action, "abstain")
        self.assertEqual(omission_dominated.action, "retry")


if __name__ == "__main__":
    unittest.main()
