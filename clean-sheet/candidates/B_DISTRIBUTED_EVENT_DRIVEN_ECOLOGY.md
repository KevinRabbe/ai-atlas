# Candidate B — Distributed Event-Driven Ecology

**Status: competing Phase-9 architecture candidate. Not selected.**

## Core hypothesis

Intelligence can emerge more efficiently from many locally stateful, locally adaptive computational processes with sparse event-driven coordination than from routing most cognition through a central executive.

Global structure exists mainly as shared identity/provenance, hard constraints and escalation—not as a single process deciding every cognitive operation.

## Organization

```text
                   shared evidence/history
                          ▲   │
                          │   ▼
                 identity/provenance fabric
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
  local process A    local process B    local process C ...
  state + policy     state + policy     state + policy
  local learning     local learning     local learning
       │                  │                  │
       └─────── sparse typed events ─────────┘
                          │
                    escalation events
                          ▼
             shared assurance/authority
                          │
                          ▼
                    external effects
                          │
                          ▼
                      new events
```

Processes can represent perception, prediction, memory abstraction, planning, specialized skills, monitoring or other roles, but roles may emerge/specialize rather than be globally fixed.

## State organization

### Local state

Each process keeps the smallest state needed for its own function and learns local update/communication policies.

### Shared evidence fabric

Important observations/actions/outcomes are addressable through common entity/provenance/time semantics without requiring every process to hold the entire global state.

### Distributed belief

No requirement for one canonical rich global belief representation. Processes may maintain partially overlapping views. Shared state is created only for variables whose coordination value justifies communication.

### Global hard state

Authority, resource envelopes, system identity/version and recovery lineage remain globally enforceable even though cognition is distributed.

## Event-driven operation

Processes activate on relevant events, uncertainty changes, requests or threshold crossings rather than in global lockstep.

Examples:

- a new observation triggers entity/state processes;
- prediction mismatch triggers model-diagnosis/learning process;
- low confidence emits evidence-acquisition request;
- consequential action proposal triggers assurance process;
- repeated local workaround emits consolidation/self-improvement candidate.

## Communication policy

Communication is sparse and value-gated.

A process asks:

`does another process need this information enough to justify transmission/synchronization cost?`

Messages are typed, versioned and scoped. Most local intermediate state never leaves the process.

## Coordination

There is no requirement for universal consensus before ordinary operations.

Coordination modes can include:

- direct request/reply;
- publish/subscribe event;
- temporary coalition for one task;
- local conflict resolution;
- escalation when competing local beliefs/actions cannot be resolved safely.

## Learning

Local processes adapt their representations/policies from local evidence and delayed system-level outcome signals.

Credit can be factorized:

- local transition eligibility/evidence;
- later task/evaluator outcome;
- selective durable update to processes plausibly responsible.

Global learning occurs when evidence shows a shared representation/coordination rule is the bottleneck.

## Assurance

A distributed cognitive system still passes external effects through authority/assurance boundaries.

Processes may propose actions; no process gains authority simply from local confidence.

For high-consequence changes, evidence from independent local processes can help only if failure correlation is estimated rather than assuming process count equals independence.

## Self-improvement

Processes can be:

- specialized;
- duplicated;
- merged;
- retired;
- replaced by a better local mechanism;
- forked into competing variants.

Global structure changes only when enough evidence shows coordination topology or shared state semantics are limiting performance.

## Functions naturally supported

Strong fit:

- F01 entity binding from distributed observations;
- F04 representation specialization;
- F06 experience abstraction;
- F08 predictive modeling through local models;
- F09 active information acquisition;
- F12 alternative generation;
- F13/F14 delegation/communication;
- F18 monitoring;
- F20 local/factorized credit;
- F21 local change routing;
- F23 physical scheduling/locality;
- F26 system-variant search.

Global F02 current belief and F25 metacontrol are intentionally distributed/approximate rather than centralized.

## Invariants this architecture makes easy

- locality and physical resource isolation;
- asynchronous sparse activity;
- functional heterogeneity;
- independent variant retention;
- limited blast radius for local failure/change;
- event/provenance-centered persistent evidence.

## Hard problems / expected bottlenecks

### Global coherence

Local beliefs may diverge or take incompatible actions without sufficient synchronization.

### Communication semantics

Sparse messages can omit a dependency the receiver needs; too much messaging destroys the locality advantage.

### Distributed credit

System-level failure may not reveal which local process should change.

### Emergent protocol drift

Locally adapting senders/receivers may become incompatible over time.

### Coordination under high interdependence

Tasks requiring dense global interaction may strongly favor more integrated computation.

### Hidden correlated errors

Processes trained from similar data can fail together despite appearing independent.

## Main unresolved choices embodied

- U02/U34: strongly distributed local control with escalation;
- U28: asynchronous/event-driven execution;
- U03: heterogeneous computation;
- U31: typed interfaces but sparse communication;
- U07: more local/factorized credit;
- U24: local/population variation retained;
- U15/U30: strong emphasis on physical locality/co-design;
- U06: multiple local persistence timescales.

## What would falsify Candidate B's central hypothesis?

If matched experiments show:

- tasks routinely require dense global state exchange;
- sparse coordination produces large tail failures or duplicated work;
- distributed belief reconciliation costs approach a central-state cost;
- local learning cannot assign credit reliably;
- asynchronous operation creates instability harder to control than its efficiency gains;

then the ecology should lose preference.

## Critical experiments

1. Scale task dependency density while measuring performance versus communication bytes/latency.
2. Compare local event-triggered operation against synchronized/global scheduling under matched compute.
3. Introduce delayed system-level failures and test local versus global credit assignment.
4. Update one process/protocol version and measure compatibility/drift recovery.
5. Remove a local process unexpectedly and measure graceful degradation/reorganization.
6. Compare energy/data-movement costs of local processing versus shared global state on identical hardware.
