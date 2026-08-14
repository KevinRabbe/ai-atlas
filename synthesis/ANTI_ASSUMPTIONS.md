# Anti-Assumptions for Clean-Sheet Design

These statements are deliberately phrased as things the project must **not** assume merely because current systems commonly use them.

## Model / representation

- Intelligence does not imply one monolithic neural network.
- A Transformer-style block is not a required primitive.
- Attention is not the definition of memory or reasoning.
- Recurrence/linear state is not automatically superior because it scales linearly.
- Human natural language is not proven to be the optimal internal reasoning or agent-to-agent representation.
- Tokenization is not known to be a fundamental representation requirement.
- A shared multimodal embedding need not erase modality-specific state.
- A point-like artificial neuron is not a privileged computational unit.
- One numeric precision everywhere is not required.

## Knowledge / memory

- Knowledge does not have to live in model weights.
- External memory does not have to be a vector database.
- More remembered information is not automatically better.
- A transcript is not a current world state.
- The most semantically similar memory is not necessarily the most useful memory.
- The latest observation is not necessarily the current truth.
- Memory should not be assumed append-only or overwrite-only.
- Forgetting is not always failure.

## Learning

- Learning does not mean updating every model weight.
- Gradient descent is not the only possible credit mechanism.
- Differentiability across the entire system is not required for learning.
- Training and deployment are not fundamental boundaries for adaptation.
- Replay is not guaranteed to prevent forgetting.
- Self-supervision, RL, preferences or demonstrations do not dictate where learned information should be stored.
- More durable state should not automatically be updated faster than reversible state.
- A single learning timescale is not required.

## Reasoning / inference

- Reasoning does not equal visible chain-of-thought.
- More reasoning tokens do not monotonically improve quality.
- Recursion is not inherently a higher level of intelligence.
- More agents do not monotonically increase capability or reliability.
- Planning does not require a natural-language plan.
- A large context does not have to be ingested as one prompt.
- Search is not always preferable to amortized direct prediction.
- Unused compute budget is not a failure.

## World models / perception

- A world model does not have to generate photorealistic observations.
- Lower reconstruction/prediction loss does not guarantee better decisions.
- One latent state is not proven sufficient for every future objective.
- Passive perception is not the only way to obtain information.
- Language is not required to mediate perception-to-action.
- Embodiment does not imply humanoid physical hardware.

## Verification / safety

- An LLM judge is not ground truth.
- More judges do not imply independent evidence.
- Process supervision is not universally better than outcome verification.
- A formal proof does not prove an unstated human objective was formalized correctly.
- Interpretability is not a proof of safety, intent or correctness.
- A high confidence score is not useful unless calibrated and behaviorally connected.
- Safety does not have to live entirely in learned model behavior.
- A refusal policy is not equivalent to capability control.
- A sandbox does not eliminate every agent risk.
- Passing a fixed regression suite does not establish absence of regressions.

## Systems / efficiency

- Parameter count is not a scalar measure of system intelligence/capacity.
- FLOPs alone do not measure actual cost.
- Lower asymptotic arithmetic complexity does not guarantee faster or more energy-efficient execution.
- Sparse/conditional computation is not free capacity.
- Current GPU constraints are not laws of intelligence.
- Training-efficient computation does not have to use the same state/execution form as inference.

## Self-improvement

- Self-improvement does not mean unrestricted self-rewriting.
- Recursive self-modification does not imply monotonic improvement.
- The current highest-scoring variant should not automatically replace every alternative lineage.
- Benchmark improvement does not imply positive lifetime utility.
- A self-improver should not be assumed trustworthy to modify its only evaluator, audit trail or rollback mechanism.
- More self-improvement iterations are not always valuable.
- Open-endedness is not automatically beneficial if assurance/evaluation capacity cannot keep up.

## Biology

- The human brain is evidence, not a design specification.
- Biological plausibility is not an optimization objective by itself.
- Evolutionary origin does not prove computational optimality.
- Human cognitive limitations are not requirements for machine intelligence.
- The genome does not directly enumerate every mature neural connection, but this does not prove indirect developmental encodings are best for AI.

## Meta-level

- No single contemporary benchmark defines intelligence.
- No single scalar objective is known to capture all relevant system utility.
- No single existing mechanism has earned status as the universal substrate for every required function.
- Elegance, biological analogy, benchmark leadership and popularity are not evidence of necessity.
