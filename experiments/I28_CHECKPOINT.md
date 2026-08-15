# I28 Evidence-Derivation Checkpoint

**Current Phase-10 validation count:** 492 added tests.

**Current provisional principle count:** 26 (`PS-001` through `PS-026`).

No PS-027 is selected by I28A–I28C. These experiments refine PS-026 and the common evidence plane.

## New tests since the 469-test I27 checkpoint

- I28A direction-aware generic aggregation: 8;
- I28B multi-hop/path-provenance aggregation: 7;
- I28C cyclic/versioned temporal evidence: 8.

Total: `469 + 8 + 7 + 8 = 492`.

## I28A — direction changes marginal evidence

A derived child that agrees its parent is often inherited evidence; the same child can become highly informative when it departs from the parent.

Fixed child discounting is insufficient. Symmetric group collapse is safer than record counting but loses correction information. A learned conditional directional model improves late calibration and nearly matches oracle behavior on child-departure cases.

## I28B — local edges do not always compose

When C can bypass immediate parent B and consult upstream A, immediate-parent novelty can misclassify `A != B, C == A` patterns.

Path/root provenance substantially reduces that error. When the shortcut is removed and the chain is truly local-Markov, extra path-conditioned state stops helping and can slightly hurt calibration.

Therefore provenance depth is value/structure conditional, not universally maximal.

## I28C — source cycles can become temporal DAGs

Mutually adapting source identities A/B form a static cycle, but versioned observations can be ordered by generation.

Final A/B outputs share one innovation root only some of the time. Static cycle collapse is therefore too coarse; final independence can overcount shared roots; treating all historical revisions as independent creates false precision.

Versioned temporal transition modeling approaches the oracle while preserving calibration.

## Current evidence-plane decomposition

```text
source identity
    !=
source quality
    !=
common-mode dependence
    !=
directional derivation
    !=
versioned/path provenance
    !=
claim aggregation
    !=
assurance authority
```

## Current PS-026 refinement

Evidence dependence/derivation should preserve the relation distinctions that change marginal evidence value:

- common-mode dependence may be learned and scoped;
- derivation may be directional;
- nonlocal provenance may matter in multi-hop paths;
- source-level cycles may need version/generation identity;
- relation state is materialized only while its assurance value pays for acquisition/carrying cost.

No particular graphical-model, provenance-graph or Bayesian-network implementation is selected.

## Next experiment

**I28D — sparse/delayed truth.**

Test when behavioral dependence/derivation learning becomes too feedback-starved and explicit provenance, targeted resolution or controlled intervention becomes the more efficient route to safe assurance.
