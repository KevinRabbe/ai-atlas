import random
import unittest

from ai_atlas_lab.evidence_aggregation import aggregate_binary_evidence
from ai_atlas_lab.evidence_dependence import EvidenceDependenceModel
from ai_atlas_lab.evidence_lineage import EvidenceLineageRegistry
from ai_atlas_lab.organism_runtime import TypedScopeRuntime


class EvidenceAggregationTests(unittest.TestCase):
    def setup_registry(self):
        runtime = TypedScopeRuntime((0, 1))
        return runtime, EvidenceLineageRegistry(runtime)

    def add(self, runtime, registry, source, *, lineage=None, value="yes"):
        if source not in registry.sources:
            registry.register_source(source, lineage_id=lineage)
        record = runtime.attach_evidence(0, source_ref=source)
        registry.annotate(
            record.evidence_id,
            source_id=source,
            claim_ref="claim:x",
            observed_step=0,
            resolves_claim=True,
            value_ref=value,
        )

    def estimate(self, registry, errors, *, model=None):
        return aggregate_binary_evidence(
            registry,
            "claim:x",
            current_step=1200,
            source_error_estimates=errors,
            positive_value_ref="yes",
            negative_value_ref="no",
            dependence_model=model,
        )

    def test_many_copies_from_one_lineage_do_not_create_false_precision(self) -> None:
        runtime, registry = self.setup_registry()
        for source in ("a", "b", "c", "d"):
            self.add(runtime, registry, source, lineage="shared")
        result = self.estimate(
            registry,
            {source: 0.10 for source in ("a", "b", "c", "d")},
        )
        self.assertTrue(result.label)
        self.assertEqual(result.used_groups, 1)
        self.assertAlmostEqual(result.estimated_error, 0.10, places=6)

    def test_two_independent_agreeing_lineages_can_reduce_error(self) -> None:
        runtime, registry = self.setup_registry()
        self.add(runtime, registry, "a", lineage="lineage-a")
        self.add(runtime, registry, "b", lineage="lineage-b")
        result = self.estimate(registry, {"a": 0.10, "b": 0.10})
        self.assertTrue(result.label)
        self.assertEqual(result.used_groups, 2)
        self.assertLess(result.estimated_error, 0.02)

    def test_unknown_source_names_do_not_create_precision_without_dependence_evidence(self) -> None:
        runtime, registry = self.setup_registry()
        self.add(runtime, registry, "a")
        self.add(runtime, registry, "b")
        result = self.estimate(registry, {"a": 0.10, "b": 0.10})
        self.assertEqual(result.used_groups, 1)
        self.assertEqual(result.unresolved_dependence_sources, 2)
        self.assertAlmostEqual(result.estimated_error, 0.10, places=6)

    def test_supported_learned_independence_can_reduce_unknown_source_error(self) -> None:
        runtime, registry = self.setup_registry()
        self.add(runtime, registry, "a")
        self.add(runtime, registry, "b")
        model = EvidenceDependenceModel(decay=0.99, covariance_threshold=0.02)
        model.register_source("a")
        model.register_source("b")
        rng = random.Random(3)
        for _ in range(1200):
            truth = rng.random() < 0.5
            model.observe_resolution(
                {
                    "a": not truth if rng.random() < 0.10 else truth,
                    "b": not truth if rng.random() < 0.10 else truth,
                },
                truth,
            )
        result = self.estimate(
            registry,
            {"a": 0.10, "b": 0.10},
            model=model,
        )
        self.assertEqual(result.used_groups, 2)
        self.assertEqual(result.unresolved_dependence_sources, 0)
        self.assertLess(result.estimated_error, 0.02)

    def test_untrained_model_does_not_reduce_unknown_source_error(self) -> None:
        runtime, registry = self.setup_registry()
        self.add(runtime, registry, "a")
        self.add(runtime, registry, "b")
        model = EvidenceDependenceModel()
        model.register_source("a")
        model.register_source("b")
        result = self.estimate(
            registry,
            {"a": 0.10, "b": 0.10},
            model=model,
        )
        self.assertEqual(result.used_groups, 1)
        self.assertAlmostEqual(result.estimated_error, 0.10, places=6)

    def test_equal_independent_conflict_remains_unresolved(self) -> None:
        runtime, registry = self.setup_registry()
        self.add(runtime, registry, "a", lineage="lineage-a", value="yes")
        self.add(runtime, registry, "b", lineage="lineage-b", value="no")
        result = self.estimate(registry, {"a": 0.10, "b": 0.10})
        self.assertIsNone(result.label)
        self.assertAlmostEqual(result.estimated_error, 0.5, places=6)

    def test_best_supported_source_represents_conflicting_shared_group(self) -> None:
        runtime, registry = self.setup_registry()
        self.add(runtime, registry, "a", lineage="shared", value="yes")
        self.add(runtime, registry, "b", lineage="shared", value="no")
        result = self.estimate(registry, {"a": 0.05, "b": 0.20})
        self.assertTrue(result.label)
        self.assertEqual(result.used_groups, 1)
        self.assertAlmostEqual(result.estimated_error, 0.05, places=6)


if __name__ == "__main__":
    unittest.main()
