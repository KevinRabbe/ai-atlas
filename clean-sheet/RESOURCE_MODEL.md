# Clean-Sheet Resource Model

**Phase 8 — abstract physical/economic model.**

Any candidate architecture must be evaluated as a physical system over its full lifetime, not by parameter count, nominal operation count or benchmark accuracy alone.

## 1. Resource vector

Represent the resource state as a vector rather than one scalar:

`R = {compute, fast_memory, persistent_memory, local_bandwidth, network_bandwidth, latency, energy, precision, interaction, verification, storage, human/external_attention}`

Additional deployment-specific resources may be added. Different operations consume different mixtures and resource prices can change over time.

## 2. Compute

Track at least:

- arithmetic operations by type/precision where useful;
- sequential critical-path depth;
- available parallelism;
- utilization/effective throughput;
- repeated computation that could be cached/consolidated.

Nominal operation count is insufficient when memory/communication dominates.

## 3. Memory capacity and lifetime

Separate:

- operation-local temporary state;
- fast repeatedly accessed active state;
- persistent mutable state;
- archival/history state;
- durable learned/structural state.

Measure:

- bytes/capacity;
- read/write frequency;
- lifetime;
- retention/replication cost;
- migration/reconstruction cost;
- fragmentation/unused allocation where relevant.

## 4. Data movement

For every important operation, estimate movement across physical distance/hierarchy:

- local register/cache/scratch state;
- accelerator/local memory;
- host/shared memory;
- device-to-device/network;
- persistent storage;
- remote service/environment.

The architecture should optimize useful work per byte moved, not merely arithmetic per token/step.

## 5. Communication

Track:

- bytes/messages;
- synchronization points;
- fan-out/fan-in;
- tail latency/stragglers;
- serialization/translation cost;
- redundancy/correlated messages;
- protocol compatibility cost.

A distributed intelligent system that spends most of its resources exchanging internal state has not gained efficiency from modularity.

## 6. Latency

Distinguish:

- time to first useful action;
- end-to-end task latency;
- per-operation latency;
- critical-path latency;
- background/non-critical work;
- hard real-time deadlines versus flexible tasks.

Parallel work can reduce wall-clock latency while increasing total resource use.

## 7. Energy

Where measurable, track energy for:

- computation;
- memory movement;
- communication;
- storage/retention;
- sensing/interaction;
- cooling/support overhead.

Energy is not only a deployment concern: it can change which representation, locality and sparsity policies are optimal.

## 8. Numerical/information fidelity

Precision is a resource.

For each state/operation define tolerable error such as:

- exact/lossless required;
- bounded numeric error;
- probabilistic/approximate representation;
- lossy summary allowed with source recoverability.

Long-lived recurrent/persistent state may need stricter accumulated-error analysis than disposable intermediate state.

## 9. Interaction cost

External interaction can be more expensive than internal compute.

Track:

- API/tool calls;
- environment/sensor observations;
- real-world action cost/risk;
- experiments/probes;
- human clarification/review;
- data acquisition.

A better internal model may be valuable primarily because it saves interactions; conversely a cheap observation can dominate an expensive uncertain simulation.

## 10. Verification/assurance cost

Verification consumes real resources:

- deterministic checking;
- simulation;
- independent model/process evaluation;
- hidden/adversarial tests;
- sandbox execution;
- human/external authorization;
- post-action effect checks.

The system should not pretend assurance is free or maximize verification regardless of consequence.

## 11. Persistent-state maintenance cost

Long-lived intelligence incurs ongoing cost for:

- indexing/retrieval;
- contradiction resolution;
- confidence refresh;
- version/schema migration;
- consolidation;
- archival storage;
- deletion/retention policy;
- security/provenance checks.

Memory should therefore be evaluated by lifetime decision value minus maintenance cost.

## 12. Self-improvement cost

An improvement iteration consumes:

- failure diagnosis;
- candidate generation/search;
- parallel variants;
- evaluation/hidden tests;
- migration;
- monitoring;
- rollback storage;
- opportunity cost while compute is unavailable for productive tasks.

Net improvement requires future utility/savings to exceed this total cost and regression risk.

## 13. Lifetime cost

For architecture candidate `A`, evaluate approximately:

`LifetimeCost(A) = build/train + deployment inference + persistent-state maintenance + interaction + assurance + self-improvement + migration + failure/recovery`.

The terms need not be converted to money; retain a vector/Pareto view where appropriate.

An architecture that is cheap to train but expensive to run for years may be inferior to a more expensive initial learner. The reverse can also occur for one-off tasks.

## 14. Resource substitution matrix

Candidate systems should document substitutions such as:

- more persistent state ↔ less repeated computation;
- more model/learned capacity ↔ less external retrieval;
- more inference search ↔ less training investment;
- more observation ↔ less uncertain simulation;
- more verification ↔ lower generator reliability requirement;
- more specialization ↔ more routing/communication;
- more precision ↔ more memory/bandwidth/energy;
- more archival evidence ↔ easier correction/audit but higher storage/retrieval cost;
- more self-improvement search ↔ potentially lower future task cost.

These substitutions are core design variables, not implementation details.

## 15. Resource-rational operation test

For a candidate operation `o`, the controller eventually needs an approximation of:

`ExpectedNetValue(o) = expected downstream benefit + reusable information/skill value - resource vector cost - delay/opportunity cost - risk/assurance cost`.

This is conceptual, not a requirement for one scalar value function. Hard constraints can remove operations before comparison.

## 16. Required benchmark reporting

When experimentally comparing clean-sheet mechanisms, report at minimum:

- task utility/quality;
- wall-clock latency;
- arithmetic/compute estimate;
- peak and persistent memory;
- bytes/data movement when measurable;
- communication volume/synchronization;
- interaction/tool calls;
- verification cost;
- energy when feasible;
- persistent-state growth;
- change/self-improvement cost if relevant.

A benchmark result that hides these dimensions should not be used to select the final architecture.
