# I18 — Publication Provenance in Crash Recovery

**Status:** implemented. I18 refines the minimum semantics required by I14/PS-024; it does not add a new provisional principle.

## Question

I14 initially represented recovery with:

- expected base version;
- intended target version;
- target state identity/digest.

Integration with the reusable runtime exposed two assumptions:

1. the exact numeric target version may not be knowable at preparation time if unrelated objects share a version allocator;
2. another publication can independently create the same target state/value.

I18 asks whether version + state value are sufficient for exact transition attribution.

## Family A — target version is not predictable at prepare time

A resource starts at version `10`. Unrelated publications can advance a broader/global version sequence before this handoff becomes authoritative.

If our handoff publishes, its resulting version can therefore be `11..15`, although the resource itself was still prepared against version `10`.

### 30-seed result

| recovery evidence | correct recovery | missed completed publication |
|---|---:|---:|
| predict `base+1` target version | ~0.519 | ~0.481 |
| target state identity only | **1.000** | 0 |
| publication provenance | **1.000** | 0 |

The lesson is not that versions are useless. The **base version fence** is still needed to decide whether retry can safely replace the same state. What fails is requiring the future target version to be known before publication.

## Family B — another publication creates the same target state

A different publication can move the resource to the exact same semantic target (`holder B`) even though our prepared transition never published.

### 30-seed result

| recovery evidence | correct recovery | false completion attribution |
|---|---:|---:|
| predicted version + target state | ~0.912 | ~0.0883 |
| target state identity only | ~0.912 | ~0.0883 |
| **publication provenance** | **1.000** | **0** |

A state value answers:

> what is authoritative now?

It does not always answer:

> which transition made it authoritative?

That distinction matters for exact recovery, causal credit, audit and deciding whether cleanup/retirement associated with this publication is complete.

## Refined minimum recovery semantics

The implementation-neutral recovery record is now:

```text
stable publication identity
expected base authoritative version
target semantic identity/digest
optional predicted target version
references needed to reacquire current validation
```

And the authoritative published state needs an equivalent way to expose **which publication/transition produced it** when exact attribution matters.

The numeric target version can be optional:

```text
current publication identity == this publication
+ current target identity matches
+ current version advanced beyond expected base
    -> already published

current version == expected base
    -> not published; retry only after CURRENT validation/assurance

current version advanced under another publication
    -> superseded / conflict; do not overwrite
```

## Architecture implication

I18 strengthens PS-001/004/015/024 rather than creating another law:

> **Authoritative state identity and publication provenance are different semantics. A version fence protects replacement of the expected base; publication provenance identifies which transition actually produced the resulting authority.**

A particular storage engine may encode this as a commit ID, generation record, transaction identity, content-addressed root, lineage pointer or something else. Atlas does not select that implementation here.

## Runtime consequence

`RecoveryRecord.target_version` is now optional, and `RecoveryObservation` can carry `current_publication_id`.

If authoritative publication provenance is available, recovery remains exact even when the numeric target version could not be predicted at preparation time.

If provenance is unavailable and only the same semantic target value is visible, exact attribution must not be fabricated.

## Remaining implementation gap

`TypedScopeRuntime` and `PublicationProtocol` still represent topology/resource authority separately from the generic recovery record. Before calling crash recovery fully integrated, the authoritative publication boundary should expose publication provenance in the same coherence domain as the topology/lease change.

That is the next runtime hardening target; a side registry updated after publication would merely recreate the crash window I14 is designed to remove.
