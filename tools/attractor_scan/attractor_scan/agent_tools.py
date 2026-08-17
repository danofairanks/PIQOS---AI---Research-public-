"""Stable, JSON-in/JSON-out function surface for agent tool-calling.

Same contract as `bifp/agent_tools.py` and `basin_depth/agent_tools.py`:
every function here takes and returns only plain JSON-serializable
types, so it can be wrapped directly as MCP tool handlers without any
adaptation layer. `tools/mcp_server/` does exactly that.
"""

from __future__ import annotations

from .scan import scan, scan_corpus
from .visual_proof_judge import DEFAULT_MODEL, VisualProofJudgeError, judge_visual_proof


def attractor_scan_text(text: str) -> dict:
    """Run every implemented maneuver (§4.1, 7 categories), semantic-
    laundering (§2.8, 5 of 6 cases) classifier, and the unglossed-
    formal-object detector (bare private equation notation + law-naming
    + self-attribution co-occurrence; not one of the six §2.8 cases --
    see formal_object.py) against a single piece of text. Returns
    matched spans per category, not just labels -- a lead for a
    human/agent review pass, not a verdict; see README for what
    `density` does and does not mean, and why it excludes the
    unglossed-formal-object result."""
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


def attractor_scan_judge_visual_proof(claim_text: str, image_path: str, *,
                                       model: str = DEFAULT_MODEL) -> dict:
    """Get one AI-generated (Groq vision) candidate read on Case 6
    (§2.8: technical precision borrowed as visual proof) for a single
    image + claim pair. Advisory only -- a research aid for drafting a
    case study, never a verdict, never wired into scan()/scan_corpus();
    see visual_proof_judge.py's module docstring and the README's "Why
    Case 6 isn't here" for why this stays single-specimen. Requires
    GROQ_API_KEY in the environment; returns {"error": ...} rather than
    raising if it's missing, the image can't be read, or the call
    fails, matching this module's existing tool-calling ABI contract."""
    try:
        result = judge_visual_proof(claim_text, image_path=image_path, model=model)
    except VisualProofJudgeError as exc:
        return {"error": str(exc)}
    return result.to_dict()
