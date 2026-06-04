"""LangChain tool: aigraph get_idea_report — the canonical Stage 3 deliverable.

200ms, 0 LLM (uses the cached query layer + Atlas overlap filter + tuned MMR).
Returns the FULL Stage 3 markdown — heading + coverage banner + Selected
Hypotheses section grounded in real claim citations. Output format matches
the contract enforced by OMC's Stage 3 critic.
"""

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
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read().decode()
        new_sess = r.headers.get("Mcp-Session-Id")
    for line in raw.splitlines():
        if line.startswith("data:"):
            return new_sess, json.loads(line[5:])
    return new_sess, None


@tool
def aigraph_get_idea_report(
    topic: str,
    run: str,
    k: int = 8,
    kind: str = "creator",
    out_path: str = "",
    mcp_url: str | None = None,
) -> str:
    """Render the Stage 3 'Idea Generation' deliverable for ``topic``.

    Wraps the aigraph MCP server's ``get_idea_report`` tool (same-host).

    The returned markdown is a COMPLETE Stage 3 report: ``# Stage 3: Idea
    Generation — <topic>`` heading, corpus-coverage banner, ``# Selected
    Hypotheses`` section with hypothesis items (``### h…`` critic ideas
    and/or ``### a…#cr…`` creator ideas) grounded in real claim citations.
    This format matches the contract OMC's Stage 3 critic enforces.

    Cost: 0 LLM. Latency: ~200ms. Atlas overlap filter is applied
    automatically at threshold 3 (drops ~20% tangential hyps).
    """
    url = mcp_url or DEFAULT_MCP_URL
    args = {"topic": topic, "run": run, "k": k, "kind": kind}
    if out_path:
        args["out_path"] = out_path
    sess, _ = _mcp_post(url, {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                   "clientInfo": {"name": "talent-aigraph-tool", "version": "0.1"}},
    })
    _mcp_post(url, {"jsonrpc": "2.0", "method": "notifications/initialized"}, sess)
    _, resp = _mcp_post(url, {
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "get_idea_report", "arguments": args},
    }, sess)
    out = (resp or {}).get("result", {})
    contents = out.get("content", [])
    if contents and contents[0].get("type") == "text":
        return contents[0].get("text", "")
    return json.dumps(out, ensure_ascii=False)
