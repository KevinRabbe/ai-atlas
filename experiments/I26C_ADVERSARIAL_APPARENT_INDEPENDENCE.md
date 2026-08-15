# I26C — Adversarial Apparent Independence

**Status:** implemented PS-026 falsifier/refinement. No new provisional principle.

## Question

I24/I25 learn evidence dependence from resolved co-failure. I26A scopes that relation by domain. I26B adds directional derivation.

A harder failure remains:

> **What if correlated sources look independent on the distribution where outcomes are observable, then route through a shared failure path specifically on rare consequential frontier cases?**

This is not ordinary noise. It is selective distribution shift / adversarial apparent independence.

## Environment

Three visible sources:

- B and C: the pair under dependence uncertainty;
- D: genuinely independent comparator.

### Ordinary resolved tasks

B/C have independent 10% errors. These are the tasks from which passive dependence learning receives outcome feedback.

### Frontier tasks

8% of tasks are high-consequence frontier cases. Here B/C route through one hidden shared failure mechanism and fail together with probability 38%.

These frontier outcomes are **not** available to the passive dependence learner during the experiment. The stress intentionally models new/unresolved frontier work where historical evaluation data do not cover the failure mode.

D remains independently wrong with probability 12% in both regimes.

Consequences:

- ordinary task: 1 or 2;
- frontier task: 8.

## Policies

### `record_count`

Counts B/C/D as three independent votes.

### `passive_history`

Learns B/C dependence only from resolved ordinary history. Because B/C are genuinely independent there, the learned residual dependence score stays near zero.

### `always_dependent`

Collapses B/C everywhere. This protects frontier cases but destroys useful ordinary diversity.

### `stress_probe`

Uses ordinary independence by default. On a frontier case, a bounded provenance/perturbation diagnostic can establish that B/C share the consequential frontier failure path for a limited lifetime.

The probe is purchased only when a configured expected frontier-dependence risk × consequence × expected covered frontier work exceeds probe cost.

### `oracle`

Knows B/C are independent ordinarily and shared on the frontier.

## Approximate 30-seed result

12,000 tasks/seed:

| policy | utility/task | weighted harm/task | ordinary error | frontier error | dependency probes/task |
|---|---:|---:|---:|---:|---:|
| record count | ~0.858 | ~0.291 | ~0.0315 | ~0.384 | 0 |
| passive history | ~0.858 | ~0.291 | ~0.0315 | ~0.384 | 0 |
| always dependent | ~1.040 | ~0.246 | ~0.120 | ~0.124 | 0 |
| **frontier stress probe** | **~1.524** | **~0.124** | **~0.0315** | **~0.124** | ~0.0108 |
| oracle | ~1.529 | ~0.124 | ~0.0315 | ~0.124 | 0 |

The passive resolved-history B/C dependence score remains approximately zero (`~0.0004` in the prototype), which is correct for the observed ordinary distribution and dangerously incomplete for the frontier distribution.

## Why the conservative baseline is necessary

The benchmark deliberately includes `always_dependent`.

Without it, stress probing could look like a generic argument for more skepticism.

But universal dependence loses ordinary ensemble value:

```text
ordinary independent B/C
        ↓
collapse anyway
        ↓
ordinary error ~3.2% -> ~12%
```

The useful mechanism is **scoped dependence discovery**, not blanket source collapse.

## What this adds to PS-026

Observational absence of dependence is always relative to:

- the distribution observed;
- the outcomes that were resolved;
- the contexts where feedback existed;
- the failure modes that were activated.

So PS-026 must distinguish:

```text
observed independence
        !=
structural/provenance independence
        !=
independence under future distribution shift
```

When consequence is high and historical coverage is weak, explicit provenance/interventional stress evidence can have value even if ordinary co-failure statistics look clean.

## Probe economics

The stress probe is not mandatory.

Its current policy uses an explicit estimated frontier-dependence risk and the expected number of consequential decisions covered by the probe TTL. Raising probe cost high enough causes the policy to stop buying the diagnostic.

This preserves the Atlas resource rule: uncertainty does not automatically justify measurement.

## Architecture consequence

`EvidenceDependenceModel` remains useful for learned observational relation state, but it should not be treated as proof of structural independence.

The assurance layer may consume several evidence types about dependence:

```text
resolved behavioral co-failure
context-conditioned residual dependence
directional derivation evidence
explicit provenance
controlled/stress intervention
coverage / distribution-shift uncertainty
```

Their failure modes are themselves different.

## Remaining I26 stress

The next question is computational:

> **What happens when the evidence-source population becomes large and independently resolved feedback becomes sparse?**

A dense pairwise O(N²) relation model may become more expensive than the assurance harm it prevents. I26D should compare dense pairwise state against sparse/hierarchical/common-factor alternatives and active pair selection.
