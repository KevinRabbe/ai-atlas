# Tier-1 Preliminary Results — 2026-08-14

**Status:** reproducible synthetic evidence, not architecture selection.

This checkpoint aggregates the first Tier-1 sweeps and their initial promotion-quality follow-ups. Full E01/E02/E04 aggregates are reproducible with `python -m ai_atlas_lab.tier1_sweep --seeds 12`.

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

DL-002 still needs a structurally different nonlinear/compositional family.

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

The project is intentionally not converting replicated toy results into a finished architecture. DL-001 now has two task families but still awaits E22; DL-002 and DL-004 have resource-regime evidence but not yet second task families. That asymmetry is useful: it tells us exactly which new experiments have the highest information value.

## Next evidence needed

1. nonlinear/compositional E02 family + partially shared alternatives;
2. E04 backtracking/constraint messages + learned latent channel with exact side state;
3. adaptive E09 consolidation under hidden volatility;
4. E22 cross-resource metacontrol;
5. then Tier-2 E06/E07 without freezing unresolved boundaries.