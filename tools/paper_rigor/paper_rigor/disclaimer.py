"""A paper's "what this does not establish" check reuses
verification_lint's disclaimer check (inline-phrase detection: "does
not claim," "does not establish," "not yet establish") as one of two
signals, rather than duplicating that logic -- it's already tuned
against this repo's own case_studies/ convention and a second,
independently-tuned copy would just drift from it. This is the one
place `paper_rigor` is NOT standalone-installable -- see README
"Install".

The second signal is new here: a recognized limitations-section
*heading* -- via `headings.py`'s shared detector, so it works whether
the paper uses markdown ("## Limitations", "## 10. Limitations and
Scope Caveats") or the plain numbered-heading convention PDF-extracted
text uses (see `headings.py`'s own module docstring for the real
specimen that motivated dual-format support). The name match itself is
deliberately a substring search, not a full match against a fixed
phrase list: a real specimen titled its section "7. Honest Limitations
and Genuine Improvements" -- "Honest" before, "and Genuine
Improvements" after -- which no fixed-phrase match would have caught
even with the heading correctly detected. Searching for the word
"limitations" anywhere in a heading's text is a strong enough signal
on its own that the false-positive risk of loosening past an exact
phrase is low.

Originally caught during tuning against this repo's own
`protocols/noether_coherence_test_protocol_v1.md` -- a real, rigorous
document with a full "## 10. LIMITATIONS AND SCOPE CAVEATS" section
that `verification_lint`'s inline-phrase-only check does not
recognize, because it was tuned for a different, narrower house
convention (exact case-study/tracker phrasing) than the general
academic "Limitations" heading convention this tool also needs to
recognize. Rather than loosen `verification_lint`'s own tuned regex
and risk drifting its already-pinned `case_studies/` numbers, this
module adds the heading check as its own second signal on top.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from verification_lint.disclaimer import check_disclaimer

from .headings import has_heading_matching

_LIMITATIONS_NAME_RE = re.compile(r'\blimitations\b|threats\s+to\s+validity|\bcaveats\b', re.IGNORECASE)


@dataclass
class LimitationsCheck:
    present: bool
    applicable: bool
    word_count: int
    min_word_count: int
    has_inline_phrase: bool
    has_heading_section: bool

    @property
    def gap(self) -> bool:
        return self.applicable and not self.present

    def to_dict(self) -> dict:
        return {"present": self.present, "applicable": self.applicable,
                "word_count": self.word_count, "min_word_count": self.min_word_count,
                "has_inline_phrase": self.has_inline_phrase,
                "has_heading_section": self.has_heading_section, "gap": self.gap}


def check_limitations_section(text: str, *, min_word_count: int = 400) -> LimitationsCheck:
    inline = check_disclaimer(text, min_word_count=min_word_count)
    has_heading = has_heading_matching(text, _LIMITATIONS_NAME_RE)
    return LimitationsCheck(
        present=inline.present or has_heading,
        applicable=inline.applicable, word_count=inline.word_count, min_word_count=inline.min_word_count,
        has_inline_phrase=inline.present, has_heading_section=has_heading,
    )
