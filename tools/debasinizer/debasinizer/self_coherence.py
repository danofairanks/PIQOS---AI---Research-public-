"""Detector for self-referential coherence-assertion phrasing: language
that asserts a claim's own internal consistency or certainty as if that
were evidence of its correspondence to reality, rather than presenting
anything checkable against reality.

This is the narrow, deliberately-scoped piece of a broader claim (see
this project's private research notes on "coherent behavior as terminal
target, reality optional") that a keyword scanner can honestly attempt:
NOT whether a claim is actually supported (this tool has no way to know
that), but whether the text is doing the specific rhetorical move of
treating its own fluency, internal consistency, or confidence AS IF it
were the support.

**This module does not detect absent citations.** For that half of the
picture -- unattributed quotes, uncited high-precision statistics --
see `tools/verification_lint` elsewhere in this repository, a separate
tool with its own, more developed proximity-based citation-gap
detection. Run both together for the fuller picture: this module flags
the self-coherence assertions; verification_lint flags the citation
gaps those assertions often stand in for.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_ASSERTION_PHRASES_RE = re.compile(
    r"\b(as\s+we(?:'ve|\s+have)\s+established|as\s+(?:already\s+)?established|"
    r"this\s+proves|which\s+proves|clearly|obviously|undeniably|"
    r"it\s+all\s+connects|everything\s+fits|the\s+pieces\s+(?:all\s+)?align|"
    r"makes?\s+perfect\s+sense|cannot\s+be\s+(?:a\s+)?coincidence|"
    r"too\s+coherent\s+to\s+be\s+false|the\s+pattern\s+is\s+unmistakable|"
    r"the\s+truth\s+(?:is\s+)?self[- ]evident)\b",
    re.IGNORECASE,
)


@dataclass
class Match:
    text: str
    start: int
    end: int

    def to_dict(self) -> dict:
        return {"text": self.text, "start": self.start, "end": self.end}


@dataclass
class SelfCoherenceResult:
    matches: list[Match] = field(default_factory=list)

    @property
    def flagged(self) -> bool:
        return len(self.matches) > 0

    @property
    def match_count(self) -> int:
        return len(self.matches)

    def to_dict(self) -> dict:
        return {
            "flagged": self.flagged,
            "match_count": self.match_count,
            "matches": [m.to_dict() for m in self.matches],
        }


def scan_self_coherence(text: str) -> SelfCoherenceResult:
    """Flag language that asserts a claim's own coherence/certainty as
    if that were evidence, rather than presenting anything checkable.
    Each phrase in the list is specific enough that a single match is a
    real lead -- unlike `resonance.py`'s ordinary-English word list,
    this list is not cross-category-gated."""
    matches = [Match(m.group(0), m.start(), m.end()) for m in _ASSERTION_PHRASES_RE.finditer(text)]
    return SelfCoherenceResult(matches=matches)
