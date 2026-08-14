# Design Ledger

No architectural choice is accepted without a traceable reason.

## Status

**Phase 9 candidate generation complete to first-pass depth. Phase-10 evidence is now updating confidence, but no final architecture selection has been accepted.**

| Decision ID | Design question | Candidates | Selected | Evidence basis | Rejected assumptions | Confidence | Falsifier / decisive experiment |
|---|---|---|---|---|---|---|---|
| DL-001 | control organization | hierarchical allocation / distributed local control / integrated implicit control / developmental organization | unresolved; evidence favors adaptive coordination scope rather than one fixed topology | E01 dependency family + E01B shared-resource contention: sparse/local coupling rewards local execution; deeper dependencies require wider coordination; resource-local arbitration can match global allocation without a universal executive | one global executive is required; decentralization is inherently superior; local autonomy means no coordination | medium provisional principle | E22 must test whether coordination-scope adaptation survives simultaneous substitution among multiple resource classes and learned metacontrol |
| DL-002 | cognitive integration | explicit heterogeneous processes / tightly integrated shared core / emergent structural mixture | unresolved | E02 matched-parameter sweep: sharing helps highly related low-data tasks but introduces interference and loses as task structure diverges | more modules means more intelligence; one block can do everything best | medium that integration should depend on reusable structure; boundary open | second nonlinear/compositional E02 family + matched realized compute |
| DL-003 | history/current-state representation | mostly direct-address evidence / compressed evolving state / hybrid | unresolved | architecture state trade-off + persistent intelligence | context size or bounded state alone solves memory | open | E03 |
| DL-004 | internal reasoning/communication representation | human-readable discrete / continuous machine-native / structured-executable / hybrid | unresolved | focused representation pass + E04 serialization/bandwidth sweep: approximate values, exact identity, versioning and audit have different requirements | human language or any one latent form is universal | medium that representation should be typed by information/interface requirements; implementation open | second E04 task family + learned continuous channel with exact side state |
| DL-005 | inference budget | fixed / heuristic adaptive / learned marginal-value allocation | unresolved | inference + metareasoning evidence | more compute always helps | medium that adaptation can help; mechanism open | E05 |
| DL-006 | belief ambiguity | one best state / multiple hypotheses / adaptive hybrid | unresolved | partial-observability + uncertainty evidence | current state is always a single fact set | open | E06 |
| DL-007 | information acquisition | passive / fixed query / value-driven active acquisition | unresolved | exploration + active perception | perception is only incoming data | medium-high for conditional active value | E07 |
| DL-008 | predictive-state breadth | broad reconstructive / decision-sufficient / hybrid source-recoverable | unresolved | world-model + objective-transfer synthesis | realism or one compact state guarantees generality | open | E08 |
| DL-009 | learning persistence | immediate durable / staged consolidation / learned multi-timescale | unresolved | learning + biology + persistence | one update lifetime is sufficient | medium-high for heterogeneity | E09 |
| DL-010 | credit architecture | global / local-factorized / hybrid | unresolved | foundations + biology + agent-system boundaries | full differentiability is necessary | open | E10 |
| DL-011 | memory retrieval policy | similarity / temporal-causal rules / learned decision value / hybrid | unresolved | persistent-memory benchmarks | nearest representation is best memory | medium-high that task value matters | E11 |
| DL-012 | verification granularity | outcome / process-transition / adaptive hybrid | unresolved | verification evidence | one verification granularity dominates | open | E12 |
| DL-013 | evaluator redundancy | repeated similar evaluators / heterogeneous independent evidence | unresolved implementation; principle favors independence | evaluator/Goodhart synthesis | judge count equals confidence | high principle | E13 |
| DL-014 | capability constraints | behavior-only / external boundaries / hybrid | unresolved; hard boundary retained for consequential actions by invariant | security/control evidence | learned obedience alone is sufficient | high for separation principle | E14 |
| DL-015 | self-improvement lineage | greedy incumbent / bounded archive / population | unresolved | self-improvement/evolution search evidence | current best should erase alternatives | open | E15 |
| DL-016 | repair scope | local patch / isolated durable update / broad structural change | unresolved | mutation attribution + lifetime economics | deepest possible change is best; easiest patch is best | open | E16 |
| DL-017 | mature structure | fixed / directly mutable / developmental-generative | unresolved | biological development + architecture search | mature topology must be fixed or continually changing | low-medium | E17 |
| DL-018 | execution timing | synchronized / asynchronous event-driven / hybrid | unresolved | systems locality + biological/event evidence | global lockstep is required | open | E18 |
| DL-019 | fidelity allocation | uniform / adaptive | unresolved | systems precision + representation granularity | one precision/granularity fits all state | medium | E19 |
| DL-020 | self-change test exposure | transparent / mixed hidden / rotating-adversarial | principle favors independent hidden evidence under repeated optimization | verification/self-improvement evidence | passing visible tests proves improvement | high principle | E20 |
| DL-021 | assurance allocator | implicit cognitive judgment / explicit consequence-sensitive policy / uniform heavy checking | unresolved | Phase-5 assurance synthesis | self-confidence alone or max verification are optimal | medium-high for adaptive assurance | E21 |
| DL-022 | cross-resource metacontrol | independent fixed heuristics / shared adaptive policy / hierarchical hybrid | unresolved | objective/metareasoning synthesis | resources can be optimized independently | open | E22 |

## Current provisional directions

These are **not selected architecture components**. They are evidence-weighted constraints on what the next experiments should attempt to falsify.

- **Control:** coordination scope appears conditional on coupling scope. Local execution remains attractive when interactions are sparse; coordination should emerge at resource/domain/global scope only when dependencies or contention cross those boundaries.
- **Integration:** shared learned state is valuable when structure is reusable, but the same sharing creates an interference surface. The next useful candidates are partially shared mechanisms rather than only the two extremes.
- **Representation:** exact identity, approximate state, protocol metadata and audit/recovery have measurably different fidelity/bandwidth requirements; a homogeneous wire representation is not yet justified.

## Architecture-family status

| Candidate | Status | What it tests |
|---|---|---|
| A — Hierarchical Adaptive System | retain | value/cost of explicit hierarchical allocation and typed specialization |
| B — Distributed Event-Driven Ecology | retain | locality, asynchronous local control and sparse coordination |
| C — Integrated Predictive Core + External Evidence | retain | value of tight cognitive integration and minimal internal interfaces |
| D — Developmental Variant System | retain | value of structural adaptation, indirect organization and variant populations |

## Selection rule

A design decision may move from `unresolved` to `selected for current experimental generation` only after:

1. the relevant experiment(s) run under matched resource/assurance budgets;
2. target benefit survives at least one structurally different task family;
3. the mechanism survives an ablation/failure test aimed at its claimed advantage;
4. resource costs and regressions are reported;
5. the falsifier is updated based on observed evidence.

Selections are version-specific research conclusions, not permanent truths.

## Rule

“Current systems do it this way” is evidence of feasibility, not sufficient evidence of optimality.