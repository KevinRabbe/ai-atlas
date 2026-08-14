# Learned Inter-Agent / Inter-Module Communication

## Required function

Transmit only the information another computational process needs, using a protocol that can be learned or adapted to task, bandwidth and receiver capabilities.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| R-LC-01 | Cooperative agents can learn continuous communication protocols jointly with action policies instead of using a hand-designed language. | O | E4 | R-S002, R-S003 |
| R-LC-02 | Agents can also develop grounded discrete compositional symbols and non-verbal signals under suitable multi-agent tasks. | O | E3 | R-S004 |
| R-LC-03 | Learned gating can remove large fractions of communication under bandwidth constraints with little performance loss in studied tasks. | O | E2 | R-S005 |
| R-LC-04 | Recent LLM-agent latent-communication systems report reduced token/latency cost and improved task performance over text communication in controlled benchmarks. | O | E2 | R-S007, R-S008, R-S009 |

## Communication is selective state sharing

A module does not necessarily need another module's full internal state. A useful communication policy decides:

- whether to send anything;
- what subset/summary/state delta to send;
- representation/precision;
- recipient(s);
- timing;
- expected response/acknowledgment;
- confidence/provenance.

This mirrors memory retrieval and compute routing: communication itself is an allocation problem.

## Protocol learning

A learned protocol can exploit task-specific regularities unavailable to a fixed human language. But co-adaptation creates compatibility problems: if sender or receiver changes, the implicit code can drift.

Potential stabilizers include:

- shared interface training;
- explicit protocol versioning;
- adapters/translators;
- semantic anchors;
- self-describing metadata;
- fallback human-readable summaries;
- compatibility tests after model updates.

## Discrete versus continuous messages

Discrete communication offers compression, robust boundaries and easier logging. Continuous communication can transmit richer state with lower serialization loss. Either can become inefficient if message frequency/content is not controlled.

A hybrid can send a structured discrete header (identity, confidence, operation, provenance) plus compressed latent payload.

## Communication as a physical cost

The Phase-1 systems result applies directly: bytes moved, synchronization and locality can dominate. Multi-agent “intelligence” that depends on huge state exchanges may be inferior to a more locally capable module even if abstract reasoning quality is higher.

## Clean-sheet restatement

Inter-component communication should be a learned/engineered **information contract**, not assumed conversation. Optimize what information crosses boundaries, how much, when, and with what semantics/trust.

## Failure modes

Protocol drift; sender/receiver co-adaptation lock-in; latent message uninterpretable after failure; bandwidth explosion; messages sent every cycle regardless of value; hidden correlated errors shared across agents; accidental authority encoded in data payload; communication channel used to bypass permission boundaries; compression drops rare but critical state.
