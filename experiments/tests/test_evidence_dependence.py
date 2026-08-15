import random
import unittest

from ai_atlas_lab.evidence_dependence import EvidenceDependenceModel


class EvidenceDependenceModelTests(unittest.TestCase):
    def model(self, *, threshold: float = 0.02) -> EvidenceDependenceModel:
        model = EvidenceDependenceModel(
            decay=0.99,
            covariance_threshold=threshold,
            confidence_scale=0.03,
        )
        for source in ("a", "b", "c", "d"):
            model.register_source(source)
        return model

    def test_shared_failure_history_creates_dependence(self) -> None:
        rng = random.Random(3)
        model = self.model()
        for _ in range(1200):
            truth = rng.random() < 0.5
            shared = rng.random() < 0.16
            a = not truth if shared else truth
            b = not truth if shared else truth
            c = not truth if rng.random() < 0.16 else truth
            model.observe_resolution(
                {"a": a, "b": b, "c": c},
                truth,
            )
        self.assertTrue(model.estimate("a", "b", step=1200).same_failure_lineage)
        self.assertFalse(model.estimate("a", "c", step=1200).same_failure_lineage)

    def test_context_conditioning_reduces_difficulty_confound(self) -> None:
        rng = random.Random(7)
        raw = self.model(threshold=0.015)
        conditioned = self.model(threshold=0.015)
        for _ in range(1800):
            truth = rng.random() < 0.5
            hard = rng.random() < 0.30
            error = 0.38 if hard else 0.02
            labels = {
                source: (not truth if rng.random() < error else truth)
                for source in ("a", "b", "c", "d")
            }
            raw.observe_resolution(labels, truth, context_key="all")
            conditioned.observe_resolution(
                labels,
                truth,
                context_key="hard" if hard else "easy",
            )
        self.assertGreater(
            raw.dependence_score("a", "c"),
            conditioned.dependence_score("a", "c") + 0.01,
        )

    def test_probe_temporarily_overrides_observational_inference(self) -> None:
        model = self.model()
        model.remember_probe(
            "a",
            "b",
            same_failure_lineage=True,
            step=10,
            ttl=5,
        )
        current = model.estimate("a", "b", step=12)
        expired = model.estimate("a", "b", step=16)
        self.assertTrue(current.same_failure_lineage)
        self.assertTrue(current.explicitly_probed)
        self.assertFalse(expired.explicitly_probed)

    def test_components_collapse_only_inferred_dependent_sources(self) -> None:
        model = self.model()
        model.remember_probe(
            "a",
            "b",
            same_failure_lineage=True,
            step=0,
            ttl=100,
        )
        model.remember_probe(
            "a",
            "c",
            same_failure_lineage=False,
            step=0,
            ttl=100,
        )
        groups = model.components(("a", "b", "c"), step=1)
        self.assertEqual(groups["a"], groups["b"])
        self.assertNotEqual(groups["a"], groups["c"])

    def test_source_identity_and_dependence_are_separate(self) -> None:
        model = self.model()
        self.assertNotEqual("a", "b")
        self.assertFalse(model.estimate("a", "b", step=0).same_failure_lineage)
        model.remember_probe(
            "a",
            "b",
            same_failure_lineage=True,
            step=0,
            ttl=10,
        )
        self.assertTrue(model.estimate("a", "b", step=1).same_failure_lineage)

    def test_unknown_source_is_rejected(self) -> None:
        model = self.model()
        with self.assertRaises(KeyError):
            model.estimate("a", "missing", step=0)


if __name__ == "__main__":
    unittest.main()
