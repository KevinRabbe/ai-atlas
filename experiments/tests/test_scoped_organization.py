import statistics
import unittest

from ai_atlas_lab.scoped_organization import AF03Config, run_af03


class ScopedOrganizationTests(unittest.TestCase):
    def mean(self, heterogeneous: bool, cross: float, policy: str, key: str) -> float:
        return statistics.mean(
            float(
                run_af03(
                    AF03Config(
                        seed=seed,
                        cycles=4,
                        regime_duration=60,
                        heterogeneous_domains=heterogeneous,
                        cross_domain_coupling=cross,
                    ),
                    policy,
                )[key]
            )
            for seed in range(6)
        )

    def test_scoped_organization_wins_when_domains_differ_and_coupling_is_low(self) -> None:
        scoped = self.mean(True, 0.12, "scoped_adaptive", "net_utility_per_domain_step")
        global_mode = self.mean(True, 0.12, "global_adaptive", "net_utility_per_domain_step")
        self.assertGreater(scoped, global_mode + 0.03)

    def test_global_organization_wins_when_domains_are_homogeneous_and_tightly_coupled(self) -> None:
        global_mode = self.mean(False, 0.80, "global_adaptive", "net_utility_per_domain_step")
        scoped = self.mean(False, 0.80, "scoped_adaptive", "net_utility_per_domain_step")
        self.assertGreater(global_mode, scoped + 0.01)

    def test_cross_domain_coupling_erodes_scoped_advantage(self) -> None:
        low = self.mean(True, 0.0, "scoped_adaptive", "net_utility_per_domain_step")
        high = self.mean(True, 1.0, "scoped_adaptive", "net_utility_per_domain_step")
        self.assertGreater(low, high + 0.04)

    def test_maximal_coupling_can_remove_scoped_advantage(self) -> None:
        scoped = self.mean(True, 1.0, "scoped_adaptive", "net_utility_per_domain_step")
        global_mode = self.mean(True, 1.0, "global_adaptive", "net_utility_per_domain_step")
        self.assertLess(scoped, global_mode + 0.005)

    def test_oracle_bounds_remain_above_learned_policies(self) -> None:
        self.assertGreater(
            self.mean(True, 0.12, "oracle_scoped", "net_utility_per_domain_step"),
            self.mean(True, 0.12, "scoped_adaptive", "net_utility_per_domain_step") + 0.01,
        )
        self.assertGreater(
            self.mean(False, 0.80, "oracle_global", "net_utility_per_domain_step"),
            self.mean(False, 0.80, "global_adaptive", "net_utility_per_domain_step") + 0.01,
        )


if __name__ == "__main__":
    unittest.main()
