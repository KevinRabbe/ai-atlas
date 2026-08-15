import random
import unittest

from ai_atlas_lab.evidence_dependence import EvidenceDependenceModel
from ai_atlas_lab.evidence_lineage import EvidenceLineageRegistry
from ai_atlas_lab.organism_recovery import OrganismRecoveryCoordinator
from ai_atlas_lab.organism_runtime import TypedScopeRuntime


class OrganismRecoveryLearnedDependenceTests(unittest.TestCase):
    def setup(self):
        runtime = TypedScopeRuntime((0, 1))
        registry = EvidenceLineageRegistry(runtime)
        model = EvidenceDependenceModel(decay=0.99, covariance_threshold=0.02)
        recovery = OrganismRecoveryCoordinator(
            runtime,
            evidence_registry=registry,
            evidence_dependence_model=model,
        )
        return runtime, registry, model, recovery

    def add(self, runtime, registry, source, *, value="absent", lineage=None):
        if source not in registry.sources:
            registry.register_source(source, lineage_id=lineage)
        record = runtime.attach_evidence(0, source_ref=source)
        registry.annotate(
            record.evidence_id,
            source_id=source,
            claim_ref="effect:x",
            observed_step=0,
            resolves_claim=True,
            value_ref=value,
        )

    def plan(self, recovery, errors):
        return recovery.plan_external_execution_evidence_from_sources(
            "effect:x",
            current_step=1200,
            source_error_estimates=errors,
            estimated_independent_error=0.03,
            consequence=4.0,
            duplicate_penalty=4.0,
            missed_penalty=1.0,
            independent_cost=0.05,
            unresolved_penalty=0.8,
        )

    def train_independent(self, model, seed=3):
        rng = random.Random(seed)
        for _ in range(1200):
            truth = rng.random() < 0.5
            model.observe_resolution(
                {
                    "a": not truth if rng.random() < 0.10 else truth,
                    "b": not truth if rng.random() < 0.10 else truth,
                },
                truth,
            )

    def train_dependent(self, model, seed=4):
        rng = random.Random(seed)
        for _ in range(1200):
            truth = rng.random() < 0.5
            shared = rng.random() < 0.16
            value = not truth if shared else truth
            model.observe_resolution({"a": value, "b": value}, truth)

    def test_unknown_source_names_do_not_avoid_needed_independent_check(self) -> None:
        runtime, registry, model, recovery = self.setup()
        for source in ("a", "b"):
            model.register_source(source)
            self.add(runtime, registry, source)
        result = self.plan(recovery, {"a": 0.10, "b": 0.10})
        self.assertEqual(result.estimate.used_groups, 1)
        self.assertAlmostEqual(result.estimate.estimated_error, 0.10, places=6)
        self.assertEqual(result.assurance.action, "acquire_independent")

    def test_supported_learned_independence_can_avoid_unnecessary_check(self) -> None:
        runtime, registry, model, recovery = self.setup()
        for source in ("a", "b"):
            model.register_source(source)
            self.add(runtime, registry, source)
        self.train_independent(model)
        result = self.plan(recovery, {"a": 0.10, "b": 0.10})
        self.assertEqual(result.estimate.used_groups, 2)
        self.assertLess(result.estimate.estimated_error, 0.02)
        self.assertEqual(result.assurance.action, "use_current")

    def test_learned_dependence_keeps_agreeing_unknown_sources_one_group(self) -> None:
        runtime, registry, model, recovery = self.setup()
        for source in ("a", "b"):
            model.register_source(source)
            self.add(runtime, registry, source)
        self.train_dependent(model)
        result = self.plan(recovery, {"a": 0.10, "b": 0.10})
        self.assertEqual(result.estimate.used_groups, 1)
        self.assertGreater(result.estimate.estimated_error, 0.08)
        self.assertEqual(result.assurance.action, "acquire_independent")

    def test_exact_shared_lineage_overrides_learned_independence(self) -> None:
        runtime, registry, model, recovery = self.setup()
        for source in ("a", "b"):
            model.register_source(source)
            self.add(runtime, registry, source, lineage="known-copy")
        self.train_independent(model)
        result = self.plan(recovery, {"a": 0.10, "b": 0.10})
        self.assertEqual(result.estimate.used_groups, 1)
        self.assertEqual(result.assurance.action, "acquire_independent")

    def test_independent_conflict_remains_unresolved_or_requires_new_evidence(self) -> None:
        runtime, registry, model, recovery = self.setup()
        for source, value in (("a", "applied"), ("b", "absent")):
            model.register_source(source)
            self.add(runtime, registry, source, value=value)
        self.train_independent(model)
        result = self.plan(recovery, {"a": 0.10, "b": 0.10})
        self.assertIsNone(result.estimate.label)
        self.assertEqual(result.assurance.action, "acquire_independent")

    def test_copied_record_count_cannot_enter_through_aggregator(self) -> None:
        runtime, registry, model, recovery = self.setup()
        errors = {}
        for index in range(8):
            source = f"copy-{index}"
            self.add(runtime, registry, source, lineage="same-lineage")
            errors[source] = 0.10
        result = self.plan(recovery, errors)
        self.assertEqual(result.estimate.used_groups, 1)
        self.assertAlmostEqual(result.estimate.estimated_error, 0.10, places=6)


if __name__ == "__main__":
    unittest.main()
