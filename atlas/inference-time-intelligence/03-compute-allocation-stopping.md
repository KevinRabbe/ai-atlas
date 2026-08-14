# Compute Allocation and Stopping

## Required function

Choose how much inference-time computation a problem deserves and terminate when the expected marginal value of additional work falls below its cost/risk.

## Evidence

- **I-S008 — s1:** controlling/forcing reasoning length changed reasoning performance, demonstrating that the same trained model can trade additional test-time computation for quality in some regimes.
- **I-S009 — compute-optimal test-time scaling:** different scaling strategies work best at different problem difficulties; adaptive allocation improved efficiency relative to uniform best-of-N and sometimes allowed a smaller model plus inference compute to beat a much larger model on selected tasks.
- **I-S010 — verification vs verifier-free scaling:** theoretical/empirical analysis identifies regimes where verifier-guided approaches scale more favorably than simply cloning/lengthening traces.
- **Learning P-L11:** repeated expensive inference may later be worth distilling/consolidating, coupling inference budgeting to long-term learning.

## Central problem

A fixed “reasoning effort” is structurally wasteful because tasks vary in:

- difficulty;
- uncertainty;
- consequence/risk;
- decomposability;
- evaluator availability;
- tool latency;
- expected future reuse.

The controller needs to decide among:

`answer now / think longer / branch / retrieve / use tool / delegate / verify / ask for information / stop`.

## Marginal-value framing

A rational stopping criterion is approximately:

`continue if E[improvement in downstream utility | next computation] > computation + latency + risk cost`.

The exact value estimator is unsolved. Confidence alone is insufficient because uncertainty can be irreducible or cheap information may be available externally.

## Budget hierarchy

Budgets should exist at multiple levels:

- total task budget;
- branch/worker budget;
- tool-call budget;
- verification budget;
- recursion depth;
- wall-clock deadline;
- memory/context budget.

Unused budget should not be treated as failure; solving cheaply is a positive outcome.

## Failure modes

Overthinking; premature stopping; token-count proxy for progress; recursive runaway; budget starvation of difficult subproblems; spending compute where no verifier/information can resolve uncertainty; latency ignored in nominal compute metrics.