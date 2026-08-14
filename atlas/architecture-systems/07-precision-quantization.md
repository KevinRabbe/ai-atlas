# Numerical Precision and Quantization

## Required function

Represent parameters, activations, state and intermediate computations with enough numerical fidelity for learning/inference while minimizing storage, movement and arithmetic cost.

## Evidence

| ID | Finding | Class | Strength | Sources |
|---|---|---|---|---|
| AS-PQ-01 | Post-training transformations can enable INT8 weight/activation execution with small accuracy loss in broad LLM families while reducing memory and improving throughput. | O | E3 | AS-S035 |
| AS-PQ-02 | Activation-aware low-bit weight quantization demonstrates that numerical sensitivity is highly non-uniform across channels/weights. | O | E3 | AS-S036 |
| AS-PQ-03 | Ternary-weight BitNet b1.58 reports competitive matched-size language-model performance in its training regime, suggesting numerical representation can be co-designed with training rather than only compressed afterward. | O | E2 | AS-S037 |
| AS-PQ-04 | FlashAttention-3 uses hardware-supported FP8 while explicitly controlling numerical error, illustrating that precision, algorithm and hardware scheduling are coupled. | O | E3 | AS-S029 |
| AS-PQ-05 | Specialized low-precision matrix hardware can produce major performance/energy gains when workload structure matches it. | O | E4 | AS-S038 |

## Key deduction

Precision should be treated as **allocated fidelity**, not a single global datatype.

Different information may require different precision depending on:

- sensitivity/error amplification;
- uncertainty;
- persistence duration;
- update frequency;
- accumulator depth;
- whether the value is used for routing/control versus bulk representation;
- cost of recovering/recomputing it.

## Training-time versus inference-time precision

A representation that is safe after training may not be safe for optimization dynamics. Likewise, persistent memory/state may accumulate quantization error differently from feed-forward activations. The Atlas must keep these regimes separate.

## Clean-sheet restatement

Spend numerical precision where additional bits materially improve downstream decisions or learning stability. Allow precision to vary by operation/state class if the control and conversion costs do not erase the gain.

## Open questions

- Can precision be dynamically routed like compute?
- What state variables require high precision because errors compound over time?
- Could uncertainty estimates determine precision allocation?
- What hardware primitives become attractive if the model is trained from the beginning for very low-bit representations?

## Failure modes

Silent accuracy loss; accumulated recurrent-state error; outlier sensitivity; conversion overhead; hardware-specific quantization recipes; benchmark parity that hides calibration or rare-event failures.