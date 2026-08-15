import unittest

from ai_atlas_lab.evidence_lineage import EvidenceLineageRegistry
from ai_atlas_lab.organism_recovery import OrganismRecoveryCoordinator
from ai_atlas_lab.organism_runtime import TypedScopeRuntime


class OrganismRecoveryEvidenceTests(unittest.TestCase):
    def setup(self):
        runtime = TypedScopeRuntime((0, 1))
        registry = EvidenceLineageRegistry(runtime)
        coordinator = OrganismRecoveryCoordinator(runtime, registry)
        return runtime, registry, coordinator

    def attach(self, runtime, registry, *, source, lineage, value, step=0, validity=None, resolves=True):
        if source not in registry.sources:
            registry.register_source(source, lineage_id=lineage, validity_steps=validity)
        record = runtime.attach_evidence(0, source_ref=source)
        registry.annotate(
            record.evidence_id,
            source_id=source,
            claim_ref="effect:x",
            observed_step=step,
            resolves_claim=resolves,
            value_ref=value,
        )

    def plan(self, coordinator, *, current_step=1, current_label=True, current_error=0.08, independent_cost=0.10):
        return coordinator.plan_external_execution_evidence(
            "effect:x",
            current_step=current_step,
            current_label=current_label,
            estimated_current_error=current_error,
            estimated_independent_error=0.03,
            consequence=4.0,
            duplicate_penalty=4.0,
            missed_penalty=1.5,
            independent_cost=independent_cost,
            unresolved_penalty=0.7,
        )

    def test_three_copies_from_one_good_lineage_can_still_use_current_when_check_is_expensive(self) -> None:
        runtime, registry, coordinator = self.setup()
        for source in ("copy-a", "copy-b", "copy-c"):
            self.attach(runtime, registry, source=source, lineage="lineage-a", value="applied")
        decision = self.plan(
            coordinator,
            current_error=0.01,
            independent_cost=2.0,
        )
        self.assertEqual(decision.action, "use_current")

    def test_stale_lineage_triggers_independent_reconciliation_when_worth_it(self) -> None:
        runtime, registry, coordinator = self.setup()
        self.attach(
            runtime,
            registry,
            source="receipt",
            lineage="lineage-a",
            value="applied",
            step=0,
            validity=2,
        )
        decision = self.plan(coordinator, current_step=10)
        self.assertEqual(decision.action, "acquire_independent")

    def test_independent_conflict_triggers_another_lineage_when_cheap(self) -> None:
        runtime, registry, coordinator = self.setup()
        self.attach(runtime, registry, source="receipt", lineage="a", value="applied")
        self.attach(runtime, registry, source="reconcile", lineage="b", value="absent")
        decision = self.plan(coordinator, independent_cost=0.05)
        self.assertEqual(decision.action, "acquire_independent")

    def test_independent_conflict_can_remain_unresolved_when_resolution_is_too_expensive(self) -> None:
        runtime, registry, coordinator = self.setup()
        self.attach(runtime, registry, source="receipt", lineage="a", value="applied")
        self.attach(runtime, registry, source="reconcile", lineage="b", value="absent")
        decision = self.plan(coordinator, independent_cost=20.0)
        self.assertEqual(decision.action, "unresolved")

    def test_nonresolving_record_is_not_treated_as_execution_confirmation(self) -> None:
        runtime, registry, coordinator = self.setup()
        self.attach(
            runtime,
            registry,
            source="timeout",
            lineage="a",
            value="unknown",
            resolves=False,
        )
        decision = self.plan(coordinator, current_label=None)
        self.assertEqual(decision.action, "acquire_independent")

    def test_coordinator_requires_explicit_lineage_registry_for_evidence_planning(self) -> None:
        runtime = TypedScopeRuntime((0, 1))
        coordinator = OrganismRecoveryCoordinator(runtime)
        with self.assertRaises(RuntimeError):
            coordinator.plan_external_execution_evidence(
                "effect:x",
                current_step=0,
                current_label=True,
                estimated_current_error=0.1,
                estimated_independent_error=0.03,
                consequence=4.0,
                duplicate_penalty=4.0,
                missed_penalty=1.0,
                independent_cost=0.1,
                unresolved_penalty=0.7,
            )


if __name__ == "__main__":
    unittest.main()
