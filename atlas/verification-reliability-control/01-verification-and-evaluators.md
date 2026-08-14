# Verification and Evaluators

## Required function

Estimate whether a candidate output, state transition, plan or action satisfies the properties that matter strongly enough to guide selection, search or authorization.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| V-VE-01 | Generating multiple candidate solutions and ranking them with a learned verifier can materially improve mathematical reasoning accuracy. | O | E4 | V-S001 |
| V-VE-02 | Search/evolution becomes substantially more useful when candidates can be scored by reliable automated objectives. | I | E4 | V-S012, earlier AlphaEvolve evidence |
| V-VE-03 | Optimization for correctness alone can reduce checkability/legibility; adversarial prover-verifier training can improve verifier robustness in studied reasoning settings. | O | E3 | V-S004 |
| V-VE-04 | Weak supervisors can elicit capability above their own level, but naive weak-to-strong supervision leaves substantial performance unrecovered. | O | E3 | V-S013 |

## Verification is property-specific

“Correct” is usually shorthand for several properties:

- factual truth;
- logical validity;
- satisfying a formal specification;
- passing tests;
- preserving invariants;
- meeting user intent;
- safe side effects;
- calibration/uncertainty;
- resource constraints.

An evaluator that checks one property provides no automatic evidence about the others.

## Generator/evaluator independence

If generator and evaluator share the same blind spot, agreement creates false confidence. Independence can come from:

- different algorithms/models;
- deterministic tools/tests;
- separate data/sensors;
- adversarial roles;
- hidden holdouts;
- formal proof kernels;
- human/external review.

The objective is not diversity for its own sake but **uncorrelated failure evidence**.

## Trust should be conditional

Evaluator output should carry scope:

`verified property + assumptions + evidence source + confidence + coverage + time/context`.

A unit test can prove a particular behavior on tested cases; it does not prove the program is globally correct. A learned judge can provide useful ranking evidence; it does not become ground truth because its score is high.

## Clean-sheet restatement

Verification is an information-producing operation. The controller should choose a checker whose evidence is relevant to the decision and whose expected error/cost profile justifies the trust being granted.

## Failure modes

Correlated generator/judge errors; rubber-stamp self-evaluation; evaluator overfitting; untested properties silently assumed; majority agreement mistaken for independence; hidden assumptions in tests; verifier distribution shift; verification cost exceeding value; evaluator score treated as truth rather than evidence.
