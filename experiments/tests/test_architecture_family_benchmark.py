import statistics
import unittest

from ai_atlas_lab.architecture_family_benchmark import (
    ARCHITECTURES,
    DEVELOPMENTAL_D,
    DISTRIBUTED_B,
    HIERARCHICAL_A,
    INTEGRATED_C,
    ArchitectureScenario,
    coupled_switching,
    recurring_mixed,
    run_architecture_family,
    sparse_stationary,
)


class ArchitectureFamilyBenchmarkTests(unittest.TestCase):
    def small(self, builder, seed: int) -> ArchitectureScenario:
        scenario = builder(seed)
        if scenario.name == "sparse_stationary":
            regime_length = 10_000
        elif scenario.name == "coupled_switching":
            regime_length = 55
        else:
            regime_length = 44
        return ArchitectureScenario(
            **{
                **scenario.__dict__,
                "batches": 220,
                "tasks_per_batch": 8,
                "regime_length": regime_length,
                "central_batch_cost": 0.288,
                "archive_batch_cost": 0.192,
            }
        )

    def mean(self, builder, architecture, key: str) -> float:
        return statistics.mean(
            float(run_architecture_family(self.small(builder, seed), architecture)[key])
            for seed in range(3)
        )

    def test_distributed_organization_reduces_control_traffic(self) -> None:
        self.assertLess(
            self.mean(sparse_stationary, DISTRIBUTED_B, "control_messages_per_task"),
            self.mean(sparse_stationary, HIERARCHICAL_A, "control_messages_per_task") * 0.6,
        )
        self.assertLess(
            self.mean(sparse_stationary, DISTRIBUTED_B, "explicit_overhead_per_task"),
            self.mean(sparse_stationary, HIERARCHICAL_A, "explicit_overhead_per_task"),
        )

    def test_pooled_core_pays_interference_on_family_specific_stationary_work(self) -> None:
        pooled = self.mean(sparse_stationary, INTEGRATED_C, "net_utility_per_task")
        conditional = self.mean(sparse_stationary, HIERARCHICAL_A, "net_utility_per_task")
        self.assertGreater(conditional, pooled + 0.03)

    def test_pooled_core_can_win_recurring_mixed_work(self) -> None:
        pooled = self.mean(recurring_mixed, INTEGRATED_C, "net_utility_per_task")
        hierarchical = self.mean(recurring_mixed, HIERARCHICAL_A, "net_utility_per_task")
        distributed = self.mean(recurring_mixed, DISTRIBUTED_B, "net_utility_per_task")
        self.assertGreater(pooled, hierarchical + 0.05)
        self.assertGreater(pooled, distributed + 0.05)

    def test_developmental_variants_reuse_multiple_regimes(self) -> None:
        switches = self.mean(recurring_mixed, DEVELOPMENTAL_D, "archive_switches")
        self.assertGreater(switches, 1.0)
        self.assertLess(
            self.mean(recurring_mixed, DEVELOPMENTAL_D, "error_rate"),
            self.mean(recurring_mixed, HIERARCHICAL_A, "error_rate"),
        )

    def test_first_family_comparison_has_no_universal_utility_winner(self) -> None:
        winners = set()
        for builder in (sparse_stationary, coupled_switching, recurring_mixed):
            utilities = {
                architecture.family: self.mean(builder, architecture, "net_utility_per_task")
                for architecture in ARCHITECTURES
            }
            winners.add(max(utilities, key=utilities.get))
        self.assertGreaterEqual(len(winners), 2)


if __name__ == "__main__":
    unittest.main()
