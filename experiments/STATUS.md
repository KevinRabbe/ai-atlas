# Phase 10 Experimental Status

**Checkpoint: first model-free organism baseline implemented on 2026-08-14.**

## Implemented

### E03 — direct-address history vs compressed state

Variants:

- direct-address retained history;
- compressed current state;
- hybrid current state + indexed source history.

Measured:

- current/historical/exact accuracy;
- reads/writes/comparisons;
- logical active/archive/index state size.

### E05 — fixed vs adaptive computation

Variants:

- several fixed evidence budgets;
- confidence-threshold adaptive stopping with a hard maximum.

Measured:

- accuracy;
- average evidence/computation samples;
- allocation by hidden task difficulty/evidence signal;
- total logical operations/samples.

### E09 — immediate durable updates vs staged consolidation

Variants:

- immediate durable overwrite;
- N-confirmation tentative staging;
- decaying evidence-threshold staging.

Measured:

- current-state accuracy;
- true regime switches;
- durable update count;
- false durable updates;
- adaptation delay after real change;
- logical reads/writes/operations.

## Validation

The current implementation was executed locally with Python 3.11+ stdlib only.

**10 unit tests pass** across the three probes.

The tests validate benchmark semantics such as:

- compressed state intentionally loses history/exact payload while preserving current-state lookup;
- direct/hybrid state preserves the required query types in controlled fixtures;
- adaptive compute respects its maximum budget and allocates fewer samples to easier evidence regimes than harder ones;
- staged consolidation reduces durable churn from noisy observations but introduces delay after genuine state changes.

These are benchmark/instrumentation checks, **not architecture conclusions**.

## Current research status

No Phase-9 architecture family has been selected.

The organism exists to generate evidence for the unresolved design ledger. A result is promoted only after matched multi-seed/task/resource sweeps and a mechanism-specific failure/ablation test.

## Next implementation targets

1. **E01** — hierarchical versus distributed operation allocation;
2. **E02** — integrated versus heterogeneous computation;
3. **E04** — internal representation/interface format;
4. extend E09 so the consolidation threshold is learned/adapted to hidden environment volatility rather than hand-fixed;
5. add multi-seed sweep/result aggregation without adding runtime dependencies.

## Guardrail

Do not add a language model merely to make the organism look more like a modern AI system. Add learned models only when the active experiment requires a capability that cannot be meaningfully represented by controlled synthetic mechanisms.
