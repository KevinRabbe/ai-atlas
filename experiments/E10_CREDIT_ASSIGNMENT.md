# E10 — Delayed Credit Assignment: Global History vs Local Eligibility

**Status: first family implemented; 5/5 replicated semantic tests pass; 30-seed sweep complete. DL-010 remains unresolved pending a second structurally different family.**

## Question

When a long multi-stage task fails only at the end, must the full trajectory remain globally available for credit assignment, or can local evidence/eligibility preserve enough causal information to learn with less false blame and retained state?

This experiment was motivated by both the Foundations credit-assignment pass and the biology pass on local eligibility plus delayed global teaching signals.

## Environment

Each episode has:

- one of three contexts;
- nine sequential stages;
- a hidden correct binary action at each stage;
- a noisy local diagnostic at each stage (`0.78` reliable by default);
- one delayed final success bit that is true **only if all nine stage choices are correct**.

The nine-stage default is deliberate. A five-stage dry run showed that final success remained frequent enough for blunt global credit to learn nearly as well. Increasing compositional depth makes the final reward sparse enough that a single failure creates genuine credit ambiguity.

## Policies

### 1. Global trajectory credit

Retain every stage action until the final result.

- final success → reinforce every chosen stage action;
- final failure → blame every chosen stage action.

This is deliberately simple and exposes the classic diffusion problem: one bad stage causes correct stages to receive negative credit too.

### 2. Local diagnostic credit

Update each stage immediately from its noisy local diagnostic.

No delayed trajectory state is retained.

This can miss/blame stages when local evidence is wrong, but a final failure does not indiscriminately punish unrelated correct stages.

### 3. Eligibility hybrid

- positive local diagnostic → learn immediately;
- suspicious/negative local diagnostic → retain only that stage's compact eligibility item;
- when the delayed final outcome arrives, use it to resolve the retained suspicious stages.

Thus the global signal modulates **locally selected eligibility** rather than being broadcast as identical blame to the entire trajectory.

## Validation

`5/5` replicated semantic tests pass:

- global final-only credit false-blames correct stages on partial failures;
- local credit requires no delayed full-trajectory storage;
- local/factorized learning strongly beats sparse global credit in the nine-stage regime;
- eligibility retains fewer delayed items than full history;
- the advantage of local evidence shrinks as the local diagnostic becomes less informative.

## 30-seed default result

| policy | overall success | tail success | false blame/episode | missed blame/episode | delayed retained items/episode |
|---|---:|---:|---:|---:|---:|
| global trajectory | 0.153 | **0.189** | **4.038** | 0.000 | **9.000** |
| local diagnostics | 0.687 | **0.692** | 1.898 | 0.082 | **0.000** |
| eligibility hybrid | **0.689** | **0.692** | **0.537** | 0.082 | **2.186** |

All three perform nine parameter updates/episode; the difference is **where the credit signal comes from and how much delayed state is required**.

## Stage-count boundary

The first dry run matters because it prevents overclaiming.

Approximate 10-seed tail-success behavior:

| stages | global trajectory | local diagnostic | eligibility hybrid |
|---:|---:|---:|---:|
| 5 | 0.811 | 0.811 | 0.811 |
| 7 | 0.524 | 0.751 | 0.751 |
| 9 | 0.141 | 0.695 | 0.695 |
| 12 | 0.021 | 0.608 | 0.608 |

The factorized advantage appears as **global outcome ambiguity grows**. There is no claim that local credit universally dominates when final outcomes already identify responsible decisions well.

## Interpretation

### Global reward is not the same thing as global credit

A delayed final outcome can remain globally meaningful without assigning identical credit to every earlier state transition.

The experiment supports a decomposition:

`local event -> local eligibility/evidence -> delayed outcome -> selective/factorized update`

rather than:

`delayed outcome -> update everything in the trajectory equally`.

### Credit memory can be sparse

The hybrid retains only ~2.19 suspicious stages on average rather than all 9. This suggests that persistent trajectory state for learning may be selected by **credit relevance**, not by chronology alone.

### Local evidence quality is a first-class variable

Local factorization only helps when local diagnostics contain useful information. When those signals approach noise, the advantage shrinks. The architecture therefore still needs a way to estimate which local checks are informative and when broader/global attribution is worth its cost.

## Why DL-010 is not promoted yet

This is one task family: a serial all-stages-required pipeline with noisy local diagnostics.

Before selecting a credit architecture, a second family should differ structurally, for example:

- sparse causal responsibility where only a subset of invoked tools affects the outcome;
- branching workflows with optional/skipped stages;
- multi-agent work where final reward is shared but local contributions overlap;
- continuous/additive outcomes rather than all-or-none success.

The second family should compare lifetime utility, retained trajectory state, update communication and attribution errors under matched feedback budgets.

## Current provisional lesson

> **Credit assignment does not require identical global propagation merely because the outcome is delayed. Local eligibility can preserve causal specificity and let a later global signal modulate only the state transitions that remain plausibly responsible.**

This remains evidence, not yet PS-level selection.
