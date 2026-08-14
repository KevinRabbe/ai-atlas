import unittest

from ai_atlas_lab.metacognitive_feedback import (
    MetacognitiveFeedbackConfig,
    run_metacognitive_feedback,
)


def mean_metric(mode, metric, seeds=12):
    values = [
        run_metacognitive_feedback(
            MetacognitiveFeedbackConfig(seed=seed),
            mode,
        )[metric]
        for seed in range(seeds)
    ]
    return sum(values) / len(values)


class MetacognitiveFeedbackTests(unittest.TestCase):
    def test_active_audit_beats_sparse_noisy_passive_feedback(self):
        active = mean_metric("active", "net_utility_per_task")
        passive = mean_metric("passive", "net_utility_per_task")
        self.assertGreater(active, passive + 0.12)

    def test_active_audit_beats_no_feedback(self):
        active = mean_metric("active", "net_utility_per_task")
        none = mean_metric("none", "net_utility_per_task")
        self.assertGreater(active, none + 0.30)

    def test_active_audit_suppresses_false_durable_learning(self):
        active = mean_metric("active", "false_durable_writes")
        none = mean_metric("none", "false_durable_writes")
        self.assertLess(active, none * 0.15)

    def test_active_audit_recovers_after_hidden_quality_swap(self):
        early = mean_metric("active", "early_post_shift_utility")
        late = mean_metric("active", "late_post_shift_utility")
        self.assertGreater(late, early + 0.60)

    def test_audit_is_selective_not_permanent(self):
        rate = mean_metric("active", "active_audits_per_task")
        self.assertGreater(rate, 0.25)
        self.assertLess(rate, 0.50)

    def test_audit_demand_falls_after_learning(self):
        early_lifetime = mean_metric("active", "pre_shift_active_audit_rate")
        late = mean_metric("active", "late_post_shift_active_audit_rate")
        self.assertLess(late, early_lifetime - 0.10)


if __name__ == "__main__":
    unittest.main()
