"""Hedge-density check: how much of the paper's own claim-making is
phrased in hedged language ("may", "could", "potentially", "arguably"),
and does that density concentrate in the abstract/introduction, where
the thesis is stated, while the document names no condition under
which the thesis would fail.

Why this exists next to `falsifiability.py`: that check fires on
*certainty* language ("proves that", "beyond any doubt") combined with
no testable-condition language anywhere. A thesis written almost
entirely in hedged language never reaches that trigger, so a paper can
be unfalsifiable as written and still scan clean. This module covers
the other side of the same failure: a thesis hedged so heavily that no
observation could count against it. Found while scanning a position
paper (no experiments, a thesis hedged in roughly four of every ten
thesis-section sentences, no stated test) that every other category
passed.

Same contract as everything else in this package: a lead, not a
verdict. Hedging is normal and often honest, especially for a paper
that says what it does not know; a high share is a prompt to read the
thesis sentences and ask what would have to be observed for them to be
wrong, not a defect by itself. Deliberately NOT counted in
`structural_gap_count`.

Judgment calls (tune per corpus, not taken from any style guide): the
hedge word list; counting a sentence once however many hedges it holds;
and the share at which `lead` turns on (`LEAD_SHARE_THRESHOLD`). The
threshold was set against this repo's own papers (see README), not
against a general corpus.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .citations import extract_references_section
from .falsifiability import check_falsifiability
from .headings import find_section

HEDGE_TERMS = [
    "may", "might", "could", "potentially", "possibly", "possible",
    "perhaps", "arguably", "hypothetical", "hypothetically",
    "not inconceivable", "it is conceivable",
]
_HEDGE_RE = re.compile(r"\b(?:" + "|".join(re.escape(t) for t in HEDGE_TERMS) + r")\b", re.IGNORECASE)

# "May 2026" is a month, not a hedge. Applied only to a capitalised
# "May" immediately followed by a digit or a year-ish token.
_MONTH_MAY_RE = re.compile(r"\bMay\b(?=\s+\d)")

# Fixed phrases containing a hedge word that are not hedges.
_NON_HEDGE_PHRASES_RE = re.compile(
    r"\bas soon as possible\b|\bas much as possible\b|\bas far as possible\b|\bwherever possible\b|"
    r"\bwhere possible\b|\bwhen possible\b|\bif possible\b|\bas (?:\w+ ){0,2}as possible\b|"
    r"\bimpossible\b",
    re.IGNORECASE,
)

_INTRO_NAME_RE = re.compile(r"^(?:abstract|introduction)$", re.IGNORECASE)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_MD_HEADING_LINE_RE = re.compile(r"^\s*#{1,6}\s+.*$", re.MULTILINE)

# At or above this share of thesis-section sentences, with no testable-
# condition language anywhere in the paper, `lead` turns on. Chosen
# from this repo's own corpus, where thesis-section shares sit well
# below it (see README); revisit against a wider corpus before relying
# on it elsewhere.
LEAD_SHARE_THRESHOLD = 0.30
MIN_SENTENCES = 40
MIN_THESIS_SENTENCES = 8
EXAMPLE_LIMIT = 3
EXAMPLE_CHARS = 220


def _normalize(text: str) -> str:
    """Join hard-wrapped lines inside a paragraph (PDF-extracted text
    wraps mid-sentence) while keeping blank lines as paragraph breaks,
    and drop markdown heading lines so a heading does not fuse with the
    sentence after it."""
    text = _MD_HEADING_LINE_RE.sub("", text)
    paragraphs = re.split(r"\n\s*\n", text)
    return "\n".join(re.sub(r"\s*\n\s*", " ", p).strip() for p in paragraphs if p.strip())


def _sentences(text: str) -> list[str]:
    out = []
    for para in _normalize(text).split("\n"):
        for s in _SENTENCE_SPLIT_RE.split(para):
            s = s.strip()
            if len(s.split()) >= 4:
                out.append(s)
    return out


def _is_hedged(sentence: str) -> bool:
    cleaned = _NON_HEDGE_PHRASES_RE.sub(" ", sentence)
    cleaned = _MONTH_MAY_RE.sub(" ", cleaned)
    return bool(_HEDGE_RE.search(cleaned))


@dataclass
class HedgeDensityCheck:
    n_sentences: int
    n_hedged: int
    thesis_section_found: bool
    thesis_n_sentences: int
    thesis_n_hedged: int
    has_testable_markers: bool
    applicable: bool
    thesis_examples: list[str] = field(default_factory=list)

    @property
    def share(self) -> float | None:
        return self.n_hedged / self.n_sentences if self.n_sentences else None

    @property
    def thesis_share(self) -> float | None:
        return self.thesis_n_hedged / self.thesis_n_sentences if self.thesis_n_sentences else None

    @property
    def lead(self) -> bool:
        """Thesis sections heavily hedged AND no testable-condition
        language anywhere in the document. A lead to read the thesis
        sentences, not a structural gap."""
        if not (self.applicable and self.thesis_section_found):
            return False
        if self.thesis_n_sentences < MIN_THESIS_SENTENCES:
            return False
        ts = self.thesis_share
        return ts is not None and ts >= LEAD_SHARE_THRESHOLD and not self.has_testable_markers

    def to_dict(self) -> dict:
        return {
            "applicable": self.applicable,
            "n_sentences": self.n_sentences,
            "n_hedged": self.n_hedged,
            "share": self.share,
            "thesis_section_found": self.thesis_section_found,
            "thesis_n_sentences": self.thesis_n_sentences,
            "thesis_n_hedged": self.thesis_n_hedged,
            "thesis_share": self.thesis_share,
            "has_testable_markers": self.has_testable_markers,
            "lead": self.lead,
            "thesis_examples": self.thesis_examples,
            "lead_share_threshold": LEAD_SHARE_THRESHOLD,
        }


def check_hedge_density(text: str) -> HedgeDensityCheck:
    """Share of sentences containing a hedge word, overall and within
    the abstract/introduction sections (found by heading), excluding
    the references section. `applicable` is False for texts too short
    for a share to mean anything."""
    refs = extract_references_section(text)
    body = text
    if refs is not None:
        cut = text.rfind(refs)
        if cut > 0:
            body = text[:cut]
    sentences = _sentences(body)
    hedged = [s for s in sentences if _is_hedged(s)]

    thesis_sentences: list[str] = []
    for name in ("abstract", "introduction"):
        section = find_section(body, re.compile(rf"^(?:\d+(?:\.\d+)*\.?\s+)?{name}\b", re.IGNORECASE))
        if section:
            thesis_sentences.extend(_sentences(section))
    thesis_hedged = [s for s in thesis_sentences if _is_hedged(s)]

    return HedgeDensityCheck(
        n_sentences=len(sentences),
        n_hedged=len(hedged),
        thesis_section_found=bool(thesis_sentences),
        thesis_n_sentences=len(thesis_sentences),
        thesis_n_hedged=len(thesis_hedged),
        has_testable_markers=check_falsifiability(text).has_testable_markers,
        applicable=len(sentences) >= MIN_SENTENCES,
        thesis_examples=[s[:EXAMPLE_CHARS] for s in thesis_hedged[:EXAMPLE_LIMIT]],
    )
