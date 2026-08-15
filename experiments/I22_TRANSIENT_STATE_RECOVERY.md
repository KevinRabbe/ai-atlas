# I22 — Transient Cognitive State Across Crash / Structural Recovery

**Status:** implemented composition checkpoint. No new provisional principle is added.

## Question

I14–I21 harden authoritative state, external execution and evidence interpretation across crash/restart.

But an intelligent runtime also has transient state:

- hot/predictive cache;
- delayed causal-credit eligibility;
- tentative working state;
- queued/in-flight work.

Persisting all transient state can preserve useful work, but it can also preserve stale values or attribution that no longer refers to the same post-recovery structure.

I22 asks:

> which transient state deserves recovery, which should be rematerialized from stable source evidence, and which should be discarded because its identity/value no longer justifies restoration?

## Family A — source-backed hot / predictive state

Twenty-four hot-state items per episode move through four recurring regimes:

- low future reuse / low staleness;
- high future reuse / low staleness;
- low future reuse / high staleness;
- high future reuse / high staleness.

The recovery policy sees noisy estimates of reuse and stale probability, not hidden outcomes.

Policies:

1. persist all hot values;
2. discard hot values but rematerialize from stable source if reused;
3. discard without recovery;
4. adaptive persist/rematerialize/discard by expected future value.

### 30-seed result

| policy | utility/item | persisted | rematerialized | stale reuse | missed reuse |
|---|---:|---:|---:|---:|---:|
| persist all | ~0.2314 | 1.000 | 0 | ~0.0694 | 0 |
| rematerialize | ~0.3278 | 0 | ~0.4202 | 0 | 0 |
| discard | 0 | 0 | 0 | 0 | ~0.4202 |
| **adaptive** | **~0.3335** | ~0.1713 | ~0.3007 | **~0.0060** | 0 |

The result is not `never persist cache`.

The adaptive policy preserves some high-reuse/low-staleness state while rematerializing more volatile or cheaper-to-recover distinctions.

This is PS-012 applied to recovery:

> **hotness and crash persistence are both lifetime-value decisions; stable source recoverability can substitute for carrying exact transient state.**

## Family B — delayed causal-credit eligibility

A delayed outcome arrives after recovery. Six eligibility-trace items refer to historical transitions.

Structural change can happen before the outcome arrives. After a structural change, only some historical transition identities still have a valid semantic learning target.

Policies:

1. discard trace;
2. restore unversioned/positional trace into current structure;
3. retain versioned causal transition identities and credit only still-valid targets;
4. replay retained source/history to reconstruct the valid historical trace;
5. adaptive choice using noisy structural-change estimates and changing persistence price.

### 30-seed result

| policy | utility/item | correct credit | false blame | persisted trace | replayed trace | missed credit |
|---|---:|---:|---:|---:|---:|---:|
| discard | 0 | 0 | 0 | 0 | 0 | 1.000 |
| unversioned restore | ~0.6083 | ~0.8473 | **~0.1527** | 1.000 | 0 | 0 |
| versioned causal trace | ~0.7073 | ~0.8473 | **0** | 1.000 | 0 | ~0.1527 |
| source replay | ~0.7073 | ~0.8473 | **0** | 0 | 1.000 | ~0.1527 |
| **adaptive** | **~0.7859** | ~0.8473 | ~0.0050 | ~0.7447 | ~0.2553 | ~0.1476 |

The adaptive policy uses exact trace persistence when carrying identity is cheap and source replay when persistent trace state becomes expensive.

## Core result

Two transient state classes require different recovery evidence:

```text
hot predictive/cache state
    value = future reuse
    safety = currentness
    alternative = rematerialize from stable source

credit eligibility
    value = delayed attribution
    safety = exact causal/transition identity after structure change
    alternative = replay retained historical source
```

A raw memory snapshot does not encode this distinction by itself.

## Architecture implication

Crash recovery now follows the same recurring Atlas law as normal execution:

```text
recover transient state only while
expected future value
    > persistence / replay / rematerialization / stale-attribution cost
```

But the **type of validity condition remains non-scalar**:

- cache validity asks whether the represented information is still current;
- credit validity asks whether the historical transition identity is still a legitimate causal learning target.

This strengthens:

- **PS-012:** adaptive state breadth / recoverable optionality;
- **PS-015:** causal/eligibility-scoped delayed credit;
- **PS-022:** event/version scope survives structural change;
- **PS-024:** recovery should not publish stale/incorrect semantics merely because bytes survived.

## No new storage assumption

I22 does not select:

- checkpoint everything;
- persist all activations/cache;
- replay all history;
- a specific cache hierarchy;
- a specific trace database.

It establishes what the recovery controller must be able to distinguish.

## Next implementation step

The reusable organism can now add a minimal transient-state registry with two typed records:

1. source-backed hot state with rematerialization reference and creation/version context;
2. delayed credit eligibility tied to stable transition identity/version, optionally replayable from retained source history.

That registry should remain subordinate to the shared value allocator rather than automatically restoring everything after restart.
