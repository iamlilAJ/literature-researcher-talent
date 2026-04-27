---
name: aigraph_extract_claims
description: Extract 0-6 structured claims per paper using the LLM extractor — each claim has 16 fields (method, task, dataset, metric, baseline, direction, magnitude, conditions, scope, setting, mechanism, ...) plus a verbatim evidence_span and section grounding.
---

# aigraph_extract_claims

Stage 2a of the pipeline. Reads paper full text from the corpus artifacts, runs heuristic prefilter to pick top candidate sentences, then asks the LLM to emit structured claims with grounded evidence.

## When to use

- After `aigraph_corpus_build` has produced artifacts
- User asks "what does each paper say about X" / "extract claims" / "what's the structured statement of paper P"
- Before running the conflict graph (which consumes claims)

## Parameters

| Name | Type | Default | Notes |
|---|---|---|---|
| `papers_path` | string | required | JSONL of Paper records (e.g. corpus manifest). |
| `output_path` | string | required | Where to write the claims JSONL. |
| `model` | string | env `AIGRAPH_MODEL` | LLM model id. |
| `workers` | int | 8 | Thread-pool size for parallel LLM calls. |
| `top_k_papers` | int | null | If set, only process top-K by priority_score. |

## Output

Each line of `output_path` is a Claim with:
- `claim_id`, `paper_id`, `claim_text`, `direction` (positive/negative/mixed)
- `method` + `canonical_method` (one of 25 reasoning categories)
- `task` + `canonical_task` (one of 19 categories)
- `dataset`, `metric`, `baseline`, `magnitude_text`, `conditions`, `scope`
- `setting` (retriever / top_k / context_length / task_type)
- `evidence_span` — verbatim quote from the paper
- `section_id`, `section_title`, `section_kind` — provenance

## Cost / time

- ~$0.01 per paper (gpt-5.4 minimal reasoning, ~5K input + 500 output tokens)
- ~5s per paper at workers=8 → 100 papers ≈ 1 min, 5000 papers ≈ 1 hour
- 5000-paper run cost ≈ $50
