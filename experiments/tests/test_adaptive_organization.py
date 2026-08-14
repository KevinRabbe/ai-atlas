import statistics
import unittest

from ai_atlas_lab.adaptive_organization import AF02Config, MODES, run_af02


class AdaptiveOrganizationTests(unittest.TestCase):
    def configs(self, duration: int = 70, switch_cost: float = 0.18):
        return [
            AF02Config(
                seed=seed,
                cycles=5,
                regime_duration=duration,
                switch_cost=switch_cost,
            )
            for seed in range(6)
        ]

    def mean(self, policy: str, key: str, duration: int = 70, switch_cost: float = 0.18) -> float:
        return statistics.mean(
            float(run_af02(config, policy)[key])
            for config in self.configs(duration, switch_cost)
        )

    def test_adaptive_selector_beats_every_fixed_mode_when_regimes_persist(self) -> None:
        adaptive = self.mean("adaptive", "net_utility_per_step")
        best_fixed = max(self.mean(mode, "net_utility_per_step") for mode in MODES)
        self.assertGreater(adaptive, best_fixed + 0.02)

    def test_oracle_remains_upper_bound(self) -> None:
        self.assertGreater(
            self.mean("oracle", "net_utility_per_step"),
            self.mean("adaptive", "net_utility_per_step") + 0.01,
        )

    def test_selector_learns_distinct_organizational_modes_from_observable_cues(self) -> None:
        target = {"local": "B", "coupled": "A", "shared": "C", "recurrent": "D"}
        fractions = {key: [] for key in target}
        for config in self.configs():
            result = run_af02(config, "adaptive")
            mapping = result["context_mode_fractions"]
            for context, mode in target.items():
                fractions[context].append(float(mapping[f"{context}_{mode}"]))
        for context in target:
            self.assertGreater(statistics.mean(fractions[context]), 0.72)

    def test_adaptive_selector_does_not_receive_perfect_mode_information(self) -> None:
        self.assertLess(self.mean("adaptive", "best_mode_fraction"), 0.98)
        self.assertGreater(self.mean("adaptive", "best_mode_fraction"), 0.70)

    def test_fast_regime_changes_can_make_fixed_organization_better(self) -> None:
        adaptive = self.mean("adaptive", "net_utility_per_step", duration=20)
        best_fixed = max(
            self.mean(mode, "net_utility_per_step", duration=20) for mode in MODES
        )
        self.assertLess(adaptive, best_fixed)

    def test_switching_cost_is_a_real_falsifier(self) -> None:
        low_cost = self.mean("adaptive", "net_utility_per_step", duration=80, switch_cost=0.05)
        high_cost = self.mean("adaptive", "net_utility_per_step", duration=80, switch_cost=1.0)
        self.assertGreater(low_cost, high_cost + 0.015)


if __name__ == "__main__":
    unittest.main()
