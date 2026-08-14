# Research Roadmap

## Phases 0–7

Taxonomy/evidence discipline, computational substrate, learning/adaptation, inference-time intelligence, persistent intelligence, verification/control, self-improvement and first cross-domain synthesis completed first passes on 2026-08-14. Targeted gap closure remains open.

Discovery/epistemic growth is explicit: human knowledge is bootstrap evidence/methodology rather than a permanent epistemic ceiling; F26 requires turning uncertainty into testable hypotheses and independently supported new knowledge.

## Phase 8 — Forget implementations

First-pass clean-sheet functional reconstruction completed on 2026-08-14. **Exit gate: PASS.**

## Phase 9 — Clean-sheet architecture

First-pass candidate generation completed on 2026-08-14. **Exit gate: PASS.** A/B/C/D remain useful reference organizations, but current Phase-10 evidence treats their mechanisms as conditional modes/scopes rather than mutually exclusive final systems.

## Phase 10 — Experimental reconstruction

**Active. Twenty-three reversible implementation-neutral principles survive their current promotion gates.** The validation history now contains **260 added test cases**.

The experimental strategy has progressed through:

1. isolated mechanism discrimination;
2. integrated epistemic/resource composition;
3. guarded self-improvement;
4. learned metacognition under imperfect feedback;
5. interaction-aware runtime allocation;
6. fixed architecture-family comparison;
7. adaptive organizational modes;
8. simultaneous scoped organization;
9. learned dynamic topology;
10. typed-state migration across topology epochs;
11. independent assurance for structural reconfiguration;
12. a persistent reusable typed-scope runtime API;
13. overlapping/non-owning coordination scopes;
14. directional dependency semantics and reciprocity-triggered sharing.

## Current architecture spine

```text
stable typed semantic identities
  subjects / evidence / provenance / sources
  authority versions / resource leases
        |
        +--> directional dependencies
        |
        +--> disjoint ownership topology
        |       + dynamic split / merge
        |
        +--> overlapping non-owning coordination scopes
                temporary or persistent
        ↓
typed transition proposals
        ↓
interaction-aware value/resource allocation
        ↓
consequence-sensitive independent assurance
        ↓
versioned transition protocol
  execute / forward / stage / commit / rollback
        ↓
observe → causal credit → staged appropriately-scoped update
```

The scalar/value allocator cannot manufacture epistemic, capability or topology authority.

## I06–I09 — architecture-scale composition

I06 shows that fidelity, rematerialization/hot state, synchronization and intervention interact enough that independent operation pricing loses to joint allocation (~`1.564` vs ~`1.355` utility/task).

AF01–AF03 and I07 then show that organizational mode, organizational scope and scope membership can all be adaptive state, but each form of structural plasticity has a persistence-vs-transition-cost timescale.

I08 gives dynamic scopes real typed state. Stable evidence/provenance, authority, resource leases and in-flight work survive split/merge when semantics are addressed independently from topology and events carry topology epochs.

I09 adds the promotion boundary: under correlated/spoofed coupling evidence, a higher threshold on the same source is insufficient; sufficiently independent assurance may be worth buying before moving real state.

## I10 — reusable typed-scope organism runtime

`TypedScopeRuntime` is now the common architecture substrate for later experiments.

It provides:

- evidence/source and predictive-rematerialization records;
- current versioned authority;
- singular resource leases;
- typed transition proposals;
- interaction-aware bundle allocation;
- independent proposal-specific assurance;
- staged scope changes + rollback;
- topology epochs and exactly-once event forwarding.

Eight semantic tests and five end-to-end scenario tests exercise these boundaries. The scenario repeatedly changes topology and authority while work is in flight without bypassing the runtime API.

## I11 — cross-cutting coordination without forced ownership migration

A component may need to coordinate with more than one group while its semantic ownership remains stable.

Sparse cross-cutting work favors temporary non-owning overlays. Frequent recurring cross-cutting work can justify persistent overlap. Dense continuous coupling eventually makes one merged/global scope cheaper again.

The runtime therefore gains a separate `CoordinationScopeRegistry`. Membership may overlap, but coordination scopes do not own evidence, leases or authority.

## I12 — directional dependency semantics

One-way dependency does not imply reverse flow.

Sparse directional work favors directional links over symmetric relationships. Reciprocal clusters justify shared coordination. Mixed regimes require both simultaneously. The adaptive representation reaches ~`0.7394` lifetime utility versus ~`0.7116` global, ~`0.7034` directed-only and ~`0.6689` symmetric-only at the default 180-step regime duration.

At 20-step regimes static global wins, again showing that richer structure must amortize inference lag.

The runtime now includes a typed `DependencyRegistry`; reciprocity is detectable evidence for sharing but does not automatically create a scope, authority or ownership transfer.

## JEPA / E24

JEPA remains a candidate mechanism, not a commitment. E24 shows latent prediction can be efficient while passive predictive sufficiency still fails under future objectives/interventions. Recoverable source evidence substantially improves the compression/optionality frontier.

No JEPA-specific principle is selected.

## Current provisional selection count

**PS-001 through PS-023** are active reversible constraints. I08–I12 refine/compose those rules rather than creating additional principle labels.

## Next milestone — I13 partial structural commit

The reusable runtime still assumes structural commit is atomic.

I13 should deliberately fail migration at different points and compare:

1. naive in-place migration;
2. stop-the-world copy/replace;
3. staged transactional migration with version fence + rollback;
4. incremental/dual-version handoff if needed as a separate alternative.

Measure:

- semantic corruption after failure;
- evidence/source reachability;
- resource-lease uniqueness;
- current authority correctness;
- exactly-once in-flight event behavior;
- topology epoch consistency;
- downtime/blocked work;
- copied state / migration operations;
- rollback/recovery work.

### Discriminator

A structural-update protocol earns selection only if it preserves invariants under partial failure without paying more downtime/copy cost than the avoided corruption is worth.

Do not assume “transactions” by name; compare the mechanisms.

## After I13

High-value stresses remain:

- nested/overlapping **ownership** only if non-owning overlays prove insufficient;
- partial migration of bounded caches and delayed credit traces;
- simultaneous structural change + authority revocation;
- I05C correlated/adversarial evaluator audits and partially unresolved outcomes;
- neural E24C only if predictive-objective geometry remains architecture-discriminating;
- hardware co-design only after the transition/topology/fidelity laws are stable enough for substrate assumptions to be informative.

## Phase-10 substantial-completion condition

Before Phase 10 is considered substantially complete, the combined organism should show that:

- selected principles retain lifetime value under composition;
- learned metacontrol overhead does not consume the gains;
- authority/provenance remain stable under learned control and topology changes;
- world/tool/evaluator/self uncertainty remain distinguishable;
- self-change uses independent refreshing evidence and scoped rollback/change;
- failures remain attributable enough to revise mechanisms;
- unsupported transitions can remain tentative/unresolved;
- the common executable runtime reproduces important experimental boundaries without experiment-specific privileged semantics;
- structural updates remain safe enough under partial failure or the evidence identifies where static organization is preferable.

## Open targeted gap closure

Add literature only when it materially changes an active experimental/design decision. The Atlas optimizes discriminatory evidence, not source count.
