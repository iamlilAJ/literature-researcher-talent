"""LangChain tool: aigraph generate_ideas — cascade idea generator via MCP."""

from __future__ import annotations

import json
import os
import urllib.request

from langchain_core.tools import tool

DEFAULT_MCP_URL = os.environ.get("AIGRAPH_MCP_URL", "http://localhost:8765/mcp/")
_HEADERS = {"Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"}


def _mcp_post(url: str, body: dict, session_id: str | None = None) -> tuple[str | None, dict | None]:
    h = dict(_HEADERS)
    if session_id:
        h["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode()
        new_sess = r.headers.get("Mcp-Session-Id")
    for line in raw.splitlines():
        if line.startswith("data:"):
            return new_sess, json.loads(line[5:])
    return new_sess, None


@tool
def aigraph_generate_ideas(
    topic: str,
    run: str,
    min_ideas: int = 5,
    as_markdown: bool = True,
    mcp_url: str | None = None,
) -> str:
    """Generate research ideas for ``topic`` from an existing aigraph ``run``.

    Cascades through five idea tiers (critic-conflict, creator-new-method,
    community-bridge, method-extension, limitation-forward) plus a deterministic
    paper-seeded backstop, stopping when ``min_ideas`` is reached. Guaranteed
    non-empty as long as the run has >=1 paper. Tiers D/E (LLM-driven) are
    cached to ``<run>/forward_ideas.jsonl`` so repeat calls are 0-LLM.

    Wraps the aigraph MCP server's ``generate_ideas`` tool (same-host). aigraph
    MCP must be running on ``mcp_url`` (default ``http://localhost:8765/mcp/``).
    """
    url = mcp_url or DEFAULT_MCP_URL
    sess, _ = _mcp_post(url, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "talent-aigraph-tool", "version": "0.1"}},
    })
    _mcp_post(url, {"jsonrpc": "2.0", "method": "notifications/initialized"}, sess)
    _, resp = _mcp_post(url, {
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "generate_ideas",
                   "arguments": {"topic": topic, "run": run,
                                 "min_ideas": min_ideas,
                                 "as_markdown": as_markdown}},
    }, sess)
    out = (resp or {}).get("result", {})
    contents = out.get("content", [])
    if contents and contents[0].get("type") == "text":
        return contents[0].get("text", "")
    return json.dumps(out, ensure_ascii=False)
