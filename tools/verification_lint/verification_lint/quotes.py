"""Detect direct quotes with no nearby attribution signal.

This is the content-level version of the discipline this project's
own case studies apply by hand: a quoted claim needs a named source
(who said it, on what platform, when), not just quotation marks. The
detector is deliberately coarse -- proximity of a plausible attribution
signal, not a parsed sentence -- see README for exactly what that does
and doesn't catch.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_STRAIGHT_QUOTE_RE = re.compile(r'"([^"\n]{40,300})"')
_CURLY_QUOTE_RE = re.compile(r'“([^”\n]{40,300})”')

_ATTRIBUTION_SIGNALS = [
    re.compile(r'\b(said|wrote|posted|tweeted|stated|replied|responded|writes|says|reads|argues|documents)\b', re.IGNORECASE),
    re.compile(r'\bper\b|\bquoted\s+(?:in\s+full|verbatim|directly)\b', re.IGNORECASE),
    re.compile(r'\b(X|Twitter|LinkedIn|Reddit|YouTube|Substack|blog|interview|podcast|press release)\b', re.IGNORECASE),
    re.compile(r'@\w+'),
    re.compile(r'\]\('),  # a markdown link nearby
    re.compile(r'\b(19|20)\d{2}\b'),  # a year, loosely signaling a dated citation
    re.compile(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'),  # a plausible proper name (First Last)
    re.compile(r'§\s?\d'),  # a section-number citation (this project's own protocol/paper style)
    re.compile(r'\bPhase\s+\d\b', re.IGNORECASE),  # e.g. "BIFP Phase 5"
    re.compile(r'\b[A-Z]{2,}\b'),  # an acronym (BIFP, ICML, ...) standing in for a named source
    re.compile(r'\([^)]*\d[^)]*\)'),  # any parenthetical containing a digit (date, section, figure ref)
]

DEFAULT_WINDOW = 250  # characters searched before/after a quote for an attribution signal


@dataclass
class QuoteFinding:
    quote: str
    start: int
    end: int
    context: str

    def to_dict(self) -> dict:
        return {"quote": self.quote, "start": self.start, "end": self.end, "context": self.context}


def _iter_quotes(text: str):
    for m in _STRAIGHT_QUOTE_RE.finditer(text):
        yield m
    for m in _CURLY_QUOTE_RE.finditer(text):
        yield m


def find_unattributed_quotes(text: str, *, window: int = DEFAULT_WINDOW) -> list[QuoteFinding]:
    """Flag quoted spans (40+ characters -- long enough that they read as
    a substantive claim rather than a scare-quoted term like "safety" or
    "coding harness and tool calls") with no attribution signal within
    `window` characters on either side. A quote's exact text is only
    flagged once per document: once a phrase has been attributed
    anywhere it appears, repeating that same phrase later (e.g. a
    specimen quoted in full once, then referenced again in a "Checked
    Against Primary Sources" section) is not re-flagged."""
    findings: list[QuoteFinding] = []
    seen_starts: set[int] = set()
    attributed_quote_texts: set[str] = set()
    unattributed_by_text: dict[str, QuoteFinding] = {}

    for m in sorted(_iter_quotes(text), key=lambda m: m.start()):
        if m.start() in seen_starts:
            continue
        seen_starts.add(m.start())
        window_start = max(0, m.start() - window)
        window_end = min(len(text), m.end() + window)
        context = text[window_start:window_end]
        quote_text = m.group(1)
        if any(sig.search(context) for sig in _ATTRIBUTION_SIGNALS):
            attributed_quote_texts.add(quote_text)
            unattributed_by_text.pop(quote_text, None)
        elif quote_text not in attributed_quote_texts and quote_text not in unattributed_by_text:
            unattributed_by_text[quote_text] = QuoteFinding(
                quote=quote_text, start=m.start(), end=m.end(), context=context
            )

    return list(unattributed_by_text.values())
