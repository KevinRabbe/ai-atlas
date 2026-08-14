# Architecture and Algorithm Discovery

## Required function

Search over computational structures, learning rules and executable algorithms when improvement requires changing more than parameters or runtime policy.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| SI-AA-01 | Neural architecture search can automatically discover architectures competitive with strong human-designed baselines in studied domains. | O | E4 | SI-S007 |
| SI-AA-02 | Population-based methods can adapt hyperparameter schedules during training rather than selecting one static configuration. | O | E4 | SI-S006 |
| SI-AA-03 | AlphaTensor discovered provably correct matrix-multiplication algorithms that improved known complexity for several sizes and hardware-specific runtime for some workloads. | O | E5 | SI-S010 |
| SI-AA-04 | AlphaEvolve combines model-generated program mutations with automated evaluators and has produced deployable algorithmic/system improvements. | O | E4 | SI-S009 |
| SI-AA-05 | Darwin Gödel Machine demonstrates empirical self-modification of the agent implementation itself with benchmark-gated selection. | O | E3 | SI-S005 |

## Search representation matters

The space can be encoded as:

- explicit graph/code;
- parameterized templates;
- grammar/program transformations;
- developmental/generative encodings;
- modular component composition;
- learned mutation operators.

The biological pass suggests that indirect generative encodings deserve comparison with direct mature-graph specification because compact rules can generate large structured phenotypes.

## Algorithm versus model discovery

A reusable improvement need not remain neural. Search can produce:

- symbolic algorithms;
- data structures;
- compiler/kernel transformations;
- tool workflows;
- architecture modules;
- routing policies;
- training curricula;
- mathematical constructions.

When correctness can be mechanically checked, algorithm discovery is especially attractive because the evaluator can remain stronger/more objective than the generator.

## Hardware dependence

AlphaTensor's hardware-specific search reinforces the Phase-1 principle that “better algorithm” is relative to physical execution. Architecture/algorithm self-improvement should therefore retain performance profiles across hardware rather than assuming one implementation-neutral scalar fitness.

## Recursive self-modification

A self-modifier can change the procedure that generates future changes. This expands the search space but also changes the distribution and trustworthiness of future proposals. Meta-mutation therefore requires stronger regression/assurance than ordinary task-level edits.

## Clean-sheet restatement

Self-improvement should be able to escalate from local parameter/procedure changes to **search over computation itself** when evidence indicates the current representation/operator family is the bottleneck. Structural search is an expensive high-assurance operation, not the default response to ordinary errors.

## Failure modes

Search-space lock-in; architecture benchmark overfit; generated code unsafe despite target score; hardware-specific improvement mislabeled universal; mutation operator collapse; meta-mutation destroys future search diversity; evaluator cannot check novel structures; combinatorial cost exceeds likely gain.
