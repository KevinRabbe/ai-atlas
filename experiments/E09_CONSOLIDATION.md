# E09 — Immediate Durable Update vs Staged Consolidation

## Research question

When observations are noisy but the underlying environment sometimes genuinely changes, should new evidence immediately overwrite durable state or remain tentative until additional support accumulates?

This is the first direct experimental probe of the Atlas multi-timescale-learning hypothesis.

## Environment

The hidden state is binary and persists over time but changes regimes with configurable probability.

At each step the system receives a noisy observation of that state.

The policy does **not** receive a “real change happened” flag.

## Variants

### `immediate_durable`

Every observation becomes the new durable state immediately.

Expected strength: minimal adaptation delay after a true change.

Expected weakness: observation noise causes frequent durable churn.

### `staged_N`

An observation inconsistent with durable state is stored as temporary candidate evidence. Durable state changes only after `N` consecutive contradictory observations.

Expected strength: filters isolated noise.

Expected weakness: delays genuine regime changes and can fail when evidence is intermittent.

### `evidence_tX`

Contradictory observations accumulate temporary evidence; observations supporting the incumbent decay that evidence. Durable state flips only after an evidence threshold.

Expected strength: demonstrates a non-consecutive staged update policy.

Expected weakness: threshold/decay can be badly tuned to environment volatility/noise.

## Metrics

- `accuracy` — fraction of steps where durable state equals hidden true state;
- `actual_switches` — true environment regime changes;
- `durable_updates` — number of persistent state changes made by policy;
- `false_updates` — durable updates that end in the wrong hidden state;
- `avg_switch_delay` — delay from a true regime change until durable state catches up;
- `resolved_switches` — true changes for which adaptation was observed before the stream ended;
- logical reads/writes/operations.

## Run

```bash
cd experiments
python -m pip install -e .
python -m ai_atlas_lab.consolidation_cli --seed 7
```

Example parameter sweep dimensions:

```text
observation reliability: 0.60 .. 0.98
regime switch probability: 0.001 .. 0.10
staging confirmations: 2, 3, 5, 8
```

## Falsification logic

The claim is **not** “staging is better.”

The experiment is intended to find the crossover surface:

- as observation noise rises, immediate durable updates should become increasingly unstable;
- as real regime changes become frequent, high consolidation thresholds should become increasingly stale;
- a useful adaptive policy would need to infer this stability/volatility trade-off rather than rely on one permanent threshold.

If immediate updating dominates staged policies across noisy/nonstationary regimes after cost is included, the multi-timescale persistence hypothesis is weakened for this class of state.

If one fixed staging threshold dominates across all regimes, the need for learned/adaptive consolidation is weakened.

## Next extension

E09 should later hide the volatility/reliability regime and ask a policy to **learn the consolidation threshold itself**. That would connect this experiment to Phase-8 F21 change/substrate routing and F25 cross-resource metacontrol rather than only comparing hand-written thresholds.
