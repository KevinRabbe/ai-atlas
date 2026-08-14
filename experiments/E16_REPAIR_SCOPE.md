# E16 — Repair / Change Scope

**Status:** implemented, tested and swept across three causal-scope regimes. DL-016 meets the Atlas promotion gate.

## Question

When a persistent system detects a defect, should it apply a local reversible patch, replace/change an isolated component, or make a structural system-wide change?

The central hypothesis is that change scope should follow evidence about **causal scope and recurrence**, not a fixed preference for small or large edits.

## Environment families

All families contain 12 components and explicitly price repair cost plus regression/blast-radius risk.

### A — sparse isolated faults

Incidents are infrequent and independent. There is no durable shared root to remove. Broad changes therefore cannot amortize their larger cost/risk.

### B — recurring component root

One hidden component produces most incidents until its root is durably repaired. Local patches fix symptoms; component or structural changes can remove the recurrence source.

### C — systemic shared root

Incidents appear across many components until a successful structural repair removes the shared cause. Local/component changes treat symptoms rather than the common source.

The adaptive policy receives no family label. It uses only recent recurrence/coupling observations:

- isolated incident -> local repair;
- repeated same-component incidents -> component scope;
- incidents across many distinct components -> structural scope;
- structural retries are rate-limited.

## Policies

- `local_only`;
- `component_only`;
- `structural_only`;
- `adaptive_scope` inferred from recent causal/recurrence pattern.

## 30-seed results

### Sparse isolated faults

| policy | net utility/step | change cost/step | regressions/run |
|---|---:|---:|---:|
| **local only** | **-0.06698** | **0.00239** | **1.87** |
| component only | -0.07512 | 0.01077 | 4.27 |
| structural only | -0.11541 | 0.03889 | 17.00 |
| adaptive scope | -0.06989 | 0.00491 | 2.73 |

The smallest repair is correctly best; adaptive remains close while occasionally escalating on misleading recurrence coincidences.

### Recurring component root

| policy | net utility/step | incidents/step | root fixed |
|---|---:|---:|---:|
| local only | -0.49970 | 0.45043 | 0 |
| component only | -0.06297 | 0.05007 | 1 |
| structural only | -0.09650 | 0.05003 | 1 |
| **adaptive scope** | **-0.05872** | 0.05042 | 1 |

The middle scope is enough to remove the recurrent root; always-structural pays unnecessary blast-radius cost. Adaptive infers the recurrence and reaches comparable/better lifetime utility without requiring a family label.

### Shared systemic root

| policy | net utility/step | incidents/step | structural changes/run |
|---|---:|---:|---:|
| local only | -0.61242 | 0.55226 | 0 |
| component only | -0.68739 | 0.55226 | 0 |
| structural only | -0.09665 | 0.05013 | 120.30 |
| **adaptive scope** | **-0.06024** | 0.05150 | **5.33** |

Here broad change is necessary because the cause is broad. The adaptive policy waits for cross-component evidence, performs far fewer structural edits, and beats always-structural lifetime utility.

## DL-016 promotion implication

The same fixed repair scope does not dominate across the three causal regimes. A provisional principle is justified:

> **Prefer the smallest reversible change whose causal scope plausibly covers the defect; escalate to isolated durable or structural change only when recurrence/coupling evidence makes the wider scope's expected future benefit exceed its regression, assurance and rollback cost.**

This is **PS-020 — evidence-scaled repair scope / minimal sufficient blast radius**.

The selected object is the scope-escalation rule, not patching, modularity, microservices, adapters, weight surgery or architecture mutation by name.

## Relation to other selections

- **PS-003:** change scope follows causal coupling similarly to coordination scope;
- **PS-002:** broader durable changes should pass stronger staging/consolidation gates;
- **PS-014/016:** verification budget and failure-layer coverage should grow with blast radius;
- **PS-018:** self-change promotion requires refreshing independent regression evidence;
- **PS-019:** alternative lineages may preserve rollback/option value while a broader repair is still tentative;
- **PS-015:** attribution must distinguish the transition/component actually responsible for improvement/regression.

## Falsifiers / next work

- causal-scope estimation errors cause repeated under- or over-escalation;
- rollback/reversible snapshots make broad repairs cheap enough to dominate;
- highly coupled systems make local repair impossible even for apparently isolated defects;
- structural change creates delayed side effects outside current regression coverage;
- one learned generative repair mechanism implicitly discovers scope better than explicit scope control under equal resources.

E17 can now ask a different question: not **how broad should a repair be**, but **whether mature system structure itself should remain fixed, be directly mutated, or be generated/developed from a more compact organization rule**.
