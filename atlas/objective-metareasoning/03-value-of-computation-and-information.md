# Value of Computation and Information

## Required function

Estimate whether another internal computation or information-gathering operation is worth its resource cost before executing it.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| O-VC-01 | Rational-metareasoning approaches can train language models to reduce unnecessary reasoning while maintaining task performance in studied datasets. | O | E2 | O-S010 |
| O-VC-02 | Metareasoning can be formalized as a decision problem over costly computations, including uncertainty about the underlying environment/reward. | O/I | E3 | O-S011 |
| O-VC-03 | Phase-3 test-time scaling evidence shows optimal inference compute depends on task difficulty and strategy, motivating per-instance resource allocation. | O | E3 | prior Inference evidence |
| O-VC-04 | Foundations and Phase-4 evidence show information acquisition itself can have instrumental value when it changes later action quality. | O/I | E5 | prior Foundations/Persistent evidence |

## Computation is an action

An internal operation has:

- expected information/quality gain;
- compute/latency/energy cost;
- opportunity cost;
- risk of misleading the system;
- possible future reuse if consolidated.

Examples:

- another reasoning iteration;
- generate another candidate;
- run a verifier;
- simulate a future;
- retrieve memory;
- ask a specialist;
- inspect a file;
- query a sensor;
- run a test.

## Marginal value

The ideal quantity is not “is reasoning generally useful?” but approximately:

`expected improvement in downstream utility from operation - operation cost`.

The estimate depends on current uncertainty and what has already been computed. Ten nearly identical samples can have lower value than one independent checker.

## Value of information

Information-gathering operations should be evaluated by how they may change future decisions, not merely how much entropy they reduce. Learning a fact that cannot affect any feasible action has low instrumental value even if it is surprising.

## Cost can be future-facing

Some expensive computation creates reusable artifacts:

- verified proof;
- cached result;
- reusable skill;
- improved memory/world model;
- training example.

Therefore value-of-computation can include expected future amortization, not only current task reward.

## Approximation problem

Exact metareasoning can itself be more expensive than the computation being selected. A practical system needs cheap learned/heuristic approximations and should reserve expensive meta-analysis for high-stakes/ambiguous cases.

This creates recursive metareasoning:

> how much computation should be spent deciding how much computation to spend?

The recursion must terminate through approximate policies/budgets.

## Clean-sheet restatement

The system needs a **resource-rational metacontrol estimate**: cheap predictions of marginal downstream value for candidate computations/information-acquisition actions, calibrated well enough to outperform fixed allocation rules.

## Failure modes

Metacontrol overhead exceeds savings; underthinking hard problems; overthinking easy ones; biased value estimates starve unfamiliar strategies; verifier/retrieval value double-counted; future reuse overestimated; cost model ignores memory/communication; recursive meta-analysis loop; exploitation of metacontrol proxy rather than task utility.
