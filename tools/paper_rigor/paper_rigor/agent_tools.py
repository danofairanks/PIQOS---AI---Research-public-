"""Stable, JSON-in/JSON-out function surface for agent tool-calling.

Same contract as the other four packages' agent_tools.py modules:
every function here takes and returns only plain JSON-serializable
types, so it can be wrapped directly as MCP tool handlers.
`tools/research_mcp/` does exactly that.

`paper_rigor_scan`'s output is meant to drive a two-step agent flow:
call it first to get `structural_gap_count` (fixable by an author, no
lookup needed) and `external_verification_worklist` (leads an agent
with real web search/fetch access should resolve) separately -- the
worklist is not itself a verdict.
"""

from __future__ import annotations

from .scan import scan_paper


def paper_rigor_scan(text: str, *, byline_authors: list[str] | None = None,
                      min_word_count: int = 400) -> dict:
    """Scan a paper's text for placeholder/hand-wave phrases, an
    unstated falsifiability condition, self-citation ratio and
    formal/informal sourcing mix, uncited empirical-certainty claims,
    credential-substituted-for-evidence claims, unsupported consensus
    claims, and a missing limitations section.

    `byline_authors`: the paper's own declared author last names, if
    any -- needed to compute self-citation ratio; omit for anonymous/
    collective-voice documents (self_citation.ratio comes back `null`
    rather than a meaningless 0.0).
    """
    return scan_paper(text, byline_authors=byline_authors, min_word_count=min_word_count).to_dict()
