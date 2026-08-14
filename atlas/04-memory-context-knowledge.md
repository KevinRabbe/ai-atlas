# Memory, Context & Knowledge

## Required function

Preserve useful information across timescales and make the right information available to computation at the right time without overwhelming the active substrate.

## Distinctions to preserve

Parametric knowledge; active/working state; episodic memory; semantic memory; procedural/skill memory; external factual stores; environment/world state; caches; learned recurrent state; provenance and confidence metadata.

## Early evidence anchors

RAG demonstrates a practical division between parametric and non-parametric knowledge. MemGPT demonstrates explicit hierarchical context management. Generative Agents demonstrate retrieval plus reflection over episodic records. Titans explores learned neural long-term memory updated at test time. RLM shows that large input can remain an external environment rather than being consumed wholesale by the model.

## Clean-sheet questions

- What should be remembered verbatim versus compressed/generalized?
- Who decides when memory is written, consolidated or forgotten?
- How are contradictions represented instead of overwritten?
- What retrieval objective predicts downstream usefulness rather than semantic similarity alone?
- When should repeated external knowledge migrate into weights or executable skills?
- Can active context be treated as a cache whose contents are optimized dynamically?
