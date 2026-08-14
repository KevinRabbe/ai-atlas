# Evaluator-Guided Iterative and Evolutionary Loops

## Required function

Turn a generative system into an optimizer over candidate solutions when candidate quality can be measured more reliably than it can be generated directly.

## Evidence

- **I-S017 — AlphaEvolve:** LLM-generated code candidates, automated evaluators and evolutionary retention/mutation produced deployed infrastructure improvements and novel algorithmic/mathematical results.
- **I-S010 — verifier-guided scaling:** verification changes the scaling behavior of test-time search in analyzed settings, supporting the broader generator/evaluator separation.
- **I-S005/I-S007:** execution, tests and external tools provide evaluator channels that are stronger than self-assessed language in domains with executable specifications.

## Fundamental asymmetry

Many problems satisfy:

`verify(candidate) << construct(optimal candidate)`

in cost/difficulty.

When this holds, intelligence can be amplified by separating:

- **generator** — proposes diverse candidates;
- **evaluator** — measures constraint satisfaction/quality;
- **search controller** — decides what to retain, mutate, combine or discard;
- **archive/memory** — preserves useful diversity and prior evidence.

## Evolutionary value

Population-based search is useful when local gradients are unavailable/unreliable and candidates can be evaluated independently. It also creates parallelism and preserves multiple basins of promising solutions.

But if the evaluator is incomplete, evolutionary pressure is especially dangerous because the loop will systematically find its loopholes.

## Clean-sheet restatement

Where candidate evaluation is robust, do not require the neural reasoner to internally derive the final solution in one pass. Let generation and objective selection form a computational loop.

## Learning connection

Successful search trajectories/candidates can later become training data or distilled skills. Thus:

`inference search -> verified archive -> consolidation -> better future generator`

is a potential bridge from Phase 3 back to Phase 2.

## Failure modes

Evaluator exploitation; diversity collapse; archive contamination; overfitting to deterministic benchmarks; expensive evaluation dominating generation; invalid transfer from proxy score to real objective; evolutionary drift into brittle edge cases.