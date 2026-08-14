# Phase 10 Experimental Status

**Checkpoint: Tier-1 implementation complete; promotion-quality follow-ups started on 2026-08-14.**

## Implemented probes

E01 hierarchical vs distributed allocation; E02 integrated vs heterogeneous learned computation; E03 direct-address vs compressed state; E04 representation/interface; E05 fixed vs adaptive compute; E09 immediate vs staged consolidation.

A second E01 family, `E01B_RESOURCE_CONTENTION`, is also implemented to test control topology under a structurally different coupling mechanism.

## Validation in this turn

The new E01/E02/E04 implementation and E01B follow-up were executed locally with Python 3.11+ stdlib only.

**12 newly added unit tests pass locally**: 10 for E01/E02/E04 and 2 for E01B. The pre-existing E03/E05/E09 source files were not modified by these implementation passes.

A reproducible 12-seed aggregate sweep was completed for E01/E02/E04. E01B was independently swept across 20 seeds and three verification-capacity regimes.

## Preliminary replicated patterns

- **E01 dependency family:** sparse dependencies favor cheap local coordination; dense/deep dependencies require additional coordination, but extra local propagation can recover hierarchical quality at a different communication cost.
- **E01B contention family:** scarce shared resources make uncoordinated local requests inefficient; resource-local arbitration matches global allocation quality in this benchmark without requiring a universal executive, at higher message cost.
- **E02:** at equal parameter count, highly shared task structure can favor integrated transfer; as tasks diverge, specialists dominate and shared updates create cross-task interference.
- **E04:** approximate float state is compact and accurate for approximate values, while exact identity, protocol evolution, integrity and audit/recovery impose different interface requirements.

These are still **not final architecture selections**.

## Resource-regime follow-ups already run

- E02 was swept at 300 / 1,200 / 4,800 training examples. At sharedness 0.98 the integrated learner leads in the low/mid-data regimes and converges toward specialist performance with abundant data; at sharedness 0.75 specialists remain stronger.
- E04 was swept across 24 / 32 / 48 / 96 / 192-byte caps. The 28-byte float vector becomes feasible at 32 bytes; the 38-byte tagged representation at 48; verbose/redundant formats require substantially larger budgets.

## Design-ledger implication

DL-001 now has evidence from two structurally different control problems. The evidence favors the **principle** that coordination scope should track coupling scope, but DL-001 remains unresolved because E22 has not yet tested whether this generalizes to simultaneous substitution among multiple resource classes and learned metacontrol.

DL-002 and DL-004 also remain unresolved: their resource sweeps are informative, but each still needs a second task family.

## Next targets

1. nonlinear/compositional E02 family plus partially shared alternatives;
2. second E04 task family using backtracking/constraint messages plus a learned continuous channel with exact side state;
3. adaptive E09 consolidation threshold conditioned on hidden volatility;
4. aggregate E03/E05/E09 in the same multi-seed schema;
5. E22 cross-resource metacontrol before promoting DL-001;
6. then Tier-2 E06 multiple belief hypotheses and E07 active information acquisition.

## Guardrail

During Phase 10 the measuring instrument must remain simpler than the hypotheses it measures.