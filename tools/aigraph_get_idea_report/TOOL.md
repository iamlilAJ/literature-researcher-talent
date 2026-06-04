# aigraph_get_idea_report

**The canonical Stage 3 deliverable tool.** 200ms, 0 LLM, full markdown.

## Why
Wraps aigraph's `get_idea_report` MCP tool. Returns the COMPLETE Stage 3
markdown that matches OMC's Stage 3 critic contract:
- `# Stage 3: Idea Generation — <topic>` heading
- Corpus-coverage banner (strong / weak / none)
- `# Selected Hypotheses` section with hypothesis items grounded in real
  claim citations

Internally applies the tuned MMR settings + Atlas overlap filter at threshold
3 (drops ~20% tangential hyps validated to lift top-K signal).

## When to use vs the alternatives
| Need | Tool |
|---|---|
| **Default Stage 3 deliverable** | `aigraph_get_idea_report` (this tool) ✓ |
| Programmatic structured records | `query_hypotheses` (via aigraph_mcp_tools.py if available) |
| Cascade with non-empty guarantee (13s, LLM) | `aigraph_generate_ideas` |
| Auto-corpus discovery (paid build risk) | `aigraph_research_ideas` (carefully) |
| Fresh corpus build | `aigraph_pipeline_run` |

## Inputs
- `topic` (required): research topic
- `run` (required): existing aigraph run id; `list_runs` to discover
- `k` (default 8): top-K hypotheses surfaced
- `kind` (default `creator`): `creator` (new-method, recommended) | `critic`
  (conflict-explanation, lower LLM-judge score) | `both`
- `out_path` (optional): also persist to file
- `mcp_url` (default `http://localhost:8765/mcp/`): override endpoint

## Output
Complete Stage 3 markdown (~30-40KB typical).

## Cost
0 LLM, ~200ms. Concurrent calls are fine (server scales).
