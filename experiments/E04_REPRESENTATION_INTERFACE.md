# E04 — Internal Representation and Interface Format

**Status:** first serialized-interface probe; preliminary multi-seed evidence only.

## Question

What should cross-process/intermediate state optimize for: compact numerical bandwidth, exact machine semantics, human readability, recovery, or some mixture?

The experiment tests real serialization behavior rather than assigning subjective scores to representation families.

## State carried across the interface

Large exact entity identifier; small action code; approximate numerical score; large exact target identifier; signed exact constraint field; flags; a version-2 optional priority field.

Large identifiers are above the exact-integer range of float32 on purpose. The message therefore contains both naturally approximate and non-negotiably exact information.

## Variants

- `human_readable_json` — exact/extensible but verbose and without a dedicated integrity layer.
- `opaque_float32_vector` — compact and accurate for approximate numerical fields, but positional/unversioned and unable to preserve the large exact integer fields.
- `structured_tagged_binary` — tagged typed fields plus CRC32; old consumers can ignore unknown future tags.
- `hybrid_structured_plus_audit` — tagged core plus redundant human-readable audit copy, trading bandwidth for recovery.

## Preliminary 12-seed result

Each seed uses 300 generated states and 100 corruption trials.

| representation | avg bytes | exact discrete fields | action accuracy | mean score abs. error | v2→v1 compatibility | corruption detect | corruption recover |
|---|---:|---:|---:|---:|---:|---:|---:|
| JSON | 134.7 | 1.000 | 1.000 | 0 | 1.000 | 0.533 | 0.098 |
| float32 vector | 28.0 | 0.000 | 1.000 | ~3.4e-8 | 0.000 | 0.000 | 0.000 |
| tagged binary | 38.0 | 1.000 | 1.000 | ~3.4e-8 | 1.000 | 1.000 | 0.000 |
| structured + audit | 173.7 | 1.000 | 1.000 | ~3.4e-8 | 1.000 | 0.000* | 1.000 |

`*` The hybrid reports recovery rather than rejection when its protected core is corrupted and the redundant audit copy remains intact.

Under the default 48-byte cap, the float vector and tagged binary fit; JSON and the redundant hybrid do not.

## Interpretation boundary

The float32 result must not be generalized to “continuous latent representations are bad.” The tested variant is specifically an unversioned positional float32 wire protocol carrying exact identifiers. It performs excellently on the approximate score and small categorical action while failing requirements it was not designed to preserve.

The first-pass lesson is narrower: representation should be typed by information/interface requirements; exact identity, approximate latent state, version metadata and audit evidence do not necessarily belong in one homogeneous encoding.

## Next discriminators

Equal-bandwidth sweeps; backtracking/constraint messages; learned continuous code with a separate exact side channel; independent producer/consumer protocol evolution; malformed/adversarial messages; audit-on-demand versus inline redundant audit.
