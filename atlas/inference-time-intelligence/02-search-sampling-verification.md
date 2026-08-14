# Search, Sampling and Verification

## Required function

Explore multiple candidate computations/solutions when one greedy trajectory is unreliable, then allocate further work toward candidates with higher expected value.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| I-SS-01 | Sampling multiple independent reasoning paths and aggregating can outperform greedy decoding. | O | E4 | I-S002 |
| I-SS-02 | Explicit tree search with state evaluation/backtracking can dramatically outperform a single chain on tasks requiring lookahead. | O | E3 | I-S003 |
| I-SS-03 | The benefit of test-time search depends strongly on problem difficulty and verifier quality; compute-optimal allocation can outperform uniform best-of-N. | O | E3 | I-S008, I-S009 |
| I-SS-04 | Verifier-guided search/RL can scale differently from unguided trace imitation when a trustworthy verification signal exists. | O/I | E3 | I-S010 |
| I-SS-05 | LLM-guided evolutionary candidate generation plus automated evaluators can discover deployable improvements and new algorithms. | O | E4 | I-S017 |

## Search dimensions

Search is not one mechanism. Important choices include:

- branching factor;
- depth;
- sequential refinement vs parallel sampling;
- candidate diversity;
- state reuse;
- evaluator frequency;
- hard pruning vs soft allocation;
- backtracking;
- population/evolutionary retention;
- termination policy.

## Verification changes the economics

Without an evaluator, additional samples mainly increase diversity and require heuristics/consensus to select among them. With a reliable evaluator, compute can be concentrated on candidates that demonstrate progress.

A weak learned evaluator creates a different problem: optimization can exploit its mistakes. Therefore search budget and evaluator trust should be coupled.

## Clean-sheet restatement

Use branching only when:

`expected value of exploring alternatives > extra generation + evaluation + coordination cost`.

Search should be stateful: a failed candidate can still contribute constraints, counterexamples or reusable partial results instead of being thrown away as dead tokens.

## Failure modes

Search explosion; correlated samples mistaken for independent evidence; verifier gaming; pruning the ultimately correct branch; excessive evaluator cost; diversity collapse; selection bias; repeated rediscovery of the same failure.