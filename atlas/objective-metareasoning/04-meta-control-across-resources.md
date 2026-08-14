# Meta-Control Across Resources

## Required function

Apply value estimates consistently across computation, information, interaction, persistence, assurance and self-improvement rather than optimizing each budget independently.

## Resource/action classes

A meta-controller may allocate:

- inference compute;
- memory/context bandwidth;
- sensor/tool/environment interaction;
- communication/delegation;
- learning/consolidation;
- verification/assurance;
- self-improvement/search;
- physical hardware/energy/time.

## Cross-resource substitutions

Different resources can solve the same bottleneck:

- retrieve a fact instead of memorizing it parametrically;
- spend more inference compute instead of training a larger model;
- query reality instead of extending an uncertain simulation;
- use a deterministic tool instead of neural reasoning;
- verify an action instead of training the generator to near-perfect reliability;
- compile a repeated search into a skill to reduce future compute;
- preserve multiple hypotheses instead of paying immediately for more observation.

A controller that optimizes each resource in isolation misses these substitutions.

## Meta-state

Useful allocation requires estimates of:

- current objective/constraints and their uncertainty;
- task difficulty;
- belief/world-model uncertainty;
- available operation capabilities;
- reliability of evaluators/tools;
- expected future reuse;
- current budgets and physical cost;
- consequence/irreversibility;
- opportunity cost.

This meta-state is itself uncertain and should not be assumed perfectly observed.

## Hierarchical control hypothesis

Because evaluating every possible system operation globally is expensive, a plausible structure is hierarchical:

1. cheap local policies handle common decisions;
2. higher-level metacontrol intervenes when uncertainty, conflict or consequence crosses thresholds;
3. rare structural/self-improvement decisions receive the most expensive assurance and search.

Biological local/global modulation, system routing and Phase-5 assurance scaling all make this worth testing, but they do not prove a specific hierarchy.

## Learned vs explicit meta-control

Explicit rules provide predictability and constraints. Learned policies can exploit complex task/resource structure. A hybrid could use learned value estimates inside hard authority/resource envelopes.

The key experimental question is whether learned allocation generalizes under distribution shift or overfits to benchmark cost/quality patterns.

## Meta-learning target

The system can learn not only task behavior but:

- when to think;
- when to ask;
- when to retrieve;
- when to verify;
- when to consolidate;
- when to forget;
- when to self-improve;
- when to stop.

These are all policies over internal/external operations.

## Clean-sheet restatement

A general intelligent system may need **metacontrol over its own finite resources and mutable state**, but the controller should be evaluated against simpler distributed heuristics. Central metacognition is a hypothesis, not a required module.

## Failure modes

Global controller bottleneck; meta-policy single point of failure; learned allocation starves novel operations; local controllers optimize incompatible objectives; cost estimates stale after hardware/model change; meta-state too large/expensive; assurance budget reduced to chase performance; recursive control hierarchy with no termination; resource substitutions ignored.
