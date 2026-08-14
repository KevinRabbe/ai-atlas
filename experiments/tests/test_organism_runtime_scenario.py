import statistics
import unittest

from ai_atlas_lab.organism_runtime_scenario import I10ScenarioConfig, run_i10_scenario


class OrganismRuntimeScenarioTests(unittest.TestCase):
    def results(self):
        return [
            run_i10_scenario(I10ScenarioConfig(seed=seed))
            for seed in range(6)
        ]

    def test_scenario_preserves_all_semantic_invariants(self) -> None:
        for result in self.results():
            self.assertTrue(result["all_semantic_invariants"])
            self.assertTrue(result["resource_leases_singular"])

    def test_scenario_performs_and_rejects_real_topology_changes(self) -> None:
        results = self.results()
        self.assertGreater(
            statistics.mean(float(item["topology_epochs"]) for item in results),
            3.0,
        )
        self.assertGreater(
            statistics.mean(float(item["rejected_changes"]) for item in results),
            0.5,
        )

    def test_in_flight_work_is_forwarded_across_topology_epochs(self) -> None:
        self.assertGreater(
            statistics.mean(
                float(item["forwarded_events"])
                for item in self.results()
            ),
            2.0,
        )

    def test_current_revocation_blocks_queued_external_work(self) -> None:
        self.assertGreater(
            statistics.mean(
                float(item["blocked_external_events"])
                for item in self.results()
            ),
            2.0,
        )

    def test_all_queued_events_are_eventually_processed_once(self) -> None:
        for result in self.results():
            self.assertEqual(
                result["queued_events"],
                result["processed_events"],
            )


if __name__ == "__main__":
    unittest.main()
