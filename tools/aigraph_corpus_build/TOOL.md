---
name: aigraph_corpus_build
description: Build or refresh an offline arXiv reasoning corpus — seeds candidate papers from 49 default reasoning queries, syncs full text via three-tier fallback (TeX -> HTML -> PDF), and optionally enriches with Semantic Scholar citation counts.
---

# aigraph_corpus_build

Stage 1 of the literature-researcher pipeline. Produces a structured offline corpus that downstream tools consume.

## When to use

- The user asks to "start a research run on <topic>" or "build a corpus on X"
- A downstream skill (claim-extract, conflict-detect, idea-synthesize) reports the manifest is missing or stale
- The user wants to refresh citation counts on an existing corpus (set `enrich_citations: true`)

## Parameters

| Name | Type | Default | Notes |
|---|---|---|---|
| `root` | string | required | Filesystem directory for the corpus, e.g. `data/corpus/arxiv_reasoning`. Created if missing. |
| `per_query_limit` | int | 200 | Cap per arXiv query. 200 is fine for a balanced 4000–5000 paper corpus across the 49 default queries. |
| `sync_batch_size` | int | 20 | How many papers to download/parse per sync round. |
| `enrich_citations` | bool | true | Whether to call Semantic Scholar batch API after sync. Free, ~15s for 5000 papers. |

## Output

- `<root>/papers.jsonl` — manifest with `priority_score`, `sync_status`, `cited_by_count` per paper
- `<root>/artifacts/<paper_id>/{text,sections,sentences,metadata}.json` — full-text artifacts
- `<root>/artifacts/<paper_id>/source/` (or `html/`, `pdf/`) — raw download

## Cost / time

- $0 LLM cost (pure HTTP fetch + parse)
- ~2–3 hours wall-clock for a fresh 5000-paper run (network bound)
- ~15s for citation enrich (Semantic Scholar batch endpoint, 500 papers per request)
