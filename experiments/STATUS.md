# Phase 10 Experimental Status

**Checkpoint: Tier-1 implementation complete; first provisional design principles selected on 2026-08-14.**

## Implemented probes

E01 hierarchical vs distributed allocation; E02 integrated vs heterogeneous learned computation; E03 direct-address vs compressed state; E04 representation/interface; E05 fixed vs adaptive compute; E09 immediate vs staged consolidation.

Promotion follow-ups now include:

- `E01B_RESOURCE_CONTENTION` — second control-topology family with scarce shared verification capacity;
- `E02B_COMPOSITIONAL_INTEGRATION` — second integration family using compositional features and a partially shared candidate;
- `E04B_SEARCH_STATE_REPRESENTATION` — second representation family with backtracking state, exact IDs, variable stack state and learned quantized scores;
- `E09B_ADAPTIVE_VOLATILITY` — adaptive consolidation threshold under hidden stable/volatile regimes.

## Local validation added during this continuation

**24 newly added unit tests pass in local validation groups**: 10 for E01/E02/E04, 2 for E01B, 4 for E02B, 4 for E04B and 4 for E09B. The original E03/E05/E09 baseline source remained untouched except that E09B imports the existing fixed-threshold policy as a reference.

Multi-seed sweeps completed:

- E01/E02/E04: 12 seeds;
- E01B: 20 seeds × three verification-capacity regimes;
- E02B: 12 seeds × three relatedness regimes × three training-data budgets;
- E04B: 20 seeds × score-distribution shifts;
- E09B: 30 seeds across alternating hidden volatility regimes.

## Replicated patterns

- **Control:** coordination cost/benefit follows coupling. Sparse dependencies reward local execution; deeper dependencies require broader message propagation; scarce shared resources require arbitration, but resource-local arbitration can match a global allocator without becoming a universal executive.
- **Integration:** two task families now show a transfer/interference continuum. Shared state helps when structure is genuinely reusable and data are scarce; isolation wins as task rules diverge; partial sharing can occupy the middle but must still justify extra arithmetic.
- **Representation:** two families show that exact identity/control state, approximate numerical state, protocol/version metadata and audit/recovery have different fidelity/bandwidth requirements. A learned quantized score channel plus exact side state reached ~27 bytes/message and ~0.99 search-decision accuracy while preserving exact structural state.
- **Persistence:** hidden-volatility adaptation improves the stability/plasticity frontier. The adaptive E09B policy reached ~0.968 accuracy with ~4.2 false durable updates versus ~18.1 for the similarly accurate aggressive fixed policy and changed its threshold without access to hidden regime labels.

## First provisional selections

The design ledger now contains two selections for the **current experimental generation**, not final architecture choices:

1. **PS-001 / DL-004 — typed hybrid boundary state.** Exact fields stay exact; tolerant numerical fields may use compact approximate/learned channels; version/integrity semantics are explicit; human-readable audit need not occupy the hot path.
2. **PS-002 / DL-009 — staged adaptive persistence.** New evidence normally enters reversible state before globally durable mutation, and the consolidation lifetime/threshold may adapt to estimated environmental stability.

No A/B/C/D architecture family is selected; both principles are compatible with several families.

## Still unresolved

- DL-001 control topology: two task families support adaptive coordination scope, but E22 cross-resource metacontrol remains the decisive test.
- DL-002 integration: two families support adaptive degree-of-sharing, but the most interesting partial E02B mechanism is not yet compute-matched.
- DL-003 history/current-state balance and DL-005 inference budget still require promotion-quality replication.

## Next targets

1. E22 cross-resource metacontrol across changing compute/memory/observation/verification prices;
2. compute-matched conditional sharing for E02B;
3. aggregate/shift E03 and E05 to the same promotion standard;
4. E09B reliability-vs-volatility disentanglement and eventually learned consolidation control;
5. Tier-2 E06 multiple belief hypotheses and E07 active information acquisition.

## Guardrail

During Phase 10 the measuring instrument must remain simpler than the hypotheses it measures, and provisional selections remain reversible research constraints.