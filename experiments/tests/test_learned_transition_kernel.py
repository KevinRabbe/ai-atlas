import unittest

from ai_atlas_lab.learned_transition_kernel import (
    FROZEN_CONDITIONAL,
    LEARNED_CONDITIONAL,
    LEARNED_GLOBAL,
    ORACLE_UPPER_BOUND,
    LearnedKernelConfig,
    run_learned_transition_kernel,
)


def mean_metric(variant, metric, seeds=12):
    values = [
        run_learned_transition_kernel(LearnedKernelConfig(seed=seed), variant)[metric]
        for seed in range(seeds)
    ]
    return sum(values) / len(values)


class LearnedTransitionKernelTests(unittest.TestCase):
    def test_typed_authority_remains_exact(self):
        for variant in (ORACLE_UPPER_BOUND, LEARNED_CONDITIONAL, LEARNED_GLOBAL, FROZEN_CONDITIONAL):
            self.assertEqual(mean_metric(variant, "authority_violations", 6), 0.0)

    def test_learned_conditional_beats_frozen_after_shift(self):
        learned = mean_metric(LEARNED_CONDITIONAL, "post_shift_late_utility")
        frozen = mean_metric(FROZEN_CONDITIONAL, "post_shift_late_utility")
        self.assertGreater(learned, frozen + 0.15)

    def test_conditional_learning_beats_global_pooling(self):
        learned = mean_metric(LEARNED_CONDITIONAL, "net_utility_per_task")
        global_model = mean_metric(LEARNED_GLOBAL, "net_utility_per_task")
        self.assertGreater(learned, global_model + 0.025)

    def test_learned_policy_recovers_after_shift(self):
        early = mean_metric(LEARNED_CONDITIONAL, "post_shift_early_utility")
        late = mean_metric(LEARNED_CONDITIONAL, "post_shift_late_utility")
        self.assertGreater(late, early + 0.12)

    def test_coupling_allocation_reverses_with_evidence(self):
        before_f1 = mean_metric(LEARNED_CONDITIONAL, "phase0_coupled_family1_work_rate")
        before_f0 = mean_metric(LEARNED_CONDITIONAL, "phase0_coupled_family0_work_rate")
        after_f0 = mean_metric(LEARNED_CONDITIONAL, "phase1_coupled_family0_work_rate")
        after_f1 = mean_metric(LEARNED_CONDITIONAL, "phase1_coupled_family1_work_rate")
        self.assertGreater(before_f1, before_f0 + 0.02)
        self.assertGreater(after_f0, after_f1 + 0.01)

    def test_oracle_remains_upper_bound(self):
        oracle = mean_metric(ORACLE_UPPER_BOUND, "net_utility_per_task")
        learned = mean_metric(LEARNED_CONDITIONAL, "net_utility_per_task")
        self.assertGreater(oracle, learned)


if __name__ == "__main__":
    unittest.main()
