"""Detect high-precision numeric claims with no nearby citation signal.

Same proximity-heuristic approach as quotes.py, applied to the other
half of "no exemption by source" evidentiary discipline: a specific
number (a percentage to two decimal places, a dollar figure, a large
count) reads as more credible than a round one, precisely because it
looks measured -- which is exactly why it needs a source, not less of one.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_STAT_PATTERNS: dict[str, re.Pattern] = {
    "decimal_percent": re.compile(r'\b\d+\.\d+\s*%'),
    # A trailing lookahead, not \b: a suffix like "T" directly abutting the
    # number (e.g. "$3.9T") is itself a word character, so \b would force
    # the regex to backtrack off the decimal portion to find a boundary --
    # a real bug caught by testing against this repo's own real numbers
    # (see tests/test_statistics.py's regression test for "$3.9T").
    "dollar_amount": re.compile(
        r'\$\d[\d,]*(?:\.\d+)?\s*(?:[BMKT]|billion|million|thousand|trillion)?(?=[\s,.:;!?)]|$)',
        re.IGNORECASE,
    ),
    "large_comma_count": re.compile(r'\b\d{1,3}(?:,\d{3})+\b'),
    "fraction_count": re.compile(r'\b\d+/\d+\b'),
}

_CITATION_SIGNALS = [
    re.compile(r'\]\('),  # markdown link
    re.compile(r'\bper\b|\baccording to\b|\bsource:\b|\bcited in\b|\bpublished\b', re.IGNORECASE),
    re.compile(r'\([A-Z][a-zA-Z.\'-]+(?:,|\set al\.,)?\s*(?:19|20)\d{2}\)'),  # (Author, 2026) / (Author et al., 2026)
    re.compile(r'\[\^?\d+\]'),  # footnote-style marker
]

DEFAULT_WINDOW = 150


@dataclass
class StatFinding:
    kind: str
    value: str
    start: int
    end: int
    context: str

    def to_dict(self) -> dict:
        return {"kind": self.kind, "value": self.value, "start": self.start,
                "end": self.end, "context": self.context}


def find_uncited_statistics(text: str, *, window: int = DEFAULT_WINDOW) -> list[StatFinding]:
    """Flag high-precision numbers with no citation signal within
    `window` characters. A plain round integer ("about 20 sources") is
    not flagged -- only the four higher-specificity patterns above,
    which is where unearned precision actually tends to hide."""
    findings: list[StatFinding] = []
    seen: set[tuple[int, int]] = set()
    matches = []
    for kind, pattern in _STAT_PATTERNS.items():
        for m in pattern.finditer(text):
            matches.append((kind, m))
    matches.sort(key=lambda km: km[1].start())

    for kind, m in matches:
        span = (m.start(), m.end())
        if span in seen:
            continue
        seen.add(span)
        window_start = max(0, m.start() - window)
        window_end = min(len(text), m.end() + window)
        context = text[window_start:window_end]
        if not any(sig.search(context) for sig in _CITATION_SIGNALS):
            findings.append(StatFinding(kind=kind, value=m.group(0), start=m.start(),
                                         end=m.end(), context=context))
    return findings
