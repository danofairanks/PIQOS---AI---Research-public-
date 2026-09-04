"""Small helper shared across paper_rigor's own modules (not a
standalone-install concern the way sibling *packages* duplicating each
other's phrase lists is -- this is internal reuse within one package).

Caught during tuning against this repo's own real
`papers/published/mirror_test_v1.md`: a proximity heuristic alone
flagged "scientific consensus" and "studies show" as the paper's own
unsupported assertions, when the paper was actually *describing a
rhetorical maneuver* -- "the absence of published criticism was then
cited AS EVIDENCE OF scientific consensus" (a Lysenkoism case study,
critiquing the move, not making it) and a dismissal-tactic list entry
("Economic studies showing low productivity impact -> 'Lag effect'").
Neither is the document's own claim. A short pre-match window for
meta-framing verbs, and a short post-match window for the "->"/"→"
arrow this project's own dismissal-maneuver lists consistently use,
catches both real cases found -- not a general solution to
distinguishing assertion from description, just the specific shape
that showed up.

Extended when `credentialing.py` was wired in against
`papers/published/laundered_vocabulary_v1.md`: that document's "Law"
entry defines the founder-of-discursivity pattern itself, illustrating
it with "styling its author\nas 'Founder of' the field" -- the same
description-not-assertion shape as the cases above, but with the verb
and "as" separated by a short intervening phrase ("its author") rather
than sitting adjacent. `_STYLED_AS_RE` below tolerates up to four
intervening words for exactly this verb pair; checked against every
other document in this package's own real-document test fixtures
first (none contain "styled"/"styling" followed by "as" within that
gap), so this addition only newly excludes the shape it was built for.
"""

from __future__ import annotations

import re

_META_FRAMING_RE = re.compile(
    r'\b(?:cited as|described as|framed as|used as|presented as|dismissed as|labeled as|labelled as)\b',
    re.IGNORECASE,
)
_STYLED_AS_RE = re.compile(r'\bstyl(?:ed|ing)\b(?:\s+\S+){0,4}\s+as\b', re.IGNORECASE)
_ARROW_RE = re.compile(r'→|->')


def has_meta_framing_nearby(text: str, start: int, end: int, *,
                             before_window: int = 60, after_window: int = 40) -> bool:
    before = text[max(0, start - before_window):start]
    after = text[end:end + after_window]
    return (
        bool(_META_FRAMING_RE.search(before))
        or bool(_ARROW_RE.search(after))
        or bool(_STYLED_AS_RE.search(before))
    )
