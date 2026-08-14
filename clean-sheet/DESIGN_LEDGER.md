# Design Ledger

No architectural choice is accepted without a traceable reason.

## Status

**Phase 9 candidate generation complete to first-pass depth. Phase-10 evidence has now produced three provisional selections for the current experimental generation. No whole architecture family has been selected.**

| Decision ID | Design question | Candidates | Selected | Evidence basis | Rejected assumptions | Confidence | Falsifier / decisive experiment |
|---|---|---|---|---|---|---|---|
| DL-001 | control organization | hierarchical allocation / distributed local control / integrated implicit control / developmental organization | **provisional: coupling-scoped coordination** — keep execution/local decisions local when dependencies are local; introduce explicit resource/domain/global arbitration only at the scope where shared dependencies or scarcity couple decisions | E01 dependency family: local coordination matches global quality cheaply when dependencies are sparse and needs wider propagation as chains densify; E01B contention: resource-local arbitration matches global selection under scarce shared capacity; E22: resource-local bids and compact shared metacontrol make equivalent substitutions while exposing their different communication costs | one global executive is required; decentralization is inherently superior; local autonomy means no coordination; every resource should optimize itself independently | medium-high for the scope principle; concrete topology/dynamic implementation open | create workloads with changing/hidden coupling where a fixed globally centralized or fully local topology consistently beats coupling-scoped coordination under equal latency/communication/quality, or show that estimating coupling costs more than the coordination it saves |
| DL-002 | cognitive integration | explicit heterogeneous processes / tightly integrated shared core / emergent structural mixture | unresolved; evidence favors degree-of-sharing as a variable rather than a binary choice | E02 linear matched-parameter family + E02B compositional family: reusable structure enables transfer; divergence and local repair expose interference; partial sharing can occupy intermediate low-data regimes but currently costs more realized arithmetic | more modules means more intelligence; one block can do everything best | medium-high that integration should follow reusable structure/interference; mechanism boundary open | compute-matched/conditional E02B sharing plus matched latency/communication |
| DL-003 | history/current-state representation | mostly direct-address evidence / compressed evolving state / hybrid | unresolved | architecture state trade-off + persistent intelligence | context size or bounded state alone solves memory | open | E03 |
| DL-004 | internal reasoning/communication representation | human-readable discrete / continuous machine-native / structured-executable / hybrid | **provisional: typed hybrid boundary representation** — preserve exact identity/control fields exactly; allow compact approximate/learned channels for tolerant fields; make version/integrity explicit at changing boundaries; keep human-readable audit off the hot path unless required | E04 flat-state serialization + bandwidth sweep + E04B search/backtracking state + learned quantized/exact-side channel + score distribution shift + corruption/version tests | human language is the universal machine representation; one latent format should carry exact identity, approximate state, protocol metadata and audit equally well | medium-high for the principle; concrete codecs/latent formats remain open | a homogeneous representation matches or beats typed hybrid utility, exact-field semantics, protocol evolution and failure detection under equal bandwidth/compute without recreating typed side channels implicitly |
| DL-005 | inference budget | fixed / heuristic adaptive / learned marginal-value allocation | unresolved | inference + metareasoning evidence | more compute always helps | medium that adaptation can help; mechanism open | E05 |
| DL-006 | belief ambiguity | one best state / multiple hypotheses / adaptive hybrid | unresolved | partial-observability + uncertainty evidence | current state is always a single fact set | open | E06 |
| DL-007 | information acquisition | passive / fixed query / value-driven active acquisition | unresolved | exploration + active perception | perception is only incoming data | medium-high for conditional active value | E07 |
| DL-008 | predictive-state breadth | broad reconstructive / decision-sufficient / hybrid source-recoverable | unresolved | world-model + objective-transfer synthesis | realism or one compact state guarantees generality | open | E08 |
| DL-009 | learning persistence | immediate durable / staged consolidation / learned multi-timescale | **provisional: reversible staging plus adaptive persistence timescales** — new evidence should not become globally durable immediately by default; consolidation threshold/lifetime should respond to estimated environmental stability | E09 noisy regime stream shows staging reduces false durable churn at an adaptation-delay cost; E09B hidden-volatility stream adapts threshold from observation history and reaches ~0.968 accuracy with ~4.2 false durable updates versus ~18.1 for the similarly accurate aggressive fixed policy | one global update lifetime is sufficient; durability threshold should be constant; immediate writes maximize useful learning | medium-high for adaptive multi-timescale persistence; volatility estimator/consolidation algorithm open | vary observation reliability independently of true volatility and show that adaptive timescale control cannot separate noise from change or loses lifetime utility to a fixed policy across regimes |
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
| DL-022 | cross-resource metacontrol | independent fixed heuristics / shared adaptive policy / hierarchical hybrid | unresolved; first E22 family favors adaptive substitution over frozen resource economics while compact shared and resource-local bid implementations trade state locality against message cost | E22: learned per-task resource quality + current prices produces post-shift regret ~0.032 vs ~0.505 when resource economics are frozen; resource-local bids match selection quality but add ~4.84 messages/task | resources can be optimized independently; compute budget can be chosen without considering memory/observation/verification substitutes | medium after one task family | second E22 family with simultaneous resource capacity contention + quality drift + learned price/value estimation |

## Provisional selections

These are **version-specific experimental constraints, not declarations of final architecture**.

### PS-001 — typed hybrid boundary state (from DL-004)

A boundary message/state should not force all information into one fidelity or interpretability regime. Exact identity/control/provenance semantics remain exact; tolerant numerical state may use compact approximate learned representations; version/integrity semantics remain explicit. Human-readable views are generated when audit/communication requires them rather than serving as the mandatory internal hot path.

### PS-002 — staged, adaptive persistence (from DL-009)

Evidence should normally enter reversible/tentative state before globally durable mutation. The required evidence/lifetime should adapt to estimated volatility and confidence. Stable environments justify stronger consolidation thresholds; rapidly changing environments justify faster reversible adaptation. The estimator and storage implementation remain experimental.

### PS-003 — coupling-scoped coordination (from DL-001)

Local operations need not report through one permanent global executive, but coupled decisions must share enough state to respect their common dependency/resource constraint. Coordination scope should therefore expand and contract with the observed coupling graph: local → resource/domain → broader coordination only when the interaction actually crosses those boundaries.

This is deliberately compatible with hierarchical and distributed implementations. The selected object is the **scope rule**, not a fixed controller topology.

## Current provisional directions

- **Control:** E01/E01B/E22 now support PS-003: local execution plus coupling-scoped arbitration rather than universal centralization or universal independence.
- **Integration:** shared learned state is valuable when structure is reusable, but the same sharing creates an interference surface. Two task families support treating degree of sharing as adaptive; compute-matched conditional sharing is the next discriminator.
- **Representation:** two task families support typed boundary semantics rather than one universal wire representation. This is PS-001.
- **Persistence:** constant-timescale staging shows a stability/plasticity trade-off and hidden-volatility adaptation improves that frontier. This is PS-002.
- **Cross-resource allocation:** E22 strongly supports adaptive substitution, but DL-022 remains open until a second resource-allocation family introduces shared capacity and quality drift.

## Architecture-family status

| Candidate | Status | What it tests |
|---|---|---|
| A — Hierarchical Adaptive System | retain | value/cost of explicit hierarchical allocation and typed specialization |
| B — Distributed Event-Driven Ecology | retain | locality, asynchronous local control and sparse coordination |
| C — Integrated Predictive Core + External Evidence | retain | value of tight cognitive integration and minimal internal interfaces |
| D — Developmental Variant System | retain | value of structural adaptation, indirect organization and variant populations |

No family is selected because PS-001/002/003 can all be implemented by multiple families.

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