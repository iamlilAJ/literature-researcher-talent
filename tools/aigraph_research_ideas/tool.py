"""LangChain tool: aigraph research_ideas — one-shot topic→ideas via MCP."""

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
    with urllib.request.urlopen(req, timeout=1600) as r:
        raw = r.read().decode()
        new_sess = r.headers.get("Mcp-Session-Id")
    for line in raw.splitlines():
        if line.startswith("data:"):
            return new_sess, json.loads(line[5:])
    return new_sess, None


@tool
def aigraph_research_ideas(
    topic: str,
    max_papers: int = 50,
    min_ideas: int = 5,
    reuse: bool = True,
    wait_seconds: int = 0,
    as_markdown: bool = True,
    mcp_url: str | None = None,
) -> str:
    """One-shot: ``topic`` in → ideas out.

    Reuses a matching existing aigraph corpus when ``reuse=True`` (INSTANT, 0
    corpus-build cost). Otherwise kicks off a fresh corpus build (SLOW, PAID
    — fetches up to ``max_papers`` papers, extracts claims/anomalies), polls
    for up to ``wait_seconds``, and on completion generates ideas. If the
    build is not done within the wait budget, returns ``{status:"building",
    run}`` for downstream polling via ``get_run_status``.

    Wraps the aigraph MCP server's ``research_ideas`` tool.
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
        "params": {"name": "research_ideas",
                   "arguments": {"topic": topic, "max_papers": max_papers,
                                 "min_ideas": min_ideas, "reuse": reuse,
                                 "wait_seconds": wait_seconds,
                                 "as_markdown": as_markdown}},
    }, sess)
    out = (resp or {}).get("result", {})
    contents = out.get("content", [])
    if contents and contents[0].get("type") == "text":
        return contents[0].get("text", "")
    return json.dumps(out, ensure_ascii=False)
