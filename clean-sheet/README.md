# Clean-Sheet Reconstruction

This directory begins after evidence has been synthesized and current implementations are deliberately removed from the design vocabulary.

## Phase-8 status

**Functional reconstruction complete to first-pass depth. Architecture selection has not yet begun.**

The clean-sheet specification is split into:

- [`PROBLEM_MODEL.md`](PROBLEM_MODEL.md) — environment, semantic state classes, operation classes and transition-value problem.
- [`FUNCTIONAL_SPECIFICATION.md`](FUNCTIONAL_SPECIFICATION.md) — implementation-independent capability contracts with inputs, outputs, invariants and failure signals.
- [`STATE_AND_INFORMATION_MODEL.md`](STATE_AND_INFORMATION_MODEL.md) — evidence, belief, provenance, authority, uncertainty, time, identity and persistence semantics.
- [`RESOURCE_MODEL.md`](RESOURCE_MODEL.md) — compute, memory, movement, communication, latency, energy, interaction, verification and lifetime cost.
- [`INVARIANTS.md`](INVARIANTS.md) — cross-system rules candidate architectures must satisfy or explicitly falsify.
- [`ASSURANCE_AND_CHANGE_PROTOCOL.md`](ASSURANCE_AND_CHANGE_PROTOCOL.md) — consequence-sensitive transition gating, versioning, recovery and trusted-change semantics.
- [`UNRESOLVED_CHOICES.md`](UNRESOLVED_CHOICES.md) — experimental design dimensions the evidence does not yet resolve.
- [`TRACEABILITY.md`](TRACEABILITY.md) — mapping from clean-sheet requirements back to synthesis/evidence.
- [`ARCHITECTURE_QUESTIONS.md`](ARCHITECTURE_QUESTIONS.md) — open architecture questions retained from the initial scaffold.
- [`DESIGN_LEDGER.md`](DESIGN_LEDGER.md) — decisions will be recorded here only after candidate comparison.

## Forgetting protocol

Before selecting a mechanism:

1. State the required function without implementation names.
2. State consumed/produced state, invariants and physical constraints.
3. Trace the requirement back to evidence.
4. Remove assumptions inherited from contemporary systems.
5. Generate multiple mechanistically distinct candidates where uncertainty permits.
6. Compare candidates under matched capability/resource/assurance budgets.
7. Specify an experiment or observation that could reverse the preference.
8. Record the eventual choice and rejected alternatives in `DESIGN_LEDGER.md`.

Forbidden shortcuts include:

- selecting a computational block because current high-performing systems use it;
- using human language internally merely because it is convenient for humans;
- choosing a memory mechanism because it is popular rather than because its access/update semantics match the requirement;
- increasing the number of reasoning processes merely because parallelism sounds more intelligent;
- adding recursion, search, simulation or self-modification without showing positive marginal value relative to their coordination/assurance cost.

## Design discipline for Phase 9

Architecture candidates must be derived from the specification rather than from product/model names.

Every proposed mechanism must answer:

- Which clean-sheet functions does it implement?
- Which state classes does it read/write?
- Which invariants constrain it?
- What physical resources dominate?
- What uncertainty/authority does it preserve?
- What competing mechanism could provide the same function?
- What experiment would falsify its inclusion?

## Principle

The goal is not novelty. An existing mechanism may reappear later if the clean-sheet requirements independently lead back to it. The goal is to ensure every retained mechanism survives reconstruction for a reason rather than inheritance by default.
