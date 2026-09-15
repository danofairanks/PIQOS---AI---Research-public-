"""Stable, JSON-in/JSON-out function surface for agent tool-calling.
Same contract as `debasinizer/agent_tools.py`, `rigor_cosplay/agent_tools.py`,
`attractor_scan/agent_tools.py`, `bifp/agent_tools.py`, and
`basin_depth/agent_tools.py`: every function here takes and returns only
plain JSON-serializable types, so it can be wrapped directly as MCP tool
handlers without any adaptation layer.
"""

from __future__ import annotations

from .scan import scan, scan_corpus


def hedge_dogwhistle_scan_text(text: str) -> dict:
    """Find paralipsis constructions ("I'm not saying X, but...") in a
    single piece of text and return the text with every containing
    sentence removed (`text_with_hedges_removed`). This mechanizes the
    FIRST STEP of the removal test only -- it does not judge whether the
    disclaimed content is established elsewhere in the remaining text by
    a direct, unhedged statement. An agent calling this tool should
    re-read `text_with_hedges_removed` and make that judgment itself; see
    README."""
    return scan(text).to_dict()


def hedge_dogwhistle_scan_corpus(documents: list[dict]) -> dict:
    """Scan a list of documents and aggregate paralipsis-construction
    frequency across the corpus -- counting, not statistics; see
    `tools/basin_depth` for the significance-tested measurement this
    project ships. `documents`: list of `{"doc_id": str, "text": str}`."""
    try:
        pairs = [(str(d["doc_id"]), str(d["text"])) for d in documents]
    except (KeyError, TypeError) as exc:
        return {"error": f"malformed document: {exc}"}
    return scan_corpus(pairs).to_dict()
