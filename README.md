# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The repository does **not** assemble today's AI stack by habit. It extracts mechanisms, evidence, constraints and failures; deliberately forgets implementation assumptions; derives competing clean-sheet organizations; and tests them experimentally.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

Named model blocks, natural-language reasoning, databases, agents, harnesses, biological mechanisms, learning algorithms, verifier products, JEPA, world-model implementations and current hardware are evidence/candidates—not axioms.

## Current state

Phases 0–7 evidence/synthesis: first-pass complete. Phase 8 implementation forgetting: **PASS**. Phase 9 competing architecture generation: **PASS**. Phase 10 experimental reconstruction: **active**.

Phase 10 now contains **278 added test cases**, integrated work through **I13C**, architecture-family comparisons **AF01–AF03**, and a persistent reusable architecture substrate. **Twenty-four provisional implementation-neutral principles** survive their current promotion gates.

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
- ownership, coordination, directional dependence, authority, provenance and resource identity are different typed relationships rather than one generic module graph;
- **multi-step consequential change must separate preparation from authoritative publication whenever partial visibility can violate invariants.**

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
PREPARE non-authoritative candidate state
        ↓
version + current-authority publication fence
        ↓
PUBLISH coherent topology / ownership / durable version
        ↓
retire old version / forward in-flight work
        ↓
observe → causal credit → staged appropriately-scoped update
```

This is **not** yet a frozen final architecture.

## I06–I09 — from allocation to safe dynamic topology

I06 combines fidelity, source rematerialization/hot state, synchronization and intervention in one runtime budget. Learned joint allocation reaches ~`1.564` utility/task versus ~`1.355` for factorized independent controllers.

AF01–AF03 show that A/B/C/D behave as regime-dependent organizational modes. AF02 learns mode selection; AF03 shows multiple modes can coexist at different scopes; I07 learns scope membership itself from changing dependency evidence.

I08 is the first real typed-state migration runtime. Across 30 seeds the typed-epoch variant reaches ~`1.0744` utility/step versus ~`0.9957` static typed topology while preserving zero tested failures in event routing, current authority, provenance, predictive rematerialization and resource uniqueness.

I09 attacks topology evidence with a correlated spoof source. Selective independent assurance raises attacked scope accuracy to ~`0.933` with zero harmful accepted migrations in the matched family. A higher confidence threshold on the same correlated source is not sufficient.

## I10 — persistent organism runtime API

I10 turns those results into a reusable `TypedScopeRuntime` rather than another standalone benchmark.

It exposes exact evidence/source records, predictive rematerialization, current versioned authority, singular resource leases, typed transition proposals, interaction-aware bundle allocation, proposal-specific assurance, staged/rolled-back topology changes and topology-epoch event forwarding.

Eight semantic API tests plus five integration-scenario tests exercise these invariants while topology and authority change with work in flight.

## I11 — coordination can overlap ownership

A disjoint ownership partition is not sufficient to represent every useful relationship.

Sparse cross-cutting work favors temporary non-owning coordination overlays; frequent recurring cross-cutting work can justify persistent overlap; dense continuous coupling eventually makes one global scope cheaper.

The runtime therefore has a separate `CoordinationScopeRegistry`: memberships may overlap, but scopes do not own or duplicate evidence, authority or resource leases.

## I12 — dependency is directional until reciprocity earns sharing

A one-way dependency does not imply reverse information flow or shared state.

In sparse directional structure, symmetric links create ~`11.94` unsupported reverse relationships/step while directed/adaptive representations are effectively zero. Reciprocal clusters can justify shared coordination. Mixed regimes use both simultaneously.

Default 30-seed lifetime utility is ~`0.7394` reciprocity-adaptive versus ~`0.7116` global, ~`0.7034` directed-only and ~`0.6689` symmetric-only. At 20-step regimes static global wins because structural evidence changes too quickly.

The runtime also has a typed `DependencyRegistry`; reciprocity may motivate shared coordination but does not automatically create reverse flow, authority, ownership or a scope.

## I13 / I13B — the path to a new structure matters

I13 injects failure halfway through topology migration. Naive live mutation exposes mixed old/new state, losing/duplicating work. Stop-world replacement, staged publication and dual-version handoff keep the live system coherent but pay different blocking/state costs.

I13B reproduces the same boundary in a different problem: singular resource/service ownership. Make-before-break can produce two writers; break-before-make can produce no writer. Failure-isolated publication preserves singular ownership.

The two families have real mechanism crossovers:

- near-zero failure + negligible traffic can make direct update cheapest;
- high failure + low traffic can justify blocking replacement;
- ordinary live load favors staged/version-fenced publication;
- high live traffic can justify temporary dual-version handoff.

This promotes:

> **PS-024 — failure-isolated consequential transition publication:** prepare multi-step consequential changes in non-authoritative/reversible state when partial visibility can violate invariants; publish topology/ownership/authority-bearing versions only across a coherence boundary after required validation. Choose direct, blocking, staged or dual-version publication according to failure risk, blast radius, live-work pressure and isolation cost.

The selected object is the failure-isolation semantic, not transactions, locks, consensus or blue/green deployment by name.

## I13C — publication fences are now explicit

`PublicationProtocol` makes PS-024 executable:

- preparation does not mutate live ownership/topology;
- topology candidates remember their prepared-against epoch;
- resource handoffs remember the prepared-against lease version;
- stale plans are rejected at publication;
- current authority is re-read at publication, so revocation after preparation wins over stale prepared intent;
- consequential publication still requires independent assurance;
- discard leaves the live system unchanged.

This also closes a concurrency hole: two topology plans staged from the same epoch cannot both publish after one has already advanced the epoch.

## JEPA / E24

JEPA remains explicitly inside the Atlas as a candidate predictive-representation mechanism, not a selected component.

E24 shows that coarse predictive latent state can be highly efficient yet discard a future/action-relevant distinction. Dense predictive state or compact latent + recoverable source evidence preserves the option.

> Predictive compression should optimize lifetime decision/intervention utility, not passive prediction accuracy alone.

## Discovery target

Human knowledge is treated as bootstrap state rather than the final epistemic ceiling:

`inherited knowledge -> competing hypothesis -> search/experiment -> candidate discovery -> scoped verification -> independent evidence/replication -> consolidated knowledge`

The goal is an AI capable of expanding the shared knowledge frontier through independently verifiable discovery, not merely reproducing humanity's bootstrap knowledge.

## Current provisional selection count

**PS-001 through PS-024** are active reversible constraints. See `clean-sheet/DESIGN_LEDGER.md` for the complete evidence trail and falsifiers.

## Next milestone

The next stress should combine **authority revocation + in-flight work + a prepared or dual-version structural handoff** through `PublicationProtocol`.

Then inject crash/restart between prepare and publish. Only if recovery requires durable intent/version records should the Atlas add a persistence/logging mechanism; do not assume a WAL/database beforehand.

## Organizing hypothesis

Practical intelligence may be adaptive selection of typed state transitions **and typed organizational relationships**, with consequential changes prepared, assured and coherently published under finite resources—while authority and evidence semantics remain stronger than ordinary confidence scores.

This remains falsifiable.

## End goal

Produce a defensible answer to:

**If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?**

The eventual architecture must remain evidence-traceable and experimentally falsifiable.
