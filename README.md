# AI Atlas

A research atlas for reconstructing artificial intelligence from first principles.

The repository does **not** assemble today's AI stack by habit. It extracts mechanisms, evidence, constraints and failures; deliberately forgets implementation assumptions; derives competing clean-sheet organizations; and tests them experimentally.

## Core rule

> Learn from implementations. Do not inherit their assumptions automatically.

Transformers, agents, RAG, databases, JEPA, world models, natural-language reasoning, biological mechanisms, verifier products, current hardware and other named implementations are evidence/candidates—not axioms.

## Current state

- Phases 0–7 evidence/synthesis: first-pass complete.
- Phase 8 implementation forgetting: **PASS**.
- Phase 9 competing architecture generation: **PASS**.
- Phase 10 experimental reconstruction: **active**.

Phase 10 currently contains **522 added semantic test cases** and **27 provisional implementation-neutral principles (`PS-001` through `PS-027`)**.

No fixed Phase-9 architecture family A/B/C/D is selected as one universal whole-system architecture. Their useful behaviors increasingly appear as conditional organizational modes that can coexist at different scopes and timescales.

See:

- `experiments/STATUS.md` — current experimental checkpoint;
- `clean-sheet/DESIGN_LEDGER.md` — principle/evidence ledger through PS-026;
- `clean-sheet/PS027_SELECTION_AWARE_EVIDENCE.md` — PS-027 promotion addendum;
- individual `experiments/*.md` notes for measurements/falsifiers.

## What the experiments are converging toward

A smaller set of recurring laws keeps reappearing across unrelated tasks:

- **scope follows coupling / causal responsibility**;
- **state follows expected future value and recoverability**;
- **optional work follows marginal value under shared scarcity**;
- **sharing follows reusable regularity; isolation follows interference**;
- **execution follows events until consistency coupling earns synchronization**;
- **fidelity follows sensitivity and consequence**;
- **authority follows explicit current invariants, not confidence**;
- **durability raises the evidence requirement**;
- **verification targets the remaining failure layer**;
- **consequential multi-step change separates preparation from publication**;
- **recovery restores semantic validity, not merely surviving bytes**;
- **external execution history and permission to act again are separate**;
- **evidence independence itself may be unknown and learned**;
- **evidence acquisition can change what the observed sample means**.

## Current executable architecture hypothesis

```text
STABLE TYPED SEMANTIC PLANE
  subject/source identities
  source evidence
  publication provenance
  authority versions
  resource leases
        |
        +--> dynamic ownership topology
        +--> non-owning coordination scopes
        +--> directional operational dependencies
        ↓
TYPED TRANSITION PROPOSALS
        ↓
INTERACTION-AWARE VALUE / RESOURCE ALLOCATION
        ↓
EVIDENCE PLANE
  source identity
  source quality
  common-mode dependence
  directional derivation
  versioned/path provenance
  acquisition / selection provenance
        ↓
effective evidence + claim aggregation
        ↓
CONSEQUENCE-SENSITIVE ASSURANCE
        ↓
PREPARE non-authoritative candidate
        ↓
current validation + version/publication/authority fence
        ↓
PUBLISH authoritative internal state
        |
        +--> external effect path
        |      effect-specific execution evidence
        |      current authority for every fresh/retry attempt
        ↓
SEMANTIC CRASH / TOPOLOGY RECOVERY
        ↓
typed transient recovery + old-epoch event forwarding
        ↓
OBSERVE OUTCOMES
        ↓
selection-aware learning + versioned causal credit
        ↓
staged / appropriately-scoped update
```

This is still a falsifiable architecture hypothesis, not a frozen final design.

## Latest evidence-plane result

The Atlas originally knew source lineages exactly. That assumption has been removed progressively.

Current experiments show:

```text
source identity
    !=
source quality
    !=
shared failure dependence
    !=
directional derivation
    !=
versioned/path provenance
    !=
how the evidence was selected
    !=
claim confidence
    !=
assurance authority
```

### PS-026 — learned / causally qualified evidence dependence

Evidence sources are not independent merely because they have different names or records. Dependence can be hidden, changing, domain-specific, directional, nonlocal and partly unobserved. Common causes can also make genuinely independent sources fail together.

The system therefore treats evidence dependence as revisable relational state and buys explicit dependency/provenance evidence only where its value justifies the cost.

### PS-027 — selection-aware evidence semantics

When system policy affects which outcomes become observable, the selected observations cannot automatically be generalized to unobserved cases.

I28D shows this while learning a changing source-dependence relation: querying truth mostly on source disagreements obtains more labels yet biases the learned joint relation.

I29 reproduces the failure in self-change auditing: auditing mostly candidates already flagged as risky makes the selected audit sample look dramatically worse than the true population evaluator error.

I30 carries the rule into discovery. Independently verified near-threshold hypotheses are authoritative about themselves, but their success rate cannot be generalized to all rejected hypotheses.

> **Verification authority is not statistical generalization authority.**

## JEPA / predictive representation

JEPA remains explicitly inside the Atlas as a candidate mechanism, not a selected component.

E24 shows that coarse predictive latent state can be efficient yet discard distinctions required by later objectives or interventions. Dense predictive state or compact latent state backed by recoverable source evidence preserves more option value.

> Passive predictive sufficiency is not necessarily causal/interventional sufficiency.

## Discovery target

Human knowledge is treated as bootstrap state, not an epistemic ceiling:

```text
inherited knowledge
    -> competing hypotheses
    -> search / experiment / proof
    -> candidate discovery
    -> scoped independent verification
    -> replication / consolidation
    -> expanded knowledge frontier
```

Novel output is not new knowledge. Promotion requires evidence strong enough to survive the relevant verification process.

The recent evidence-dependence and selection results matter directly here: many agreeing outputs may share one hidden source, and a selectively verified discovery set may tell us very little about unverified regions of hypothesis space.

## Current organizing hypothesis

Practical intelligence may be adaptive selection of **typed state transitions and typed relationships under finite resources**, with semantic boundaries strong enough that confidence, record count, source identity, evidence dependence, acquisition process, publication state, historical approval, causal identity and current authority cannot impersonate one another.

## Next high-value work

The immediate architecture question is whether the growing evidence relations should remain separate typed layers or whether they can be compressed into a smaller unified causal-evidence representation **without losing the distinctions the experiments have earned**.

Other active targets:

- self-improvement regression selection under PS-027;
- noisy/contested rather than exact delayed truth;
- nested/overlapping ownership only if non-owning coordination proves insufficient;
- neural E24C only if representation geometry becomes architecture-discriminating;
- hardware co-design only after the semantic/runtime laws stabilize enough for substrate assumptions to be useful.

## End goal

Produce a defensible answer to:

**If we had to build an intelligent computational system from scratch, using everything humanity has learned but none of the accidental constraints of existing implementations, what would we build—and why?**

Every surviving architecture claim must remain evidence-traceable and experimentally falsifiable.
