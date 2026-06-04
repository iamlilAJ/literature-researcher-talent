# aigraph_research_ideas

One-shot topic → ideas pipeline. Wraps the aigraph MCP server's
`research_ideas` tool (same-host).

## Why
Compared to `aigraph_generate_ideas` (requires an existing run), this tool
handles corpus discovery automatically:
- If a matching corpus already exists → instant idea generation (0 build cost)
- Otherwise → optional corpus build (SLOW + PAID), then cascade

## Inputs
- `topic` (required): research topic
- `max_papers` (default 50): cap on fresh-corpus build
- `min_ideas` (default 5): target count
- `reuse` (default true): prefer existing corpus
- `wait_seconds` (default 0, max 1500): block for fresh-build completion;
  0 = submit-and-return; 600 = roughly enough for max_papers≤30
- `as_markdown` (default true): markdown vs structured dict
- `mcp_url` (default `http://localhost:8765/mcp/`): override

## Output
- If reused or built within wait budget: markdown report (or structured dict)
- If still building when budget expires: `{status:"building", run}` —
  poll with `get_run_status`, then call `aigraph_generate_ideas` directly

## Cost
- `reuse=true` and existing corpus matches → free (0 LLM unless cache miss)
- `reuse=false` OR no match → triggers aigraph `start_run` corpus build:
  ~$1-2 per 100 papers, 5-30 min
