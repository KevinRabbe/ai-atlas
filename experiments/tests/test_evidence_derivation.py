import random
import unittest

from ai_atlas_lab.evidence_derivation import EvidenceDerivationModel


class EvidenceDerivationModelTests(unittest.TestCase):
    def model(self) -> EvidenceDerivationModel:
        model = EvidenceDerivationModel(decay=0.99)
        for source in ("a", "b", "c", "d"):
            model.register_source(source)
        return model

    def train_parent_children(self, model: EvidenceDerivationModel, seed: int = 3) -> None:
        rng = random.Random(seed)
        for _ in range(1800):
            truth = rng.random() < 0.5
            parent = not truth if rng.random() < 0.25 else truth
            labels = {"a": parent}
            for child in ("b", "c"):
                if rng.random() < 0.40:
                    labels[child] = not truth if rng.random() < 0.03 else truth
                else:
                    labels[child] = parent
            labels["d"] = not truth if rng.random() < 0.18 else truth
            model.observe_resolution(labels, truth)

    def test_parent_to_child_direction_is_inferred(self) -> None:
        model = self.model()
        self.train_parent_children(model)
        self.assertEqual(model.inferred_parent("b"), "a")
        self.assertEqual(model.inferred_parent("c"), "a")

    def test_direction_is_not_forced_symmetric(self) -> None:
        model = self.model()
        self.train_parent_children(model)
        self.assertTrue(model.estimate("a", "b").inherits_failures)
        self.assertFalse(model.estimate("b", "a").inherits_failures)

    def test_independent_source_is_not_inferred_as_parent(self) -> None:
        model = self.model()
        self.train_parent_children(model)
        self.assertFalse(model.estimate("d", "b").inherits_failures)
        self.assertNotEqual(model.inferred_parent("b"), "d")

    def test_children_of_returns_directional_descendants(self) -> None:
        model = self.model()
        self.train_parent_children(model)
        self.assertEqual(model.children_of("a"), ("b", "c"))

    def test_direction_can_be_context_specific(self) -> None:
        rng = random.Random(9)
        model = self.model()
        for _ in range(1800):
            truth = rng.random() < 0.5
            a = not truth if rng.random() < 0.25 else truth
            b = a if rng.random() > 0.40 else (not truth if rng.random() < 0.03 else truth)
            model.observe_resolution(
                {"a": a, "b": b},
                truth,
                context_key="derived",
            )
            model.observe_resolution(
                {
                    "a": not truth if rng.random() < 0.18 else truth,
                    "b": not truth if rng.random() < 0.18 else truth,
                },
                truth,
                context_key="independent",
            )
        self.assertTrue(
            model.estimate("a", "b", context_key="derived").inherits_failures
        )
        self.assertFalse(
            model.estimate("a", "b", context_key="independent").inherits_failures
        )

    def test_source_identity_does_not_imply_direction(self) -> None:
        model = self.model()
        self.assertIsNone(model.inferred_parent("b"))


if __name__ == "__main__":
    unittest.main()
