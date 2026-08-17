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

from ._code_fences import mask_code_fences

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
    # (?<!\d\.) excludes a fraction-shaped match whose digits are actually
    # the tail of a decimal-point version number ("Sonnet 4.6/5" reads as
    # fraction "6/5" without this guard, because \b sits right between "."
    # and "6") -- a real false positive caught scanning
    # governance_binding_axiom_v1.md's model-version list ("4.6/5",
    # "4.6/4.8"). A genuine fraction ("3/4 of respondents") is never
    # preceded by "<digit>.", so this doesn't cost real detections.
    "fraction_count": re.compile(r'(?<!\d\.)\b\d+/\d+\b'),
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
    which is where unearned precision actually tends to hide. Fenced
    code blocks are masked before matching (see `_code_fences.py`) -- a
    slash-separated number or long literal inside a quoted-in-full code
    specimen is not an uncited empirical claim, and code content within
    `window` of a real flagged number must not count as a citation
    signal either (same reasoning as quotes.py's signal_window fix --
    e.g. a `[1]`-shaped list index or an in-code year-like constant
    should not silently "cite" a nearby prose statistic), so the
    citation-signal search runs against the masked text too; only the
    returned `context` field uses the original, readable text."""
    findings: list[StatFinding] = []
    seen: set[tuple[int, int]] = set()
    matches = []
    search_text = mask_code_fences(text)
    for kind, pattern in _STAT_PATTERNS.items():
        for m in pattern.finditer(search_text):
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
        signal_window = search_text[window_start:window_end]
        if not any(sig.search(signal_window) for sig in _CITATION_SIGNALS):
            findings.append(StatFinding(kind=kind, value=m.group(0), start=m.start(),
                                         end=m.end(), context=context))
    return findings
