# Tier-1 Preliminary Results — 2026-08-14

**Status:** reproducible synthetic evidence, not architecture selection.

This checkpoint aggregates the first Tier-1 sweeps and their promotion-quality follow-ups. Full E01/E02/E04 aggregates are reproducible with `python -m ai_atlas_lab.tier1_sweep --seeds 12`.

## E01 — dependency coordination

At dependency density 0.04, hierarchical and 3-round distributed control both reach ~0.788 success, while distributed control uses ~0.063 messages/task versus ~1.559 centralized dispatch messages/task. At density 0.35, one-round distributed drops to ~0.773 while hierarchical and 3-round local propagation reach ~0.817. At density 0.72, one-round distributed reaches ~0.779 while hierarchical and 3-round local propagation reach ~0.847.

This supports a coordination-horizon hypothesis rather than either universal centralization or universal locality.

## E01B — shared-resource contention

A structurally different second family removes dependency chains and instead gives independent tasks a scarce verification resource.

20-seed means:

| verification slots | hierarchical weighted correctness | local threshold | resource-local auction |
|---:|---:|---:|---:|
| 5% | 0.769 | 0.754 | 0.769 |
| 20% | 0.856 | 0.811 | 0.856 |
| 80% | 0.989 | 0.978 | 0.989 |

The resource-local auction matches the global allocator's allocation quality in this toy environment, while paying more messages. Together with dependency E01, this suggests that **coordination should be introduced at the scope where coupling exists**, rather than assuming either one universal executive or fully independent local policies.

DL-001 remains unresolved pending E22 cross-resource metacontrol.

## E02 — integrated vs heterogeneous learning

With exactly 18 learned parameters in both variants:

- sharedness 0.98: integrated 0.977 accuracy vs specialists 0.958;
- sharedness 0.75: integrated 0.907 vs specialists 0.962;
- sharedness 0.15: integrated 0.759 vs specialists 0.952.

A task-0 rule-shift repair changes unrelated-task accuracy in the integrated system by an absolute ~0.199 / 0.140 / 0.060 across those regimes, versus 0 for isolated specialists.

### Training-resource shift

10-seed means under 300 / 1,200 / 4,800 training examples:

- sharedness 0.98: integrated 0.936 / 0.979 / 0.978 vs specialists 0.906 / 0.959 / 0.980;
- sharedness 0.75: integrated 0.887 / 0.907 / 0.949 vs specialists 0.911 / 0.964 / 0.983.

This strengthens the interpretation that sharing is valuable when structure is truly reusable and data are scarce, but is not free: interference and approximation constraints can dominate as task diversity increases.

## E02B — nonlinear/compositional integration

The second E02 family maps six raw binary variables into 15 pairwise interaction features, then learns task-specific compositional rules. The parameter-matched comparison is 45 parameters of `shared + isolated residual` against 45 parameters of independent specialists; a 15-parameter shared-only learner is retained as a lower-capacity transfer reference.

12-seed mean accuracy:

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

This second family reproduces the same broad transfer/interference continuum: stronger sharing becomes more valuable as reusable structure rises and task-specific data fall; isolation becomes more valuable as task rules diverge. The partially shared candidate can occupy the intermediate low-data regime rather than forcing a binary integrated-vs-specialist choice.

However, the partial learner currently spends about **140 logical operations per training example** versus **75** for shared-only and specialists. Therefore DL-002 still remains unresolved: parameter matching is not enough; the next comparison must match realized computation/latency or make the partial path conditional so it earns the extra work.

## E04 — representation/interface

- JSON: exact/version-compatible, ~134.7 bytes;
- positional float32: ~28 bytes, action exact and score error ~3.4e-8, but large exact identifiers lost and version mismatch rejected;
- tagged binary: ~38 bytes, exact discrete state, version-compatible, corruption detected;
- tagged binary + redundant audit: ~173.7 bytes, exact and able to recover the tested core corruption from the redundant copy.

### Bandwidth-resource shift

Under 24 / 32 / 48 / 96 / 192-byte caps:

- 24 bytes: none of the tested encodings fit;
- 32 bytes: only the float32 vector fits;
- 48 and 96 bytes: float32 and tagged binary fit;
- 192 bytes: all four formats fit.

This is evidence for typed/interface-sensitive representation, not evidence against continuous internal state. DL-004 still needs a second task family and a learned continuous channel with an exact side path.

## Why the design ledger is still conservative

The project is intentionally not converting replicated toy results into a finished architecture. DL-001 now has two task families but still awaits E22. DL-002 now also has two task families, but its most interesting partially shared mechanism has an unmatched arithmetic cost. DL-004 has a resource-regime sweep but not yet a second task family.

That is useful: the remaining uncertainty is increasingly about **where the crossover lies under matched physical cost**, not about whether the trade-offs exist at all.

## Next evidence needed

1. compute-matched/conditional E02B partial sharing;
2. E04 backtracking/constraint messages + continuous latent channel with exact side state;
3. adaptive E09 consolidation under hidden volatility;
4. E22 cross-resource metacontrol;
5. then Tier-2 E06/E07 without freezing unresolved boundaries.