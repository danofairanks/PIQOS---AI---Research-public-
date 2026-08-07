"""Detect unsupported consensus claims -- "it is well known that,"
"the scientific consensus is," "everyone agrees" -- with no citation
signal nearby. Same proximity-heuristic shape as verification_lint's
quote/statistic detectors and citations.py's uncited-empirical-claims
check; a different phrase list, same mechanism, deliberately not
imported (see citations.py's module docstring on why the mechanism is
duplicated a few times across this project's tools rather than shared).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ._shared import has_meta_framing_nearby

CONSENSUS_PHRASES = [
    "widely accepted", "well established", "well-established", "scientific consensus",
    "it is well known that", "it is well-known that", "everyone agrees", "no one disputes",
    "universally recognized", "consensus view", "broad consensus", "general consensus",
    "most researchers agree", "most experts agree", "the field agrees",
]
_CONSENSUS_RE = re.compile("|".join(re.escape(p) for p in CONSENSUS_PHRASES), re.IGNORECASE)

_CITATION_SIGNALS = [
    re.compile(r'\([A-Z][A-Za-z\'-]+(?:\s*(?:&|and|,)\s*[A-Z][A-Za-z\'-]+)*,?\s*\d{4}[a-z]?\)'),
    re.compile(r'\[\^?\d+\]'),
    re.compile(r'https?://\S+'),
    re.compile(r'\bet al\.'),
    re.compile(r'\bsurvey(?:ed)?\b', re.IGNORECASE),
    re.compile(r'\bmeta-analysis\b', re.IGNORECASE),
]

CONTEXT_CHARS = 150


@dataclass
class ConsensusMatch:
    phrase: str
    start: int
    end: int
    context: str

    def to_dict(self) -> dict:
        return {"phrase": self.phrase, "start": self.start, "end": self.end, "context": self.context}


def find_unsupported_consensus_claims(text: str, *, window: int = CONTEXT_CHARS) -> list[ConsensusMatch]:
    out = []
    for m in _CONSENSUS_RE.finditer(text):
        if has_meta_framing_nearby(text, m.start(), m.end()):
            continue
        start, end = max(0, m.start() - window), min(len(text), m.end() + window)
        context = text[start:end]
        if not any(sig.search(context) for sig in _CITATION_SIGNALS):
            out.append(ConsensusMatch(phrase=m.group(0), start=m.start(), end=m.end(), context=context))
    return out
