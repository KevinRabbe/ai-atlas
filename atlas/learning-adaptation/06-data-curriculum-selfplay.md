# Data Selection, Curriculum, Self-Play and Imitation

## Required function

Control which experiences the learner sees, in what order, and from which generator so that limited training/interaction compute produces useful transferable change.

## Evidence

- **L-S021 — Curriculum Learning:** ordering examples from easier/more structured to harder examples can change optimization and generalization behavior in studied settings.
- **L-S016 — AlphaGo Zero:** self-play coupled to search and outcome feedback generated its own progressively stronger training distribution without human game records.
- **L-S018 — DAgger:** in sequential imitation, collecting data from states induced by the learner helps correct the distribution mismatch that occurs when a policy is trained only on expert-state demonstrations.
- **L-S002 — SimCLR:** data transformations/augmentations are not innocuous preprocessing; they define which views should be treated as equivalent and materially determine learned representations.
- **L-S022 — Noisy Student:** pseudo-labeled unlabeled examples plus deliberate noise can improve a student beyond the initial teacher, providing a concrete self-training mechanism.

## Key deduction

The dataset is not a static neutral object. **Data generation, selection, ordering and transformation are part of the learning algorithm and part of its inductive bias.**

This connects directly to Foundations: moving bias from architecture/objective into curriculum or generated experience does not eliminate it.

## Self-generated curricula

A capable learner can change its future data distribution by:

- acting/exploring;
- self-play;
- generating candidate problems;
- adversarially producing failures;
- querying humans/tools/evaluators;
- replaying rare or high-information events;
- creating synthetic variants/counterfactuals.

The useful target is not “more synthetic data.” It is **higher expected learning value per unit collection/training cost**.

## Clean-sheet question

Can the system estimate the marginal value of a candidate experience before paying the cost to generate, label, simulate or train on it?

That turns curriculum/data acquisition into the same resource-allocation problem seen elsewhere in the Atlas.

## Failure modes

Curriculum lock-in; self-play cycling or collapse; synthetic-data model bias; teacher-error amplification; loss of rare modes; easy-example overfocus; adversarial examples that exploit evaluator weaknesses; imitation distribution shift.