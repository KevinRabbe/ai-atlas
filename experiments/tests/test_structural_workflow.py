import unittest

from ai_atlas_lab.structural_workflow import (
    StructuralWorkflowConfig,
    run_structural_workflow,
)


def mean_metric(family, variant, metric, seeds=12):
    values = [
        run_structural_workflow(
            StructuralWorkflowConfig(seed=seed),
            family,
            variant,
        )[metric]
        for seed in range(seeds)
    ]
    return sum(values) / len(values)


class StructuralWorkflowTests(unittest.TestCase):
    def test_indirect_structure_wins_repeated_workflow(self):
        indirect = mean_metric("repeated_workflow", "adaptive_indirect", "net_utility_per_round")
        direct = mean_metric("repeated_workflow", "direct", "net_utility_per_round")
        self.assertGreater(indirect, direct + 0.010)

    def test_indirect_recovers_coherent_topology_shift_immediately(self):
        indirect = mean_metric("repeated_workflow", "adaptive_indirect", "first10_after_shift")
        direct = mean_metric("repeated_workflow", "direct", "first10_after_shift")
        self.assertGreater(indirect, 0.99)
        self.assertGreater(indirect, direct + 0.20)

    def test_always_generative_loses_on_irregular_workflow(self):
        direct = mean_metric("irregular_workflow", "direct", "net_utility_per_round")
        generative = mean_metric("irregular_workflow", "generative", "net_utility_per_round")
        self.assertGreater(direct, generative + 0.004)

    def test_adaptive_indirect_keeps_local_fallback(self):
        adaptive = mean_metric("irregular_workflow", "adaptive_indirect", "net_utility_per_round")
        direct = mean_metric("irregular_workflow", "direct", "net_utility_per_round")
        self.assertGreaterEqual(adaptive, direct - 0.001)

    def test_repeated_indirect_reduces_dependency_overhead(self):
        indirect = mean_metric("repeated_workflow", "adaptive_indirect", "dependency_violation_rate")
        direct = mean_metric("repeated_workflow", "direct", "dependency_violation_rate")
        self.assertLess(indirect, direct * 0.10)


if __name__ == "__main__":
    unittest.main()
