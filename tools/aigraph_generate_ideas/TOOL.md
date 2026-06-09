# aigraph_generate_ideas

Cascade idea generator with non-empty guarantee. Wraps the aigraph MCP server's
`generate_ideas` tool (same-host).

## Why
Stage 3 of the research pipeline. Given a topic and an existing aigraph run
(corpus), produces 1-20 ideas by walking five idea-extraction tiers from
high-signal to permissive, falling through to a deterministic backstop. Works
even on sparse corpora that have no cross-paper anomalies.

## Inputs
- `topic` (required): research topic / search phrase
- `run` (required): existing aigraph run id; use `list_runs` to discover
- `min_ideas` (default 5): target count, clamped 1..20
- `as_markdown` (default true): return rendered report vs structured dict
- `mcp_url` (default `http://localhost:8765/mcp/`): override aigraph MCP endpoint

## Output
Rendered markdown report (default) or JSON of `{ideas, stats}`.

## Prereq
aigraph MCP server (v0.7.0+) running on the same host. See aigraph repo's
`MCP_README.md`.

## Cost
0-LLM if all five cascade tiers hit cache. Tiers D/E (method-extension,
limitation-forward) call the LLM once per anomaly on first invocation and
cache to `<run>/forward_ideas.jsonl`; subsequent calls are 0-LLM.
