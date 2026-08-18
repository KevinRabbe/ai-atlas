# Phase 10 Experimental Status

**Checkpoint: twenty-seven provisional implementation-neutral principles selected; composition has progressed through I30 with a crash-aware typed organism, learned evidence-dependence/derivation semantics, selection-aware acquisition provenance and discovery verification. No fixed Phase-9 A/B/C/D family is selected as a universal whole-system architecture.**

## Validation

Phase 10 now contains **522 added semantic test cases**.

Latest delta:

- I28A direction-aware evidence aggregation: 8 tests;
- I28B multi-hop/path provenance: 7;
- I28C cyclic/versioned temporal evidence: 8;
- I28D sparse/delayed truth: 8;
- I29 selective self-change auditing: 8;
- reusable `EvidenceAcquisitionRegistry`: 6;
- I30 selection-aware discovery verification: 8.

The shell environment has previously been unable to clone GitHub because DNS resolution is unavailable there. Numerical discriminators are exercised in the local Python reasoning environment before connector publication; GitHub connector writes are verified on `main`. Do not interpret the committed test count as a claim that a fresh clean-checkout suite was executed in that shell.

---

# Current architecture checkpoint

## Stable typed semantic plane

The common runtime increasingly separates semantics that conventional architectures often blur:

```text
semantic/source identity
    !=
current belief
    !=
evidence provenance
    !=
publication provenance
    !=
capability authority
    !=
resource ownership
    !=
coordination membership
    !=
directional dependency
    !=
causal credit identity
```

Dynamic topology may reorganize while these exact semantics remain stable/versioned.

## Shared transition/resource plane

Optional work is represented as typed transition proposals competing under finite resources. I04/I06 and later composition show allocation can be shared while authority cannot be flattened into the same scalar score.

Current recurring controls include:

- compute/stop decisions;
- observation/intervention;
- retrieval/rematerialization;
- fidelity escalation;
- synchronization;
- verification/audit;
- persistence/consolidation;
- structural/topology change.

Material complements, substitutions and shared scarcity are priced jointly enough to avoid locally rational but globally wasteful choices.

## Publication, authority and recovery

I13–I23 established the crash-aware publication/recovery spine:

```text
PREPARE non-authoritative candidate
    -> independent/current validation
    -> version/publication/authority fence
    -> PUBLISH coherent authoritative state
    -> recover from authoritative semantic provenance
```

PS-024 requires failure-isolated consequential publication when partial visibility can violate invariants.

PS-025 separates external execution history from current permission to execute again. Local intent or old approval cannot prove the outside world already acted.

Typed transient recovery preserves useful hot state and delayed credit only when their semantic identity/currentness survives; otherwise state is rematerialized/replayed or discarded.

## Evidence plane through I27

The common evidence path now distinguishes:

```text
source identity
    !=
source quality
    !=
common-mode dependence
    !=
directional derivation
    !=
claim aggregation
    !=
assurance authority
```

PS-026 treats evidence independence as uncertain, revisable relational state.

`EvidenceDependenceModel` represents scoped/common-mode dependence learned from resolved outcomes and optional dependency probes. Raw co-failure is not sufficient because broad task difficulty can correlate independent sources.

`EvidenceDerivationModel` separately represents directional inheritance where downstream evidence can copy upstream errors yet also contribute independent correction.

`EvidenceLineageRegistry` combines exact provenance where genuinely known with learned effective dependence. Unknown source names do **not** create independent evidence.

`aggregate_binary_evidence()` aggregates once per effective failure group, so record count cannot re-enter as false precision through an upstream confidence estimate.

## I28A–I28C — conditional/path/versioned derivation

### I28A — direction changes marginal evidence

Derived-child agreement often contains little new information; a child departure can be the genuinely new evidence. Static child discounting and symmetric collapse both lose important cases. Learned conditional direction improves late calibration and approaches the generative oracle on child-departure cases.

### I28B — immediate-parent edges are not always enough

When C can bypass B and consult A directly, `A != B, C == A` requires nonlocal provenance. Path-aware aggregation materially reduces those errors.

When the shortcut is removed, extra path state stops helping and can slightly hurt. Full provenance depth is therefore conditional on actual nonlocal dependency.

### I28C — source cycles can unroll through versioned observations

Static source identities can form `A <-> B`, while individual revisions form a temporal DAG across generations. Static cycle collapse loses distinct innovation; treating every revision as independent creates false precision. Versioned temporal provenance approaches oracle calibration.

## I28D — sparse/delayed truth

The A/B structural relation changes while visible identities remain stable. Passive truth arrives on only ~1.18% of tasks and is delayed.

Approximate 30-seed means:

| policy | error | net utility | relation accuracy | post-shift relation accuracy |
|---|---:|---:|---:|---:|
| conservative | ~0.0854 | ~2.4679 | — | — |
| passive behavioral | ~0.0830 | ~2.5032 | ~0.732 | ~0.000 |
| disagreement-targeted truth | ~0.1152 | ~2.0001 | ~0.541 | ~0.987 |
| coverage-targeted truth | ~0.0824 | ~2.5038 | ~0.828 | ~0.059 |
| **provenance probe** | **~0.0809** | **~2.5332** | **~0.995** | **~0.926** |
| oracle relation | ~0.0808 | ~2.5353 | 1.000 | 1.000 |

The important failure is disagreement-targeted truth acquisition: it gets many more labels and detects the shift quickly, yet makes lifetime relation learning worse because the learner treats an `A != B` selected sample as representative of the full joint error process.

## I29 / PS-027 — selection-aware evidence semantics

I29 reproduces the selection failure in self-change auditing.

A cheap evaluator has true population error ~15.5%. Auditing mostly candidates it flagged as risky and treating that selected audit set as population calibration drives the learned scalar error toward ~64%.

A representative random audit recovers the global scalar, but the downstream promotion decision needs the conditional risks `P(harm|safe-looking)` and `P(harm|flagged)`. A conditional learner with heavy flagged auditing plus a small safe-path coverage sample learns both and improves lifetime utility.

This promotes:

### PS-027 — selection-aware evidence semantics

> **When system policy affects which outcomes become observable, preserve enough acquisition/selection semantics that downstream learning does not silently generalize a selected sample to a population, stratum, dependence relation, calibration target or causal claim it does not support.**

The selected object is the semantic requirement, not random sampling, inverse-propensity weighting, a fixed coverage percentage or any particular audit estimator.

`EvidenceAcquisitionRegistry` is the current minimal runtime substrate. It records acquisition identity/mode and optional inclusion probability/scope separately from evidence content, lineage, quality and truth.

## I30 — PS-027 inside discovery

Discovery candidates above the visible threshold are independently verified before promotion. Rejected hypotheses can optionally be checked.

Near-threshold rejected candidates are far richer in real discoveries than deep rejects. Sampling that near-threshold region and generalizing its success rate to all rejects inflates the ordinary-domain rejected truth estimate to ~0.48, versus ~0.15 under representative coverage.

Approximate 30-seed means:

| policy | net utility | discoveries | recovered discoveries | rejected verification rate |
|---|---:|---:|---:|---:|
| pass only | ~0.377 | ~0.178 | 0 | 0 |
| near-threshold global | ~0.421 | ~0.237 | ~0.059 | ~0.266 |
| random-domain scalar | ~0.381 | ~0.200 | ~0.023 | ~0.132 |
| **selection-aware score bins** | **~0.461** | **~0.214** | **~0.036** | **~0.155** |
| oracle score | ~0.524 | ~0.242 | ~0.065 | ~0.177 |

I30 exposes another important boundary:

> **verification authority is not statistical generalization authority.**

An independently verified discovery can be authoritative about itself while the policy-selected set of verified discoveries remains a biased sample of the surrounding hypothesis space.

## E25 — external DiffusionBlocks/local-training branch (specified, not executed)

Sakana AI's ICLR-2026 DiffusionBlocks work is now recorded as explicit primary-source evidence.

Atlas extraction:

> **Training dependency scope may be smaller than inference dependency scope when local learning objectives are constructed so their solutions compose into the required global behavior.**

Current external evidence reports block-proportional active training-memory reduction and zero inter-block training dependency for the transformed objective, while also showing a non-monotonic block-count/quality frontier. Moderate decomposition can match or improve some task metrics; excessive decomposition degrades quality.

This literature addition does **not** create a new provisional principle and does not establish billion/frontier-scale behavior.

Files:

- `sources/DIFFUSION_BLOCKWISE_TRAINING.md` — primary-source claims, limits and corrections to common overstatements;
- `synthesis/LOCAL_OBJECTIVES_AND_TRAINING_DECOMPOSITION.md` — implementation-neutral extraction;
- `experiments/E25_LOCAL_TRAINING_DECOMPOSITION.md` — staged falsifier including real VRAM accounting, checkpointing/sharding controls, block-capacity sweeps, downstream language tasks, communication topology and scale trends.

E25 execution requires a neural-training environment; the current 522 semantic-test count is unchanged.

---

# Current provisional selections

**PS-001 through PS-027** are active reversible constraints.

Newest selections:

- PS-024 — failure-isolated consequential transition publication;
- PS-025 — externally grounded effect recovery / execution-authority separation;
- PS-026 — learned / causally qualified evidence dependence;
- PS-027 — selection-aware evidence semantics.

Earlier PS-001–PS-023 remain active; their detailed evidence trail is retained in `clean-sheet/DESIGN_LEDGER.md` and experiment notes.

---

# Current executable architecture hypothesis

```text
stable typed semantic identities
  source / subject / publication / authority / lease identities
        |
        +--> dynamic ownership topology
        +--> non-owning coordination scopes
        +--> directional operational dependencies
        ↓
typed transition proposals
        ↓
interaction-aware value/resource allocator
        ↓
EVIDENCE STRUCTURE
  exact source/provenance where known
  learned source quality
  scoped common-mode dependence
  directional derivation
  versioned/path provenance when earned
  acquisition/selection provenance
        ↓
effective evidence groups + conditional aggregation
        ↓
consequence-sensitive assurance allocation
        ↓
PREPARE non-authoritative candidate
        ↓
current validation + version/publication/authority fence
        ↓
PUBLISH authoritative internal state
        |
        +--> external effects
        |      external execution evidence
        |      current authority for each new attempt
        ↓
semantic crash recovery
        ↓
typed transient recovery / event forwarding
        ↓
observe outcomes
        ↓
selection-aware learning + versioned causal credit
        ↓
staged appropriately-scoped update
```

## Current strongest evidence-plane inference

> **Evidence is not a bag of records. Its value depends on source quality, failure-mode dependence, derivation direction, version/path provenance, acquisition process, scope/coverage and consequence. These relations are themselves typed state and should be learned/materialized only while their decision value pays for them.**

## Next high-value work

1. test whether the separate evidence representations (common-mode dependence, directional derivation, temporal/path provenance, acquisition provenance) should remain typed layers or can be compressed into a smaller unified causal evidence representation without losing semantics;
2. execute E25A/B when a suitable neural-training environment is available, before extrapolating DiffusionBlocks into a large-GPU training claim;
3. compose PS-027 with self-improvement regression selection, where the optimizer can influence which failures become visible;
4. test evidence relation/acquisition learning when truth itself is noisy or contested rather than exact delayed ground truth;
5. nested/overlapping ownership remains unearned while non-owning coordination overlays suffice;