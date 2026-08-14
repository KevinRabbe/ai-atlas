# AF01 — First Matched Architecture-Family Comparison

**Status:** implemented first family-level discriminator. **No A/B/C/D family is eliminated or selected from AF01 alone.**

## Goal

After I06, the Atlas has enough common runtime machinery to compare organization without quietly giving one architecture better memory, precision, source access or resource budgets.

AF01 therefore fixes the I06 task semantics and optional runtime operations, then changes only the organizational bias:

- **A — Hierarchical Adaptive System:** conditional/local estimates, globally joint central arbitration;
- **B — Distributed Event-Driven Ecology:** conditional/local estimates, local best-bundle bids and resource-local auction;
- **C — Integrated Predictive Core + External Evidence:** globally pooled experience and joint allocation, deliberately accepting a shared-core interference risk;
- **D — Developmental Variant System:** two preserved conditional runtime models with online predictive-loss selection and archive maintenance cost.

These are canonical stress embodiments, not claims that every future implementation of A/B/C/D must use these exact mechanisms.

## Matched substrate

All families receive the same:

- task stream and outcome draws;
- I06 operation bundles;
- success/error model;
- task value and consequence distribution;
- shared operation capacity;
- source-rematerialization, synchronization, fidelity and intervention semantics.

No family receives the hidden regime bit.

Organization-specific overhead is explicit and priced. The absolute synthetic prices are not treated as real hardware measurements, so AF01 also includes an overhead-price sensitivity check.

## Stress regimes

### Sparse stationary

Higher capacity, mostly local/decision/latent work and no regime recurrence. This should reward cheap local organization and penalize unnecessary central/archive overhead.

### Coupled switching

Tighter shared capacity, many consistency-coupled tasks and repeated hidden regime changes. This stresses global scarcity handling and adaptation.

### Recurring mixed

Balanced task mixture with recurring regimes. This gives shared generalization and preserved variants both a chance to earn their costs.

## Eight-seed means

### Sparse stationary

| family | utility/task | error rate | control messages/task | explicit overhead/task |
|---|---:|---:|---:|---:|
| A hierarchy | 1.6033 | **0.0879** | 2.0000 | 0.0360 |
| B distributed | 1.5991 | 0.0947 | **0.7721** | **0.0022** |
| C integrated | 1.5614 | 0.0952 | **0.0000** | **0.0000** |
| D developmental | **1.6098** | 0.0887 | **0.0000** | 0.0240 |

The sparse case does not produce a clean winner. A has the lowest error; B cuts explicit coordination overhead/message traffic dramatically; D gets slightly higher utility while paying archive maintenance; C is cheapest organizationally but loses from pooling family-specific evidence.

### Coupled switching

| family | utility/task | error rate | control messages/task | explicit overhead/task | archive switches/run |
|---|---:|---:|---:|---:|---:|
| A hierarchy | 1.3683 | 0.1409 | 2.0000 | 0.0360 | 0.000 |
| B distributed | 1.3704 | 0.1421 | 1.1086 | 0.0040 | 0.000 |
| C integrated | 1.3896 | 0.1467 | **0.0000** | **0.0000** | 0.000 |
| **D developmental** | **1.4435** | **0.1257** | **0.0000** | 0.0242 | 2.375 |

Preserved variants earn their maintenance cost in this regime: the developmental embodiment detects that its active model has become a worse predictor, switches, and later reuses alternatives rather than overwriting one incumbent repeatedly.

### Recurring mixed

| family | utility/task | error rate | control messages/task | explicit overhead/task | archive switches/run |
|---|---:|---:|---:|---:|---:|
| A hierarchy | 1.3953 | 0.1241 | 2.0000 | 0.0360 | 0.000 |
| B distributed | 1.3806 | 0.1275 | 1.0032 | 0.0029 | 0.000 |
| **C integrated** | **1.4797** | 0.1196 | **0.0000** | **0.0000** | 0.000 |
| D developmental | 1.4367 | **0.1168** | **0.0000** | 0.0244 | 3.750 |

Here the pooled core's sharing/generalization benefit outweighs its interference. D remains slightly safer but pays maintenance/selection cost.

## Organizational-price sensitivity

Because central coordination and archive maintenance prices are synthetic, AF01 repeated the sparse and recurring scenarios with all organization-specific overhead prices scaled together by `0.5x`, `1x` and `2x`.

Three-seed utility means:

### Sparse stationary

| overhead scale | A | B | C | D |
|---:|---:|---:|---:|---:|
| 0.5x | **1.5989** | 1.5765 | 1.5102 | 1.5902 |
| 1.0x | **1.5809** | 1.5754 | 1.5102 | 1.5782 |
| 2.0x | 1.5449 | **1.5732** | 1.5102 | 1.5542 |

The ranking changes as coordination becomes expensive. That is evidence against declaring a fixed central/distributed winner from one arbitrary price point.

### Recurring mixed

| overhead scale | A | B | C | D |
|---:|---:|---:|---:|---:|
| 0.5x | 1.3553 | 1.3058 | **1.4356** | 1.4152 |
| 1.0x | 1.3373 | 1.3043 | **1.4356** | 1.4030 |
| 2.0x | 1.3013 | 1.3014 | **1.4356** | 1.3786 |

C's advantage in this specific recurring mixed family is robust to the tested organization-cost scale, but AF01 is still only one representation of integrated pooling.

## Interpretation

AF01 does **not** support selecting one Phase-9 family.

Instead it reproduces the clean-sheet laws at architecture scale:

- hierarchy earns itself when global scarcity/coupling is worth central arbitration;
- distribution earns itself when locality makes coordination overhead avoidable;
- integration earns itself when shared structure/generalization exceeds interference;
- developmental variants earn themselves when recurrence/stepping-stone option value exceeds archive cost.

This is exactly the pattern predicted by PS-003, PS-009, PS-010, PS-019, PS-021 and PS-022.

The architecture-family labels are therefore beginning to look less like mutually exclusive final designs and more like **organizational modes that may each be useful in different regions of one adaptive system**.

## Why no family is eliminated yet

A family should not be removed merely because another family has better scalar utility in one scenario. AF01 exposes genuine different costs:

- A: central message/arbitration burden;
- B: weaker global bundle reconsideration under contention;
- C: interference from pooling heterogeneous evidence;
- D: archive/selector maintenance and switch cost.

No one of those costs is universally largest under the current matched regimes.

## Next discriminator — AF02

AF02 should attack the frontier instead of repeating AF01:

1. make dependency/coupling structure partially hidden and changing, so the system must infer whether hierarchy/distribution is currently justified;
2. vary sharedness continuously instead of hard-coding family-specific vs pooled evidence;
3. include real selector/communication/state-size costs rather than only synthetic scalar overhead;
4. allow a **mode-switching hybrid** constrained by the same total budget.

The key question becomes:

> can a system dynamically move among local, hierarchical, integrated and variant-preserving organization based on inferred coupling/regularity, and does that dominate every permanently fixed family after switching overhead?

If yes, the likely architecture result is not A, B, C or D. It is a typed substrate that can instantiate each organization only where its evidence-conditioned value justifies it.