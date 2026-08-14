# I13C — Runtime Publication Fence for PS-024

**Status:** implemented runtime hardening after the I13/I13B promotion.

I13 and I13B provide the experimental evidence. I13C makes the promoted failure-isolation rule explicit in the reusable runtime rather than leaving `stage -> commit` dependent on atomic Python method semantics.

## `PublicationProtocol`

The protocol supports prepared publications for:

- topology changes;
- singular resource-lease handoffs.

Preparation records the authoritative version the candidate was built against but does **not** change the live topology or lease.

Publication then checks:

1. required independent assurance for the exact proposal;
2. topology epoch or lease version is still the prepared-against version;
3. current capability authority at publication time for a new resource holder;
4. only then perform the visible version/ownership change.

Discard leaves the live state unchanged and rolls back any still-staged topology candidate.

## Why version fences matter

Two candidates can both be valid relative to the same starting state but conflict with one another.

Example:

```text
epoch 7
  prepare topology A
  prepare topology B

publish A
  -> epoch 8

publish B against epoch 7
  -> MUST FAIL AS STALE
```

Without the fence, B can overwrite A even though B's validation/assurance was performed against a state that no longer exists.

The same applies to a resource lease: a handoff prepared against lease version 4 cannot publish after some other transition has already advanced the lease to version 5.

## Authority is resolved at publication, not captured at preparation

A particularly important test is:

```text
prepare resource handoff to subject B
        ↓
independent assurance succeeds
        ↓
B is revoked before publication
        ↓
publish
        -> denied
```

Preparation and even prior assurance do not freeze categorical authority.

This extends PS-017 through PS-024: **current authority outranks stale prepared intent.**

## Six runtime tests

1. preparing a resource handoff does not change live ownership;
2. revocation after preparation blocks publication;
3. a changed lease version invalidates a prepared handoff;
4. a second topology plan from an old epoch cannot overwrite a newer commit;
5. non-independent assurance cannot publish a consequential change;
6. discard preserves live topology/ownership.

## Current transition lifecycle

```text
PROPOSE
   ↓
PREPARE non-authoritative candidate state
   ↓
ASSURE / VALIDATE
   ↓
CHECK current version + current authority
   ↓
PUBLICATION FENCE
   ↓
new authoritative topology / ownership version
   ↓
retire old candidate/cache/version state
```

This is still an implementation-neutral semantic protocol. The eventual substrate may implement the boundary with transactions, compare-and-swap, epochs, consensus, leases, copy-on-write, dual versioning or another mechanism.

The Atlas selects the **failure-isolation semantics**, not those names.
