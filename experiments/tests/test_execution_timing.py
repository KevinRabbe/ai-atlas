import unittest

from ai_atlas_lab.execution_timing import (
    ExecutionTimingConfig,
    run_sparse_event_graph,
    run_version_coupled_workload,
)


def mean_metric(fn, variant, metric, seeds=12, **config_updates):
    values = [
        fn(
            ExecutionTimingConfig(seed=seed, **config_updates),
            variant,
        )[metric]
        for seed in range(seeds)
    ]
    return sum(values) / len(values)


class ExecutionTimingTests(unittest.TestCase):
    def test_scoped_events_beat_global_ticks_on_sparse_graph(self):
        scoped = mean_metric(run_sparse_event_graph, "scoped_event", "net_utility_per_step")
        sync = mean_metric(run_sparse_event_graph, "sync_global", "net_utility_per_step")
        self.assertGreater(scoped, sync + 0.10)

    def test_scoped_events_use_far_less_sparse_work(self):
        scoped = mean_metric(run_sparse_event_graph, "scoped_event", "operations_per_step")
        sync = mean_metric(run_sparse_event_graph, "sync_global", "operations_per_step")
        self.assertLess(scoped, sync * 0.15)

    def test_naive_async_accumulates_stale_dependencies(self):
        stale = mean_metric(run_sparse_event_graph, "async_naive", "stale_read_rate")
        scoped = mean_metric(run_sparse_event_graph, "scoped_event", "stale_read_rate")
        self.assertGreater(stale, 0.20)
        self.assertEqual(scoped, 0.0)

    def test_version_barrier_prevents_mixed_snapshots(self):
        naive = mean_metric(run_version_coupled_workload, "async_naive", "inconsistent_query_rate")
        scoped = mean_metric(run_version_coupled_workload, "scoped_event", "inconsistent_query_rate")
        self.assertGreater(naive, 0.95)
        self.assertEqual(scoped, 0.0)

    def test_scoped_barrier_can_coalesce_coupled_updates(self):
        scoped = mean_metric(run_version_coupled_workload, "scoped_event", "net_utility_per_step")
        sync = mean_metric(run_version_coupled_workload, "sync_global", "net_utility_per_step")
        self.assertGreater(scoped, sync)

    def test_eager_sync_can_win_when_consistent_snapshots_are_continuous(self):
        scoped = mean_metric(
            run_version_coupled_workload,
            "scoped_event",
            "net_utility_per_step",
            coupled_query_probability=0.90,
        )
        sync = mean_metric(
            run_version_coupled_workload,
            "sync_global",
            "net_utility_per_step",
            coupled_query_probability=0.90,
        )
        self.assertGreater(sync, scoped + 0.015)


if __name__ == "__main__":
    unittest.main()
