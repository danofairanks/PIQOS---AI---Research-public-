"""Detector for unglossed formal objects: an equation-shaped span with
a private, subscripted/superscripted variable, no nearby definition,
units, or falsifiability language, co-occurring in the same document
with self-titling ("Law of X," "Founder of X") legitimation language.

Distinct from `laundering.py`'s six §2.8 semantic-laundering cases and
deliberately NOT a revival of Case 6 ("A Term's Own Technical
Precision Borrowed as Visual Proof," left unimplemented there because
it is cross-modal -- an image read against a claim -- and genuinely
resists a text-only scanner). This detector targets a narrower, more
text-tractable pattern: bare mathematical notation asserting the
*textual* precision a "Law" claims, in a document that also stakes a
founder-of-discursivity claim about the term's own field. Both
conditions -- unglossed equation AND self-titling language -- must be
present; either alone is common in legitimate writing (a textbook
states E = mc^2 with no inline re-derivation; an author bio says
"founder of" a real company with no equation nearby) and is not
flagged on its own. See README "Why this is not Case 6" for the full
reasoning.

Local, adapted copy of testable-marker and credential-marker phrase
lists rather than importing paper_rigor -- same "duplicate small
phrase lists to stay standalone" convention already used between this
package's siblings (debasinizer, bifp).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# A variable-like token: one or two letters, followed by a Unicode
# subscript/superscript digit run or an ASCII _N / ^N / _{N} / ^{N}
# modifier -- NOT a bare trailing digit with no marker (m1, r2), which
# is deliberately excluded: "m1"/"r2"-style bare suffixes are common
# in ordinary chemistry/business/model-name text (H2O, GPT4, Q3) and
# would be a real false-positive source; catching them would need a
# much more context-heavy design than a v1 warrants. The negative
# lookahead after each token additionally guards against a token
# partially matching into a bare-digit run and producing a truncated,
# wrong span (e.g. "m1" matching as "m" alone and corrupting the rest
# of the equation match) -- this was a real bug caught in testing, not
# a hypothetical one.
_SUBSCRIPT_DIGITS = "₀₁₂₃₄₅₆₇₈₉"
_SUPERSCRIPT_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
_MODIFIER = rf"(?:[{_SUBSCRIPT_DIGITS}{_SUPERSCRIPT_DIGITS}]+|[_^]\{{?\d+\}}?)"
_PLAIN_VAR = r"[A-Za-zΑ-Ωα-ω]{1,2}(?!\d)"
_MODIFIED_VAR = rf"[A-Za-zΑ-Ωα-ω]{{1,2}}{_MODIFIER}(?!\d)"
_ANY_VAR = rf"(?:{_MODIFIED_VAR}|{_PLAIN_VAR})"
_OPERATOR = r"[×x*·/+\-]"

# Requires: var = var (operator var)+, with at least one of the
# variable tokens carrying a subscript/superscript modifier somewhere
# in the whole match. The modifier requirement is enforced by matching
# _MODIFIED_VAR at least once via a lookahead rather than requiring it
# at a fixed position, since the private constant can appear anywhere
# in the expression (T = C7 x U3, or C7 = T / U3). The three-term
# minimum (var = var op var) is deliberate, not incidental: it is what
# keeps ordinary two-term physics statements using implicit
# multiplication (E = mc^2 has no explicit operator between m and c^2)
# from matching, while still catching the multi-term private formulas
# this detector targets -- confirmed in testing, not just intended.
_EQUATION_RE = re.compile(
    rf"\b(?=[^.?!\n]*{_MODIFIED_VAR})"
    rf"{_ANY_VAR}\s*=\s*{_ANY_VAR}(?:\s*{_OPERATOR}\s*{_ANY_VAR})+"
)

# Local, narrower copy of paper_rigor's TESTABLE_MARKERS -- falsifiability
# language near an equation is exactly the kind of grounding that
# should suppress a flag, same reasoning as that module's own docstring.
_GLOSS_NEARBY_RE = re.compile(
    r"\bwhere\s+[A-Za-zΑ-Ωα-ω]{1,2}\b|\bis\s+defined\s+as\b|\bdenotes\b|\bstands\s+for\b|"
    r"\bmeasured\s+in\b|\bunits?\s+of\b|\bexpressed\s+in\b|"
    r"\bwould\s+be\s+falsified\s+if\b|\bwould\s+falsify\s+this\b|\bpredicts\s+that\b|"
    r"\bthis\s+claim\s+fails\s+if\b|\bwould\s+refute\s+this\b|\bnull\s+hypothesis\b",
    re.IGNORECASE,
)

# Self-titling / founder-of-discursivity legitimation language.
# Deliberately requires BOTH a law/theory-naming phrase AND a
# self-attribution phrase to be present -- either alone is common in
# legitimate writing (a real professor's bio says "founder of" a real
# institute with no invented law nearby; a real paper says "law of
# gravitation" with no founder self-attribution nearby). Requiring
# both is what caught and fixed a real false positive in testing: an
# unrelated "founder of the Applied Physics Institute" bio, next to a
# correctly-cited Newton's law of gravitation, flagged under the
# single-signal design -- the co-occurrence of two INDEPENDENT
# ordinary things, not a laundering instance.
_LAW_NAMING_RE = re.compile(r"\blaw\s+of\s+[A-Z]\w*\b|\btheory\s+of\s+[A-Z]\w*\b", re.IGNORECASE)
_SELF_ATTRIBUTION_RE = re.compile(
    r"\bfounder\s+of\b|\bco-founder\s+of\b|\bdeveloper\s+of\s+the\b|\bcreator\s+of\s+the\b|"
    r"\bi\s+discovered\b|\bmy\s+(?:own\s+)?(?:law|theory)\b",
    re.IGNORECASE,
)

_GLOSS_WINDOW = 400  # characters of proximity searched for grounding language


@dataclass
class EquationSpan:
    text: str
    start: int
    end: int
    has_gloss_nearby: bool

    def to_dict(self) -> dict:
        return {"text": self.text, "start": self.start, "end": self.end,
                "has_gloss_nearby": self.has_gloss_nearby}


@dataclass
class UnglossedFormalObjectResult:
    source: str = "not in basin_attractors_v1.md's six §2.8 cases -- see module docstring"
    unglossed_spans: list[EquationSpan] = field(default_factory=list)
    self_titling_present: bool = False
    confidence: str = "none"
    explanation: str = ""

    @property
    def flagged(self) -> bool:
        return bool(self.unglossed_spans) and self.self_titling_present

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "flagged": self.flagged,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "unglossed_spans": [s.to_dict() for s in self.unglossed_spans],
            "self_titling_present": self.self_titling_present,
        }


def scan_unglossed_formal_object(text: str) -> UnglossedFormalObjectResult:
    """Flags an equation-shaped span carrying a private, subscripted
    variable with no definition/units/falsifiability language within
    `_GLOSS_WINDOW` characters, but ONLY when the same document ALSO
    contains BOTH a law/theory-naming phrase ("Law of X") AND a
    self-attribution phrase ("Founder of," "I discovered") -- three
    independent conditions, not one. Any one or two alone are common in
    legitimate writing (a real equation with no inline re-derivation; a
    real founder bio; a real paper naming "the law of gravitation")
    and are not flagged; the full co-occurrence is the lead. A flag
    here means 'this specific formal object was never operationalized
    in a document that also stakes both a law-naming and a
    self-attribution claim about it' -- it is not a claim the
    underlying idea is false, only that nothing here lets a reader
    check it. See README for what this does not establish."""
    self_titling_present = bool(_LAW_NAMING_RE.search(text)) and bool(_SELF_ATTRIBUTION_RE.search(text))

    unglossed = []
    for m in _EQUATION_RE.finditer(text):
        window_start = max(0, m.start() - _GLOSS_WINDOW)
        window_end = min(len(text), m.end() + _GLOSS_WINDOW)
        has_gloss = bool(_GLOSS_NEARBY_RE.search(text[window_start:window_end]))
        if not has_gloss:
            unglossed.append(EquationSpan(m.group(0), m.start(), m.end(), has_gloss_nearby=False))

    flagged = bool(unglossed) and self_titling_present
    return UnglossedFormalObjectResult(
        unglossed_spans=unglossed,
        self_titling_present=self_titling_present,
        confidence="weak" if flagged else "none",
        explanation=(
            "Equation-shaped span(s) with a private subscripted/superscripted variable, "
            "no definition/units/falsifiability language within "
            f"{_GLOSS_WINDOW} characters, in a document that also names a 'law of'/"
            "'theory of' claim AND a 'founder of'/self-attribution claim -- review "
            "whether the notation is doing argumentative work its own text never "
            "operationalizes."
            if flagged else
            "No unglossed private-variable equation matched, or the law-naming and "
            "self-attribution language required alongside it don't both co-occur -- "
            "all three conditions are required; see module docstring for why any one "
            "or two alone are not flagged."
        ),
    )
