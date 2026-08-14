import unittest

from ai_atlas_lab.core import CostMeter
from ai_atlas_lab.environments.temporal_state import Event, Query, TemporalStateDataset
from ai_atlas_lab.memory import CompressedState, DirectAddressState, HybridState, evaluate_state_policy


class MemoryPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        events = (
            Event(0, 0, "a", 10, "p0"),
            Event(1, 1, "b", 20, "p1"),
            Event(2, 2, "a", 30, "p2"),
        )
        queries = (
            Query("current", entity="a", expected=30),
            Query("historical", entity="a", time=0, expected=10),
            Query("exact", event_id=1, expected="p1"),
        )
        self.dataset = TemporalStateDataset(events, queries)

    def test_direct_address_preserves_all_query_types(self) -> None:
        metrics, _ = evaluate_state_policy(DirectAddressState(), self.dataset)
        self.assertEqual(metrics["overall_accuracy"], 1.0)

    def test_compressed_state_trades_history_for_current_access(self) -> None:
        metrics, _ = evaluate_state_policy(CompressedState(), self.dataset)
        self.assertEqual(metrics["current_accuracy"], 1.0)
        self.assertEqual(metrics["historical_accuracy"], 0.0)
        self.assertEqual(metrics["exact_accuracy"], 0.0)

    def test_hybrid_preserves_all_query_types(self) -> None:
        metrics, _ = evaluate_state_policy(HybridState(), self.dataset)
        self.assertEqual(metrics["overall_accuracy"], 1.0)

    def test_direct_address_read_cost_exceeds_hybrid_for_current_lookup(self) -> None:
        direct = DirectAddressState()
        hybrid = HybridState()
        write_cost = CostMeter()
        for event in self.dataset.events:
            direct.write(event, write_cost)
            hybrid.write(event, write_cost)
        query = Query("current", entity="b", expected=20)
        direct_cost = CostMeter()
        hybrid_cost = CostMeter()
        self.assertEqual(direct.answer(query, direct_cost), 20)
        self.assertEqual(hybrid.answer(query, hybrid_cost), 20)
        self.assertGreater(direct_cost.reads, hybrid_cost.reads)


if __name__ == "__main__":
    unittest.main()
