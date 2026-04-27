---
name: aigraph_pipeline_run
description: Run the full conflict + creator pipeline end to end — build graph, detect anomalies, generate critic + creator hypotheses, select top-K, render interactive HTML graph.
---

# aigraph_pipeline_run

The headline tool. Chains build-graph → detect-anomalies → generate-hypotheses(critic) → generate-creator-hypotheses → select → visualize. Produces a complete run directory.

## When to use

- After `aigraph_extract_claims` and `aigraph_extract_open_questions` have written claims.jsonl + open_questions.jsonl
- User asks "find conflicts" / "propose new methods" / "what should I research next"
- Final step before handing the user a markdown report + interactive graph

## Parameters

| Name | Type | Default | Notes |
|---|---|---|---|
| `claims_path` | string | required | JSONL of Claim records. |
| `papers_path` | string | required | JSONL of Paper records (for citation metadata in graph nodes). |
| `open_questions_path` | string | required | JSONL of OpenQuestion records (creator grounding). |
| `output_dir` | string | required | Run directory. Created if missing. |
| `model` | string | env `AIGRAPH_MODEL` | LLM model id. |
| `select_k` | int | 12 | Top-K hypotheses to surface in the markdown report. |
| `creator_max_anomalies` | int | null | Cost guard — cap anomalies fed to creator. |

## Output (under `output_dir/`)

- `graph.json` — node-link graph (1500–5000 nodes typical)
- `anomalies.jsonl` + `anomalies_high.jsonl` — 7-category conflict patterns
- `hypotheses_critic.jsonl` — methodological critiques per anomaly
- `hypotheses_creator.jsonl` — NEW method proposals grounded in anomaly + open_questions
- `hypotheses.jsonl` — combined critic + creator
- `selected.md` — top-K markdown report with utility breakdown
- `index.html` — interactive D3 graph visualization

## Cost / time

- Graph + anomaly detection: ~5 min, $0
- LLM critic on 77 high-signal anomalies: ~25 min, ~$2
- LLM creator on `creator_max_anomalies` (default unlimited): ~30s per anomaly, ~$0.02 each
- Select + visualize: < 10s, $0

For a 100-paper run with all defaults: ~25 min total, ~$2-5.
