# Research Roadmap

## Phases 0–7

Taxonomy/evidence discipline, computational substrate, learning/adaptation, inference-time intelligence, persistent intelligence, verification/control, self-improvement and first cross-domain synthesis completed first passes on 2026-08-14. Targeted gap closure remains open.

Discovery/epistemic growth is explicit: human knowledge is bootstrap evidence/methodology rather than a permanent epistemic ceiling; F26 requires turning uncertainty into testable hypotheses and independently supported new knowledge.

## Phase 8 — Forget implementations

First-pass clean-sheet functional reconstruction completed on 2026-08-14. **Exit gate: PASS.**

## Phase 9 — Clean-sheet architecture

First-pass candidate generation completed on 2026-08-14. **Exit gate: PASS.** A/B/C/D remain useful reference organizations, but current Phase-10 evidence treats their mechanisms as conditional modes/scopes rather than mutually exclusive final systems.

## Phase 10 — Experimental reconstruction

**Active. Twenty-five reversible implementation-neutral principles survive their current promotion gates.** The validation history now contains **377 added test cases**.

The experimental strategy has progressed through:

1. isolated mechanism discrimination;
2. integrated epistemic/resource composition;
3. guarded self-improvement;
4. learned metacognition under imperfect feedback;
5. interaction-aware runtime allocation;
6. architecture-family Pareto comparison;
7. adaptive organizational modes/scopes/topology;
8. typed-state migration and structural assurance;
9. persistent reusable typed-scope runtime;
10. overlapping coordination and directional dependencies;
11. failure-isolated topology/resource publication;
12. crash/restart recovery from semantic publication identity;
13. external-effect recovery and current-authority separation;
14. correlated/stale external evidence and partially-unresolved metacognitive audits;
15. publication provenance inside authoritative state;
16. common crash-aware organism recovery;
17. shared typed evidence-lineage + assurance allocation;
18. transient cache/credit recovery across structural change.

## Current architecture spine

```text
stable typed semantic identities
  subjects / source evidence / publication provenance
  authority versions / resource leases
        |
        +--> directional dependencies
        +--> dynamic ownership topology
        +--> overlapping non-owning coordination scopes
        ↓
typed transition proposals
        ↓
interaction-aware value/resource allocation
        ↓
evidence-lineage structure
  lineage / stale? / resolves? / conflict
        + learned source-quality estimates
        ↓
consequence-sensitive assurance allocation
        ↓
PREPARE non-authoritative candidate state
        ↓
version / publication-provenance / current-authority fence
        ↓
PUBLISH coherent internal authoritative state
        |
        +--> external effect path
        |       effect-specific external evidence
        |       current authority for every fresh/retry attempt
        |       unresolved execution when exact status cannot be known
        ↓
crash recovery from semantic identity/provenance
        ↓
selective transient-state persistence / rematerialization / replay
        ↓
observe → versioned causal credit → staged appropriately-scoped update
```

The value allocator cannot manufacture epistemic, capability, publication, causal or external-execution authority.

## I06–I13 — architecture-scale composition

I06 shows runtime operations interact enough that joint allocation (~`1.564` utility/task) beats factorized control (~`1.355`). AF01–AF03 and I07 show organizational mode/scope/membership can all be adaptive when persistence pays for switching/migration. I08–I10 make stable semantic state movable through live topology. I11/I12 split ownership, overlapping coordination and directional dependency into distinct relations.

I13/I13B expose partial visibility as a first-class failure mode. This promotes **PS-024 — failure-isolated consequential transition publication**.

## I14 / I18 / I19 — crash-aware internal publication

I14 shows a local phase marker cannot distinguish `already published but completion marker lost` from `not published`, and old assurance cannot safely overwrite current revocation/retraction or newer state.

I18 refines the minimum recovery semantics:

```text
stable publication identity
expected base authoritative version
target semantic identity/digest
optional predicted target version
references needed to reacquire current validation
```

Target numeric version can be unknown at preparation time. State value alone can also be produced by another transition. `ResourceLease.publication_ref` and `topology_publication_ref` therefore carry publication provenance at the same modeled authoritative commit boundary.

I19 integrates those semantics into `OrganismRecoveryCoordinator` over the common runtime.

## I15–I17 / PS-025 — external execution recovery

I15 shows local state cannot prove that the outside world already acted. Receiver-recognized stable effect identity or exact effect-specific reconciliation can remove ambiguity; a non-identifiable physical effect can remain irreducibly uncertain.

I16 separates historical execution evidence from current permission to execute again. This promotes **PS-025 — externally grounded effect recovery / execution-authority separation**.

I17 then corrupts the external evidence plane itself. Three copied receipts from one failure lineage behave like one source. Independent reconciliation helps only when aggregation respects failure provenance, and its use is resource-priced.

## I05C — metacognitive audits reproduce the same evidence law

Verifier-quality audit records can be correlated, stale and unavailable.

Uniform independent audit calibrates much better than correlated majority; selective independent audit preserves similar calibration with fewer checks. Treating missing resolution as success can raise throughput while worsening calibration and false durable writes, showing that epistemic support and action value remain distinct.

## Shared evidence-lineage runtime

`EvidenceLineageRegistry` represents:

- source/failure lineage;
- staleness;
- whether a record actually resolves the claim;
- contradiction across independent resolving lineages.

It does not assign truth/reliability.

`EvidenceAssuranceDecision` combines that structure with separately learned source-quality estimates, consequence/asymmetric harm and independent-check cost.

## I20 / I21 — one assurance controller across domains

I20 mixes external-execution and metacognitive claims under one policy.

Default 30-seed result:

- record-count confidence: ~`3.062` utility/task, ~`1.438` harm;
- stale-only: ~`3.651`, ~`0.798`;
- uniform independent: ~`3.585`, ~`0.733`, 1.0 check/task;
- **lineage-value:** ~`3.782`, ~`0.592`, ~`0.695` checks/task.

I21 moves lineage-aware evidence planning inside `OrganismRecoveryCoordinator`, removing the privileged assumption that external receipts arrive already interpreted.

## I22 — transient state recovery

### Hot/predictive cache

Adaptive persist/rematerialize reaches ~`0.3335` utility/item versus ~`0.3278` rematerialize-all and ~`0.2314` persist-all. It retains only ~`0.171` of items and greatly reduces stale cache reuse.

### Delayed causal-credit trace

Unversioned positional restoration reaches ~`0.6083` utility/item but falsely blames ~`15.3%` of recovered trace items after structure changes. Versioned causal identity or source replay removes false blame (~`0.7073` utility). Adaptive recovery mixes exact trace persistence and replay for ~`0.7859`.

This composes PS-012/015/022/024: transient recovery is value-priced, but validity remains typed by currentness or causal identity.

## JEPA / E24

JEPA remains a candidate mechanism, not a commitment. E24 shows latent prediction can be efficient while passive predictive sufficiency fails under future objectives/interventions. Recoverable source evidence improves the compression/optionality frontier.

No JEPA-specific principle is selected.

## Current provisional selection count

**PS-001 through PS-025** are active reversible constraints. I17–I22 are composition/refinement evidence, not new principle selections.

## Next milestone — typed transient-state runtime

Implement the minimum runtime records implied by I22:

1. source-backed hot state:
   - stable subject/state identity;
   - source/rematerialization reference;
   - creation/generation context;
   - currentness/recovery status;
2. delayed credit eligibility:
   - stable historical transition identity;
   - structural/generation context;
   - optional replay/source reference;
   - explicit invalidation when no legitimate causal target survives.

Then run a real integrated crash scenario where:

- topology/resource publication may commit or remain prepared;
- authority may change while the process is down;
- external effect evidence can be stale/correlated;
- old-epoch events are pending;
- hot state can be persisted/rematerialized;
- delayed credit arrives after recovery.

The discriminator is whether all typed invariants survive **without** restoring an opaque full-process snapshot.

## Later targeted work

- learn/uncertain evidence-lineage relations rather than receiving lineage IDs as exact metadata;
- nested/overlapping **ownership** only if non-owning coordination overlays prove insufficient;
- neural E24C only if predictive-objective geometry remains architecture-discriminating;
- hardware co-design only after transition/topology/fidelity/recovery laws are stable enough for substrate assumptions to be informative.

## Phase-10 substantial-completion condition

Before Phase 10 is considered substantially complete, the combined organism should show that:

- selected principles retain lifetime value under composition;
- learned metacontrol overhead does not consume the gains;
- authority/provenance remain stable under learned control, topology change, handoff and crash recovery;
- world/tool/evaluator/self uncertainty remain distinguishable;
- self-change uses independent refreshing evidence and scoped rollback/change;
- failures remain attributable enough to revise mechanisms;
- unsupported transitions can remain tentative/unresolved;
- crash/restart cannot turn prepared state, copied evidence, old approval or unversioned transient pointers into accidental authority/knowledge/credit;
- external effect recovery separates local intent, execution history and current permission;
- the common executable runtime reproduces these boundaries without experiment-specific privileged semantics.

## Open targeted gap closure

Add literature only when it materially changes an active experimental/design decision. The Atlas optimizes discriminatory evidence, not source count.
