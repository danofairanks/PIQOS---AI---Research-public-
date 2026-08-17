"""Stable, JSON-in/JSON-out function surface for agent tool-calling.
Same contract as `basin_depth/agent_tools.py`, `bifp/agent_tools.py`,
`attractor_scan/agent_tools.py`, `debasinizer/agent_tools.py`, and
`paper_rigor/agent_tools.py`: every function here takes and returns only
plain JSON-serializable types, so it can be wrapped directly as MCP tool
handlers -- or called from a Pyodide-in-browser scanner -- without any
adaptation layer.

Not wired into `tools/research_mcp/` -- that server's own README scopes
this package as a repository-maintenance tool (linting this repo's own
`case_studies/` house format) rather than an agent-callable research
tool. That reasoning is specific to research_mcp's own scope question;
it doesn't disqualify this surface from other callers (e.g. a combined
paper-rigor report) for which unattributed-quote and uncited-statistic
detection is directly relevant regardless of source repository.
"""

from __future__ import annotations

from .scan import scan_document


def verification_lint_scan_text(text: str, *, min_word_count: int = 400) -> dict:
    """Scan a piece of text for unattributed direct quotes (40+ chars,
    no attribution signal within 250 chars), uncited high-precision
    statistics (decimal percentages, dollar amounts, large comma-grouped
    counts, fractions), and a missing disclaimer/scoping ("what this
    does not claim") section. Domain-agnostic -- no PIQOS-specific
    vocabulary required. `severe_gap_count` (not the raw `gap_count`) is
    the primary signal: it discounts findings when the document has an
    end-of-document blanket-citation statement to fall back on. A flag
    is a lead for a human/agent review pass, not a verdict; see
    README."""
    return scan_document(text, min_word_count=min_word_count).to_dict()
