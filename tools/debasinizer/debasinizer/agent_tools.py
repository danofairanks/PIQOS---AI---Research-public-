"""Stable, JSON-in/JSON-out function surface for agent tool-calling.
Same contract as `attractor_scan/agent_tools.py`, `bifp/agent_tools.py`,
and `basin_depth/agent_tools.py`: every function here takes and returns
only plain JSON-serializable types, so it can be wrapped directly as MCP
tool handlers without any adaptation layer.
"""

from __future__ import annotations

from .scan import scan, scan_corpus


def debasinizer_scan_text(text: str) -> dict:
    """Run the resonance-register (5 categories from the Mind Viruses
    paper's own reported vocabulary) and self-coherence-assertion
    detectors against a single piece of text. `register_flagged`
    requires 2+ distinct resonance categories to co-occur -- the
    cross-category signature the source paper actually found, not any
    single word. A flag is a lead for a human/agent review pass, not a
    verdict; see README."""
    return scan(text).to_dict()


def debasinizer_scan_corpus(documents: list[dict]) -> dict:
    """Scan a list of documents and aggregate flag frequency across the
    corpus -- counting, not statistics; see `tools/basin_depth` for the
    significance-tested measurement this project ships. `documents`:
    list of `{"doc_id": str, "text": str}`."""
    try:
        pairs = [(str(d["doc_id"]), str(d["text"])) for d in documents]
    except (KeyError, TypeError) as exc:
        return {"error": f"malformed document: {exc}"}
    return scan_corpus(pairs).to_dict()
