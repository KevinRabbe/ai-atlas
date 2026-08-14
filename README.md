# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The repository does **not** assemble today's AI stack by habit. It extracts mechanisms, evidence, constraints, failures and open questions; deliberately forgets implementation assumptions; derives competing clean-sheet organizations; and then tests them experimentally.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

Named model blocks, natural-language reasoning, databases, agents, recursive systems, harnesses, biological mechanisms, particular learning algorithms, world-model products, verifier products, self-improvement frameworks and current hardware are candidates or evidence—not axioms.

## Repository layers

- `atlas/` — mechanism-centric evidence notes;
- `sources/` — primary-source registry;
- `research/` — roadmap, claims, contradictions and failure modes;
- `synthesis/` — cross-domain deductions;
- `clean-sheet/` — implementation-free requirements, competing architecture families, experiment matrix and design ledger;
- `experiments/` — Phase-10 instrumented research organism.

## Current state

Evidence passes through self-improvement are complete to first-pass depth. Cross-domain synthesis is complete to first-pass depth. Phase 8 implementation forgetting: **PASS**. Phase 9 competing architecture generation: **PASS; no architecture family selected**. Phase 10 experimental reconstruction: **active**.

All Tier-1 experiment shapes are implemented, with second-family/promotion tests for control, integration, memory state, representation, inference compute and persistence plus cross-resource metacontrol.

The experiments increasingly show **conditional structure rather than universal winners**:

- coordination scope should grow only when dependencies/contention cross local boundaries;
- learned sharing trades reusable transfer against cross-task interference;
- current belief and source evidence solve different persistence problems;
- exact state, approximate numerical state, protocol metadata and auditability have different representation requirements;
- useful inference depth changes with uncertainty, consequence and operation price;
- persistence timescale should respond to environmental stability;
- compute, memory, observation and verification can substitute for one another as task/resource economics change.

## Provisional clean-sheet selections

Phase 10 has produced five reversible principle-level selections for the current experimental generation:

1. **PS-001 — typed hybrid boundary state.** Exact identity/control/provenance stays exact; tolerant numerical state may use compact approximate/learned channels; version/integrity is explicit; human-readable audit need not be the hot path.
2. **PS-002 — staged adaptive persistence.** Evidence normally enters reversible state before globally durable mutation, with consolidation timescale/threshold allowed to adapt to estimated environmental stability.
3. **PS-003 — coupling-scoped coordination.** Keep execution/local decisions local while coupling is local; introduce resource/domain/global arbitration only where dependencies or shared scarcity actually couple decisions.
4. **PS-004 — derived current belief with evidence linkage.** Keep a cheap current-state representation for repeated action/reasoning while retaining source linkage when correction, contradiction handling or provenance has future value.
5. **PS-005 — value-of-computation stopping.** Spend additional inference effort only while estimated marginal downstream value exceeds current computation/latency/risk cost; maximum budgets are ceilings, not consumption targets.

These are not product components and do not select architecture A/B/C/D. Their concrete implementations remain open and falsifiable.

See `clean-sheet/DESIGN_LEDGER.md`, `experiments/STATUS.md` and `research/ROADMAP.md` for the current checkpoint.

## Organizing hypothesis

The synthesis treats practical intelligence as potentially involving adaptive selection of state transitions and allocation of compute, durable change, information, assurance and exploration/design effort under uncertainty and finite resources. Phase-10 experiments now support several pieces of that hypothesis independently, but it remains falsifiable and does not determine a final architecture.

## Next decisive targets

The highest-value open questions are compute-matched conditional sharing (DL-002), multiple competing belief hypotheses under partial observability (DL-006), active value-driven information acquisition (DL-007), and a second cross-resource metacontrol family with simultaneous capacity contention and quality drift (DL-022).

## End goal

Produce a defensible answer to: **If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?**

The eventual architecture must remain evidence-traceable and experimentally falsifiable.