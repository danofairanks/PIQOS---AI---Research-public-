"""Mechanizes the removal-test half of the Hedge-as-Dog-Whistle
diagnostic. The operator's own proposed test, stated precisely: "We
could have removed the hedging all together and would it have promoted
that assumption?" Operationalized: take the disclaiming sentence(s) out
of the specimen entirely, then ask whether the reader's association
with the disclaimed content survives the removal.

- If the association DEPENDS ON the disclaimer -- no direct, unhedged
  statement establishes it anywhere else in the specimen, and removing
  the denial removes the association -- the disclaimer is doing the
  planting. Consistent with the dog-whistle reading.
- If the association is ALREADY ESTABLISHED elsewhere in the specimen
  by direct, unhedged statement, and removing the disclaimer leaves
  that association exactly as strong, the disclaimer is not what
  plants it -- ordinary epistemic hygiene, not covert signaling.

**What this module does, precisely, and what it does NOT do.** It
performs the mechanical half only: finding each paralipsis sentence and
producing the text with those sentences removed, so a human or agent
can re-read what remains and make the actual judgment call above. It
cannot itself determine whether the disclaimed content is "established
elsewhere... by direct, unhedged statement" -- that requires knowing
what the disclaimed content *is* (a semantic question about what "X" in
"I'm not saying X" refers to) and searching the remaining text for it,
neither of which a regex construction-detector can do. Read the
`text_with_hedges_removed` output directly and apply the test above by
hand (or hand it to an LLM agent to judge) -- this tool gets you to that
point mechanically, it does not complete the judgment.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .paralipsis import ParalipsisMatch, find_paralipsis


def _merge_spans(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not spans:
        return []
    ordered = sorted(spans)
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))
    return merged


def remove_spans(text: str, spans: list[tuple[int, int]]) -> str:
    """Remove each (start, end) span from `text`, joining the
    remaining pieces with a single space and trimming. Overlapping or
    adjacent spans are merged first so nothing is double-removed."""
    merged = _merge_spans(spans)
    pieces: list[str] = []
    cursor = 0
    for start, end in merged:
        if start > cursor:
            pieces.append(text[cursor:start])
        cursor = max(cursor, end)
    pieces.append(text[cursor:])
    joined = " ".join(p.strip() for p in pieces if p.strip())
    return joined


@dataclass
class RemovalTestResult:
    matches: list[ParalipsisMatch] = field(default_factory=list)
    text_with_hedges_removed: str = ""

    @property
    def has_paralipsis(self) -> bool:
        return len(self.matches) > 0

    def to_dict(self) -> dict:
        return {
            "matches": [m.to_dict() for m in self.matches],
            "has_paralipsis": self.has_paralipsis,
            "text_with_hedges_removed": self.text_with_hedges_removed,
            "note": (
                "text_with_hedges_removed has every sentence containing a "
                "paralipsis construction deleted. Re-read it and ask: does "
                "the disclaimed content's association still stand without "
                "the hedge? If yes -- some other, unhedged sentence already "
                "established it -- this reads as a genuine scope-limit, not "
                "a dog whistle. If the association clearly depended on the "
                "removed sentence, that is consistent with the dog-whistle "
                "reading. This tool does not make that call for you."
            ),
        }


def run_removal_test(text: str) -> RemovalTestResult:
    """Find paralipsis constructions in `text` and return the text with
    every containing sentence removed, mechanizing the first step of
    the removal test. See module docstring for what judgment is left to
    the reader (human or agent)."""
    matches = find_paralipsis(text)
    spans = [(m.sentence_start, m.sentence_end) for m in matches]
    return RemovalTestResult(
        matches=matches, text_with_hedges_removed=remove_spans(text, spans)
    )
