# Candidate C — Integrated Predictive Core + External Evidence

**Status: competing Phase-9 architecture candidate. Not selected.**

## Core hypothesis

A tightly integrated learned computational core can implement most perception, current-state estimation, prediction, operation selection and fast adaptation more efficiently than a collection of explicit specialists, provided exact persistent evidence and high-consequence authority remain externally addressable.

The architecture deliberately minimizes internal module boundaries to test whether integration/communication efficiency outweighs modularity and explicit metacontrol.

## Organization

```text
          observations / goals
                 │
                 ▼
       ┌──────────────────────┐
       │ Integrated adaptive  │
       │ predictive core      │
       │                      │
       │ compact current state│
       │ prediction           │
       │ fast operation choice│
       │ local adaptation     │
       └───────┬───────┬──────┘
               │       │
         evidence ref  │ candidate effect
               │       ▼
               ▼    external assurance/
      persistent evidence  authority boundary
      + exact reusable data     │
               ▲                ▼
               └──────── observed effects
```

Most cognitive functions share one learned state and transformation dynamics. External systems provide evidence preservation, exact interfaces, tools/actions, verification and versioned recovery.

## State organization

### Compact evolving internal state

The core continuously maintains compressed state sufficient for common prediction/action decisions.

It does not repeatedly reload the full evidence history.

### External evidence archive

Raw/typed observations, important episodes, exact identifiers and provenance remain separately addressable.

The core can retrieve source evidence when uncertainty or correction requires it.

### External objective/authority state

Goals/constraints are presented to the core but high-authority enforcement is not stored only in mutable core state.

### Recovery lineage

Core versions and compatible persistent-state schemas remain versioned externally.

## Computation

Rather than explicit top-level routing among many modules, operation selection can emerge from the shared learned state.

The core may internally perform different transformations/iterations, but Phase 9 does not assume those are separately inspectable components.

External operations occur when the core emits a typed request:

- retrieve source evidence;
- acquire new observation;
- perform exact/deterministic computation;
- cause an external effect;
- request verification;
- create a candidate durable change.

## Why this candidate matters

The Atlas has substantial evidence that modular/harness/system design matters, but that does **not** prove maximal decomposition is optimal. Candidate C is the necessary counter-hypothesis:

> maybe much of the allocation, representation and prediction machinery is more efficient when learned jointly inside one stateful substrate, while only provenance, exactness and authority boundaries remain explicit.

Without this candidate, the project would be biased toward architecture complexity simply because the Atlas categorizes functions separately.

## Learning

Fast experience can alter mutable internal state. Durable updates to the core are gated by external learning/change protocols.

Repeated retrieval/search/procedures can be integrated into core behavior if lifetime reuse justifies it.

External evidence is retained long enough to detect whether durable integration created false/generalized behavior.

## Assurance

The core is **not** trusted as the sole authority for consequential effects.

It proposes state transitions; external enforcement checks:

- authority;
- exact interface/schema;
- required verification;
- resource limits;
- transactional durable-change protocol.

This lets the candidate test cognitive integration without also making safety/control fully implicit.

## Functions naturally supported

Strong fit inside integrated core:

- F01 observation interpretation;
- F02 current-state estimation;
- F03 working-state management;
- F04 representation transformation;
- F08 prediction;
- F10 uncertainty representation;
- F11 operation selection/stopping;
- F20 learning/credit within the learned substrate;
- F24 objective-conditioned behavior;
- portions of F25 metacontrol implicitly.

External support naturally handles:

- F05 persistent evidence governance;
- F07 source retrieval;
- F15/F16 action/authority;
- F17/F19 verification/assurance;
- F23 physical scheduling;
- F27 transactional recovery.

## Invariants this architecture makes easy

- low internal communication/serialization overhead;
- shared representation across tightly coupled cognitive functions;
- fast recurrent/current-state updates;
- simple critical path for ordinary tasks;
- clean external boundary for exact evidence/authority.

## Hard problems / expected bottlenecks

### State compression/interference

A bounded integrated state may discard details or mix unrelated tasks/users/episodes.

### Poor internal attribution

When output fails, it may be difficult to identify whether perception, state estimate, prediction or operation choice was responsible.

### Continual-learning interference

Shared learned structure can suffer broad regressions from durable updates.

### Audit gap

Human-readable/external audit may not faithfully reconstruct internal computation.

### Single-substrate bias

One representation/computation family may be inefficient for exact, spatial, symbolic, long-horizon or highly specialized tasks.

### Hidden metacontrol failure

If operation allocation is implicit, it can be harder to calibrate or override than Candidate A's explicit allocator.

## Main unresolved choices embodied

- U02/U34: mostly integrated/implicit control rather than explicit distributed hierarchy;
- U03: more homogeneous cognitive computation;
- U01: compact evolving state plus external source evidence;
- U04/U32: machine-native internal state with separate audit interface;
- U05: strong durable integration for frequent knowledge, external evidence retained for correction;
- U10: adaptive computation may be learned internally;
- U22: external authority boundary retained;
- U29: deployment-time mutable state allowed but durable updates gated.

## What would falsify Candidate C's central hypothesis?

If matched systems show:

- integrated state loses important information despite external evidence access;
- heterogeneous specialist computation provides much higher capability per physical cost;
- attribution/verification failures dominate;
- durable updates cause unacceptable cross-task interference;
- implicit operation selection cannot generalize to new resource/tool regimes;

then integration should lose preference.

## Critical experiments

1. Compare integrated state versus explicit heterogeneous modules under fixed total learned capacity/compute.
2. Stress exact recall/current-state tracking as history grows while measuring external retrieval frequency.
3. Change task/tool/resource distributions and test whether implicit operation choice adapts without retraining.
4. Apply a local durable update and measure broad representation/capability interference versus modular candidates.
5. Measure audit/diagnosis quality after injected internal failure compared with architectures exposing component boundaries.
6. Quantify total memory movement/latency saved by integration relative to modular communication cost.
