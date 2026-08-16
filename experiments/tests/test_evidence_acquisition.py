import unittest

from ai_atlas_lab.evidence_acquisition import EvidenceAcquisitionRegistry
from ai_atlas_lab.organism_runtime import TypedScopeRuntime


class EvidenceAcquisitionRegistryTests(unittest.TestCase):
    def setup_registry(self):
        runtime = TypedScopeRuntime((0, 1))
        registry = EvidenceAcquisitionRegistry(runtime)
        evidence = runtime.attach_evidence(0, source_ref="source:x")
        return runtime, registry, evidence.evidence_id

    def test_targeted_acquisition_is_recorded_separately_from_evidence(self) -> None:
        runtime, registry, evidence_id = self.setup_registry()
        registry.record(
            evidence_id,
            acquisition_ref="audit:suspicious-only:v1",
            mode="targeted",
            selection_scope_ref="evaluator-output:flagged",
        )
        self.assertIn(evidence_id, runtime.evidence)
        self.assertEqual(registry.metadata[evidence_id].mode, "targeted")

    def test_unknown_evidence_cannot_receive_invalid_probability(self) -> None:
        _, registry, _ = self.setup_registry()
        with self.assertRaises(KeyError):
            registry.record(
                999,
                acquisition_ref="audit:x",
                mode="randomized",
                inclusion_probability=0.1,
            )

    def test_inclusion_probability_must_be_valid(self) -> None:
        _, registry, evidence_id = self.setup_registry()
        with self.assertRaises(ValueError):
            registry.record(
                evidence_id,
                acquisition_ref="audit:x",
                mode="randomized",
                inclusion_probability=0.0,
            )

    def test_known_randomized_probability_exposes_inverse_weight_without_making_truth(self) -> None:
        _, registry, evidence_id = self.setup_registry()
        registry.record(
            evidence_id,
            acquisition_ref="coverage:v1",
            mode="randomized",
            inclusion_probability=0.04,
        )
        self.assertAlmostEqual(
            registry.inverse_inclusion_weight(evidence_id),
            25.0,
        )

    def test_targeted_unknown_probability_is_flagged_as_unmodeled_selection(self) -> None:
        runtime = TypedScopeRuntime((0, 1))
        registry = EvidenceAcquisitionRegistry(runtime)
        ids = []
        for source in ("a", "b"):
            evidence = runtime.attach_evidence(0, source_ref=source)
            ids.append(evidence.evidence_id)
        registry.record(
            ids[0],
            acquisition_ref="targeted:v1",
            mode="targeted",
        )
        registry.record(
            ids[1],
            acquisition_ref="coverage:v1",
            mode="randomized",
            inclusion_probability=0.05,
        )
        summary = registry.summarize(tuple(ids))
        self.assertEqual(summary.unmodeled_selection_records, 1)
        self.assertEqual(summary.randomized_records, 1)

    def test_selection_metadata_does_not_create_lineage_or_authority(self) -> None:
        runtime, registry, evidence_id = self.setup_registry()
        before_authority = runtime.read_authority(0)
        registry.record(
            evidence_id,
            acquisition_ref="audit:v1",
            mode="interventional",
            inclusion_probability=0.2,
        )
        after_authority = runtime.read_authority(0)
        self.assertEqual(before_authority, after_authority)
        self.assertEqual(runtime.evidence[evidence_id].source_ref, "source:x")


if __name__ == "__main__":
    unittest.main()
