"""A small, honest, regex-based sentence splitter -- not a real NLP
sentence boundary detector. It handles the common case (a period,
question mark, or exclamation point followed by whitespace and a
capital letter, digit, or opening quote/paren) and will mis-split on
abbreviations ("Dr. Smith," "e.g.," "U.S.") and mis-join sentences that
don't follow that pattern. This is a deliberate scope choice, not an
oversight: `removal_test.run_removal_test` needs *some* notion of "the
sentence containing this match" to remove, and a naive splitter that
you can read and reason about beats a silent dependency on a heavy NLP
library for what is, in this tool's target material (LinkedIn posts,
comments, short-form argumentative text), a mostly well-behaved case.
Read the `sentence` field of any match directly before trusting a
removal.
"""

from __future__ import annotations

import re

_SENTENCE_BOUNDARY_RE = re.compile(r'(?<=[.!?])\s+(?=[A-Z0-9"‘’“(])')


def split_sentences(text: str) -> list[tuple[int, int]]:
    """Return a list of (start, end) character spans, one per detected
    sentence, covering the entirety of `text` with no gaps or overlaps."""
    if not text:
        return []
    spans: list[tuple[int, int]] = []
    start = 0
    for m in _SENTENCE_BOUNDARY_RE.finditer(text):
        end = m.start()
        spans.append((start, end))
        start = m.end()
    spans.append((start, len(text)))
    return spans


def sentence_containing(text: str, spans: list[tuple[int, int]], position: int) -> tuple[int, int]:
    """Return the (start, end) span from `spans` that contains
    `position`. Falls back to the last span if `position` is at or past
    the end of `text` (can happen for a match ending exactly at the
    final character)."""
    for start, end in spans:
        if start <= position < end:
            return (start, end)
    return spans[-1] if spans else (0, len(text))
