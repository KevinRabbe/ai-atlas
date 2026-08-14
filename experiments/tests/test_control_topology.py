import unittest

from ai_atlas_lab.control_topology import ControlTopologyExperimentConfig, run_control_topology_experiment


class ControlTopologyTests(unittest.TestCase):
    def _rows(self, density: float):
        rows = run_control_topology_experiment(ControlTopologyExperimentConfig(seed=11, task_count=900, dependency_density=density, distributed_rounds=(1, 3)))
        return {name: metrics for name, metrics, _cost in rows}

    def test_sparse_distributed_uses_less_communication(self):
        rows = self._rows(0.04)
        self.assertLess(rows["distributed_r1"]["messages_per_task"], rows["hierarchical_global"]["messages_per_task"])
        self.assertLess(abs(rows["distributed_r3"]["success_rate"] - rows["hierarchical_global"]["success_rate"]), 0.01)

    def test_dense_dependencies_expose_bounded_coordination(self):
        rows = self._rows(0.72)
        self.assertGreater(rows["hierarchical_global"]["success_rate"], rows["distributed_r1"]["success_rate"] + 0.03)
        self.assertGreater(rows["distributed_r3"]["success_rate"], rows["distributed_r1"]["success_rate"] + 0.03)
        self.assertGreater(rows["distributed_r3"]["messages_per_task"], rows["distributed_r1"]["messages_per_task"])


if __name__ == "__main__":
    unittest.main()
