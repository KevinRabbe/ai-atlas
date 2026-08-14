# Phase 9 Exit Check — Candidate Architecture Generation

**Result: PASS for first-pass candidate generation.**

Phase 9 does not require selecting a final architecture. It requires multiple coherent candidates and experiments precise enough to make architecture decisions empirical.

## Criterion 1 — Multiple coherent organizations exist

**PASS.** Four architecture families are retained:

- hierarchical explicit allocation;
- distributed event-driven local control;
- tightly integrated predictive computation with external evidence/authority;
- developmental/variant-generating organization.

They differ on substantive Phase-8 choices rather than cosmetic implementation details.

## Criterion 2 — All candidates derive from the same specification

**PASS.** Each candidate maps to the same state/invariant/resource contracts and differs mainly in how those functions are grouped and controlled.

## Criterion 3 — Candidate-specific failure hypotheses are explicit

**PASS.** Every candidate documents expected bottlenecks and conditions that would falsify its central hypothesis.

## Criterion 4 — No architecture wins by unmatched scale

**PASS.** The comparison requires matched compute, persistent state, interaction, assurance and hardware budgets where practical.

## Criterion 5 — Unresolved decisions remain in the design ledger

**PASS.** `DESIGN_LEDGER.md` records 22 decisions as unresolved or principle-constrained rather than silently selecting a favorite.

## Criterion 6 — Discriminating experiments are specified

**PASS.** `EXPERIMENT_MATRIX.md` defines 22 architecture experiments with variables, controls, metrics and candidate falsifiers.

## Criterion 7 — There is a minimal experiment order

**PASS.** Tier 1 isolates six core dimensions before persistent/action/control/self-improvement complexity is added:

1. direct-address versus compressed state;
2. adaptive computation;
3. hierarchical versus distributed allocation;
4. integrated versus heterogeneous computation;
5. internal representation;
6. persistence/consolidation timescale.

## Criterion 8 — Hybridization is delayed until evidence

**PASS.** Phase-9 comparison forbids combining every candidate strength preemptively. A hybrid mechanism must address a measured failure and survive ablation/resource comparison.

## Criterion 9 — The next artifact can be small

**PASS.** The experiment matrix allows Phase 10 to build one instrumented organism with replaceable policies/state mechanisms instead of four separate production systems.

## Gate decision

**Phase 9 exit condition is satisfied to first-pass depth. Phase 10 experimental reconstruction may begin.**

No architecture family is selected. Phase 10 exists specifically to turn the unresolved design ledger into measurements.
