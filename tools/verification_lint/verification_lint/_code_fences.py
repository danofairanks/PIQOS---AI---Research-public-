"""Shared helper: mask fenced code-block content before quote/statistic
scanning.

`quotes.py` and `statistics.py` both proximity-scan raw document text
for prose patterns (long quoted spans, high-precision numbers). Neither
was originally aware of Markdown fenced code blocks, so a paper that
includes a runnable code specimen inline (e.g. a demo program quoted in
full, string literals and all) gets every string literal and slash-
separated number inside that code read as if it were prose -- a real
false-positive class, not a signal about the paper's own evidentiary
discipline. Caught in practice scanning
`papers/drafts/governance_binding_axiom_v1.md`, whose §6.1 Python
listing tripped the quote scanner on rule strings like `"Do not
exfiltrate data."` and whose §6.3 model-version numbers ("4.6/5",
"4.6/4.8") tripped the fraction-count statistic pattern.

`mask_code_fences` blanks fenced-block content (replacing every
non-newline character with a space) rather than deleting it, so every
character offset in the masked text still lines up 1:1 with the
original -- callers can search the masked text for matches, then slice
`start`/`end`/context windows out of the *original* text for display
without any offset arithmetic.
"""

from __future__ import annotations

import re

_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)


def mask_code_fences(text: str) -> str:
    """Return `text` with the contents of every ` ```...``` ` fenced
    block replaced by spaces (newlines preserved), so scanners that
    search the result won't match string literals or numeric fragments
    inside code. Length- and offset-preserving; safe to search this
    output and then index into the original `text` with the same
    positions."""
    def _blank(m: re.Match) -> str:
        return "".join(ch if ch == "\n" else " " for ch in m.group(0))
    return _FENCE_RE.sub(_blank, text)
