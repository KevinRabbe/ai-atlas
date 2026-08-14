# Phase 10 Experimental Status

**Checkpoint: Tier-1 implementation complete; three provisional design principles selected on 2026-08-14.**

## Implemented probes

Tier-1: E01 hierarchical vs distributed allocation; E02 integrated vs heterogeneous learned computation; E03 direct-address vs compressed state; E04 representation/interface; E05 fixed vs adaptive compute; E09 immediate vs staged consolidation.

Promotion/system follow-ups now include:

- `E01B_RESOURCE_CONTENTION` — second control-topology family with scarce shared verification capacity;
- `E02B_COMPOSITIONAL_INTEGRATION` — second integration family using compositional features and a partially shared candidate;
- `E04B_SEARCH_STATE_REPRESENTATION` — second representation family with backtracking state, exact IDs, variable stack state and learned quantized scores;
- `E09B_ADAPTIVE_VOLATILITY` — adaptive consolidation threshold under hidden stable/volatile regimes;
- `E22_CROSS_RESOURCE_METACONTROL` — learned substitution among memory, compute, observation and verification under changing resource prices.

## Local validation added during this continuation

**28 newly added unit tests pass in local validation groups**: 10 for E01/E02/E04, 2 for E01B, 4 for E02B, 4 for E04B, 4 for E09B and 4 for E22. Original baseline E03/E05/E09 source remains intact; follow-up modules reuse baseline policies where useful.

Multi-seed sweeps completed:

- E01/E02/E04: 12 seeds;
- E01B: 20 seeds × three verification-capacity regimes;
- E02B: 12 seeds × three relatedness regimes × three training-data budgets;
- E04B: 20 seeds × score-distribution shifts;
- E09B: 30 seeds across alternating hidden volatility regimes;
- E22: 30 seeds × three resource-price regimes after common warm-up.

## Replicated patterns

- **Control:** coordination cost/benefit follows coupling. Sparse dependencies reward local execution; deeper dependencies require broader propagation; scarce shared resources require arbitration, but resource-local arbitration can match global allocation without becoming a universal executive.
- **Integration:** two task families show a transfer/interference continuum. Shared state helps when structure is reusable and data scarce; isolation wins as task rules diverge; partial sharing can occupy the middle but must justify extra arithmetic.
- **Representation:** two families show that exact identity/control state, approximate numerical state, protocol/version metadata and audit/recovery have different fidelity/bandwidth requirements. A learned quantized score channel plus exact side state uses ~27 bytes/message and retains ~99% search-decision correctness while preserving exact structural state.
- **Persistence:** hidden-volatility adaptation improves the stability/plasticity frontier. E09B reaches ~0.968 accuracy with ~4.2 false durable updates versus ~18.1 for the similarly accurate aggressive fixed policy, while changing its threshold without hidden regime labels.
- **Cross-resource metacontrol:** after resource prices change, E22 shifts from memory/compute toward observation and later verification. Mean post-shift regret is ~0.032 for adaptive allocation versus ~0.505 for frozen resource economics. Resource-local bidding matches the adaptive choices but adds explicit message overhead.

## Provisional selections

The design ledger now contains three selections for the **current experimental generation**, not final architecture choices:

1. **PS-001 / DL-004 — typed hybrid boundary state.** Exact fields stay exact; tolerant numerical fields may use compact approximate/learned channels; version/integrity is explicit; human-readable audit need not occupy the hot path.
2. **PS-002 / DL-009 — staged adaptive persistence.** Evidence normally enters reversible state before globally durable mutation, and consolidation timescale/threshold may adapt to estimated environmental stability.
3. **PS-003 / DL-001 — coupling-scoped coordination.** Local execution stays local when interaction is local; explicit resource/domain/global arbitration appears only at the scope where dependencies or shared scarcity couple decisions.

No A/B/C/D architecture family is selected; all three principles can be implemented by multiple families.

## Still unresolved

- **DL-002 integration:** two families support adaptive degree-of-sharing, but the most interesting partial E02B mechanism is not realized-compute matched.
- **DL-003 evidence/current-state balance:** E03 needs a second family/resource shift.
- **DL-005 inference budget:** E05 needs OOD cost shifts and a second problem family.
- **DL-022 cross-resource metacontrol:** E22 strongly favors adaptive substitution over frozen independent economics, but only one cross-resource task family exists so far.

## Next targets

1. compute-matched conditional sharing for E02B;
2. promotion-quality E03 and E05 replications;
3. second E22 family with simultaneous resource capacity contention and quality drift;
4. E09B observation-noise vs true-volatility disentanglement and eventually learned consolidation control;
5. Tier-2 E06 multiple belief hypotheses and E07 active information acquisition.

## Guardrail

During Phase 10 the measuring instrument must remain simpler than the hypotheses it measures, and every provisional selection remains reversible.