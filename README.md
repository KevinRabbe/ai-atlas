# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The repository does **not** assemble today's AI stack by habit. It extracts mechanisms, evidence, constraints and failures; deliberately forgets implementation assumptions; derives competing clean-sheet organizations; and tests them experimentally.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

Named model blocks, natural-language reasoning, databases, agents, harnesses, biological mechanisms, learning algorithms, verifier products, JEPA, world-model implementations and current hardware are evidence/candidates—not axioms.

## Current state

Phases 0–7 evidence/synthesis: first-pass complete. Phase 8 implementation forgetting: **PASS**. Phase 9 competing architecture generation: **PASS**. Phase 10 experimental reconstruction: **active**.

Phase 10 now contains **260 added test cases**, integrated experiments through **I12**, architecture-family comparisons **AF01–AF03**, and the first persistent reusable architecture substrate. **Twenty-three provisional implementation-neutral principles** survive their current promotion gates.

No fixed A/B/C/D architecture family is selected as a universal whole-system architecture. Their useful mechanisms increasingly behave like organizational modes that can be activated at different scopes and timescales.

## What the experiments are converging toward

The current evidence increasingly supports a smaller set of recurring laws:

- scope follows coupling, responsibility and causal extent;
- state follows expected future value and recoverability;
- optional work follows marginal value under shared scarcity;
- material complements/substitutes require interaction-aware allocation;
- sharing and structural indirectness follow reusable regularity;
- execution follows state change until consistency coupling justifies synchronization;
- fidelity follows decision sensitivity, uncertainty propagation and consequence;
- predictive compression is sufficient only relative to future/action-relevant distinctions and recoverability;
- authority follows independent current evidence/invariants, not confidence alone;
- verification follows the residual failure layer;
- durable change requires stronger and refreshing evidence;
- self-improvement diversity is retained only while future option value pays for it;
- repair blast radius expands only when evidence says the causal root is equally broad;
- metacognitive estimates are revisable state and can themselves justify active evidence acquisition;
- organizational mode, scope and membership may themselves be adaptive state;
- semantics that must survive reorganization cannot be defined only by the organization being changed;
- reconfiguration itself is a consequential transition and must earn evidence/assurance;
- **ownership, coordination, directional dependence, authority, provenance and resource identity are different typed relationships rather than one generic module graph.**

## Current executable architecture hypothesis

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
interaction-aware value/resource allocator
        ↓
consequence-sensitive independent assurance
        ↓
versioned execution + structural protocol
  execute / forward / stage / commit / rollback
        ↓
observe → causal credit → staged appropriately-scoped update
```

This is **not** yet a frozen final architecture.

## I06–I09 — from allocation to safe dynamic topology

I06 combines fidelity, source rematerialization/hot state, synchronization and intervention in one runtime budget. Learned joint allocation reaches ~`1.564` utility/task versus ~`1.355` for factorized independent controllers.

AF01–AF03 then show that A/B/C/D behave as regime-dependent organizational modes. AF02 learns mode selection; AF03 shows multiple modes can coexist at different scopes; I07 learns scope membership itself from changing dependency evidence.

I08 is the first real typed-state migration runtime. Across 30 seeds the typed-epoch variant reaches ~`1.0744` utility/step versus ~`0.9957` static typed topology while preserving zero tested failures in event routing, current authority, provenance, predictive rematerialization and resource uniqueness.

I09 then attacks the topology evidence with a correlated spoof source. Selective independent assurance raises attacked scope accuracy to ~`0.933` with zero harmful accepted migrations in the matched family. Simply raising confidence threshold on the same evidence source does not solve the correlated failure.

## I10 — persistent organism runtime API

I10 turns those results into a reusable `TypedScopeRuntime` rather than another standalone benchmark.

It exposes:

- exact evidence/source and predictive-rematerialization records;
- current versioned capability authority;
- singular versioned resource leases;
- typed transition proposals;
- interaction-aware bundle allocation;
- proposal-specific assurance tokens;
- staged/committed/rolled-back topology changes;
- topology epochs and exactly-once forwarding of in-flight work.

Eight semantic API tests plus five integration-scenario tests exercise these invariants. In the 900-step integration scenario, topology and authority change while work is queued; source state is rematerialized; structural proposals can be rejected; and every queued event is eventually processed without bypassing the architecture API.

## I11 — coordination can overlap ownership

A disjoint ownership partition is not sufficient to represent every useful relationship.

With sparse cross-cutting work (~18% active), a temporary non-owning coordination overlay wins (~`1.1303`) over base-only (~`1.1259`), forced disjoint repartition (~`1.0898`) and persistent overlap (~`1.0635`).

When cross-cutting work is active ~90% of the time, persistent overlap becomes worth carrying (~`1.1012` vs ~`1.0756` temporary). When coupling becomes effectively global and continuous, one global scope wins (~`1.5130`).

So the runtime now has a separate `CoordinationScopeRegistry`: memberships may overlap, but scopes do not own or duplicate evidence, authority or resource leases.

## I12 — dependency is directional until reciprocity earns sharing

A one-way dependency does not imply reverse information flow or shared state.

In sparse directional structure, symmetric links create ~`11.94` unsupported reverse relationships/step while directed/adaptive representations are effectively zero. In reciprocal clusters, shared coordination becomes cheaper than individually dispatched one-way links. In mixed regimes the adaptive organization uses both simultaneously.

Default 30-seed lifetime utility:

- global scope: ~`0.7116`;
- directed links: ~`0.7034`;
- symmetric links: ~`0.6689`;
- **reciprocity-adaptive: ~`0.7394`**.

At 20-step regimes, static global organization wins again because dependency inference cannot amortize its lag.

The runtime now also has a typed `DependencyRegistry`; reciprocity can be detected as evidence for shared coordination but does not automatically create reverse flow, authority, ownership or a scope.

## JEPA / E24

JEPA remains explicitly inside the Atlas as a candidate predictive-representation mechanism, not a selected component.

E24 shows that a coarse predictive latent can be very efficient yet lose a future/action-relevant distinction. Dense predictive state or compact latent + recoverable source evidence preserves the option.

Current conclusion:

> predictive compression should optimize lifetime decision/intervention utility, not passive prediction accuracy alone.

## Discovery target

Human knowledge is treated as bootstrap state rather than the final epistemic ceiling:

`inherited knowledge -> competing hypothesis -> search/experiment -> candidate discovery -> scoped verification -> independent evidence/replication -> consolidated knowledge`

The goal is not merely an AI that reproduces humanity's knowledge, but one that can expand the shared knowledge frontier through independently verifiable discovery.

## Current provisional selection count

**PS-001 through PS-023** are active reversible constraints. See `clean-sheet/DESIGN_LEDGER.md` for the complete evidence trail and falsifiers.

## Next milestone — I13 partial structural commit

The current runtime still assumes a structural topology commit is atomic.

I13 should inject failures after only part of a migration has completed and compare naive in-place mutation, stop-the-world replacement, staged transaction + rollback, and possibly incremental dual-version handoff.

The test must measure whether the transition path preserves:

- evidence/source reachability;
- singular resource leases;
- current authority semantics;
- exactly-once in-flight events;
- topology epoch consistency;
- rollback/recovery cost and downtime.

A target topology being correct is not enough if the path used to reach it can corrupt the system.

## Organizing hypothesis

Practical intelligence may be adaptive selection of typed state transitions **and typed organizational relationships**, with computation, information, interaction, durable change, assurance and exploration allocated under uncertainty and finite resources—while authority and evidence semantics remain stronger than ordinary confidence scores.

This remains falsifiable.

## End goal

Produce a defensible answer to:

**If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?**

The eventual architecture must remain evidence-traceable and experimentally falsifiable.
