# E24 — Predictive Representation Objective: Latent Target vs Reconstruction vs Task-Sufficient State

**Status:** specified; not yet implemented. This experiment is intentionally queued behind the current I04 composition checkpoint unless I04 reveals a representation bottleneck that raises its priority.

## Decision under test

Does prediction in a learned target representation preserve useful world structure more efficiently than raw reconstruction or narrow task-specific prediction **across changing future objectives**?

This is not a benchmark of the JEPA implementation family by name. It tests the implementation-neutral claim extracted from I-JEPA / V-JEPA:

> predict useful hidden/future structure in representation space rather than necessarily reproducing every raw observation detail.

## Hypotheses

### H1 — latent predictive advantage

A representation trained to predict structured latent targets will achieve better lifetime utility per unit active state/training compute than raw reconstruction because nuisance detail does not consume representational capacity.

### H2 — task-specific overcompression failure

A representation trained only for the current action/objective will be cheapest initially but lose sharply when a previously irrelevant world factor becomes decision-relevant.

### H3 — reconstruction optionality advantage

Raw/generative reconstruction will retain more future-useful detail and may outperform latent prediction after sufficiently surprising objective changes, despite higher training/state cost.

### H4 — target-granularity frontier

No fixed predictive target breadth will dominate. Coarse latent prediction should win when nuisance dimensionality is high and future objectives are stable; denser latent targets or recoverable source evidence should win as objective uncertainty and rare-factor consequence rise.

## Environment family A — predictable structure + nuisance

Generate observations from hidden factors:

- stable causal variables;
- temporally predictive variables;
- high-dimensional nuisance variables;
- one rare low-frequency factor that does not affect the initial objective;
- exact identity/control/provenance side fields that are never allowed to become approximate latent semantics.

The initial objective depends only on a subset of the causal factors.

Mid-lifetime, switch to an objective where the previously irrelevant rare factor becomes consequential.

The representation learner does **not** receive the hidden decomposition labels.

## Environment family B — passive prediction vs intervention

Create two hidden world mechanisms that generate nearly identical passive observations but diverge after an intervention.

This family tests whether a representation that is excellent at passive feature prediction actually retains enough structure for action-conditioned consequence prediction.

A later phase should allow the system to purchase interventions under PS-007 rather than assuming action-conditioned data is free.

## Compared policies/objectives

1. **raw reconstruction**
   - retain/predict enough state to reconstruct the observation;
2. **task-sufficient prediction**
   - optimize only state needed by the current objective/action;
3. **coarse latent-target prediction**
   - predict a compressed representation emphasizing temporally/predictively stable structure;
4. **dense latent-target prediction**
   - retain more spatial/local/rare structure in the predictive target;
5. **latent + recoverable source**
   - compact hot predictive state plus cold/source evidence that can rematerialize discarded distinctions;
6. optional later **adaptive target breadth**
   - change latent target granularity according to estimated future relevance and rematerialization price.

The implementation must not give the latent policies oracle access to the hidden causal decomposition.

## Resource matching

Report results at matched:

- learned parameter/state capacity;
- mean training operations;
- peak and mean active-state width;
- source/archive storage;
- rematerialization/retrieval operations;
- planning/simulation operations;
- latency if the implementation introduces materially different execution depth.

Do not compare a larger latent learner against a smaller reconstructive learner and call the objective superior.

## Metrics

### Current-task metrics

- prediction error;
- action/decision accuracy;
- planning success;
- active-state cost;
- training operations.

### Future-objective metrics

- zero/few-shot adaptation after objective switch;
- retained information about the previously irrelevant rare factor;
- rematerialization count/cost;
- catastrophic decisions caused by discarded state;
- recovery latency.

### Intervention metrics

- passive prediction accuracy;
- action-conditioned prediction accuracy;
- causal/intervention discrimination;
- calibration or abstention when the latent model cannot distinguish mechanisms.

### Representation metrics

- hot-state width;
- cold/source retention;
- nuisance sensitivity;
- transfer across objective changes;
- exact-side-state integrity.

## Primary discriminators

E24 should be considered evidence for a JEPA-like principle only if latent-target prediction shows a repeatable Pareto advantage in at least two structurally different families after matched capacity/compute **without** hiding future-objective failures.

A useful result can also be negative. For example:

- raw reconstruction may be worth its cost when future objective uncertainty is high;
- task-sufficient prediction may dominate when goals are stable;
- dense latent targets may dominate coarse ones when rare local state is safety-critical;
- recoverable source evidence may make aggressive latent compression safe enough to win lifetime utility.

## Relation to existing Atlas decisions

- **PS-001:** exact authority/provenance remains outside approximate learned channels where required.
- **PS-005:** extra reconstruction/prediction compute must earn downstream value.
- **PS-007:** intervention evidence is a priced operation, not free context.
- **PS-009:** shared predictive factors must beat interference.
- **PS-010:** memory/compute/observation can substitute under scarcity.
- **PS-012:** target/state breadth should be evaluated by expected future value and recoverability.
- **PS-013/014:** a world model's own prediction is not independent verification of itself.

## Promotion rule

Do **not** promote "use JEPA" as a design principle.

Possible promotion, if evidence survives, would be implementation-neutral, such as:

> **predictive objectives should allocate representation capacity toward future-useful predictable structure rather than raw reconstruction detail, while preserving recoverability/typed exact state where future relevance or authority demands it.**

That principle remains falsifiable by objective shifts, rare-event tasks, intervention failures and reconstructive competitors.