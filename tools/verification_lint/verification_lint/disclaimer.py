"""Detect whether a document contains any 'what this does not
claim/establish' disclaimer, anywhere in the text.

Grounded in two real, distinct headings already used across this
repo's own documents -- "What This Case Study Does Not Claim"
(case_studies/) and "What this tracker does NOT yet establish"
(papers/published/conjecture_tracker_v1.md) -- rather than assuming
one exact phrase. This is a document-level check, not a per-claim one:
it answers "does this document ever scope its own claims" rather than
"is every individual claim scoped," which the quote/statistic
detectors are closer to.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_DISCLAIMER_RE = re.compile(
    r'does\s+not\s+claim|does\s+not\s+establish|not\s+yet\s+establish|'
    r'this\s+does\s+not\s+claim',
    re.IGNORECASE,
)


@dataclass
class DisclaimerCheck:
    present: bool
    applicable: bool  # False for short documents where the check doesn't apply
    word_count: int
    min_word_count: int

    @property
    def gap(self) -> bool:
        """A reportable gap: long enough to expect scoping, and none found."""
        return self.applicable and not self.present

    def to_dict(self) -> dict:
        return {"present": self.present, "applicable": self.applicable,
                "word_count": self.word_count, "min_word_count": self.min_word_count, "gap": self.gap}


def check_disclaimer(text: str, *, min_word_count: int = 400) -> DisclaimerCheck:
    """`min_word_count` is a judgment call, not a value taken from any
    project document: short specimens/notes don't need a formal
    scoping section the way a multi-section analysis does. Tune it per
    corpus if 400 doesn't match your own documents' typical length."""
    word_count = len(text.split())
    return DisclaimerCheck(
        present=bool(_DISCLAIMER_RE.search(text)),
        applicable=word_count >= min_word_count,
        word_count=word_count,
        min_word_count=min_word_count,
    )
