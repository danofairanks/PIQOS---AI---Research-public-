"""Heuristic falsifiability check: does the paper state any condition
under which its own claim would be considered wrong, anywhere in the
document? A paper can be long and detailed and still never say what
result would count against it.

This is deliberately document-level, not per-claim -- distinguishing
"claim 4 on page 2 lacks a stated test" from "this entire paper never
states one anywhere" would need real claim segmentation, which a regex
pass can't do honestly. Document-level is the coarser but truthful
version: presence/absence of testable-condition language anywhere,
set against unconditional-certainty language.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

TESTABLE_MARKERS = [
    "we test whether", "predicts that", "would be falsified if",
    "would falsify this", "null hypothesis", "control condition",
    "baseline comparison", "ablation", "if this is true, we would expect",
    "counter-example would be", "this claim fails if", "would refute this",
]

# Unconditional-certainty language: fine on its own, but combined with
# zero testable markers anywhere in the document, it's a paper that
# asserts total confidence while never naming a way to check it.
CERTAINTY_MARKERS = [
    "proves that", "conclusively demonstrates", "conclusively shows",
    "definitively establishes", "irrefutably", "without question",
    "beyond any doubt", "indisputably",
]

_TESTABLE_RE = re.compile("|".join(re.escape(p) for p in TESTABLE_MARKERS), re.IGNORECASE)
_CERTAINTY_RE = re.compile("|".join(re.escape(p) for p in CERTAINTY_MARKERS), re.IGNORECASE)

CONTEXT_CHARS = 80


@dataclass
class FalsifiabilityCheck:
    has_testable_markers: bool
    certainty_claims: list[dict]

    @property
    def gap(self) -> bool:
        """Certainty language present with no testable-condition
        language anywhere in the document."""
        return bool(self.certainty_claims) and not self.has_testable_markers

    def to_dict(self) -> dict:
        return {"has_testable_markers": self.has_testable_markers,
                "certainty_claims": self.certainty_claims, "gap": self.gap}


def check_falsifiability(text: str) -> FalsifiabilityCheck:
    testable = bool(_TESTABLE_RE.search(text))
    certainty_claims = []
    for m in _CERTAINTY_RE.finditer(text):
        start, end = max(0, m.start() - CONTEXT_CHARS), min(len(text), m.end() + CONTEXT_CHARS)
        certainty_claims.append({"phrase": m.group(0), "start": m.start(),
                                  "end": m.end(), "context": text[start:end]})
    return FalsifiabilityCheck(has_testable_markers=testable, certainty_claims=certainty_claims)
