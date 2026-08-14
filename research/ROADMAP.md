# Research Roadmap

## Phase 0 — Build the map

Define taxonomy, evidence schema, claim IDs, contradiction handling, source standards and clean-sheet rules. **Status: initialized.**

## Phase 1 — Establish the computational substrate

Research foundations, architectures, scaling laws, sparsity/conditional computation, recurrence/state-space approaches, memory hierarchy, hardware constraints and systems efficiency.

**Progress:** Foundations first evidence pass completed on 2026-08-14; not yet saturated. It established provisional constraints around inductive bias, information/relevance, computability/resource bounds, optimization/search, uncertainty, causality/control, credit assignment, representation and joint resource scaling. Next work should deepen Foundations gaps while beginning the architecture/systems evidence map.

Exit condition: we can state which capabilities require which computational properties without assuming Transformer-style attention.

## Phase 2 — Learning and adaptation

Map self-supervised learning, supervised learning, RL/RLVR, preference learning, imitation, distillation, curriculum, continual learning, meta-learning, test-time learning and synthetic data.

Exit condition: clear separation of what belongs in weights versus external state/skills/memory.

## Phase 3 — Inference-time intelligence

Map reasoning traces, search, planning, test-time compute, decomposition, recursion/RLM, tool use, agents, harnesses, multi-agent systems and recursive harnesses.

Exit condition: a compute-allocation model that explains when to solve, search, retrieve, execute, delegate, recurse or verify.

## Phase 4 — Persistent intelligence

Map memory, knowledge, world models, simulation, multimodal perception/action, temporal state, uncertainty and continual adaptation.

## Phase 5 — Verification, reliability and control

Map evaluators, formal methods, tests, reward models, process/outcome supervision, calibration, interpretability, monitoring, containment, robustness and failure propagation.

## Phase 6 — Self-improvement

Map improvement of prompts, context policies, skills, harness code, routing, tools, memory, training data, weights and architecture. Separate timescales and require regression gates.

## Phase 7 — Cross-domain synthesis

Extract implementation-neutral laws, trade-offs, recurring patterns and contradictions. No architecture design yet.

## Phase 8 — Forget implementations

For every required function, restate the problem without names such as Transformer, RAG, CoT, RLM, agent, vector DB, or current product/framework names.

## Phase 9 — Clean-sheet architecture

Derive candidate systems from requirements and evidence. Maintain multiple competing designs where evidence is insufficient.

## Phase 10 — Experimental reconstruction

Build the smallest instrumented research organism capable of testing architectural choices. Existing models may be temporary probes; they are not presumed to be the final cognitive substrate.
