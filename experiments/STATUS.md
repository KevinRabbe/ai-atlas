# Phase 10 Experimental Status

**Checkpoint: Tier-1 implementation complete; five provisional design principles selected on 2026-08-14.**

## Implemented probes

Tier-1: E01 hierarchical vs distributed allocation; E02 integrated vs heterogeneous learned computation; E03 direct-address vs compressed state; E04 representation/interface; E05 fixed vs adaptive compute; E09 immediate vs staged consolidation.

Promotion/system follow-ups now include:

- `E01B_RESOURCE_CONTENTION` — second control-topology family with scarce shared verification capacity;
- `E02B_COMPOSITIONAL_INTEGRATION` — second integration family using compositional features and a partially shared candidate;
- `E03B_EVIDENCE_REVISION` — second memory family with source retractions/corrections and provenance queries;
- `E04B_SEARCH_STATE_REPRESENTATION` — second representation family with backtracking state, exact IDs, variable stack state and learned quantized scores;
- `E05B_VALUE_OF_SEARCH` — second adaptive-compute family with costly exact candidate evaluation;
- `E09B_ADAPTIVE_VOLATILITY` — adaptive consolidation threshold under hidden stable/volatile regimes;
- `E22_CROSS_RESOURCE_METACONTROL` — learned substitution among memory, compute, observation and verification under changing resource prices.

## Local validation added during this continuation

**36 newly added unit tests pass in local validation groups** across the new Tier-1/follow-up modules. Original baseline E03/E05/E09 source remains intact; follow-up modules reuse baseline policies where useful.

Multi-seed sweeps completed:

- E01/E02/E04: 12 seeds;
- E01B: 20 seeds × three verification-capacity regimes;
- E02B: 12 seeds × three relatedness regimes × three training-data budgets;
- E03B: 20 seeds × source-retraction regimes;
- E04B: 20 seeds × score-distribution shifts;
- E05B: 20 seeds × exact-evaluation cost regimes;
- E09B: 30 seeds across alternating hidden volatility regimes;
- E22: 30 seeds × three resource-price regimes after common warm-up.

## Replicated patterns

- **Control:** coordination cost/benefit follows coupling. Sparse dependencies reward local execution; broader dependencies and shared scarcity require arbitration at the scope of that coupling.
- **Integration:** two task families show a transfer/interference continuum. Shared state helps when structure is reusable and data scarce; isolation wins as task rules diverge; partial sharing can occupy the middle but must justify extra arithmetic.
- **Persistent state:** current-state compression is cheap when source history never matters again, but evidence retractions break unlinked compressed beliefs. Evidence-linked current state keeps current decisions cheap while preserving correction/provenance semantics.
- **Representation:** exact identity/control state, approximate numerical state, protocol/version metadata and audit/recovery have different fidelity/bandwidth requirements.
- **Inference compute:** two different task families show that useful inference effort moves with uncertainty/difficulty, task consequence and operation price; fixed maximum budgets are not efficient effort targets.
- **Persistence timescale:** hidden-volatility adaptation improves the stability/plasticity frontier.
- **Cross-resource metacontrol:** after resource prices change, adaptive allocation substitutes among memory, compute, observation and verification; frozen resource economics accumulates large regret.

## Provisional selections

The design ledger now contains five selections for the **current experimental generation**, not final architecture choices:

1. **PS-001 — typed hybrid boundary state.** Exact fields stay exact; tolerant numerical fields may use compact approximate/learned channels; version/integrity is explicit; human-readable audit need not occupy the hot path.
2. **PS-002 — staged adaptive persistence.** Evidence normally enters reversible state before globally durable mutation, and consolidation timescale/threshold may adapt to estimated environmental stability.
3. **PS-003 — coupling-scoped coordination.** Keep execution/local decisions local while coupling is local; introduce arbitration only where dependencies/shared scarcity actually couple decisions.
4. **PS-004 — derived current belief with evidence linkage.** Current belief is maintained cheaply for repeated use while remaining linked to source evidence where future correction/provenance has nonzero value.
5. **PS-005 — value-of-computation stopping.** Additional inference work is purchased only while estimated marginal downstream value exceeds current computation/latency/risk cost.

No A/B/C/D architecture family is selected; all five principles can be implemented by multiple families.

## Still unresolved

- **DL-002 cognitive integration:** two families support adaptive degree-of-sharing, but the most interesting partial E02B mechanism is not realized-compute matched.
- **DL-006/DL-007:** belief ambiguity and active information acquisition are the next Tier-2 state/action questions.
- **DL-022:** cross-resource adaptive substitution has only one system-level task family so far.

## Next targets

1. compute-matched conditional sharing for E02B;
2. E22B with simultaneous resource capacity contention and quality drift;
3. Tier-2 E06 multiple belief hypotheses and E07 active information acquisition;
4. E09B observation-noise vs true-volatility disentanglement and eventually learned consolidation control;
5. then assemble the next-generation research organism from the provisional constraints rather than from a named modern AI stack.

## Guardrail

During Phase 10 the measuring instrument must remain simpler than the hypotheses it measures, and every provisional selection remains reversible.