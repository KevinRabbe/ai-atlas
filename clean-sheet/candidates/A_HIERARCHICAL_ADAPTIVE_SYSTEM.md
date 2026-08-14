# Candidate A — Hierarchical Adaptive System

**Status: competing Phase-9 architecture candidate. Not selected.**

## Core hypothesis

System-wide resource, uncertainty and assurance trade-offs are valuable enough that a small explicit hierarchy of allocation processes should coordinate otherwise specialized computation.

## Organization

```text
External observations / goals / constraints
                 │
                 ▼
        State & objective integration
                 │
                 ▼
        ┌─────────────────────┐
        │  Meta-allocation    │
        │  state              │
        │                     │
        │ choose operation    │
        │ choose budget       │
        │ choose assurance    │
        │ choose persistence  │
        └──────────┬──────────┘
                   │ typed/scoped requests
       ┌───────────┼────────────┬────────────┐
       ▼           ▼            ▼            ▼
   transformation prediction  search/     evidence/
   & abstraction             alternatives  experience
       │           │            │            │
       └───────────┼────────────┼────────────┘
                   ▼
             working/belief state
                   │
             ┌─────┴─────┐
             ▼           ▼
          action       verification
             │           │
             └─────┬─────┘
                   ▼
             controlled effect
                   │
                   ▼
            observation/mismatch
                   │
                   └────────→ learning/change routing
```

The boxes are **functional roles**, not necessarily separate models/processes.

## State organization

### Shared compact meta-state

Contains only information necessary to allocate operations:

- current goal/constraints;
- belief uncertainty summary;
- active resource state;
- available operations/capabilities;
- evaluator/tool reliability estimates;
- consequence/authority information;
- expected future reuse signals.

It should not duplicate full task evidence.

### Working/belief state

Current task-relevant state plus references to source evidence.

### Persistent evidence/history

Externally addressable, typed, versioned and governed.

### Reusable knowledge/procedure state

Generalized knowledge and skills accessed as needed.

### Assurance/authority state

Protected from ordinary task computation; consulted before consequential transitions.

## Operation allocation

A hierarchical policy decides among operation classes rather than running all capabilities on every input.

Example hierarchy:

1. **fast local gate** — direct action if confidence is high and consequence low;
2. **task-level allocator** — retrieval, prediction, search, tool/delegation and working-state updates;
3. **high-consequence escalation** — stronger verification/authority checks;
4. **rare learning/self-improvement allocation** — consolidation or system-variant search.

This reduces the need for one expensive global decision at every micro-step.

## Representation/communication

Components communicate through typed/versioned contracts rather than unrestricted full-state sharing.

A message may include:

`task/request type + compact payload + uncertainty + provenance + authority + resource budget + response contract`.

Payload format can be machine-native where components are compatible; stable metadata survives representation changes.

## Learning

Learning is routed by diagnosis:

- volatile/local information -> reversible state;
- reusable experience -> procedure/knowledge;
- repeated broadly useful computation -> durable integrated learning;
- recurring system bottleneck -> runtime/structural improvement candidate.

The meta-allocation policy itself is learnable but bounded by hard authority/resource envelopes.

## Assurance

Assurance is a sibling to task reasoning, not embedded only inside the same computation that proposes an action.

High-consequence state transitions can be required to pass:

`preconditions -> prediction -> independent property checks -> authority -> effect verification`.

## Functions naturally supported

Strong fit:

- F02 current-state estimation;
- F03 working-state management;
- F05/F07 memory governance/access;
- F09 active information acquisition;
- F10 uncertainty;
- F11 operation selection/stopping;
- F13 coordination;
- F17 verification;
- F19 assurance allocation;
- F21 substrate routing;
- F23 physical scheduling;
- F24 objective interpretation;
- F25 metacontrol;
- F27 transactional change.

Other functions are delegated to lower-level computational processes.

## Invariants this architecture makes easy

- authority/data separation;
- scoped verification;
- consequence-sensitive assurance;
- typed state/provenance;
- resource bounds;
- explicit stopping;
- transactional self-change.

## Hard problems / expected bottlenecks

### Meta-controller bottleneck

Too much state/decision-making at the top can become a serial critical path.

### Wrong abstraction at the top

If meta-state discards a variable that matters for operation choice, the allocator can systematically choose wrong operations.

### Single-point allocation failure

A poorly calibrated allocator can starve useful computation everywhere.

### Interface overhead

Typed boundaries improve control but can force costly serialization/translation.

### Credit assignment across hierarchy

When a task fails, determining whether the allocator or lower-level computation was responsible is nontrivial.

## Main unresolved choices embodied

- U02/U34: hierarchical rather than purely distributed control;
- U03: heterogeneous specialists;
- U31: stable typed interfaces;
- U06/U17: multiple persistence levels and staged consolidation;
- U22: substantial external capability enforcement;
- U33: learned allocation inside hard envelopes;
- U32: machine compute and audit representations may differ.

## What would falsify Candidate A's central hypothesis?

If matched systems show that:

- meta-allocation overhead consumes most gains from selective computation;
- decentralized/local policies achieve equal global utility with less communication/latency;
- allocation errors create worse tail failures than uniform execution;
- typed boundaries materially reduce learning/information flow without compensating robustness;

then the hierarchical architecture should lose preference.

## Critical experiments

1. Compare global/hierarchical versus local operation allocation under the same task and total compute budget.
2. Corrupt/withhold one meta-state variable and measure system-wide sensitivity.
3. Measure value gained per byte/latency introduced by typed component boundaries.
4. Train learned allocation on one resource regime and switch hardware/costs to test adaptation/generalization.
5. Compare consequence-sensitive assurance routing with uniform verification cost.
