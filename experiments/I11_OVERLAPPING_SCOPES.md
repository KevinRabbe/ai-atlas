# I11 — Overlapping and Cross-Cutting Coordination Scopes

**Status:** implemented architecture-boundary experiment. No new provisional principle is added yet.

I10's persistent runtime deliberately keeps one disjoint **ownership topology**. I11 asks whether that partition assumption becomes harmful when a component participates in multiple coordination relationships at the same time.

## Question

A system can have two different meanings of “scope”:

1. **ownership / semantic placement** — where state, resources and ordinary local control currently live;
2. **coordination scope** — which components need to cooperate for a particular dependency or task.

Those sets do not have to be identical.

I11 tests whether cross-cutting work should force the ownership topology itself to reorganize, create persistent overlapping memberships, activate a temporary non-owning overlay, or merge into one global scope.

## Environment

Twelve components have three persistent four-node base groups. Those base groups represent stable reusable local structure.

At runtime, additional four-node cross-cutting groups can become active. Their members cross the base boundaries.

The benchmark prices:

- missed true pair relationships;
- false/unnecessary grouped relationships;
- persistent extra membership state;
- temporary overlay activation/messages;
- disjoint repartition/migration;
- global-scope carrying overhead.

The active cross-cutting dependency is observable as work demand. This experiment tests **scope representation economics**, not dependency inference.

## Policies

### `base_partition`

Keep only the stable disjoint base ownership groups. Cheap, but cross-cutting dependencies are missed.

### `forced_repartition`

When cross-cutting work arrives, force the disjoint partition to reorganize around that task. This captures the temporary cross relationship but breaks stable base relationships.

### `global_scope`

Put everything in one coordination scope. Captures every dependency but groups many unrelated pairs unless coupling is genuinely dense.

### `persistent_overlap`

Retain the base groups plus all cross-cutting memberships permanently. Captures future cross work immediately but pays continuous membership/interference cost.

### `temporary_overlay`

Keep the stable base ownership partition and create a non-owning coordination scope only while cross-cutting work is active. This pays activation/message cost without moving semantic ownership.

## 30-seed results

### Sparse rotating cross-cutting work — active ~18% of steps

| policy | utility/step | missed pairs/step | false pairs/step | mean memberships |
|---|---:|---:|---:|---:|
| base partition | 1.1259 | 0.904 | 0.000 | 12.00 |
| forced repartition | 1.0898 | 1.808 | 0.000 | 12.00 |
| global scope | 1.0185 | 0.000 | 47.096 | 12.00 |
| persistent overlap | 1.0635 | 0.000 | 19.096 | 28.00 |
| **temporary overlay** | **1.1303** | **0.000** | **0.000** | **12.72** |

The temporary overlay wins because it preserves the stable ownership relationships and pays cross-scope state/messages only on the ~18% of steps that need them.

A key negative result is `forced_repartition`: making one disjoint topology chase a cross-cutting dependency actually doubles the missed-pair rate relative to doing nothing because it destroys useful base relationships while representing the temporary group.

## Frequent rotating cross-cutting work — active ~90% of steps

| policy | utility/step | missed pairs/step | false pairs/step | mean memberships |
|---|---:|---:|---:|---:|
| base partition | 1.0540 | 4.498 | 0.000 | 12.00 |
| forced repartition | 0.8741 | 8.997 | 0.000 | 12.00 |
| global scope | 1.0562 | 0.000 | 43.502 | 12.00 |
| **persistent overlap** | **1.1012** | **0.000** | 15.502 | **28.00** |
| temporary overlay | 1.0756 | 0.000 | **0.000** | 15.60 |

Now the persistent overlap earns its carrying cost: repeatedly creating the same class of cross-cutting coordination state becomes more expensive than keeping it available.

A recurrence sweep gives the expected crossover:

- at 20% cross-work frequency, persistent overlap trails temporary overlay by ~`0.064` utility/step;
- at 80%, persistent overlap leads by ~`0.013`;
- at 100%, the lead is ~`0.039` in the rotating-cross-group family.

So overlap itself has a lifetime/value allocation boundary analogous to hot-state breadth and lineage diversity.

## Dense coupling — effectively all components need one scope continuously

| policy | utility/step |
|---|---:|
| base partition | 0.1840 |
| forced repartition | 1.4680 |
| **global scope** | **1.5130** |
| persistent overlap | 1.4980 |
| temporary overlay | 1.3800 |

When the cross-cutting dependency becomes effectively global and continuous, keeping a separate ownership partition plus an overlay is needless duplication. One global scope wins again.

## Architecture inference

I11 rejects two simple architectures:

```text
one component -> exactly one useful scope forever
```

and

```text
if scopes can overlap, keep every useful overlap permanently
```

The better current rule is:

> **semantic ownership and coordination membership are different dimensions. Cross-cutting coordination may overlap ownership scopes without moving identity/state; make that overlap persistent only when recurrence/value earns carrying cost, and merge scopes when coupling becomes dense enough that the distinction no longer pays.**

This is another instance of the Atlas allocation pattern:

```text
sparse temporary dependency
        -> temporary coordination overlay

recurrent cross-cutting dependency
        -> persistent overlapping coordination scope

dense near-continuous dependency
        -> merge / global scope
```

## Relation to I10

I10's disjoint topology remains useful as the **ownership/routing baseline**, but it should not be overloaded to represent every temporary dependency.

The next runtime extension should therefore be minimal:

- keep exact semantic records outside topology;
- keep one current ownership topology where useful;
- add non-owning `CoordinationScope` objects whose memberships may overlap;
- allow coordination scopes to be temporary or persistent;
- closing an overlay must not delete evidence, authority, leases or predictive source state;
- overlap must not duplicate resource ownership or manufacture authority.

This extension is smaller and better evidenced than replacing the entire runtime with arbitrary overlapping ownership graphs.

## Validation

Six tests cover:

1. sparse cross-cutting work favors temporary overlays;
2. forced disjoint repartition loses stable base structure;
3. frequent cross-cutting work can justify persistent overlap;
4. dense coupling can justify one global scope;
5. overlap strategy crosses over with recurrence;
6. temporary overlay state scales with actual cross-scope demand rather than remaining permanently hot.

## Next

Extend `TypedScopeRuntime` with **non-owning overlapping coordination scopes**, then test that:

- multiple overlaps can share a subject safely;
- closing an overlay cannot delete semantic state;
- exact resource leases remain singular;
- authority remains subject/resource based rather than inherited from coordination membership;
- event routing can reference a coordination scope without making that scope the event's permanent identity.

After that, asymmetric/directional dependencies become the next topology assumption to attack.
