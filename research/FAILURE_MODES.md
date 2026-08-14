# Failure Modes

The atlas tracks failure propagation across the entire system, not only model hallucination.

## Foundational / research reasoning

Distribution-blind algorithm ranking; capacity-equals-competence fallacy; compression-as-universal-objective fallacy; optimizer-neutrality assumption; treating confidence as calibrated probability; conflating observation prediction with intervention effects; invoking uncomputable universal ideals as practical algorithms; extrapolating asymptotic/scaling results outside their assumptions; hiding resource costs outside FLOP counts.

## Model-level

Confabulation; brittle generalization; calibration failure; reward hacking; mode collapse; catastrophic forgetting; spurious correlations; representation bottlenecks.

## Learning and adaptation

Catastrophic interference; stability-plasticity deadlock; replay-induced forgetting; self-generated-data feedback collapse; curriculum lock-in; premature consolidation; permanent memorization of transient noise; test-time drift; adapter/skill proliferation; conflicting local adaptations; reward/evaluator exploitation; loss of rare capabilities during distillation; synthetic-data mode loss; stale knowledge preserved after regime change; learning the wrong substrate/timescale; opaque unprovenanced parameter mutation.

## Inference-time intelligence

Overthinking; premature stopping; greedy-path lock-in; search explosion; correlated samples mistaken for independent evidence; verifier gaming; bad branch pruning; recursive fan-out; lossy subagent summaries; duplicated worker effort; aggregation bottlenecks; tool misuse; stale/untrusted tool output; retry loops; context flooding; harness overfitting; runtime self-modification regression; consensus of correlated agent errors; external-context retrieval misses; expensive computation with no marginal information gain.

## Persistent intelligence / memory

Write-everything memory bloat; false durable memories; stale facts treated as current truth; event history confused with current belief; temporal scope lost; identity/entity merge or split errors; contradiction accumulation; old preferences/workflows over-applied; semantic-similarity retrieval of irrelevant evidence; retrieval success without correct action use; false reflection/abstraction; provenance destroyed during consolidation; audit evidence deleted during forgetting; memory poisoning; self-reinforcing false memories; obsolete procedure retained after environment change; hidden cross-session contamination.

## Temporal state and world models

Last-observation-as-truth; partial-observability blindness; hidden-state alternatives collapsed too early; action effects not propagated into belief; model bias; omitted decision-relevant variables; reward-predictive but transfer-poor latent state; compounding rollout error; uncertainty collapsed during imagination; simulator exploitation; realistic-looking prediction mistaken for calibrated prediction; stale world model trusted after regime change; same faulty model used as generator and verifier; failure to query reality when model uncertainty dominates.

## Multimodal grounding / embodiment

Cross-modal false binding; modality dominance; disagreement collapsed before uncertainty is resolved; language bottleneck discarding sensor/action precision; stale object identity across views/sessions; semantic transfer without correct physical affordances; action tokenization reducing control fidelity; perception treated as passive when an information-gathering action is available.

## Context and memory

Retrieval misses; irrelevant-context interference; stale state; false memory consolidation; contradiction accumulation; unbounded context growth; provenance loss.

## Reasoning and search

Premature commitment; search explosion; self-confirmation; evaluator overfitting; recursive error amplification; excessive deliberation; failure to stop.

## Agent/harness

Tool misuse; interface mismatch; permission escalation; hidden state divergence; irreversible side effects; retry loops; coordination overhead; subagent duplication; trajectory corruption.

## World-model/simulation

Model bias; compounding rollout error; false counterfactual confidence; distribution shift; simulator exploitation; correlational models used as intervention models.

## Self-improvement

Regression; benchmark overfitting; evaluator gaming; capability loss outside optimization target; unsafe self-modification; irreversible drift; feedback-loop amplification; assigning credit to the wrong mutable layer.

## Systems

Bandwidth bottlenecks; communication domination; cache invalidation; memory fragmentation; tail latency; silent numerical error; hardware-specific overfitting; energy/thermal constraints; lifetime-cost displacement where training savings create much larger inference cost or vice versa.

Each atlas note should identify which of these failure classes it can introduce, amplify, detect or mitigate.
