# I28 Evidence-Derivation Checkpoint

**Current Phase-10 validation count:** 500 added tests.

**Current provisional principle count:** 26 (`PS-001` through `PS-026`).

No PS-027 is selected by I28A–I28D. These experiments refine PS-007/013/014/026 and the common evidence plane.

## New tests since the 469-test I27 checkpoint

- I28A direction-aware generic aggregation: 8;
- I28B multi-hop/path-provenance aggregation: 7;
- I28C cyclic/versioned temporal evidence: 8;
- I28D sparse/delayed truth and relation evidence: 8.

Total: `469 + 8 + 7 + 8 + 8 = 500`.

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

## I28D — sparse / delayed truth changes relation-learning economics

B is derived from A during the first half of the lifetime and becomes independent during the second half, without visible source-identity change. Passive ground truth resolves only ~1.2% of tasks and arrives 80–240 steps late.

30-seed matched-stream means:

| policy | error | net utility/task | relation accuracy | post-shift relation accuracy | active truth/task | provenance probes/task |
|---|---:|---:|---:|---:|---:|---:|
| conservative | ~0.0854 | ~2.4679 | — | — | 0 | 0 |
| passive behavioral | ~0.0830 | ~2.5032 | ~0.732 | ~0.000 | 0 | 0 |
| disagreement-targeted truth | ~0.1152 | ~2.0001 | ~0.541 | ~0.987 | ~0.0516 | 0 |
| coverage-targeted truth | ~0.0824 | ~2.5038 | ~0.828 | ~0.059 | ~0.0211 | 0 |
| **provenance probe** | **~0.0809** | **~2.5332** | **~0.995** | **~0.926** | 0 | **~0.0045** |
| oracle relation | ~0.0808 | ~2.5353 | 1.000 | 1.000 | 0 | 0 |

The important counterexample is disagreement-targeted truth acquisition. It obtains substantially more labels and reacts to the hidden shift quickly, yet lifetime relation accuracy and decision accuracy become worse because the learner receives a sample selected on `A != B` and then treats it as representative of the full joint error process.

Output-independent active resolution avoids the worst selection bias. Direct provenance/dependency evidence is more efficient at the default price because it directly resolves the relation uncertainty, but it loses once its price is raised enough.

I28D therefore adds a new falsifier/requirement for active information acquisition:

> **the acquisition policy is part of the evidence-generating process; selectively acquired truth must not be treated as an unbiased sample unless the estimator accounts for that selection.**

This remains a first-family refinement rather than PS-027. It needs a structurally different self-change/discovery assurance family before promotion.

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
claim truth evidence
    !=
relation/dependence evidence
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
- sparse truth can make behavioral relation estimates stale;
- relation evidence and task-truth evidence are different acquisition targets;
- active acquisition can bias relation learning when selection depends on observed source outputs;
- relation state is materialized only while its assurance value pays for acquisition/carrying cost.

No particular graphical-model, provenance-graph, causal-discovery or Bayesian-network implementation is selected.

## Next discriminator

Use a **second structurally different selection-bias family** before promoting anything new: self-change/regression or discovery candidates should receive selective audits, and the experiment should test whether auditing only suspicious/failing-looking candidates biases learned evaluator/dependence quality compared with coverage-corrected or randomized audit acquisition.
