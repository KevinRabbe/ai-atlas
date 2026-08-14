# Phase 10 Experimental Status

**Checkpoint: Tier-1 experiment shapes implemented on 2026-08-14.**

## Implemented probes

E01 hierarchical vs distributed allocation; E02 integrated vs heterogeneous learned computation; E03 direct-address vs compressed state; E04 representation/interface; E05 fixed vs adaptive compute; E09 immediate vs staged consolidation.

## Validation in this pass

The new E01/E02/E04 code was executed locally with Python 3.11+ stdlib only.

**10 additional unit tests pass** for the three new probes. The pre-existing E03/E05/E09 source files were not modified by this implementation pass.

A reproducible **12-seed aggregate sweep** was completed for E01/E02/E04. The complete aggregate can be regenerated with `python -m ai_atlas_lab.tier1_sweep --seeds 12`, and the load-bearing means are recorded in `PRELIMINARY_TIER1_RESULTS.md`.

## Preliminary replicated patterns

- E01: sparse dependency graphs favor cheap local coordination; deeper/dense dependencies expose bounded local coordination unless extra message rounds are spent.
- E02: at equal parameter count, strong shared task structure can favor integrated transfer, while divergent tasks favor specialists and shared updates create measurable cross-task interference.
- E04: no tested representation dominates every requirement; approximate float state is compact and accurate for approximate values, while exact identifiers, protocol evolution, integrity and audit impose different interface requirements.

These are **not architecture selections**.

## Why no design-ledger decision moved yet

The minimum promotion rule requires replication across a structurally different task family and a resource-regime change in addition to the current synthetic sweeps.

## Next targets

1. second E01 environment with independent communication latency/price;
2. nonlinear/compositional E02 family and partially shared alternatives;
3. E04 bandwidth/fidelity sweep plus learned continuous state with exact side channel;
4. adaptive E09 consolidation threshold conditioned on hidden volatility;
5. multi-seed aggregation for E03/E05/E09;
6. then E06 multiple belief hypotheses and E07 active information acquisition.

## Guardrail

During Phase 10 the measuring instrument must remain simpler than the hypotheses it measures.
