"""Stable, JSON-in/JSON-out function surface for agent tool-calling.
Same contract as `debasinizer/agent_tools.py`, `attractor_scan/agent_tools.py`,
`bifp/agent_tools.py`, and `basin_depth/agent_tools.py`: every function
here takes and returns only plain JSON-serializable types, so it can be
wrapped directly as MCP tool handlers without any adaptation layer.
"""

from __future__ import annotations

from .scan import scan, scan_corpus
from .signatures import DEFAULT_PROXIMITY_RADIUS


def rigor_cosplay_scan_text(text: str, radius: int = DEFAULT_PROXIMITY_RADIUS) -> dict:
    """Run the three Rigor Cosplay signature detectors (cosmetic
    pushback, weak-man steelmanning, honesty-as-flattery) against a
    single piece of text. `any_signature_flagged` is True if ANY ONE of
    the three is present -- they do not need to co-occur. A flag is a
    lead for a human/agent review pass, not a verdict: this scanner
    cannot judge whether a matched pushback is genuinely peripheral or
    a matched steelman is genuinely weak; see README."""
    return scan(text, radius=radius).to_dict()


def rigor_cosplay_scan_corpus(documents: list[dict], radius: int = DEFAULT_PROXIMITY_RADIUS) -> dict:
    """Scan a list of documents and aggregate flag frequency across the
    corpus -- counting, not statistics; see `tools/basin_depth` for the
    significance-tested measurement this project ships. `documents`:
    list of `{"doc_id": str, "text": str}`."""
    try:
        pairs = [(str(d["doc_id"]), str(d["text"])) for d in documents]
    except (KeyError, TypeError) as exc:
        return {"error": f"malformed document: {exc}"}
    return scan_corpus(pairs, radius=radius).to_dict()
