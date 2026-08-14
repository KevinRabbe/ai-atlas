# AF03 — Organizational Scope: Global Mode vs Simultaneous Heterogeneous Modes

**Status:** implemented. AF03 strengthens the architecture-level interpretation of PS-003; it does not add a new provisional principle.

## Question

AF02 shows that one organism can sometimes benefit from changing its **global** organizational mode over time.

But real workloads can be heterogeneous at the same moment:

- one subsystem may be sparse/local;
- another may need strong shared integration;
- another may be tightly resource-coupled;
- another may benefit from preserved variants.

AF03 asks:

> should organization be selected globally for the whole organism, or locally by subsystem scope?

## Environment

Four domains operate simultaneously.

Each domain has continuously jittered hidden structural properties:

- coupling;
- sharedness/transfer;
- recurrence.

Selectors observe only noisy proxies and their own realized organizational rewards.

Two structurally different families are compared.

### Family A — heterogeneous, weakly coupled domains

The four domains occupy different structural regimes at the same time. Cross-domain coupling is low (`0.12`).

### Family B — homogeneous, strongly coupled domains

All four domains occupy the same structural regime and cross-domain coupling is high (`0.80`).

## Policies

- fixed A/B/C/D modes;
- **global adaptive:** one learned organizational mode is imposed on every domain;
- **scoped adaptive:** each domain learns/selects its own organizational mode;
- oracle global;
- oracle scoped.

Scoped organization pays:

- per-domain selector/state carrying cost;
- per-domain switch cost;
- an explicit boundary-mismatch cost whenever tightly coupled domains use different organizational modes.

That mismatch term is critical: otherwise arbitrary modular fragmentation would be free.

## 20-seed results

### Heterogeneous domains, cross-domain coupling 0.12

| policy | utility/domain-step |
|---|---:|
| fixed A | 1.4830 |
| fixed B | 1.4520 |
| fixed C | 1.4402 |
| fixed D | 1.5081 |
| global adaptive | 1.4947 |
| **scoped adaptive** | **1.5543** |
| oracle global | 1.5055 |
| oracle scoped | **1.5721** |

A single global selector performs poorly because averaging four different domains destroys the structural distinctions needed to choose organization correctly.

Scoped selection captures most of the oracle-scoped gain while still paying selector, switch and boundary costs.

### Homogeneous domains, cross-domain coupling 0.80

| policy | utility/domain-step |
|---|---:|
| fixed A | 1.4830 |
| fixed B | 1.4520 |
| fixed C | 1.4402 |
| fixed D | 1.5081 |
| **global adaptive** | **1.5711** |
| scoped adaptive | 1.5537 |
| oracle global | **1.5852** |
| oracle scoped | 1.5813 |

When the domains genuinely share the same organizational economics, separate selectors/switch paths no longer buy useful specialization. They only add carrying/mismatch cost. Global organization correctly wins again.

## Coupling sweep

Heterogeneous-domain 20-seed means:

| cross-domain coupling | global adaptive | scoped adaptive | scoped advantage |
|---:|---:|---:|---:|
| 0.0 | 1.4947 | **1.5625** | +0.0678 |
| 0.1 | 1.4947 | **1.5557** | +0.0610 |
| 0.3 | 1.4947 | **1.5420** | +0.0473 |
| 0.5 | 1.4947 | **1.5283** | +0.0336 |
| 0.8 | 1.4947 | **1.5077** | +0.0130 |
| 1.0 | **1.4947** | 1.4940 | -0.0007 |

The scoped advantage decays continuously as cross-domain coupling rises and disappears at maximal coupling in this stress family.

This is exactly the result a clean-sheet architecture should produce if the underlying rule is real:

> **organizational scope should expand only as far as coupling makes separate organization materially inconsistent or wasteful.**

## Architecture consequence

AF01–AF03 now suggest two independent dimensions:

1. **organizational mode** — local/distributed, hierarchical, integrated, variant-preserving;
2. **organizational scope** — which domains/subsystems must share that mode.

A candidate mature system therefore looks less like:

```text
choose architecture A, B, C or D
```

and more like:

```text
for each currently relevant coupling scope:
    estimate locality / sharing / recurrence / contention
    choose useful organizational mode
    price boundary + switch + carrying cost
    merge scopes when coupling makes separation uneconomic
    split scopes when local specialization pays again
```

This is the architecture-level analogue of PS-003 and PS-020: **scope follows causal/resource coupling rather than being fixed globally.**

## What AF03 does not prove

The benchmark still abstracts away important implementation problems:

- live state migration when a scope splits or merges;
- nested scopes and overlapping resource dependencies;
- authority/provenance flow across organization boundaries;
- asynchronous in-flight work during reorganization;
- imperfect estimates of cross-domain coupling itself;
- real message/cache/memory-layout costs.

## Next discriminator — I07 / AF04

The next step should combine AF02 and AF03 into **dynamic scope formation**.

Instead of being told four fixed domain boundaries, the system receives a changing dependency graph and must decide:

- which nodes should remain local;
- which should form a shared coordination scope;
- which scopes should integrate representations;
- which scopes should preserve variants;
- when scopes should split/merge again.

The falsifier is straightforward: if scope-learning/migration overhead exceeds the benefit, a more static architecture should win.

That experiment is closer to deriving an actual architecture topology than selecting among named Phase-9 families.