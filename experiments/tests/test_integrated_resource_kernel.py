import statistics
import unittest

from ai_atlas_lab.integrated_resource_kernel import (
    FACTORIZED,
    LEARNED_JOINT,
    ORACLE_JOINT,
    UNIFORM_CHEAP,
    UNIFORM_SAFE,
    I06Config,
    run_i06,
)


class IntegratedResourceKernelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.configs = [
            I06Config(
                seed=seed,
                batches=240,
                shift_batch=120,
                tasks_per_batch=10,
                shared_capacity=10,
            )
            for seed in range(6)
        ]

    def mean(self, variant, key: str) -> float:
        return statistics.mean(
            float(run_i06(config, variant)[key]) for config in self.configs
        )

    def test_joint_allocator_beats_factorized_and_cheap(self) -> None:
        joint = self.mean(LEARNED_JOINT, "net_utility_per_task")
        self.assertGreater(
            joint,
            self.mean(FACTORIZED, "net_utility_per_task") + 0.15,
        )
        self.assertGreater(
            joint,
            self.mean(UNIFORM_CHEAP, "net_utility_per_task") + 0.50,
        )

    def test_joint_allocator_recovers_after_hidden_shift(self) -> None:
        early = self.mean(LEARNED_JOINT, "early_post_shift_utility")
        late = self.mean(LEARNED_JOINT, "late_post_shift_utility")
        self.assertGreater(late, early + 0.25)

    def test_joint_allocator_can_beat_uniform_safe_with_less_capacity(self) -> None:
        joint = self.mean(LEARNED_JOINT, "net_utility_per_task")
        safe = self.mean(UNIFORM_SAFE, "net_utility_per_task")
        self.assertGreater(joint, safe + 0.01)
        self.assertLess(
            self.mean(LEARNED_JOINT, "capacity_utilization"),
            self.mean(UNIFORM_SAFE, "capacity_utilization"),
        )

    def test_factorized_controllers_expose_interaction_failures(self) -> None:
        keys = (
            "discarded_state_failure_rate",
            "consistency_failure_rate",
            "intervention_failure_rate",
            "sensitivity_failure_rate",
        )
        factorized_failures = sum(self.mean(FACTORIZED, key) for key in keys)
        joint_failures = sum(self.mean(LEARNED_JOINT, key) for key in keys)
        self.assertGreater(factorized_failures, joint_failures + 0.02)
        self.assertGreater(self.mean(FACTORIZED, "redundant_source_rate"), 0.0)
        self.assertEqual(self.mean(LEARNED_JOINT, "redundant_source_rate"), 0.0)

    def test_recoverable_source_is_used_more_than_always_hot_breadth(self) -> None:
        self.assertGreater(
            self.mean(LEARNED_JOINT, "remat_rate"),
            self.mean(LEARNED_JOINT, "broad_rate") + 0.03,
        )

    def test_oracle_remains_an_upper_bound(self) -> None:
        self.assertGreater(
            self.mean(ORACLE_JOINT, "net_utility_per_task"),
            self.mean(LEARNED_JOINT, "net_utility_per_task") + 0.10,
        )


if __name__ == "__main__":
    unittest.main()
