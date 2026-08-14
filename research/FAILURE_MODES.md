# Failure Modes

The atlas tracks failure propagation across the entire system, not only model hallucination.

## Foundational / research reasoning

Distribution-blind algorithm ranking; capacity-equals-competence fallacy; compression-as-universal-objective fallacy; optimizer-neutrality assumption; treating confidence as calibrated probability; conflating observation prediction with intervention effects; invoking uncomputable universal ideals as practical algorithms; extrapolating asymptotic/scaling results outside their assumptions; hiding resource costs outside FLOP counts.

## Model-level

Confabulation; brittle generalization; calibration failure; reward hacking; mode collapse; catastrophic forgetting; spurious correlations; representation bottlenecks.

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
