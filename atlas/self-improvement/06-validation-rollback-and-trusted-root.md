# Validation, Rollback and Trusted Root

## Required function

Ensure self-improvement can change useful components without allowing a candidate mutation to redefine its own success criteria, erase evidence, disable rollback or gain unreviewed authority.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| SI-VR-01 | Self-Harness explicitly accepts proposed harness changes only after regression validation, demonstrating that improvement generation and acceptance can be separate roles. | O | E3 | SI-S002 |
| SI-VR-02 | Darwin Gödel Machine empirically validates code-modified descendants on benchmarks and retains an archive rather than overwriting all prior variants. | O | E3 | SI-S005 |
| SI-VR-03 | Phase-5 control evidence shows untrusted powerful components can contribute useful outputs under externally enforced monitoring/restriction protocols. | O/I | E3 | prior Verification evidence |
| SI-VR-04 | Reward-tampering/Goodhart evidence shows a self-improver cannot safely rely only on an evaluator it is free to optimize or modify. | I | E4 | prior Verification evidence |

## Trusted root

A self-modifying system needs some authority that defines what counts as an accepted transition. The exact implementation is open, but candidate changes should not automatically control all of:

- objective/evaluator;
- hidden regression tests;
- permission system;
- audit history;
- rollback mechanism;
- version provenance;
- deployment activation.

If all of these are mutable within one proposal, “improvement” can be achieved by changing the ruler.

## Transactional mutation

A durable change can follow:

`branch/fork -> mutate -> sandbox -> target tests -> hidden regressions -> adversarial checks -> compare cost/utility -> authorize -> atomic activate -> monitor -> retain rollback`.

The stages can be lighter for reversible low-risk changes and stricter for weights/architecture/control-policy changes.

## Immutable vs evolvable control

A permanently immutable control layer can itself become obsolete or bottleneck future improvement. Therefore the cleaner principle is not “never change the trusted root,” but:

> changing an assurance/control component requires a higher-level or independent acceptance path that remains trustworthy during that transition.

This may require hierarchical governance, offline human/external approval, formally checked migration, or redundant old/new control versions.

## Versioned evidence

Every accepted mutation should preserve:

- parent version;
- exact diff/change description;
- triggering evidence;
- evaluator/test versions;
- results and confidence;
- resource profile;
- activation time/scope;
- rollback target;
- known limitations.

This converts self-improvement into an auditable experimental lineage rather than an opaque current state.

## Clean-sheet restatement

Self-improvement should be **transactional and lineage-preserving**. The candidate may propose radical change; acceptance authority and recovery must remain sufficiently independent to reject or reverse it.

## Failure modes

Candidate rewrites its tests; reward function changed to score itself higher; audit log erased; rollback incompatible with new state; hidden tests leaked into proposal context; unsafe migration of memory/schema; control-root stagnation; nested self-modification outruns assurance throughput; acceptance pipeline becomes bottleneck and is bypassed.
