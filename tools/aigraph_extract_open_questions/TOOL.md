---
name: aigraph_extract_open_questions
description: Extract acknowledged limitations and future-work signals from each paper's limitations and conclusion sections — produces OpenQuestion records that are the grounding signal for creator-mode hypothesis generation.
---

# aigraph_extract_open_questions

Stage 2b of the pipeline. The creator side of extraction. Where `aigraph_extract_claims` captures *what was shown*, this tool captures *what was acknowledged as unsolved or untested*.

## When to use

- After `aigraph_corpus_build` has produced artifacts
- User asks "what are open questions" / "what's missing" / "what limitations exist across the literature"
- Before running creator-mode hypothesis generation (which needs OpenQuestions as grounding)

## Parameters

| Name | Type | Default | Notes |
|---|---|---|---|
| `papers_path` | string | required | JSONL of Paper records. |
| `output_path` | string | required | Where to write the open_questions JSONL. |
| `model` | string | env `AIGRAPH_MODEL` | LLM model id. |
| `max_papers` | int | null | Optional cap. |

## Output

Each line of `output_path` is an OpenQuestion with:
- `open_question_id`, `paper_id`
- `kind` ∈ `acknowledged_limitation` | `future_work_suggestion` | `untested_extension`
- `text` — concise restatement (1-2 sentences)
- `evidence_span` — verbatim sentence from the paper
- `related_method`, `related_task`, `related_dataset` (if applicable)

## Cost / time

- ~$0.01 per paper
- ~10s per paper serial → 100 papers ≈ 17 min, 5000 papers ≈ 14 hours
- 5000-paper run cost ≈ $50

## Note

This tool reads from `<corpus_root>/artifacts/<paper_id>/sections.json`. Make sure the corpus is built first via `aigraph_corpus_build` and points to a known root via the `AIGRAPH_CORPUS_ROOT` env var or the path embedded in the paper records.
