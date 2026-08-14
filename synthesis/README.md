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

**First cross-domain synthesis completed on 2026-08-14.**

Current synthesis artifacts:

- [`CROSS_DOMAIN_SYNTHESIS.md`](CROSS_DOMAIN_SYNTHESIS.md) — recurring principles and falsifiable meta-hypothesis.
- [`REQUIRED_FUNCTIONS.md`](REQUIRED_FUNCTIONS.md) — 25 implementation-neutral functions the eventual system must address; explicitly not a module list.
- [`DESIGN_DIMENSIONS.md`](DESIGN_DIMENSIONS.md) — unresolved axes to test rather than choose philosophically.
- [`ANTI_ASSUMPTIONS.md`](ANTI_ASSUMPTIONS.md) — contemporary implementation habits that must not become axioms.
- [`HIGH_VALUE_OPEN_QUESTIONS.md`](HIGH_VALUE_OPEN_QUESTIONS.md) — uncertainty-removal priorities.

Two high-value gaps identified by the synthesis received focused evidence passes before clean-sheet restatement:

- machine-native representation & communication;
- objective uncertainty & metareasoning/resource-rational control.

## Current organizing hypothesis

Evidence is consistent with a system that adaptively selects state transitions and allocates:

- computation;
- information;
- durable change;
- assurance;
- exploration/design effort;

under uncertain world state, uncertain objectives, finite physical resources and consequence-dependent risk.

This remains a falsifiable organizing hypothesis, **not** the definition of intelligence and not an architecture decision.

## Remaining synthesis questions

- Should allocation/control be centralized, distributed, hierarchical or mostly implicit?
- Which required functions benefit from shared mechanisms and which need isolation?
- How should uncertainty compose across heterogeneous modules?
- How should decision-sufficient representations preserve optionality for unknown future goals?
- What system-level resource/capacity metric should replace parameter count?
- How should a trusted assurance system itself migrate/improve without circular approval?
- Can value-of-computation/change/assurance be estimated cheaply enough to outperform fixed heuristics?

## Gate to architecture design

Before architecture candidates are selected, Phase 8 must restate the requirements **without implementation vocabulary**. Only then should competing designs be derived.
