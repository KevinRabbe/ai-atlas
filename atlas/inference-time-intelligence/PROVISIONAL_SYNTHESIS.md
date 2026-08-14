# Inference-Time Intelligence — Provisional Synthesis

**Status: first-pass synthesis, not architecture.**

## P-I01 — Intermediate computation is useful; natural-language thought is not established as necessary

Explicit reasoning traces provide decomposition/search affordances and improve difficult tasks, but the required function is revisable intermediate state. Its optimal representation remains open.

**Confidence:** high for intermediate-state value; low that text is universally optimal.

## P-I02 — Test-time intelligence is a compute-allocation problem

Problems differ in difficulty, uncertainty, risk, tool availability and decomposability. A fixed inference budget is therefore structurally inefficient.

**Confidence:** high.

## P-I03 — More inference compute is not monotonically useful

Additional tokens, samples, branches or agents help only when they create useful diversity/progress and can be selected/integrated. The marginal return depends on task and control policy.

**Confidence:** very high.

## P-I04 — Verification changes the value of search

Reliable evaluators turn candidate generation into directed optimization and support stronger search pressure. Weak/learned evaluators create exploitability risk that must cap optimization pressure or require independent checks.

**Confidence:** high.

## P-I05 — Tools are specialist computational substrates

External tools can provide capabilities that are cheaper, more accurate, current or verifiable than reproducing them inside a general model. Effective intelligence therefore includes routing problems to external computation.

**Confidence:** very high.

## P-I06 — Interface design is part of capability

Tool and computer interfaces determine how much model capacity/context is spent manipulating the environment. Better interfaces can materially improve end-to-end performance without weight changes.

**Confidence:** high.

## P-I07 — Large context should be treated as addressable environment when full ingestion is wasteful

RLM evidence supports selective programmatic examination and bounded recursive subcomputations over state larger than the active model window.

**Confidence:** medium-high; generality beyond current tasks remains to map.

## P-I08 — Recursion is a scheduling primitive, not a definition of better reasoning

Recursion helps when decomposition reduces active-state complexity more than it adds child/aggregation overhead. Unrestricted recursive depth is not justified.

**Confidence:** high as a systems inference.

## P-I09 — Delegation is conditional computation at system scale

Subagents/workers are useful when subproblems are separable, parallelizable, independently verifiable or benefit from specialization/diversity. Agent count alone has no expected monotonic relationship with quality.

**Confidence:** high.

## P-I10 — Harness/runtime policy is an independent optimization surface

Context policy, tools, scheduling, error recovery and interfaces can materially change system capability with fixed weights, and can themselves be optimized/regression-tested.

**Confidence:** high.

## P-I11 — Generator and evaluator should be separated when verification is cheaper than construction

Evolutionary/search systems demonstrate strong gains when candidate quality can be evaluated automatically. This structure should be preferred conditionally, not universally.

**Confidence:** high in verifiable domains.

## P-I12 — Successful expensive inference is a candidate for learning-time consolidation

Repeated reasoning/search/tool trajectories can be distilled or compiled when reuse is high, creating a feedback loop between inference-time search and durable learning.

**Confidence:** medium-high.

## P-I13 — Stopping is a first-class cognitive operation

A system must estimate whether another computation is worth its cost. Unused budget is a success when confidence/utility is already sufficient.

**Confidence:** high conceptually; learned marginal-value estimation remains open.

---

## Emerging controller abstraction

A clean-sheet inference controller may repeatedly evaluate:

`current state + uncertainty + goal + available operations + budgets`

and choose among:

`answer / internal compute / retrieve / tool / execute / branch / delegate / recurse / verify / ask / store result / stop`.

The controller's optimization target is not maximum reasoning depth. It is **maximum expected downstream utility per total lifetime resource/risk cost**.

This is a synthesis hypothesis, not a final architecture.

## Strong anti-conclusions

This pass does **not** justify:

- “more thinking tokens always help”;
- “RLM should wrap every task”;
- “multi-agent is inherently stronger than single-agent”;
- “tools should replace learned knowledge”;
- “a self-improving harness is safe without regression gates”;
- “English chain-of-thought is the machine's natural reasoning format”;
- “a verifier makes optimization safe regardless of coverage.”

## Most valuable experiments

1. Hold total compute constant and compare sequential deliberation, parallel sampling, tree search, delegation and recursion by task structure.
2. Vary evaluator reliability while scaling search pressure to map exploitability thresholds.
3. Compare natural-language, structured, executable and latent intermediate state under equal compute and verification.
4. Learn the operation-selection/stopping policy and compare against fixed human heuristics.
5. Feed verified expensive inference trajectories into Phase-2 consolidation and measure whether lifetime system cost actually falls.