# Tier-1 Preliminary Results — 2026-08-14

**Status:** reproducible synthetic evidence, not architecture selection.

This checkpoint aggregates 12 deterministic seeds for E01, E02 and E04. The full aggregate is reproducible with `python -m ai_atlas_lab.tier1_sweep --seeds 12`; this note records the load-bearing means.

## E01 — control topology

At dependency density 0.04, hierarchical and 3-round distributed control both reach ~0.788 success, while distributed control uses ~0.063 messages/task versus ~1.559 centralized dispatch messages/task. At density 0.35, one-round distributed drops to ~0.773 while hierarchical and 3-round local propagation reach ~0.817. At density 0.72, one-round distributed reaches ~0.779 while hierarchical and 3-round local propagation reach ~0.847.

The result supports an experimentally testable coordination-horizon hypothesis rather than either universal centralization or universal locality.

## E02 — integrated vs heterogeneous learning

With exactly 18 learned parameters in both variants:

- sharedness 0.98: integrated 0.977 accuracy vs specialists 0.958;
- sharedness 0.75: integrated 0.907 vs specialists 0.962;
- sharedness 0.15: integrated 0.759 vs specialists 0.952.

A task-0 rule-shift repair changes unrelated-task accuracy in the integrated system by an absolute ~0.199 / 0.140 / 0.060 across those regimes, versus 0 for isolated specialists.

This demonstrates a transfer–interference frontier, not where a future architecture should sit on it.

## E04 — representation/interface

- JSON: exact/version-compatible, ~134.7 bytes;
- positional float32: ~28 bytes, action exact and score error ~3.4e-8, but large exact identifiers lost and version mismatch rejected;
- tagged binary: ~38 bytes, exact discrete state, version-compatible, corruption detected;
- tagged binary + redundant audit: ~173.7 bytes, exact and able to recover the tested core corruption from the redundant copy.

This is evidence for typed/interface-sensitive representation, not evidence against continuous internal state.

## Why the design ledger remains unresolved

The Atlas minimum conclusion rule still requires a structurally different task family, an independent resource-regime shift and targeted failure/ablation evidence where relevant. Therefore no architecture family is promoted or rejected at this checkpoint.

## Next evidence needed

1. E01 second allocation task family + independent communication/latency price sweep.
2. E02 nonlinear/compositional tasks + partially shared architectures + matched realized compute.
3. E04 bandwidth/fidelity sweep + learned latent code with exact side channel.
4. E09 adaptive consolidation threshold under hidden volatility.
5. Then Tier-2 E06/E07 without hard-coding still-unresolved Tier-1 architecture choices.
