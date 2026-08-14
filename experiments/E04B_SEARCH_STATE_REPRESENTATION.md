# E04B — Search/Backtracking State Representation

**Status:** second E04 task family; preliminary multi-seed evidence only.

## Why a second family

The first E04 benchmark transports a flat state record. E04B instead carries a search/backtracking state with variable stack depth, exact large identifiers, forbidden-node constraints, continuous heuristic scores and a version-2 budget field. Decoding errors can therefore change the next search operation rather than merely fail an equality test.

## Representations

- `search_json` — human-readable exact structured state.
- `search_float32_vector` — homogeneous positional float32 representation.
- `search_structured_binary` — exact variable-length machine state + float32 scores + version/integrity metadata.
- `learned_quantized_exact_side` — exact identifiers/stack/control state in a compact side channel while four continuous heuristic scores are quantized using calibration-set statistics learned from prior states.

The learned hybrid is deliberately simple: it learns per-score scale/location, not a neural code. The purpose is to test whether **information with different fidelity semantics benefits from different channels** before adding a powerful learned encoder.

## 20-seed means

### In-distribution score state

| representation | decision accuracy | exact structural state | score MAE | bytes | version compatible | corruption detected |
|---|---:|---:|---:|---:|---:|---:|
| JSON | 1.000 | 1.000 | 0 | ~178.5 | 1.000 | ~0.41 |
| float32 vector | 0.834 | ~0.001 | ~2e-8 | 56 | 0.000 | 0.000 |
| structured binary | 1.000 | 1.000 | ~2e-8 | ~39 | 1.000 | 1.000 |
| learned quantized + exact side | **0.997** | **1.000** | ~0.0067 | **~27** | **1.000** | **1.000** |

### Continuous-score distribution shift

When 60% of test states use a shifted/wider score distribution, the learned quantized channel's score MAE rises to ~0.0327 but mean decision accuracy across 20 seeds remains ~0.991. Structured float32 scores remain exact to float32 precision at ~39 bytes.

## What the float result means

The float vector is not failing because continuous computation is intrinsically weak. It is excellent on the approximate score fields. It fails because one homogeneous float32 wire format is being asked to represent **large exact identity and evolving protocol structure**, requirements it cannot satisfy at that precision/interface.

## Stronger E04 conclusion

Across two task families and multiple bandwidth/distribution regimes, the evidence now favors a typed boundary representation:

- exact identity/control fields remain exact;
- numerically tolerant fields may use compact approximate/learned channels;
- version/integrity metadata is explicit at changing module boundaries;
- human-readable audit need not be the hot-path payload.

This is a principle-level conclusion, not a selection of JSON, TLV, int8 quantization or any specific serialization.

## Remaining falsifier

A homogeneous representation should regain preference if it can match the typed hybrid on task utility, exact-field semantics, version evolution and failure detection under equal bandwidth/compute—without recreating typed side channels implicitly.
