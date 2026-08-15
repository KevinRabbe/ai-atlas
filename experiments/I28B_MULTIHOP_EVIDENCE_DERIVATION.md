# I28B — Multi-Hop Evidence Derivation and Path Provenance

**Status:** implemented PS-026 refinement. No new provisional principle.

## Question

I28A shows that directional derivation changes the marginal value of a child observation.

The next question is whether local parent-child semantics compose through a chain:

```text
A -> B -> C
```

If C depends only on B, local conditional evidence should be sufficient. But real derived evidence can bypass or consult earlier sources.

I28B therefore gives C three possible modes:

- copy immediate parent B;
- independently re-check the underlying claim;
- consult/copy the original upstream source A directly.

The visible derivation path is still A -> B -> C, but C's evidence can depend on both B and A.

## Environment

- A error: `0.25`;
- B: checks independently 30% of the time with error `0.04`, otherwise copies A;
- C default:
  - copies B: `0.50`;
  - independently checks: `0.30`, error `0.03`;
  - root shortcut to A: `0.20`;
- D independent error: `0.18`;
- E independent error: `0.22`;
- passive independent resolution: `0.12`.

The principal discriminating observation pattern is:

```text
A != B
C == A
```

This can mean B created a correction while C simply returned to/rooted in A. A local rule that only asks `C != B?` can mistakenly count C as another novel departure.

## Policies

### `symmetric_group`

Collapses A/B/C to one common-mode group and loses all path direction.

### `local_edge_novelty`

Uses only immediate parent comparison:

```text
B novel if B != A
C novel if C != B
```

### `root_provenance_novelty`

Keeps the root/source reference active through the chain:

```text
B novel if B != A
C novel if C != A
```

This is a deliberately simple path-provenance heuristic.

### `learned_local_conditional`

Learns:

```text
P(B correct | A correct)
P(C correct | B correct)
```

and assumes the chain is locally Markov.

### `learned_path_conditional`

Learns:

```text
P(B correct | A correct)
P(C correct | A correct, B correct)
```

so C can retain nonlocal dependence on A.

### `oracle`

Uses the exact hidden copy/check/root-shortcut probabilities.

## Approximate 20-seed result

12,000 tasks/seed, root shortcut `0.20`:

| policy | total error | Brier | `A != B, C == A` error | late bypass error |
|---|---:|---:|---:|---:|
| symmetric group | ~0.089 | ~0.073 | ~0.283 | ~0.287 |
| local-edge novelty | ~0.091 | ~0.076 | ~0.288 | ~0.291 |
| **root-provenance novelty** | **~0.089** | **~0.073** | **~0.173** | ~0.162 |
| learned local conditional | ~0.108 | ~0.081 | ~0.263 | ~0.254 |
| **learned path conditional** | ~0.107 | ~0.080 | **~0.172** | **~0.134** |
| oracle | ~0.085 | ~0.069 | ~0.118 | ~0.114 |

The whole-run learned conditional policies pay a large sparse-feedback learning cost. Their discriminating late behavior is the important result: path conditioning substantially improves the exact cases where the chain contains a nonlocal root dependency.

## Falsifier / crossover

Set the root shortcut to zero:

```text
C copies B or independently checks
C never consults A directly
```

Now the chain is locally Markov.

The extra A-conditioned C state does not help and slightly worsens late Brier in the current experiment because it fragments sparse feedback across unnecessary states.

That rejects the overgeneralization:

> `full path provenance is always better`

## Architecture implication

Local derivation edges compose only when the conditional independence assumptions behind them are actually true.

The required semantic state is therefore closer to:

```text
immediate derivation edge
+
nonlocal provenance/dependency only when evidence can bypass or consult earlier state
```

Path provenance has option value when it changes the interpretation of downstream novelty. Otherwise it is extra state and learning cost.

This mirrors several earlier Atlas results:

- organization scope expands only when coupling earns it;
- hot state persists only while reuse value pays;
- evidence relation state is materialized only while assurance value pays;
- now derivation provenance depth expands only while nonlocal dependency makes it decision-relevant.

## PS-026 refinement

Evidence dependence/derivation is not merely directional and scoped; **dependency depth can itself be conditional**.

A source can be locally derived while still retaining a relevant earlier/root provenance link.

No specific DAG, provenance graph or graphical-model implementation is selected.

## Next discriminator

I28C should remove the DAG assumption entirely.

Mutually adapting evaluators can form cycles:

```text
A <-> B
```

or iterative feedback loops where later observations depend on earlier versions of each other.

The next question is whether static derivation edges remain meaningful, whether generation/version identity is sufficient to break the cycle into a temporal DAG, or whether a different evidence semantics is required.
