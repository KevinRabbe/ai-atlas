import unittest

from ai_atlas_lab.control_contention import ControlContentionExperimentConfig, run_control_contention_experiment


class ControlContentionTests(unittest.TestCase):
    def _rows(self, slot_fraction: float):
        rows = run_control_contention_experiment(ControlContentionExperimentConfig(seed=19, batch_count=500, batch_size=24, slot_fraction=slot_fraction))
        return {name: metrics for name, metrics, _cost in rows}

    def test_scarce_shared_resource_rewards_coordination(self):
        rows = self._rows(0.08)
        self.assertGreater(rows["hierarchical_batch"]["allocation_efficiency_vs_oracle_gain"], rows["distributed_threshold"]["allocation_efficiency_vs_oracle_gain"] + 0.10)
        self.assertGreater(rows["distributed_resource_auction"]["allocation_efficiency_vs_oracle_gain"], rows["distributed_threshold"]["allocation_efficiency_vs_oracle_gain"] + 0.10)

    def test_resource_specific_auction_matches_global_allocation_quality(self):
        rows = self._rows(0.20)
        self.assertGreater(rows["distributed_resource_auction"]["allocation_efficiency_vs_oracle_gain"], 0.98)
        self.assertGreater(rows["hierarchical_batch"]["allocation_efficiency_vs_oracle_gain"], 0.999)
        self.assertGreater(rows["distributed_resource_auction"]["messages_per_task"], rows["hierarchical_batch"]["messages_per_task"])


if __name__ == "__main__":
    unittest.main()
