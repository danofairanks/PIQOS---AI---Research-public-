"""Shared section-heading detection across paper_rigor's own modules.

Two format families motivated this: markdown (`# Heading`, `## 10.
LIMITATIONS AND SCOPE CAVEATS`), used by every specimen in this repo's
own `papers/`, and plain numbered headings with no markup at all
(`7. Honest Limitations and Genuine Improvements`), found in a real
PDF-extracted specimen used to validate this tool -- PDF text
extraction drops markdown entirely, so a heading-detection regex tuned
only against `#` silently misses every section in a PDF-derived paper,
including a genuine, substantive limitations section (see README "A
harness, not another patch").

Centralized here rather than duplicated per call site --
`citations.py`'s references-section boundary and `disclaimer.py`'s
limitations-heading check were each rolling their own `#`-only regex
before this existed. A future section-aware check gets both formats
for free instead of re-solving heading detection again.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_MARKDOWN_HEADING_RE = re.compile(r'^(#{1,6})\s+(\S.*?)\s*$', re.MULTILINE)

# A line that IS a heading and nothing else: an optional numeric
# prefix ("7." / "3.2" / "Section 7:"), then a short, period-free
# phrase, the whole line ending immediately after. Excluding periods
# from the title body is what keeps this from matching ordinary
# sentences (which almost always contain one) while still matching
# real headings like "7. Honest Limitations and Genuine Improvements",
# "5.2 Elite Cognitive Stress Test: Fifteen Faculties (60/60)",
# "10. Conclusion" -- all found verbatim in the specimen that
# motivated this module.
_PLAIN_HEADING_RE = re.compile(
    r'^(?:\d{1,2}(?:\.\d{1,2})?\.?\s+|Section\s+\d+\.?\s*:?\s+)'
    r'([A-Z][^\n.]{1,78})$',
    re.MULTILINE,
)


@dataclass
class Heading:
    text: str            # the heading's own text, numbering/markup stripped
    start: int            # start of the heading line in the source text
    end: int              # end of the heading line (start of the next line)
    level: int | None     # markdown level (1-6) if known; None for plain headings

    def to_dict(self) -> dict:
        return {"text": self.text, "start": self.start, "end": self.end, "level": self.level}


def iter_headings(text: str) -> list[Heading]:
    """Every detected heading, in document order, across both formats.

    Best-effort, same contract as every other heuristic in this
    package: a short, period-free, numbered line inside a genuine
    enumerated list in body prose ("1. Fast\\n2. Cheap\\n3. Reliable")
    can false-positive as a heading; a heading using neither convention
    (underlined text, ALL-CAPS with no numbering, a title styled only
    by font in the original PDF) is not detected at all."""
    headings: list[Heading] = []
    for m in _MARKDOWN_HEADING_RE.finditer(text):
        headings.append(Heading(text=m.group(2).strip(), start=m.start(), end=m.end(), level=len(m.group(1))))
    for m in _PLAIN_HEADING_RE.finditer(text):
        headings.append(Heading(text=m.group(1).strip(), start=m.start(), end=m.end(), level=None))
    headings.sort(key=lambda h: h.start)
    return headings


def find_section(text: str, name_pattern: re.Pattern, *, extra_stop: re.Pattern | None = None) -> str | None:
    """Body text following the first heading whose text matches
    `name_pattern` (searched, not required to fully equal the heading
    -- "Honest Limitations and Genuine Improvements" matches a
    `limitations` pattern this way), up to the next heading of either
    format, an `extra_stop` match if given (e.g. a standalone `---`
    divider that ends a section without itself being a heading), or
    end of document. `None` if no matching heading is found."""
    headings = iter_headings(text)
    for i, h in enumerate(headings):
        if name_pattern.search(h.text):
            body_start = h.end
            body_end = headings[i + 1].start if i + 1 < len(headings) else len(text)
            if extra_stop:
                stop_match = extra_stop.search(text, body_start, body_end)
                if stop_match:
                    body_end = stop_match.start()
            return text[body_start:body_end]
    return None


def has_heading_matching(text: str, name_pattern: re.Pattern) -> bool:
    return any(name_pattern.search(h.text) for h in iter_headings(text))
