# Unresolved Clean-Sheet Design Dimensions

These are axes along which the evidence does not yet justify a single choice. They should become controlled experiments or competing architecture candidates later.

## D01 — Direct addressability ↔ compressed state

Keep detailed prior items directly retrievable, compress history into bounded state, or combine both.

Trade-offs: exact recall, interference, state growth, decode cost, locality, transfer.

## D02 — Centralized controller ↔ distributed/local control

One global operation allocator versus many local controllers coordinating through sparse signals.

Trade-offs: global consistency, communication, robustness, modularity, latency, credit assignment.

Biological evidence makes local control plausible; agent/harness evidence shows system-level scheduling can add value. No universal split is established.

## D03 — Homogeneous computation ↔ heterogeneous specialists

Repeated shared mechanism versus functionally distinct operators/models/tools.

Trade-offs: transfer and simplicity versus specialization and conditional efficiency; routing/communication overhead.

## D04 — Human-readable ↔ machine-native internal representation

Natural language/symbols versus latent/structured/executable codes.

Trade-offs: inspectability/interoperability versus bandwidth, ambiguity, serialization cost and representational freedom.

## D05 — Parametric integration ↔ external editable state

Embed information/procedures into shared parameters versus keep them in explicit memory/skills/tools.

Trade-offs: low-latency reuse and generalization versus updateability, provenance, capacity and interference.

## D06 — One persistence timescale ↔ hierarchical timescales

Uniform learning/memory lifetime versus fast tentative state plus slower consolidation/stability.

Trade-offs: simplicity versus rapid adaptation, rollback and continual-learning interference.

## D07 — Global end-to-end credit ↔ local/factorized credit

Backpropagate/optimize through the entire differentiable system versus local eligibility, modular evaluators, black-box feedback or hybrid credit.

Trade-offs: dense precise signals versus memory/communication/architecture flexibility.

## D08 — Reactive amortized policy ↔ explicit test-time computation

Direct learned response versus reasoning/search/simulation/tool use.

Trade-offs: latency/cost versus adaptability, verification and hard-problem performance.

## D09 — Sequential refinement ↔ branching/population search

One evolving trajectory versus multiple competing alternatives.

Trade-offs: coherent state and reuse versus escaping early commitments/diversity; aggregation/evaluation cost.

## D10 — Fixed compute ↔ adaptive compute

Uniform depth/time versus difficulty/uncertainty-conditioned compute.

Trade-offs: predictable execution versus resource efficiency; requires reliable stopping/value-of-computation estimation.

## D11 — One current belief ↔ multiple hypotheses

Maintain one best state estimate versus a distribution/set of plausible states.

Trade-offs: action simplicity versus robustness under partial observability and ambiguity.

## D12 — Reconstructive world model ↔ decision-sufficient predictive state

Model broad sensory detail versus only variables needed for current planning.

Trade-offs: transfer/general future goals versus efficiency; objective-relative information loss.

## D13 — Passive perception ↔ active information gathering

Consume available observations versus choose sensors/queries/probes/actions to reduce uncertainty.

Trade-offs: interaction cost/risk versus state-estimation quality.

## D14 — Uniform precision ↔ information-sensitive precision

One numeric fidelity across system versus state/component-specific precision.

Trade-offs: simplicity/stability versus memory/energy/bandwidth efficiency and error accumulation.

## D15 — Semantic routing ↔ physical routing coupling

Bind specialists to fixed hardware/topology versus choose semantic task assignment separately from placement/scheduling.

Trade-offs: runtime simplicity versus topology-aware efficiency and dynamic load balance.

## D16 — Fixed architecture ↔ developmental/generative structure

Directly specify mature computation graph versus generate structure from compact rules/local growth/search.

Trade-offs: precision and mature optimization versus evolvability/search-space compression/adaptation.

## D17 — Immediate durable learning ↔ staged consolidation

Put new information directly into long-lived shared state versus keep it reversible until repeated validation/reuse.

Trade-offs: rapid integration versus false-memory/interference/rollback risk.

## D18 — Append-only history ↔ revised active memory

Never alter stored records versus maintain supersession/derived current state while retaining audit evidence.

Trade-offs: provenance simplicity versus stale-state/retrieval correctness.

## D19 — Similarity retrieval ↔ decision-value retrieval

Retrieve nearest representation versus memories expected to improve current action.

Trade-offs: generality/simplicity versus task-specific causal/temporal/procedural relevance.

## D20 — Learned evaluator ↔ deterministic/formal checker

Flexible semantic judgment versus narrow high-assurance verification.

Trade-offs: coverage versus exploitability/specification cost.

## D21 — Outcome verification ↔ process/state-transition verification

Check final result versus intermediate operations/invariants.

Trade-offs: representation freedom/cost versus localization/credit/early containment.

## D22 — Learned safety policy ↔ externally enforced capability boundaries

Rely on behavioral training versus permissions/sandbox/transaction rules outside the cognitive model.

Trade-offs: flexibility versus harder guarantees; likely hybrid, but boundary unresolved.

## D23 — Transparent evaluator/tests ↔ hidden/independent checks

Expose acceptance criteria for debuggability versus preserve holdouts to detect Goodhart/overfit.

Trade-offs: repair efficiency versus evaluator gaming.

## D24 — Greedy self-improvement ↔ population/archive evolution

Maintain one best lineage versus retain diverse alternatives/stepping stones.

Trade-offs: simplicity/storage versus local-optimum/regression resilience.

## D25 — Local patching ↔ broad structural mutation

Repair nearest editable layer versus escalate to weights/architecture/mutation rules.

Trade-offs: reversibility/cheap validation versus transfer, patch debt and systemic bottlenecks.

## D26 — Immutable trusted root ↔ evolvable assurance system

Keep control/evaluation immutable versus allow improvement with a higher-level migration protocol.

Trade-offs: stable authority versus obsolescence/bottleneck; circular self-approval risk.

## D27 — One scalar objective ↔ constrained/multi-objective utility

Collapse quality/cost/safety/etc. into one fitness versus maintain explicit constraints/Pareto trade-offs.

Trade-offs: simple optimization versus proxy gaming and preference ambiguity.

## D28 — Synchronous global steps ↔ asynchronous/event-driven computation

Lockstep execution versus independently triggered modules/state updates.

Trade-offs: coordination simplicity versus locality, latency and sparse activity.

## D29 — Training-time optimization ↔ deployment-time adaptation

Freeze after training versus continue updating state/parameters/tools during use.

Trade-offs: stability/reproducibility versus adaptation to current environment.

## D30 — Software-defined ↔ hardware/co-designed primitives

Implement general abstractions on standard accelerators versus design computation/state representation jointly with physical substrate.

Trade-offs: portability/development velocity versus efficiency/locality/energy.

---

## How these dimensions should be used

Do not choose one side philosophically. Construct matched experiments that vary one dimension while controlling task, total resources and evaluator quality. Where interactions are strong, use factorial experiments rather than isolated benchmark comparisons.

A clean-sheet architecture should remain a *set of competing candidates* wherever these dimensions are unresolved.
