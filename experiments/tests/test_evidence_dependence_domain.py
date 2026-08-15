import statistics
import unittest

from ai_atlas_lab.evidence_dependence_domain import I26AConfig, run_i26a


class EvidenceDependenceDomainTests(unittest.TestCase):
    def mean(
        self,
        policy: str,
        key: str,
        *,
        probe_cost: float = 0.06,
    ) -> float:
        return statistics.mean(
            run_i26a(
                I26AConfig(seed=seed, probe_cost=probe_cost),
                policy,
            ).get(key, 0.0)
            for seed in range(6)
        )

    def test_domain_scoped_dependence_beats_one_global_graph(self) -> None:
        self.assertGreater(
            self.mean("domain", "utility"),
            self.mean("global", "utility") + 0.05,
        )

    def test_domain_scoping_reduces_unnecessary_independent_audits(self) -> None:
        self.assertLess(
            self.mean("domain", "independent_audits"),
            self.mean("global", "independent_audits") * 0.80,
        )

    def test_global_graph_has_cross_domain_negative_transfer(self) -> None:
        self.assertLess(
            self.mean("global", "external_pair_accuracy"),
            0.90,
        )
        self.assertLess(
            self.mean("global", "metacognitive_pair_accuracy"),
            0.90,
        )

    def test_domain_model_recovers_both_hidden_relation_sets(self) -> None:
        self.assertGreater(
            self.mean("domain", "external_pair_accuracy"),
            0.95,
        )
        self.assertGreater(
            self.mean("domain", "metacognitive_pair_accuracy"),
            0.95,
        )

    def test_domain_probe_reduces_harm_and_is_sparse(self) -> None:
        self.assertLess(
            self.mean("domain_probe", "weighted_harm"),
            self.mean("domain", "weighted_harm") - 0.003,
        )
        self.assertLess(
            self.mean("domain_probe", "domain_probes"),
            0.10,
        )

    def test_domain_probe_nearly_reaches_oracle_relation_accuracy(self) -> None:
        self.assertGreater(
            self.mean("domain_probe", "external_pair_accuracy"),
            0.98,
        )
        self.assertGreater(
            self.mean("domain_probe", "metacognitive_pair_accuracy"),
            0.98,
        )

    def test_domain_probe_usage_falls_when_expensive(self) -> None:
        cheap = self.mean(
            "domain_probe",
            "domain_probes",
            probe_cost=0.01,
        )
        expensive = self.mean(
            "domain_probe",
            "domain_probes",
            probe_cost=0.80,
        )
        self.assertGreater(cheap, expensive + 0.02)


if __name__ == "__main__":
    unittest.main()
