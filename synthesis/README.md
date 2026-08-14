# Synthesis

Synthesis is where findings across atlas domains are combined. It is intentionally separate from both raw research and architecture design.

A synthesis document must:

1. cite/trace the atlas claims/evidence it depends on;
2. distinguish observation from inference;
3. include evidence against its conclusion;
4. state the range of conditions where it is expected to hold;
5. avoid turning a successful implementation into a universal principle;
6. produce implementation-neutral requirements where possible.

Example progression:

`paper result -> mechanism evidence -> cross-domain pattern -> requirement -> clean-sheet candidate`

Not:

`paper result -> add that component to our AI`.

## Phase-7 synthesis state

**First cross-domain synthesis completed on 2026-08-14, with later focused gap closures integrated as they become architecture-relevant.**

Current synthesis artifacts:

- [`CROSS_DOMAIN_SYNTHESIS.md`](CROSS_DOMAIN_SYNTHESIS.md) — recurring principles and falsifiable meta-hypothesis.
- [`DISCOVERY_AND_EPISTEMIC_GROWTH.md`](DISCOVERY_AND_EPISTEMIC_GROWTH.md) — focused synthesis on human knowledge as bootstrap, beyond-teacher supervision, hypothesis/verification lifecycles and expanding the epistemic frontier.
- [`REQUIRED_FUNCTIONS.md`](REQUIRED_FUNCTIONS.md) — 26 implementation-neutral functions the eventual system must address; explicitly not a module list.
- [`DESIGN_DIMENSIONS.md`](DESIGN_DIMENSIONS.md) — unresolved axes to test rather than choose philosophically.
- [`ANTI_ASSUMPTIONS.md`](ANTI_ASSUMPTIONS.md) — contemporary implementation habits that must not become axioms.
- [`HIGH_VALUE_OPEN_QUESTIONS.md`](HIGH_VALUE_OPEN_QUESTIONS.md) — uncertainty-removal priorities.

Focused evidence passes have now closed several high-value synthesis gaps:

- machine-native representation & communication;
- objective uncertainty & metareasoning/resource-rational control;
- discovery & epistemic growth beyond the bootstrap human corpus.

## Current organizing hypothesis

Evidence is consistent with a system that adaptively selects state transitions and allocates:

- computation;
- information;
- durable change;
- assurance;
- exploration/discovery/design effort;

under uncertain world state, uncertain objectives, finite physical resources and consequence-dependent risk.

The discovery extension adds a second long-horizon objective beyond solving current tasks: **reduce meaningful uncertainty and expand the verified shared knowledge frontier when the expected value of doing so exceeds resource/risk cost.**

This remains a falsifiable organizing hypothesis, **not** the definition of intelligence and not an architecture decision.

## Remaining synthesis questions

- Should allocation/control be centralized, distributed, hierarchical or mostly implicit?
- Which required functions benefit from shared mechanisms and which need isolation?
- How should uncertainty compose across heterogeneous modules?
- How should decision-sufficient representations preserve optionality for unknown future goals?
- What system-level resource/capacity metric should replace parameter count?
- How should a trusted assurance system itself migrate/improve without circular approval?
- Can value-of-computation/change/assurance/discovery be estimated cheaply enough to outperform fixed heuristics?
- When should a system retain multiple competing hypotheses rather than collapse to one current belief?
- How should it distinguish genuine frontier expansion from rediscovery of obscure prior knowledge?
- How should empirical experiment selection work when no cheap objective verifier exists?

## Gate to architecture design

Phase 8 already restated the original requirements without implementation vocabulary and passed its exit gate. Later focused synthesis additions must obey the same rule: new functions such as F26 may constrain future experiments, but they do not automatically introduce a component into any architecture family.
