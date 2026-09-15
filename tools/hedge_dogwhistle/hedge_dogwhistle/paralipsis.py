"""Detector for paralipsis (also apophasis): raising a claim by formally
declining to raise it -- "I'm not saying X" that installs X in the
reader's mind while giving the speaker deniability for having claimed
it. Distilled from an operator's own framing: hedging that, on one
hand, says "I'm not saying," while on the other hand functions as "pay
close attention to what I'm not saying" -- a dog whistle, where the
disclaimed content is signal that arrives only through the denial,
legible to whoever is primed to read it and deniable to whoever isn't.

This module detects the CONSTRUCTION only -- the classical rhetorical
figure's surface form. It cannot and does not judge whether any given
instance is actually functioning as coded signal versus genuine,
honest scope-limiting on a claim already made openly elsewhere. That
judgment is the other half of the diagnostic (the removal test -- see
`removal_test.py` and this tool's README), and it requires reading, not
regex.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .sentences import sentence_containing, split_sentences

_PARALIPSIS_RE = re.compile(
    r"\bi'?m\s+not\s+say(?:ing)?\b"
    r"|\bi\s+am\s+not\s+say(?:ing)?\b"
    r"|\bnot\s+to\s+suggest\b"
    r"|\bfar\s+be\s+it\s+from\s+me\s+to\b"
    r"|\bi\s+won'?t\s+(?:mention|speculate\s+on\s+whether|say)\b"
    r"|\bi\s+will\s+not\s+(?:mention|speculate\s+on\s+whether|say)\b"
    r"|\bnot\s+that\s+i'?m\s+implying\b"
    r"|\bnot\s+that\s+i\s+am\s+implying\b"
    r"|\bi'?m\s+not\s+implying\b"
    r"|\bi\s+am\s+not\s+implying\b"
    r"|\bnot\s+to\s+imply\b"
    r"|\bno\s+comment\s+on\s+whether\b"
    r"|\bi'?m\s+not\s+accusing\b"
    r"|\bi\s+am\s+not\s+accusing\b"
    r"|\bi'?m\s+not\s+calling\b",
    re.IGNORECASE,
)
# Note: deliberately does NOT include phrases like "make of that what you
# will" or "I'll let you draw your own conclusions" -- those are
# insinuation without a denial structure (nothing is formally declined),
# a related but distinct rhetorical move from paralipsis/apophasis. See
# README "What this tool does NOT detect."


@dataclass
class ParalipsisMatch:
    text: str
    start: int
    end: int
    sentence_start: int
    sentence_end: int
    sentence: str

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "start": self.start,
            "end": self.end,
            "sentence_start": self.sentence_start,
            "sentence_end": self.sentence_end,
            "sentence": self.sentence,
        }


def find_paralipsis(text: str) -> list[ParalipsisMatch]:
    """Find every paralipsis-construction match in `text`, each paired
    with the (naively split, see `sentences.py`) sentence that contains
    it. A lead list -- read each sentence directly, and see
    `removal_test.run_removal_test` for the mechanized next step (the
    operator's own proposed falsifiable test: does the reader's
    association with the disclaimed content survive removing the
    disclaiming sentence entirely)."""
    spans = split_sentences(text)
    matches: list[ParalipsisMatch] = []
    for m in _PARALIPSIS_RE.finditer(text):
        s_start, s_end = sentence_containing(text, spans, m.start())
        matches.append(
            ParalipsisMatch(
                text=m.group(0),
                start=m.start(),
                end=m.end(),
                sentence_start=s_start,
                sentence_end=s_end,
                sentence=text[s_start:s_end].strip(),
            )
        )
    return matches
