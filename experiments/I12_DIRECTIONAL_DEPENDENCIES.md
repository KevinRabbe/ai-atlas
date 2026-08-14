# I12 — Directional Dependencies and Reciprocity-Triggered Sharing

**Status:** implemented architecture-boundary experiment. No new provisional principle is added.

I07–I11 progressively relaxed assumptions about fixed topology and disjoint scopes. I12 attacks another assumption: **dependency symmetry**.

## Question

If component A needs information from B, must B also share state/control with A?

Not necessarily.

I12 separates:

- one-way information dependence;
- reciprocal dependence;
- dense shared dependence.

The experiment asks when a directional link should remain directional and when repeated reciprocity makes a shared scope cheaper.

## Environment

Twelve components move repeatedly through three dependency regimes:

### Sparse directional

Each component has a persistent one-way dependency on another component. Reverse flow has no task value.

### Reciprocal clusters

Three four-node groups have dense bidirectional dependencies internally.

### Mixed

The reciprocal clusters remain, plus several one-way cross-cluster dependencies.

For every ordered node pair the system observes noisy directional interaction events and maintains a decayed rate estimate. The learner is not given the hidden regime or true graph.

## Policies

### `global_scope`

Everything shares one scope continuously.

### `directed_links`

Represent only ordered dependencies whose observed rate crosses the threshold.

### `symmetric_links`

If either direction is supported, represent both directions. This is the targeted falsifier for the assumption that dependency automatically implies symmetric coordination.

### `reciprocity_adaptive`

Keep one-way dependencies as directed links. When both directions between nodes become sufficiently persistent, form shared reciprocal components and use cheaper internal coordination. One-way cross-component relationships remain directional.

## Default 30-seed mixed lifetime

Five cycles, 180 steps per regime:

| policy | lifetime utility/step | sparse-directional segment | reciprocal-cluster segment | mixed segment |
|---|---:|---:|---:|---:|
| global scope | 0.7116 | 0.174 | 0.919 | 1.041 |
| directed links | 0.7034 | 0.211 | 0.854 | 1.045 |
| symmetric links | 0.6689 | 0.173 | 0.833 | 1.001 |
| **reciprocity adaptive** | **0.7394** | **0.213** | **0.909** | **1.096** |

The adaptive system is not best because it commits to one representation. It changes representation according to observed reciprocity.

## Sparse one-way result

In a stationary sparse directional family, symmetric links create roughly **11.94 unsupported reverse relationships per step** while directed/adaptive representations create effectively zero.

That reverse coupling has carrying/interference cost without adding downstream task value.

The clean-sheet lesson is:

> **information dependence is directed evidence; shared state/control must be earned by reciprocal or otherwise coupled value, not inferred automatically from one-way dependence.**

## Reciprocal-cluster result

When interactions become densely reciprocal, maintaining every relationship as individually dispatched directed links becomes unnecessarily expensive.

The adaptive policy detects mutual support and collapses the relevant nodes into shared coordination scopes. In the stationary reciprocal family it reaches about `0.980` utility/step versus ~`0.929` for directional links under the matched cost model.

So the result is not “prefer messages over shared state.”

It is:

```text
one-way persistent dependency
        -> directional flow

reciprocal persistent dependency
        -> shared coordination becomes valuable
```

## Mixed result

The mixed family is the most architecture-relevant condition because both forms are simultaneously correct:

- reciprocal local clusters should share;
- cross-cluster one-way dependencies should remain directed.

The adaptive system reaches ~`1.096` segment utility versus ~`1.045` directed-only and ~`1.001` symmetric-only.

This independently supports the Atlas trend that organizational semantics should be scoped to the actual dependency rather than chosen globally.

## Timescale falsifier

At only 20 steps/regime, the observed directional/reciprocal statistics change too quickly for the learner to identify the current structure before it moves again.

30-seed lifetime utility:

| policy | 20-step regimes |
|---|---:|
| **global scope** | **0.7138** |
| directed links | 0.5856 |
| symmetric links | 0.5630 |
| reciprocity adaptive | 0.6369 |

So even a more expressive dependency representation loses when structural evidence has insufficient persistence.

This reproduces the same architecture-timescale law found in AF02, I07 and I08:

> **structural plasticity is useful only when expected persistence pays for identification, transition and carrying cost.**

## Architecture implication

The current organization model now has at least three distinct concepts:

```text
ownership topology
  where stable state/resources are currently placed

coordination scopes
  possibly overlapping groups that share temporary/persistent work

directional dependencies
  one-way information/control relationships that need not create a shared scope
```

These are deliberately not collapsed into one generic “module graph.”

A useful candidate representation is therefore closer to a **typed dependency graph** than an undirected module partition:

- exact subject/resource/evidence identities;
- ownership relationships;
- directional information dependencies;
- reciprocal/shared coordination scopes;
- current authority edges;
- provenance/source edges;
- event routes and topology epochs.

That statement still does **not** select a graph database or graph neural network. It is a semantic requirement, not an implementation choice.

## Relation to existing principles

No new PS number is necessary yet:

- PS-003 already says coordination scope follows coupling;
- PS-009 says sharing earns itself from reusable transfer rather than being universal;
- PS-021 says structural sharing follows regularity with local override;
- PS-022 says execution/synchronization scope follows consistency coupling.

I12 refines “coupling” by showing that **direction and reciprocity matter**.

## Validation

Six tests cover:

1. one-way dependencies do not justify reverse coordination flow;
2. reciprocal clusters justify shared scope;
3. mixed graphs require shared clusters plus directed links simultaneously;
4. the adaptive representation wins the default changing lifetime;
5. rapid dependency changes restore the advantage of static global organization;
6. reciprocity-aware organization avoids symmetric false-flow overhead.

## Next

The persistent runtime should now gain a minimal **typed directional dependency registry** alongside the non-owning coordination-scope registry.

That registry should:

- reference stable subject identities;
- store direction explicitly;
- not manufacture reverse authority or reverse information flow;
- allow reciprocal links to motivate a coordination scope without forcing one;
- preserve dependencies across ownership-topology epochs;
- remain independent from resource leases and provenance semantics.

After that, the next dangerous assumption is **atomic structural commit**: what if a scope migration partially fails after some state/event/resource changes have already happened?
