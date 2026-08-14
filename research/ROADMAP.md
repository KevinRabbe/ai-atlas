# Research Roadmap

## Phases 0–7

Taxonomy/evidence discipline, computational substrate, learning/adaptation, inference-time intelligence, persistent intelligence, verification/control, self-improvement and first cross-domain synthesis all completed first passes on 2026-08-14. All remain open for targeted gap closure.

A later focused synthesis pass added **discovery & epistemic growth**: human knowledge is treated as bootstrap evidence/methodology rather than a permanent epistemic ceiling; F26 now captures the requirement to turn uncertainty into testable hypotheses and verified new knowledge.

## Phase 8 — Forget implementations

First-pass clean-sheet functional reconstruction completed on 2026-08-14. **Exit gate: PASS.** Produced standalone problem/state semantics, capability contracts, resource model, invariants, assurance/change protocol, unresolved choices, traceability and an explicit exit audit.

## Phase 9 — Clean-sheet architecture

**First-pass candidate generation completed on 2026-08-14. Exit gate: PASS. No architecture family selected.** Four organization families remain active: hierarchical explicit allocation; distributed event-driven local control; tightly integrated predictive computation with external evidence/authority; developmental/variant-generating organization.

## Phase 10 — Experimental reconstruction

**Active. Five provisional design-principle selections reached on 2026-08-14.**

All Tier-1 discriminator shapes are implemented, with promotion follow-ups E01B/E02B/E03B/E04B/E05B/E09B plus E22 cross-resource metacontrol.

## Current provisional selections

These are reversible **principles for the current experimental generation**, not concrete modules and not a selected Phase-9 architecture family.

1. **PS-001 / DL-004 — typed hybrid boundary state.** Exact identity/control/provenance stays exact; tolerant numerical state may use compact approximate/learned channels; version/integrity remains explicit.
2. **PS-002 / DL-009 — staged adaptive persistence.** New evidence normally enters reversible/tentative state before globally durable mutation, with lifetime/threshold adapting to estimated stability.
3. **PS-003 / DL-001 — coupling-scoped coordination.** Local decisions stay local while coupling is local; arbitration expands only to the scope of shared dependency/scarcity.
4. **PS-004 / DL-003 — derived current belief with evidence linkage.** Current belief is maintained cheaply for repeated use while source evidence remains separately linked where future correction/provenance has value.
5. **PS-005 / DL-005 — value-of-computation stopping.** Additional inference work is spent only while expected marginal downstream value exceeds current resource/latency/risk cost.

## Discovery / epistemic-growth extension

The focused synthesis `synthesis/DISCOVERY_AND_EPISTEMIC_GROWTH.md` adds a new long-horizon target:

> the system should be able to expand the verified knowledge frontier rather than merely answer from a frozen human/bootstrap corpus.

The required epistemic lifecycle is provisionally:

`inherited knowledge -> hypothesis -> candidate discovery -> scoped verification -> independent/hidden checking or replication -> consolidated knowledge`.

Novelty alone is never treated as truth. Failed hypotheses/negative results may themselves be valuable retained information.

This adds:

- **F26 — epistemic frontier expansion / discovery** to the implementation-neutral required functions;
- `sources/DISCOVERY_EPISTEMIC_GROWTH.md` as the primary-source registry;
- **E23 — weak-teacher / independent-evaluator discovery loop** as a specified Phase-10 experiment, not yet implemented.

E23 first tests the mechanics of exceeding a deliberately suboptimal teacher frontier in a controlled world. A later real-discovery claim would require an externally verified result that was not already known to the relevant human field.

## Evidence behind the latest two selections

### PS-004

Original E03 established the direct-address/current-state trade-off. E03B then added exact source retractions and provenance queries. Compressed-only state remains perfect when there are no corrections, but its current accuracy falls to roughly 0.88 / 0.79 / 0.68 as source-retraction probability rises to 5% / 15% / 30%. Raw evidence replay remains exact but costs roughly 600 reads per query. Evidence-linked current state remains exact at approximately 1–2 reads/query while retaining source provenance.

### PS-005

Original E05 showed confidence-conditioned evidence sampling. E05B uses a different problem: costly exact evaluation of heuristic-ranked candidate solutions. Across exact-evaluation costs 0.02 / 0.08 / 0.25 / 0.60, the adaptive policy uses about 1.68 / 1.62 / 1.48 / 1.31 evaluations and matches or exceeds the best tested fixed-budget net utility. It also allocates more work to ambiguous and higher-value tasks.

## Highest-value unresolved decisions

- **DL-002 cognitive integration:** two task families favor adaptive degree of sharing, but partial sharing still has unmatched realized compute; compute-matched conditional sharing is required.
- **DL-006 belief ambiguity:** one state versus multiple hypotheses under partial observability remains open and is now also a prerequisite for robust discovery.
- **DL-007 active information acquisition:** when to act specifically to gain information remains open and becomes central for empirical discovery.
- **DL-022 cross-resource metacontrol:** E22 strongly favors adaptive substitution but requires a second family with shared capacity/quality drift before selection.
- **F26 discovery:** beyond-teacher search, hidden evaluation, negative-result retention and knowledge promotion are specified but not yet experimentally reconstructed.

## Near-term order

1. compute-matched/conditional E02B sharing;
2. E22B with simultaneous capacity contention + resource-quality drift;
3. Tier-2 E06/E07, because multi-hypothesis state and active evidence acquisition are prerequisites for empirical discovery;
4. implement E23 first synthetic discovery loop and test teacher ceiling / evaluator exploitation / archive / knowledge-promotion ablations;
5. E09B observation-noise versus true-volatility disentanglement;
6. then construct a next-generation research organism constrained by PS-001 through PS-005 plus whatever survives E06/E07/E23, rather than by any named existing AI architecture.

Phase 10 is **not complete**. The current goal is to resolve the remaining architecture-boundary questions and experimentally reconstruct the machinery required for both intelligent action and verified epistemic growth.

## Open targeted gap closure

Add new literature when it materially changes an active experimental/design decision, not simply to maximize source count.
