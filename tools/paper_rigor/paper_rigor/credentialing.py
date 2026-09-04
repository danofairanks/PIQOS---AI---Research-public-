"""Detect a claim's only nearby support being an appeal to the
claimant's (or a cited party's) credentials, title, or track record --
first- or third-person, unlike `bifp`'s narrower first-person-only
"I have a PhD" detector (built for conversational specimens; papers
mostly invoke credentials about a person in the third person: author
bios, "Dr. X, a leading expert in..."). A credential mention next to a
claim that ALSO has real evidence nearby (data, a citation, a
percentage) is not flagged -- credentials plus evidence is normal
academic writing; credentials INSTEAD of evidence is the failure mode
this names. Same "lead, not verdict" contract as everything else here:
it cannot tell whether the credential is even real.

Wired to `_shared.has_meta_framing_nearby` (same helper `citations.py`
and `consensus.py` already use) and given a section-citation evidence
signal, both against a real false-positive found in this project's own
`papers/published/laundered_vocabulary_v1.md`: its "Law" entry
illustrates the founder-of-discursivity pattern it defines ("styling
its author as 'Founder of'", "framed as founder of") and separately
cross-references another document's specimen by section number
("contrast §5's treatment of 'Nobel laureate John Jumper'") -- three
matches on the document's own description OF the pattern, not the
document making a credential-substitution claim on its own behalf.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ._shared import has_meta_framing_nearby

CREDENTIAL_MARKERS = [
    r"\bph\.?d\.?\b", r"\bprofessor of\b", r"\bleading expert\b", r"\bleading authority\b",
    r"\brenowned expert\b", r"\brenowned scientist\b", r"\bworld-renowned\b",
    r"\baward-winning\b", r"\bnobel laureate\b", r"\bbestselling author\b",
    r"\bwith over \d+ years of experience\b", r"\byears of experience in\b",
    r"\bdistinguished professor\b", r"\bchief scientist\b",
    r"\bfounder of\b", r"\bco-founder of\b",
    r"\bi\s+(?:hold|have)\s+a\s+ph\.?d\b", r"\bi\s+(?:wrote|published|invented|founded|co-founded)\b",
]
_CREDENTIAL_RE = re.compile("|".join(CREDENTIAL_MARKERS), re.IGNORECASE)

# Signals that real evidence, not just standing, is present nearby --
# same shape as citations.py's inline-citation signals plus a bare
# statistic pattern (a number attached to a claim is not proof either,
# but its presence means the credential isn't the ONLY thing offered).
_EVIDENCE_SIGNALS = [
    re.compile(r'\([A-Z][A-Za-z\'-]+(?:\s*(?:&|and|,)\s*[A-Z][A-Za-z\'-]+)*,?\s*\d{4}[a-z]?\)'),
    re.compile(r'\[\^?\d+\]'),
    re.compile(r'https?://\S+'),
    re.compile(r'\bet al\.'),
    re.compile(r'\b\d+(?:\.\d+)?\s*%'),
    re.compile(r'\bp\s*[<>=]\s*0?\.\d+'),  # a p-value
    re.compile(r'§\s?\d'),  # a section-number citation (this project's own protocol/paper style)
]

CONTEXT_CHARS = 150


@dataclass
class CredentialMatch:
    phrase: str
    start: int
    end: int
    context: str

    def to_dict(self) -> dict:
        return {"phrase": self.phrase, "start": self.start, "end": self.end, "context": self.context}


def find_credential_substitution(text: str, *, window: int = CONTEXT_CHARS) -> list[CredentialMatch]:
    out = []
    for m in _CREDENTIAL_RE.finditer(text):
        start, end = max(0, m.start() - window), min(len(text), m.end() + window)
        context = text[start:end]
        if has_meta_framing_nearby(text, m.start(), m.end()):
            continue
        if not any(sig.search(context) for sig in _EVIDENCE_SIGNALS):
            out.append(CredentialMatch(phrase=m.group(0), start=m.start(), end=m.end(), context=context))
    return out
