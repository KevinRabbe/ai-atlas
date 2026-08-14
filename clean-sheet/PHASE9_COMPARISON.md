# Phase 9 Candidate Architecture Comparison

**No winner is selected.** This document states expected trade-offs and what evidence would be needed to change them.

Candidates:

- **A — Hierarchical Adaptive System**: explicit hierarchical resource/assurance allocation around specialized processes.
- **B — Distributed Event-Driven Ecology**: local adaptive processes with sparse event communication and limited global cognition.
- **C — Integrated Predictive Core + External Evidence**: tightly integrated cognitive state with explicit evidence/authority boundaries.
- **D — Developmental Variant System**: structure itself can grow/reorganize through versioned variant search.

## 1. Organization matrix

| Dimension | A Hierarchical | B Distributed | C Integrated | D Developmental |
|---|---|---|---|---|
| Cognitive coordination | explicit hierarchy | local/event-driven | mostly implicit/shared-state | generated/evolving |
| Computational heterogeneity | high, explicit | high, local/emergent | lower internally | variable/emergent |
| Global current state | compact meta/belief state | partial/distributed | strong compact shared state | depends on current phenotype |
| Persistent evidence | explicit shared | explicit shared fabric | external to core | explicit across variants |
| Interface boundaries | many typed boundaries | sparse typed boundaries | few internal boundaries | changing/versioned boundaries |
| Ordinary-task critical path | medium | low if local | potentially lowest | phenotype-dependent |
| Communication demand | medium | low-to-variable | low internally | variable/high during reorganization |
| Attribution/debuggability | medium-high | medium/low | lowest internally | medium via lineage, hard within phenotype |
| Failure blast radius | hierarchy can propagate | often local | potentially broad | variant-isolated before activation |
| Adaptation scope | routed hierarchy | local-first | integrated state/weights | state through structure/meta-rules |
| Self-improvement style | diagnosed scoped mutation | local mutation + topology escalation | external gated core update | population/structural search |
| Physical locality potential | medium-high | high | high inside core | potentially highest/adaptive |
| Assurance integration | explicit | explicit global boundary | external boundary | strongest outer transaction needed |
| Complexity/engineering burden | high | high | lowest initial | highest |

## 2. Expected strengths

### Candidate A

Expected strongest when:

- tasks vary widely in difficulty/tool needs;
- explicit assurance and resource routing have high value;
- specialized capabilities are heterogeneous;
- coordination decisions can be made from compact meta-state;
- diagnosis/traceability matters.

### Candidate B

Expected strongest when:

- locality and sparse activity dominate physical cost;
- tasks decompose naturally into event-driven subproblems;
- global synchronization is expensive;
- graceful degradation and local specialization matter;
- local state can solve most problems without dense global exchange.

### Candidate C

Expected strongest when:

- many cognitive functions benefit from shared representation;
- ordinary tasks require dense cross-feature interaction;
- communication/interface overhead would dominate modular designs;
- compact evolving state is sufficient for common decisions;
- external evidence access can repair occasional information loss.

### Candidate D

Expected strongest when:

- task/resource distributions change substantially over long lifetimes;
- fixed organization repeatedly accumulates patch debt;
- evaluator quality is strong enough to guide structural search;
- alternative lineages provide future stepping-stone value;
- physical platform/task regularities reward specialization/co-adaptation.

## 3. Expected weak regimes

### Candidate A

Likely weak when meta-control becomes a serial bottleneck, allocation is hard to predict from compact state, or component interfaces dominate data movement.

### Candidate B

Likely weak when tasks require dense global reasoning/state, local processes share hidden correlated errors, or communication/protocol reconciliation approaches the cost of a global state.

### Candidate C

Likely weak under continual multi-domain mutation, exact/provenance-heavy tasks, high need for diagnosis, or problems requiring computational forms poorly represented by the integrated substrate.

### Candidate D

Likely weak when environment is stable enough that structural change has little value, evaluator/assurance is expensive, or architecture churn/migration dominates gains.

## 4. Invariant pressure matrix

`easy` means the organization makes the invariant natural; `pressure` means explicit compensating design is likely required.

| Invariant family | A | B | C | D |
|---|---|---|---|---|
| Evidence vs belief separation | easy | easy | pressure inside core | easy externally |
| Authority/data separation | easy | easy | easy externally | easy if outer root protected |
| Uncertainty scope | easy | pressure across messages | pressure inside core | pressure across variants |
| Version/interface compatibility | easy-medium | pressure | easy internally | strongest pressure |
| Capability/authority separation | easy | easy | easy externally | easy externally |
| Scoped verification | easy | easy | easy externally | easy but expensive |
| Bounded open-ended compute | easy | pressure distributed | easy | strongest pressure |
| Rollback/version lineage | easy | medium | easy for core versions | natural/essential |
| Mechanism ablation/falsification | medium | medium | harder | natural via variants |
| Physical resource accounting | medium | natural | natural internally | difficult but adaptable |

## 5. Learning/adaptation comparison

### A: routed multi-timescale learning

The system explicitly chooses whether evidence belongs in working state, persistent knowledge, procedure, shared learned structure or structural candidate.

**Risk:** change-router becomes a bottleneck or encodes wrong persistence priors.

### B: local-first learning

Processes update local state and communicate/globalize changes only when evidence indicates broader value.

**Risk:** useful global transfer may be missed; local adaptations can become inconsistent.

### C: integrated adaptation

Fast state and durable core learning reuse shared representations; external evidence retains correction/provenance.

**Risk:** broad interference and hidden attribution.

### D: multi-level developmental adaptation

Local state, procedures, components, topology and developmental rules can all change.

**Risk:** difficult causal attribution and assurance scaling.

## 6. Representation comparison

### A

Typed interfaces encourage explicit contract boundaries. Payload format can vary by specialist.

### B

Local representations can differ substantially; messages need compact stable semantics.

### C

Shared internal representation maximizes integration but increases coupling and audit opacity.

### D

Representations/interfaces may evolve; requires strongest version compatibility/migration mechanisms.

## 7. Persistent-state comparison

All candidates retain external evidence/provenance because Phase-8 invariants require it for consequential state. They differ mainly in the **active current-state organization**:

- A: shared compact belief/meta-state plus specialist local state;
- B: distributed overlapping local beliefs with selective shared state;
- C: one strongly integrated compact current state;
- D: phenotype-defined mixture that can change across versions.

This makes current-state structure one of the highest-value experimental axes.

## 8. Self-improvement comparison

| Candidate | Default mutation scope | Structural change | Alternative lineages |
|---|---|---|---|
| A | diagnosed local/hierarchical component | rare/escalated | retained when uncertainty high |
| B | local process/interface | topology change after repeated coordination failures | local variants plausible |
| C | shared core or external procedure | rare and expensive | core versions retained transactionally |
| D | any level including developmental rules | central feature | explicit population/archive |

## 9. No candidate dominates all resource regimes

The Phase-8 resource model predicts crossovers rather than one universal winner.

Examples:

- expensive communication favors B/C over A if specialization does not compensate;
- expensive repeated reasoning but cheap storage favors stronger consolidation/integration;
- rapidly changing environments favor editable/distributed state over deep durable integration;
- abundant parallel hardware can favor branching/populations;
- scarce verification makes D harder to justify;
- strict auditability can favor A over opaque integration.

## 10. Hybrid candidates are allowed only after experiments

Likely useful hybrids exist—for example integrated local cores inside a distributed hierarchy—but Phase 9 should not immediately combine every strength. That would recreate architecture soup and make attribution impossible.

Hybridization rule:

1. identify a measured failure of one candidate;
2. identify a mechanism from another candidate that specifically addresses it;
3. add only that mechanism;
4. re-run matched ablation/resource tests;
5. retain the hybrid only if net lifetime utility improves.

## 11. Initial preference state

**No global preference.**

Research prior only:

- A is the clearest baseline for explicit system-level allocation/assurance;
- B is the strongest locality/distribution counter-hypothesis;
- C is the strongest integration/simplicity counter-hypothesis;
- D is the strongest long-horizon structural-adaptation counter-hypothesis.

The purpose of Phase 10 is to make at least some of these disagreements empirical.
