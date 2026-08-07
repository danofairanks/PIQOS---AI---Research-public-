"""Stable, JSON-in/JSON-out function surface for agent tool-calling.

Same contract as `bifp/agent_tools.py` and `basin_depth/agent_tools.py`:
every function here takes and returns only plain JSON-serializable
types, so it can be wrapped directly as MCP tool handlers without any
adaptation layer. `tools/mcp_server/` does exactly that.
"""

from __future__ import annotations

from .scan import scan, scan_corpus


def attractor_scan_text(text: str) -> dict:
    """Run every implemented maneuver (§4.1, 7 categories) and
    semantic-laundering (§2.8, 5 of 6 cases) classifier against a
    single piece of text. Returns matched spans per category, not just
    labels -- a lead for a human/agent review pass, not a verdict; see
    README for what `density` does and does not mean."""
    return scan(text).to_dict()


def attractor_scan_corpus(documents: list[dict]) -> dict:
    """Scan a list of documents and aggregate category frequency
    across the corpus -- counting, not statistics; see
    `tools/basin_depth` for the significance-tested measurement this
    project ships. `documents`: list of `{"doc_id": str, "text": str}`."""
    try:
        pairs = [(str(d["doc_id"]), str(d["text"])) for d in documents]
    except (KeyError, TypeError) as exc:
        return {"error": f"malformed document: {exc}"}
    return scan_corpus(pairs).to_dict()
