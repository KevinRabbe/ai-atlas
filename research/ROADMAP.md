# Research Roadmap

## Phases 0–7

Taxonomy/evidence discipline, computational substrate, learning/adaptation, inference-time intelligence, persistent intelligence, verification/control, self-improvement and first cross-domain synthesis completed first passes on 2026-08-14. Targeted gap closure remains open.

Discovery/epistemic growth is explicit: human knowledge is bootstrap evidence/methodology rather than a permanent epistemic ceiling; F26 requires turning uncertainty into testable hypotheses and independently supported new knowledge.

## Phase 8 — Forget implementations

First-pass clean-sheet functional reconstruction completed on 2026-08-14. **Exit gate: PASS.**

## Phase 9 — Clean-sheet architecture

First-pass candidate generation completed on 2026-08-14. **Exit gate: PASS.** A/B/C/D remain useful reference organizations, but current Phase-10 evidence treats their mechanisms as conditional modes/scopes rather than mutually exclusive final systems.

## Phase 10 — Experimental reconstruction

**Active. Twenty-six reversible implementation-neutral principles survive their current promotion gates.** The validation history now contains **412 added test cases**.

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
18. transient cache/credit recovery across structural change;
19. integrated crash/topology/evidence/transient recovery lifecycle;
20. hidden/changing evidence-dependence inference;
21. common-cause confounding of co-failure evidence;
22. reusable learned evidence-dependence substrate.

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
source identity + known provenance where available
        + learned source-quality estimates
        + revisable evidence-dependence model
            context-conditioned failure relations
            optional provenance/dependency probes
        ↓
effective independent evidence structure
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
old-epoch event forwarding + current authority re-check
        ↓
typed transient recovery
  hot state -> currentness / source rematerialization
  credit -> exact causal identity / source replay
        ↓
observe → versioned causal credit → staged appropriately-scoped update
```

The value allocator cannot manufacture epistemic, capability, publication, causal or external-execution authority. Source identity also cannot manufacture evidence independence.

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

I15 shows local state cannot prove the outside world already acted. Receiver-recognized stable effect identity or exact reconciliation can remove ambiguity; a non-identifiable physical effect can remain irreducibly uncertain.

I16 separates historical execution evidence from current permission to execute again. This promotes **PS-025 — externally grounded effect recovery / execution-authority separation**.

I17 then corrupts the external evidence plane. Three copied receipts from one failure lineage behave like one source. Independent reconciliation helps only when aggregation respects failure provenance, and its use is resource-priced.

## I05C — metacognitive audits reproduce the same evidence law

Verifier-quality audit records can be correlated, stale and unavailable. Uniform independent audit calibrates much better than correlated majority; selective independent audit preserves similar calibration with fewer checks. Missing resolution is not positive evidence, even when a riskier action can have higher short-run expected utility.

## I20 / I21 — one evidence-assurance controller across domains

`EvidenceLineageRegistry` represents known source lineage, staleness, resolution and conflict without assigning truth/reliability. `EvidenceAssuranceDecision` combines that structure with learned quality, consequence/asymmetric harm and check cost.

Default I20:

- record-count confidence: ~`3.062` utility/task, ~`1.438` harm;
- stale-only: ~`3.651`, ~`0.798`;
- uniform independent: ~`3.585`, ~`0.733`, 1.0 check/task;
- **lineage-value:** ~`3.782`, ~`0.592`, ~`0.695` checks/task.

I21 moves evidence planning inside the common recovery coordinator.

## I22 / I23 — typed transient recovery and whole-lifecycle composition

Source-backed hot state can be persisted/rematerialized according to reuse/currentness economics. Delayed credit requires exact historical transition identity/version or replayable source history after structural change.

I23 combines topology publication, crash/restart, publication provenance, source changes, transient state, delayed credit, old-epoch external events, authority revocation, stale/correlated external receipts and independent reconciliation in every episode.

Approximate 30-seed means:

| policy | utility/episode | stale hot | false credit | unauthorized old event | duplicate publication attempt |
|---|---:|---:|---:|---:|---:|
| **typed recovery** | **~2.67** | **0** | **0** | **0** | **0** |
| opaque snapshot restore | ~-1.47 | ~0.716 | ~0.397 | ~0.299 | ~0.502 |
| discard transient | ~1.27 | 0 | 0 | 0 | 0 |

This establishes a strong current architecture inference:

> **Recovery should restore semantically valid typed state, not blindly restore process memory and not indiscriminately discard all transient work.**

## I24 — hidden/changing evidence dependence

I24 removes exact lineage IDs from the learner. Stable visible sources share hidden failure ancestry that changes midway through the run.

Approximate 30-seed result:

| policy | utility/task | weighted harm | independent audits/task | dependency probes/task |
|---|---:|---:|---:|---:|
| source-count independence | ~4.157 | ~0.296 | ~0.277 | 0 |
| all correlated | ~4.002 | ~0.331 | ~0.865 | 0 |
| **learned dependence** | **~4.196** | **~0.232** | ~0.437 | 0 |
| learned + active probe | ~4.194 | **~0.221** | ~0.423 | ~0.238 |
| oracle | ~4.213 | ~0.216 | ~0.408 | 0 |

The passive learner recovers hidden relations from independently resolved co-failure history, degrades when upstream dependencies change, then relearns. Explicit dependency/provenance probes are bought only where relation uncertainty can change assurance behavior.

## I25 / PS-026 — common causes confound raw co-failure

I25 introduces a second family: global task difficulty raises error across all evaluators, creating broad co-failure even among sources with independent ancestry.

Raw co-failure therefore overstates dependence. Conditioning on a noisy observable difficulty context improves utility and reduces unnecessary auditing. Controlled pair-dependency evidence further reduces harm.

Approximate 10-seed result:

- raw co-failure: ~`4.116` utility, ~`0.296` harm, ~`0.433` audits/task;
- **difficulty-conditioned:** ~`4.149`, ~`0.294`, ~`0.337` audits/task;
- conditioned + probe: ~`4.145`, ~`0.277`, ~`0.335` audits/task;
- oracle: ~`4.165`, ~`0.281`, ~`0.337` audits/task.

This promotes:

### PS-026 — learned / causally qualified evidence dependence

> **Treat independence between evidence sources as uncertain, revisable relational state. Do not infer independent failure modes from record count, source names, agreement or raw co-failure alone. Infer dependence from outcome/provenance/intervention evidence while conditioning on plausible common causes, and acquire explicit dependency evidence when uncertainty about independence can materially change assurance value.**

`EvidenceDependenceModel` is the current reusable model-free substrate. It keeps exact source identity, learned source quality and learned dependence separate.

## JEPA / E24

JEPA remains a candidate mechanism, not a commitment. E24 shows latent prediction can be efficient while passive predictive sufficiency fails under future objectives/interventions. Recoverable source evidence improves the compression/optionality frontier.

No JEPA-specific principle is selected.

## Current provisional selection count

**PS-001 through PS-026** are active reversible constraints.

## Next milestone — conditional, directional and adversarial dependence

PS-026 is deliberately narrow. The next discriminators should attack its pairwise symmetric assumptions.

### I26A — domain-conditional dependence

The same two source identities may share an upstream mechanism for one claim family but be independent for another.

Compare:

1. one global source-pair dependence model;
2. claim-domain-conditioned dependence;
3. value-priced domain-specific provenance probe;
4. oracle relation.

Measure false independence, false dependence, assurance cost and cross-domain negative transfer.

### I26B — directional dependence

Derived/copy relations are not necessarily symmetric:

```text
A -> B
```

can mean B inherits A's errors while A does not inherit B's independent failures.

Test whether an undirected shared-lineage graph loses useful source ordering/provenance and whether a directional dependency representation improves aggregation/assurance.

### I26C — adversarial apparent independence

Let correlated sources intentionally decorrelate visible errors or selectively abstain so that ordinary co-failure statistics underestimate shared ancestry.

Compare passive correlation inference with provenance/interventional diagnostics.

### I26D — sparse / large source population

Scale source count while reducing resolved feedback. Pairwise O(N²) dependence state may stop paying for itself.

Test sparse graphs, low-rank/common-cause models, hierarchical grouping and active pair selection before selecting any scalable implementation.

## Integration milestone

After I26, the common assurance path should consume **learned effective dependence** directly and use exact lineage metadata only when provenance actually makes it known.

## Later targeted work

- nested/overlapping **ownership** only if non-owning coordination overlays prove insufficient;
- neural E24C only if predictive-objective geometry remains architecture-discriminating;
- hardware co-design only after transition/topology/fidelity/recovery/evidence-dependence laws are stable enough for substrate assumptions to be informative.

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
- evidence independence can be learned without confusing broad common causes for shared ancestry;
- the common executable runtime reproduces these boundaries without experiment-specific privileged semantics.

## Open targeted gap closure

Add literature only when it materially changes an active experimental/design decision. The Atlas optimizes discriminatory evidence, not source count.
