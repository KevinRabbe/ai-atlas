# E02B — Nonlinear/Compositional Integration Follow-up

**Status:** second E02 task family; preliminary multi-seed evidence only.

## Why a second family

The original E02 uses ordinary linear classification. E02B changes the problem representation and tests decisions generated from pairwise interactions among six binary input variables. The learned rule is linear only after expanding the raw input into 15 compositional interaction features, so the benchmark exercises a different task geometry and information-sharing pattern.

## Variants

- `shared_only_reference` — one shared 15-parameter rule across all tasks. This is intentionally lower capacity and is a transfer reference, not a matched-capacity competitor.
- `shared_plus_isolated_residual` — 15 shared parameters plus 10 isolated residual parameters per task: **45 total parameters**.
- `compositional_specialists` — one isolated 15-parameter rule per task: **45 total parameters**.

The partially shared and specialist systems are therefore parameter matched. The partial system performs more arithmetic per update (about 140 logical operations versus 75 for the other two), so realized compute is **not yet matched**.

Training is deliberately imbalanced toward task 0 so scarce-data transfer can matter. Hidden `sharedness` changes how much of the true compositional rule is reusable across task families.

## 12-seed means

### 240 training examples

| sharedness | shared only | shared + residual | specialists |
|---:|---:|---:|---:|
| 0.95 | 0.968 | 0.932 | 0.837 |
| 0.65 | 0.849 | 0.857 | 0.841 |
| 0.25 | 0.703 | 0.747 | 0.868 |

### 480 training examples

| sharedness | shared only | shared + residual | specialists |
|---:|---:|---:|---:|
| 0.95 | 0.983 | 0.957 | 0.914 |
| 0.65 | 0.857 | 0.894 | 0.911 |
| 0.25 | 0.709 | 0.793 | 0.917 |

### 1,200 training examples

| sharedness | shared only | shared + residual | specialists |
|---:|---:|---:|---:|
| 0.95 | 0.986 | 0.970 | 0.965 |
| 0.65 | 0.856 | 0.922 | 0.969 |
| 0.25 | 0.708 | 0.850 | 0.961 |

## Interpretation

The second family reproduces the **transfer–interference continuum** without reproducing the first E02 implementation.

- When the underlying rule is highly reusable and data are scarce, strong sharing is valuable.
- When rules diverge, isolated specialists dominate.
- At intermediate relatedness and scarce data, partial sharing can occupy the middle and in one tested low-data regime exceeds both the lower-capacity shared reference and the parameter-matched specialists.
- As more task-specific evidence arrives, specialists catch up or lead.

The key implication is not “use partial sharing.” It is that **the degree of computational sharing appears to be a variable that should respond to reusable structure, data regime and interference rather than a binary integrated-vs-modular choice**.

## Why DL-002 remains unresolved

E02 now has two structurally different task families and multiple data regimes, but the current partial-sharing mechanism spends substantially more arithmetic per update. The selection rule requires matched realized compute/resource accounting, not parameter matching alone.

The next discriminator should therefore compare sharing levels under equal operation/latency budgets and test a nonlinear task family where sharing can itself be routed or gated rather than fixed globally.
