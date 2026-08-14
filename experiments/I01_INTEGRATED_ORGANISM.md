# I01 — First Integrated Epistemic Organism

**Status: first composition experiment implemented; 5/5 local tests pass; 30-seed mixed-stream sweep complete.**

## Purpose

The earlier Phase-10 experiments isolated one design question at a time. I01 changes the research strategy: several selected principles now have to coexist inside one state-transition loop, so failures can arise from their interactions rather than from one mechanism in isolation.

This is **not** a miniature production AI and it does not select Phase-9 architecture A/B/C/D.

## One common state-transition kernel

The organism uses one shared representation for:

- exact task/domain/source identity and provenance;
- current evidence and uncertainty;
- tentative versus durable knowledge;
- rejected hypotheses;
- optional operation proposals;
- shared resource capacities;
- durable evidence links.

It does not instantiate eleven named modules. Different operations are selected against the same epistemic state and resource ledger.

## Mixed environment

Each run contains 400 batches × 12 tasks by default.

The stream interleaves:

1. **application tasks with memory conflicts**
   - an exact surface/topic match may be stale and wrong;
   - a deeper applicability/causal record is current and correct but costs a scarce retrieval slot;

2. **ambiguous action tasks**
   - a noisy signal supports two competing actions;
   - wrong commitment can be much more costly than abstaining;
   - an exact external probe is available at a price and under shared capacity;

3. **frontier/research tasks**
   - the bootstrap corpus has no durable answer for some domains;
   - a candidate rule can be correct or wrong;
   - the visible evaluator can falsely approve wrong candidates;
   - independent verification is scarce;
   - durable discoveries are reused by later application tasks, so a false consolidation can contaminate future behavior.

The same batch may request retrieval, observation and verification simultaneously, forcing cross-resource/scarcity decisions.

## Full organism policies exercised

The full variant operationalizes the currently selected principles most relevant to this environment:

- exact typed identity/provenance fields;
- plurality/safe action under high-consequence ambiguity;
- value-driven probing;
- applicability-aware retrieval;
- staged independent verification before durable knowledge;
- evidence-linked durable records;
- value-ranked operation selection;
- joint allocation under shared resource capacities;
- local durable domain knowledge with shared operation semantics.

State-breadth adaptation is tested separately by E08B and will be merged into the next integrated generation after this baseline composition checkpoint.

## Ablations

I01 compares the full organism against one change at a time:

- `no_plurality` — always commit to the best current action;
- `no_active_information` — never buy exact probes;
- `similarity_retrieval` — use surface/exact-topic retrieval instead of applicability checking;
- `immediate_consolidation` — promote visible-evaluator-approved discoveries directly into durable knowledge;
- `independent_allocation` — tasks request scarce operations first-come instead of being ranked jointly by expected gain.

All variants see the same generated task stream for a given seed.

## Local validation

`5/5` tests pass:

- full staging produces zero false durable writes while immediate consolidation produces false knowledge;
- applicability-aware retrieval reduces memory errors under stale conflicts;
- plurality improves utility when wrong commitments are expensive;
- joint allocation beats first-come requests under tight resource capacities;
- on the default mixed stream, the full composition beats every one-principle ablation.

## 30-seed sweep

| variant | net utility/task | safe rate | retrieval error | false durable writes/run |
|---|---:|---:|---:|---:|
| **integrated full** | **2.3589** | 0.0334 | 0.0124 | **0.0** |
| no plurality | 2.3418 | 0.0000 | 0.0252 | 0.0 |
| no active information | 2.0879 | 0.1713 | 0.0437 | 0.0 |
| similarity retrieval | 1.9437 | 0.0020 | 0.1079 | 0.0 |
| immediate consolidation | 1.8541 | 0.0332 | 0.0123 | **54.6** |
| independent allocation | 2.2756 | 0.0450 | 0.0086 | 0.0 |

The full organism averages roughly:

- `0.248` deep retrieval operations/task;
- `0.196` probes/task;
- `0.072` independent verifications/task;
- `0.434` of application decisions served from durable learned knowledge after it has been acquired.

## Interaction findings

### 1. Discovery governance has downstream value

Immediate consolidation does not merely create a bad research score. False durable rules are reused later, so evaluator mistakes become persistent behavioral errors. Independent verification prevents that contamination in the tested environment.

### 2. Better retrieval can reduce pressure on other resources

Applicability-aware retrieval resolves many known-domain decisions cheaply. When that path is removed, the organism substitutes toward expensive probes, demonstrating an interaction between PS-011 retrieval and PS-010 cross-resource substitution.

### 3. Plurality and active information are complementary

Without a probe slot, plurality can avoid some catastrophic commitments by choosing the safe action. With available evidence acquisition, the system can instead resolve ambiguity and act. Therefore `maintain alternatives` and `buy information` are not competing features; they occupy different points on the same uncertainty/resource frontier.

### 4. Local intelligence can worsen global allocation

The first-come/independent allocator uses the same task-local expected gains as the full system but cannot rank requests across tasks. Under scarce capacities it spends slots on lower-value tasks while higher-value tasks arrive later. This reproduces the E22B lesson inside a mixed epistemic environment.

## What I01 does not establish

- It does not prove all current principles compose without regressions in larger systems.
- It does not actively test adaptive state breadth, learned sharing, credit assignment, physical execution, or self-improvement.
- Its expected-value estimates are hand-specified from benchmark reliabilities rather than learned online.
- Its independent verifier is exact by construction.

Those are deliberate limitations for the first integration checkpoint.

## Next integrated generation

I02 should add:

1. E08B adaptive hot-state breadth;
2. learned rather than known operation-quality/value estimates;
3. conditional shared/private estimators from PS-009;
4. non-exact/correlated verification so assurance itself must be allocated;
5. resource-price and environment shifts inside one lifetime;
6. interaction ablations that remove pairs of principles, not only one at a time.

The main new research question is now:

> **Which selected principles remain distinct mechanism boundaries after composition, and which collapse into one general uncertainty/resource-allocation mechanism?**
