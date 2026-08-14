import unittest

from ai_atlas_lab.consolidation import (
    ConsolidationExperimentConfig,
    ConsecutiveStagingPolicy,
    ImmediateDurablePolicy,
    evaluate_consolidation_policy,
    run_consolidation_experiment,
)
from ai_atlas_lab.environments.regime_stream import generate_regime_stream


class ConsolidationTests(unittest.TestCase):
    def test_staging_reduces_noisy_durable_updates(self) -> None:
        stream = generate_regime_stream(
            seed=3, steps=6000, switch_probability=0.006, observation_reliability=0.80
        )
        immediate, _ = evaluate_consolidation_policy(ImmediateDurablePolicy(), stream)
        staged, _ = evaluate_consolidation_policy(ConsecutiveStagingPolicy(3), stream)
        self.assertLess(staged["durable_updates"], immediate["durable_updates"])

    def test_staging_introduces_real_change_delay(self) -> None:
        stream = generate_regime_stream(
            seed=11, steps=6000, switch_probability=0.01, observation_reliability=0.90
        )
        immediate, _ = evaluate_consolidation_policy(ImmediateDurablePolicy(), stream)
        staged, _ = evaluate_consolidation_policy(ConsecutiveStagingPolicy(3), stream)
        self.assertGreater(staged["avg_switch_delay"], immediate["avg_switch_delay"])

    def test_runner_contains_immediate_and_staged_variants(self) -> None:
        rows = run_consolidation_experiment(
            ConsolidationExperimentConfig(seed=1, steps=500, confirmations=(2, 4), evidence_thresholds=())
        )
        self.assertEqual(rows[0][0], "immediate_durable")
        self.assertEqual([row[0] for row in rows[1:]], ["staged_2", "staged_4"])


if __name__ == "__main__":
    unittest.main()
