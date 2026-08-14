# Clean-Sheet Unresolved Choices

**Phase 8 — implementation names removed. These are experimental dimensions, not decisions.**

The evidence constrains the problem but does not select one point on the following axes. Phase 9 must preserve multiple candidates wherever these choices materially change behavior/cost.

| ID | Design dimension | Endpoint A | Endpoint B | Main discriminators |
|---|---|---|---|---|
| U01 | History access | detailed past items remain directly addressable | history is compressed into bounded evolving state | exact recall, interference, state growth, decode cost, transfer |
| U02 | Control organization | one/global operation allocator | distributed local allocators with coordination | global coherence, latency, communication, robustness, single-point failure |
| U03 | Computational uniformity | one broadly shared computation type | heterogeneous specialized computation types | transfer, specialization, routing cost, optimization complexity |
| U04 | Internal representation | human-readable/discrete external-style state | machine-native latent/structured/executable state | bandwidth, ambiguity, auditability, compatibility, task utility |
| U05 | Knowledge integration | deeply integrated durable learned state | editable addressable external knowledge/procedures | latency, updateability, provenance, capacity, interference |
| U06 | Adaptation lifetime | one dominant update timescale | hierarchy of fast tentative and slower durable state | adaptation speed, rollback, interference, complexity |
| U07 | Credit propagation | globally propagated end-to-end credit | local/factorized/hybrid credit signals | signal quality, memory, modularity, nondifferentiable boundaries |
| U08 | Inference style | direct amortized response | explicit task-time computation/search/simulation | latency, hard-problem quality, adaptability, verification |
| U09 | Alternative management | one sequential evolving trajectory | branching/population of competing trajectories | diversity, coherence, evaluator cost, parallelism |
| U10 | Compute budget | fixed effort per input | uncertainty/difficulty-conditioned effort | predictability, efficiency, stopping reliability |
| U11 | Belief representation | one best current state | multiple weighted/plausible hypotheses | action simplicity, ambiguity robustness, state cost |
| U12 | Predictive representation | broad reconstructive state | compact decision-sufficient predictive state | efficiency, transfer when goals change, missing-variable risk |
| U13 | Observation policy | passive use of available evidence | active queries/probes/actions to reduce uncertainty | interaction cost, risk, state-estimation quality |
| U14 | Numeric/information fidelity | uniform fidelity | state/operation-dependent fidelity | stability, energy, bandwidth, accumulated error |
| U15 | Semantic vs physical routing | task specialization tied closely to placement | task assignment separated from physical scheduling | locality, load balance, routing complexity |
| U16 | Structural specification | mature computation explicitly specified | structure generated/adapted from compact developmental rules | search efficiency, controllability, modularity, evolvability |
| U17 | Durability policy | new evidence integrated durably immediately | staged tentative state then consolidation | learning speed, false updates, rollback, reuse |
| U18 | Persistent truth management | append history and derive current state later | actively maintain supersession/revision links/current active records | audit simplicity, stale-state avoidance, maintenance cost |
| U19 | Retrieval objective | representational similarity/general relevance | expected downstream decision value | generality, temporal/causal relevance, learned retrieval cost |
| U20 | Evaluator type | broad learned/subjective judgement | narrow deterministic/mechanically checked property | coverage, exploitability, formalization cost |
| U21 | Verification granularity | final-outcome checking | intermediate state/transition checking | representation freedom, error localization, verification cost |
| U22 | Behavior constraints | learned behavioral policy carries most constraints | external authority/capability enforcement carries most constraints | flexibility, hard boundaries, attack robustness, friction |
| U23 | Acceptance transparency | candidate sees most acceptance criteria | material hidden/independent acceptance evidence | debuggability, overfitting/Goodhart risk |
| U24 | Improvement lineage | one incumbent replaced greedily | archive/population of alternative system variants | simplicity, storage, stepping stones, regression resilience |
| U25 | Repair scope | prefer local/reversible patches | prefer broad integrated structural changes | validation cost, transfer, patch debt, systemic bottlenecks |
| U26 | Assurance evolution | stable protected acceptance root | assurance/control system itself can migrate/evolve | authority continuity, obsolescence, circular approval risk |
| U27 | Objective representation | one scalarized fitness/reward | structured constraints/preferences/Pareto alternatives | optimization simplicity, ambiguity, proxy gaming |
| U28 | Scheduling style | globally synchronized steps | asynchronous/event-driven operations | coordination, locality, sparse activity, race/state complexity |
| U29 | Adaptation boundary | most durable learning happens offline/before use | ongoing deployment-time adaptation | reproducibility, environment fit, drift, containment |
| U30 | Physical abstraction | computation designed mostly independently of hardware | computation/state co-designed with physical substrate | portability, efficiency, energy, development complexity |
| U31 | Interface stability | components share tightly coupled internal state | components communicate through stable typed contracts | efficiency, self-improvement compatibility, modularity |
| U32 | Audit representation | computation itself is directly inspectable | separate machine computation and lower-bandwidth audit evidence | performance, faithfulness, verification burden |
| U33 | Allocation policy | fixed engineered heuristics | learned resource/value policy | predictability, distribution shift, efficiency, exploitability |
| U34 | Allocation hierarchy | all major decisions share one controller | local policies with escalation to higher-level control | meta-control cost, coordination, robustness |
| U35 | Objective uncertainty | commit early to one interpreted goal | maintain uncertainty/alternatives and clarify when valuable | decisiveness, user interaction cost, misalignment risk |
| U36 | Exact vs approximate state | broad approximate semantic state | explicit exact substate for identifiers/formal/tool interfaces | efficiency, correctness at exact boundaries, complexity |
| U37 | Evidence retention | keep source evidence broadly for correction | aggressively consolidate/discard source detail | storage, provenance, future-goal optionality |
| U38 | Self-improvement target search | diagnose among a fixed set of mutation surfaces | mutation process can invent/restructure mutation surfaces | controllability, open-endedness, assurance complexity |

## Choice protocol

For each design dimension Phase 9 should record:

1. which required functions depend on it;
2. which invariants constrain it;
3. expected resource trade-offs;
4. at least two mechanistically distinct candidate choices when evidence remains unresolved;
5. an experiment that could change the preference;
6. what evidence would falsify the selected choice.

## Interaction warning

Several dimensions strongly interact. Examples:

- distributed control × communication representation × physical scheduling;
- multiple hypotheses × memory capacity × active information acquisition;
- machine-native representation × auditability × self-improvement compatibility;
- deployment adaptation × assurance × persistent-state governance;
- population self-improvement × evaluator independence × resource budget.

Therefore Phase 9 should avoid pretending every axis can be selected independently. Candidate architectures should be coherent bundles whose interactions can be tested.
