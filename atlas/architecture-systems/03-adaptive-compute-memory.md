# Adaptive Computation and Writable Memory

## Required function

Allow computation and state update to expand when a problem requires it rather than forcing every input through an identical fixed-depth, fixed-memory path.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| AS-AC-01 | Adaptive Computation Time demonstrated that a recurrent model can learn variable numbers of internal steps and allocate more steps to harder transitions in some tasks. | O | E2 | AS-S004 |
| AS-AC-02 | External differentiable memory can extend a neural controller with learned read/write operations and support algorithmic tasks not naturally represented by fixed hidden state alone. | O | E2 | AS-S003 |
| AS-AC-03 | Titans demonstrates a learned long-term neural memory updated at test time and combined with attention/short-term processing, including very long-context experiments. | O | E2 | AS-S019 |
| AS-AC-04 | Recurrent-depth language models can increase latent test-time computation by repeatedly applying a block without emitting additional language tokens. | O | E2 | AS-S041 |
| AS-AC-05 | Variable computation is useful only if the controller can estimate marginal value of another step; fixed recurrence otherwise risks wasted compute or unstable iteration. | I | E2 | AS-S004, AS-S041 |

## Distinguish three adaptations

### 1. Variable execution depth

Repeat/refine computation on the same state before producing an external action.

### 2. Writable persistent state

Change memory as experience arrives, without changing long-term model weights.

### 3. Test-time parameter-like adaptation

Use a learned update rule to alter a memory/module during inference.

These should not be conflated. They have different persistence, stability and verification requirements.

## Architectural implication later

Fixed feed-forward depth is a convenience, not a demonstrated requirement. The more general requirement is a stable mechanism for deciding:

`expected value of another computation > latency/energy/opportunity cost?`

This connects architecture directly to the Foundations value-of-computation question.

## Clean-sheet restatement

Provide a bounded mechanism that can spend additional internal computation, update temporary memory, or invoke another module when uncertainty/task difficulty justifies it, with explicit stopping and rollback semantics.

## Open questions

- Can halting be calibrated against objective marginal improvement rather than learned heuristics alone?
- What state is safe to mutate online without catastrophic drift?
- Can adaptive depth coexist with batching and accelerator utilization without destroying throughput?
- Should additional computation be recurrent neural steps, search, executable programs, submodels, or chosen dynamically?

## Failure modes

Non-halting; excessive deliberation; unstable recurrent refinement; online-memory corruption; state contamination across tasks; batching collapse due to highly variable per-example work.