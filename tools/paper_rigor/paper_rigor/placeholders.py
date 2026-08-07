"""Detect two distinct things that get conflated under "placeholder":
a claim asserted as settled while the actual derivation is skipped
(the real problem), versus a value explicitly labeled as unresolved
(this project's own `EMPIRICAL_FILL_IN` convention, CLAUDE.md's
"not yet run/tested" / "derivation-blocked" framing -- an honest
practice, not a gap). A detector that can't tell these apart would
flag the honest version at the same severity as the disguised one,
which defeats the point of labeling a placeholder in the first place.

Phrase lists are deliberately narrow and multi-word (not bare "clearly"
or "obviously", which are common in ordinary prose and inside quoted
material -- see README "What this does NOT do" for the false-positive
this was tuned against: a real paper quoting a source who used
"clearly" in a direct quote is not the paper's own hand-wave).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Confident-sounding phrases that substitute for showing the actual
# derivation/evidence, rather than stating a real placeholder is one.
HAND_WAVE_PHRASES = [
    "it is trivial to show", "it is trivial that", "trivially follows",
    "trivially true", "it can easily be shown", "it can trivially be shown",
    "we leave this as an exercise", "details omitted for brevity",
    "for reasons that should be clear", "it goes without saying",
    "needless to say", "as anyone can see", "clearly follows that",
    "obviously true", "self-evidently", "requires no further justification",
]

# Literal markers of unfinished content NOT accompanied by an honest
# label -- e.g. a bare "TODO" or "[insert result]" in text that
# otherwise presents itself as a finished, publishable claim. "would
# include" / "would cite" caught a real specimen during tuning: a
# References section whose entire content was "[References would
# include citations to LeCun papers, ... ]" -- describing what a
# bibliography would contain instead of containing one, while the body
# text cites specific dated statements as if sourced.
UNLABELED_MARKERS = [
    "tbd", "todo", "fixme", "xxx", "[insert", "lorem ipsum",
    "placeholder text", "insert data here", "insert citation here",
    "would include citations", "would cite", "references would include",
]

# The honest version: a value explicitly marked as unresolved. Matches
# here are informational, not gaps -- logged separately so a paper
# using this convention correctly is never penalized for it.
LABELED_PLACEHOLDER_PHRASES = [
    "empirical_fill_in", "not yet measured", "not yet tested",
    "not yet run", "derivation-blocked", "pending calibration",
    "left as future work", "left open for future work",
    "awaiting empirical", "empirically-gated", "empirical-gated",
]

_HAND_WAVE_RE = re.compile("|".join(re.escape(p) for p in HAND_WAVE_PHRASES), re.IGNORECASE)
_UNLABELED_RE = re.compile("|".join(re.escape(p) for p in UNLABELED_MARKERS), re.IGNORECASE)
_LABELED_RE = re.compile("|".join(re.escape(p) for p in LABELED_PLACEHOLDER_PHRASES), re.IGNORECASE)

CONTEXT_CHARS = 80


@dataclass
class PlaceholderMatch:
    kind: str  # "hand_wave" | "unlabeled_marker" | "labeled_placeholder"
    phrase: str
    start: int
    end: int
    context: str

    def to_dict(self) -> dict:
        return {"kind": self.kind, "phrase": self.phrase, "start": self.start,
                "end": self.end, "context": self.context}


def _matches(pattern: re.Pattern, text: str, kind: str) -> list[PlaceholderMatch]:
    out = []
    for m in pattern.finditer(text):
        start, end = max(0, m.start() - CONTEXT_CHARS), min(len(text), m.end() + CONTEXT_CHARS)
        out.append(PlaceholderMatch(kind=kind, phrase=m.group(0), start=m.start(),
                                     end=m.end(), context=text[start:end]))
    return out


def find_placeholder_issues(text: str) -> dict:
    """Returns `{"gaps": [...], "labeled": [...]}`. `gaps` are the real
    finding (hand-wave phrases and unlabeled unfinished markers);
    `labeled` is informational only -- honest placeholder usage, never
    counted toward a severity total."""
    gaps = _matches(_HAND_WAVE_RE, text, "hand_wave") + _matches(_UNLABELED_RE, text, "unlabeled_marker")
    labeled = _matches(_LABELED_RE, text, "labeled_placeholder")
    return {"gaps": gaps, "labeled": labeled}
