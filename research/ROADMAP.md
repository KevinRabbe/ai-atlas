# Research Roadmap

## Phases 0–7

Taxonomy/evidence discipline, computational substrate, learning/adaptation, inference-time intelligence, persistent intelligence, verification/control, self-improvement and first cross-domain synthesis all completed first passes on 2026-08-14. All remain open for targeted gap closure.

A later focused synthesis pass added **discovery & epistemic growth**: human knowledge is treated as bootstrap evidence/methodology rather than a permanent epistemic ceiling; F26 captures the requirement to turn uncertainty into testable hypotheses and verified new knowledge.

## Phase 8 — Forget implementations

First-pass clean-sheet functional reconstruction completed on 2026-08-14. **Exit gate: PASS.** Produced standalone problem/state semantics, capability contracts, resource model, invariants, assurance/change protocol, unresolved choices, traceability and an explicit exit audit.

## Phase 9 — Clean-sheet architecture

**First-pass candidate generation completed on 2026-08-14. Exit gate: PASS. No architecture family selected.** Four organization families remain active: hierarchical explicit allocation; distributed event-driven local control; tightly integrated predictive computation with external evidence/authority; developmental/variant-generating organization.

## Phase 10 — Experimental reconstruction

**Active. Tier-1 is complete to promotion depth and the first Tier-2 epistemic/action block is implemented. Eight provisional design principles have now been selected for the current experimental generation.**

### Current provisional selections

1. **PS-001 / DL-004 — typed hybrid boundary state.**
2. **PS-002 / DL-009 — staged adaptive persistence.**
3. **PS-003 / DL-001 — coupling-scoped coordination.**
4. **PS-004 / DL-003 — derived current belief with evidence linkage.**
5. **PS-005 / DL-005 — value-of-computation stopping.**
6. **PS-006 / DL-006 — consequence-sensitive hypothesis plurality.**
7. **PS-007 / DL-007 — value-driven active evidence acquisition.**
8. **PS-008 / DL-023 — verified epistemic frontier expansion.**

These are reversible implementation-neutral constraints, not concrete modules and not a selected Phase-9 architecture family.

## Tier-2 epistemic/action checkpoint

### E06 — multiple hypotheses

A noisy four-world family shows that forcing one maximum-posterior world is costly under ambiguous evidence and high wrong-commitment cost. Preserving several plausible worlds plus a safe action strongly improves utility in that regime; the advantage narrows as observations become decisive.

A structurally different causal ablation gives both systems the same intervention. Forced single-theory commitment is preferable when a false theory is cheap, while preserving an unresolved theory set becomes preferable as false-claim consequence rises. The selected principle is therefore adaptive plurality, not permanent multi-hypothesis expansion.

### E07 — active evidence acquisition

A noisy-probe family compares passive sensing, a fixed query schedule, one-step value-of-information and bounded two-step value-of-information.

The first implementation exposed a useful failure: one-step VOI can reject an observation whose standalone value is small even when it enables a highly valuable second observation. The final experiment therefore keeps the myopic controller as an explicit ablation.

Across probe-cost shifts, bounded lookahead transitions from full acquisition to selective acquisition to zero acquisition. This supports treating observation/experiment as a resource-priced operation rather than free context.

### E23B — causal empirical discovery

Three candidate causal theories are indistinguishable under inherited/passive evidence. Active interventions provide new information unavailable from the teacher corpus.

At low/moderate experiment cost the active hypothesis system identifies the hidden theory exactly and exceeds the passive teacher frontier. At high experiment cost it performs no intervention and leaves the theory unresolved rather than inventing an answer.

Together with E23's constructive search family, this provides two structurally different demonstrations of the mechanics behind PS-008:

- constructive search can find verified results beyond demonstrated solutions;
- empirical interaction can acquire genuinely missing evidence beyond the bootstrap corpus.

This remains synthetic evidence. It is not a claim that the organism has produced new human knowledge.

## Discovery / epistemic-growth lifecycle

The current implementation-neutral target is:

`inherited knowledge -> competing hypothesis -> selected search/experiment -> candidate discovery -> scoped verification -> independent evidence/replication -> consolidated knowledge`.

Rejected/unresolved hypotheses retain distinct state when the negative result has future value.

The central discipline remains:

> **novelty is not knowledge.**

Search power should co-scale with verifier independence and epistemic staging.

## Highest-value unresolved decisions

- **DL-002 cognitive integration:** two families favor adaptive degree of sharing, but partial sharing still has unmatched realized compute; compute-matched conditional sharing is required.
- **DL-008 predictive-state breadth:** broad reconstruction versus decision-sufficient predictive state remains open.
- **DL-011 memory retrieval objective:** similarity versus temporal/causal/downstream-value retrieval remains open experimentally.
- **DL-022 cross-resource metacontrol:** E22 strongly favors adaptive substitution but requires a second family with shared capacity and resource-quality drift.
- **E09B noise-versus-volatility:** the current adaptive persistence policy still needs a test that independently varies sensor noise and true environmental change.

## Near-term order

1. compute-matched/conditional E02B sharing;
2. E22B with simultaneous capacity contention + resource-quality drift;
3. E08 predictive-state breadth and objective-switch robustness;
4. E11 retrieval by downstream decision value;
5. E09B observation-noise versus true-volatility disentanglement;
6. then construct a next-generation integrated research organism constrained by PS-001 through PS-008 and test interaction regressions under matched lifetime resources.

Phase 10 is **not complete**. The project now has enough experimentally supported state/control/epistemic constraints to begin asking whether they compose cleanly, but several architecture-boundary and system-level allocation questions remain unresolved.

## Open targeted gap closure

Add new literature when it materially changes an active experimental/design decision, not simply to maximize source count.
