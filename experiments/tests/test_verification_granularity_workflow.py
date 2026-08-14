import unittest

from ai_atlas_lab.verification_granularity_workflow import (
    ADAPTIVE_GRANULARITY,
    OUTCOME_ONLY,
    PROCESS_ONLY,
    UNIFORM_BOTH,
    WorkflowVerificationConfig,
    run_workflow_verification,
)


class WorkflowVerificationTests(unittest.TestCase):
    def _mean(self, policy, key):
        values = [
            run_workflow_verification(WorkflowVerificationConfig(seed=seed), policy)[key]
            for seed in range(12)
        ]
        return sum(values) / len(values)

    def test_outcome_only_misses_process_harm(self):
        self.assertGreater(
            self._mean(OUTCOME_ONLY, "process_harm_rate"),
            self._mean(PROCESS_ONLY, "process_harm_rate") * 10.0,
        )

    def test_process_only_misses_final_harm(self):
        self.assertGreater(
            self._mean(PROCESS_ONLY, "outcome_harm_rate"),
            self._mean(OUTCOME_ONLY, "outcome_harm_rate") * 10.0,
        )

    def test_uniform_both_covers_both_layers(self):
        self.assertLess(self._mean(UNIFORM_BOTH, "process_harm_rate"), 0.01)
        self.assertLess(self._mean(UNIFORM_BOTH, "outcome_harm_rate"), 0.01)

    def test_adaptive_granularity_uses_fewer_checks_than_uniform_both(self):
        self.assertLess(
            self._mean(ADAPTIVE_GRANULARITY, "checks_per_task"),
            self._mean(UNIFORM_BOTH, "checks_per_task") * 0.65,
        )

    def test_adaptive_granularity_wins_default_lifetime_utility(self):
        self.assertGreater(
            self._mean(ADAPTIVE_GRANULARITY, "net_utility_per_task"),
            self._mean(UNIFORM_BOTH, "net_utility_per_task") + 0.05,
        )


if __name__ == "__main__":
    unittest.main()
