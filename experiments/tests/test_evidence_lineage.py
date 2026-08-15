import random
import unittest

from ai_atlas_lab.evidence_dependence import EvidenceDependenceModel
from ai_atlas_lab.evidence_lineage import EvidenceLineageRegistry
from ai_atlas_lab.organism_runtime import TypedScopeRuntime


class EvidenceLineageRegistryTests(unittest.TestCase):
    def setup_registry(self):
        runtime = TypedScopeRuntime((0, 1))
        registry = EvidenceLineageRegistry(runtime)
        return runtime, registry

    def attach(self, runtime, registry, *, source, lineage=None, claim="claim:x", value="yes", step=0, resolves=True, validity=None):
        if source not in registry.sources:
            registry.register_source(source, lineage_id=lineage, validity_steps=validity)
        record = runtime.attach_evidence(0, source_ref=source)
        registry.annotate(
            record.evidence_id,
            source_id=source,
            claim_ref=claim,
            observed_step=step,
            resolves_claim=resolves,
            value_ref=value,
        )
        return record

    def dependence_model(self, *sources):
        model = EvidenceDependenceModel(decay=0.99, covariance_threshold=0.02)
        for source in sources:
            model.register_source(source)
        return model

    def test_copied_records_from_one_lineage_count_once(self) -> None:
        runtime, registry = self.setup_registry()
        for source in ("mirror-a", "mirror-b", "mirror-c"):
            self.attach(runtime, registry, source=source, lineage="lineage-a")
        summary = registry.summarize("claim:x", current_step=1)
        self.assertEqual(summary.record_count, 3)
        self.assertEqual(summary.independent_lineages, 1)
        self.assertEqual(summary.resolving_lineages, 1)

    def test_independent_source_adds_a_second_lineage(self) -> None:
        runtime, registry = self.setup_registry()
        self.attach(runtime, registry, source="receipt", lineage="lineage-a")
        self.attach(runtime, registry, source="reconcile", lineage="lineage-b")
        summary = registry.summarize("claim:x", current_step=1)
        self.assertEqual(summary.independent_lineages, 2)
        self.assertEqual(summary.resolving_lineages, 2)

    def test_stale_record_does_not_count_as_current_lineage(self) -> None:
        runtime, registry = self.setup_registry()
        self.attach(
            runtime,
            registry,
            source="receipt",
            lineage="lineage-a",
            step=2,
            validity=5,
        )
        summary = registry.summarize("claim:x", current_step=9)
        self.assertEqual(summary.stale_records, 1)
        self.assertEqual(summary.independent_lineages, 0)

    def test_nonresolving_observation_does_not_become_resolution_evidence(self) -> None:
        runtime, registry = self.setup_registry()
        self.attach(
            runtime,
            registry,
            source="timeout",
            lineage="lineage-a",
            resolves=False,
            value=None,
        )
        summary = registry.summarize("claim:x", current_step=1)
        self.assertEqual(summary.independent_lineages, 1)
        self.assertEqual(summary.resolving_lineages, 0)
        self.assertEqual(summary.unresolved_records, 1)

    def test_independent_resolving_lineages_can_expose_conflict(self) -> None:
        runtime, registry = self.setup_registry()
        self.attach(runtime, registry, source="receipt", lineage="lineage-a", value="applied")
        self.attach(runtime, registry, source="sensor", lineage="lineage-b", value="absent")
        summary = registry.summarize("claim:x", current_step=1)
        self.assertTrue(summary.conflict)

    def test_many_agreeing_copies_do_not_hide_independent_conflict(self) -> None:
        runtime, registry = self.setup_registry()
        for source in ("copy-1", "copy-2", "copy-3"):
            self.attach(runtime, registry, source=source, lineage="lineage-a", value="applied")
        self.attach(runtime, registry, source="independent", lineage="lineage-b", value="absent")
        summary = registry.summarize("claim:x", current_step=1)
        self.assertEqual(summary.independent_lineages, 2)
        self.assertTrue(summary.conflict)

    def test_unknown_sources_are_not_independent_by_name_alone(self) -> None:
        runtime, registry = self.setup_registry()
        self.attach(runtime, registry, source="unknown-a")
        self.attach(runtime, registry, source="unknown-b")
        summary = registry.summarize("claim:x", current_step=1)
        self.assertEqual(summary.independent_lineages, 1)
        self.assertEqual(summary.unknown_dependence_sources, 2)
        self.assertEqual(summary.unresolved_dependence_sources, 2)

    def test_untrained_learned_model_does_not_manufacture_independence(self) -> None:
        runtime, registry = self.setup_registry()
        self.attach(runtime, registry, source="unknown-a")
        self.attach(runtime, registry, source="unknown-b")
        model = self.dependence_model("unknown-a", "unknown-b")
        summary = registry.summarize_effective(
            "claim:x",
            current_step=1,
            dependence_model=model,
        )
        self.assertEqual(summary.independent_lineages, 1)
        self.assertEqual(summary.unresolved_dependence_sources, 2)

    def test_learned_independence_can_separate_unknown_sources_after_support(self) -> None:
        runtime, registry = self.setup_registry()
        self.attach(runtime, registry, source="unknown-a")
        self.attach(runtime, registry, source="unknown-b")
        model = self.dependence_model("unknown-a", "unknown-b")
        rng = random.Random(3)
        for _ in range(1200):
            truth = rng.random() < 0.5
            model.observe_resolution(
                {
                    "unknown-a": not truth if rng.random() < 0.12 else truth,
                    "unknown-b": not truth if rng.random() < 0.12 else truth,
                },
                truth,
            )
        summary = registry.summarize_effective(
            "claim:x",
            current_step=1200,
            dependence_model=model,
        )
        self.assertEqual(summary.independent_lineages, 2)
        self.assertEqual(summary.unresolved_dependence_sources, 0)

    def test_learned_dependence_collapses_unknown_sources(self) -> None:
        runtime, registry = self.setup_registry()
        self.attach(runtime, registry, source="unknown-a")
        self.attach(runtime, registry, source="unknown-b")
        model = self.dependence_model("unknown-a", "unknown-b")
        rng = random.Random(4)
        for _ in range(1200):
            truth = rng.random() < 0.5
            shared = rng.random() < 0.18
            value = not truth if shared else truth
            model.observe_resolution(
                {"unknown-a": value, "unknown-b": value},
                truth,
            )
        summary = registry.summarize_effective(
            "claim:x",
            current_step=1200,
            dependence_model=model,
        )
        self.assertEqual(summary.independent_lineages, 1)
        self.assertEqual(summary.unresolved_dependence_sources, 0)

    def test_exact_shared_lineage_cannot_be_split_by_learned_model(self) -> None:
        runtime, registry = self.setup_registry()
        self.attach(runtime, registry, source="copy-a", lineage="exact-shared")
        self.attach(runtime, registry, source="copy-b", lineage="exact-shared")
        model = self.dependence_model("copy-a", "copy-b")
        rng = random.Random(5)
        for _ in range(1200):
            truth = rng.random() < 0.5
            model.observe_resolution(
                {
                    "copy-a": not truth if rng.random() < 0.10 else truth,
                    "copy-b": not truth if rng.random() < 0.10 else truth,
                },
                truth,
            )
        summary = registry.summarize_effective(
            "claim:x",
            current_step=1200,
            dependence_model=model,
        )
        self.assertEqual(summary.independent_lineages, 1)


if __name__ == "__main__":
    unittest.main()
