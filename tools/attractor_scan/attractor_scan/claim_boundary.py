"""Claim-boundary portability: does limitation/scope language present
in a source document travel to the point where that source is cited or
referenced elsewhere, or is it left behind at publication?

Motivated by papers/drafts/closed_path_confirmation_v1.md's distinction
between an artifact's own stated limitations (real, often genuinely
present) and whether a reader encountering only the citation -- not the
original document -- ever sees them. A two-document comparison, unlike
this package's other scanners in maneuvers.py/laundering.py/
formal_object.py, which each classify a single piece of text alone.

Purely lexical, like the rest of this package, and explicit about the
limits that implies: absence of a limitation-indicator term in the
citation text does not prove the limitation was suppressed -- a short
citation may legitimately omit it, and a paraphrase could carry the
same meaning without matching these exact surface markers. This is a
lead generator for a human or agent to read both texts directly, not a
verdict on whether anything was hidden. Generic by construction:
nothing in this module or its tests refers to any named project,
repository, organization, or individual.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Signal phrases that a sentence is stating a claim boundary / scope
# limitation, drawn from vocabulary already common across this
# project's own published papers' "What this does NOT establish"
# sections (not invented for this module) -- see README for examples.
_CLAIM_BOUNDARY_PHRASES = [
    "does not claim", "does not prove", "does not establish", "not yet validated",
    "not independently", "no claim of", "not a replacement for", "not yet been validated",
    "out of scope", "not intended to", "not production-ready", "provisional",
    "has not undergone", "not yet undergone", "remains unestablished", "not yet deployed",
]

# Generic terms whose presence anywhere in a citation context suggests
# the limitation traveled with the citation, even if the exact source
# phrase didn't. Deliberately broad and low-precision -- this is a
# recall-oriented check for "is there any trace of caveat language
# here at all", not an attempt to match the source's specific wording.
_LIMITATION_INDICATOR_TERMS = [
    "limitation", "does not", "not yet", "provisional", "caveat", "disclaimer",
    "scope", "unvalidated", "not independently", "not a replacement",
]


@dataclass
class BoundaryPhraseMatch:
    pattern: str
    matched_text: str
    start: int
    end: int
    sentence: str

    def to_dict(self) -> dict:
        return {
            "pattern": self.pattern, "text": self.matched_text,
            "start": self.start, "end": self.end, "sentence": self.sentence,
        }


def _sentence_window(text: str, start: int, end: int, *, radius: int = 120) -> str:
    lo = max(0, start - radius)
    hi = min(len(text), end + radius)
    return text[lo:hi].strip()


def extract_claim_boundary_phrases(text: str) -> list[BoundaryPhraseMatch]:
    """Find every occurrence of a claim-boundary signal phrase in
    `text`, each with a surrounding window for context. A lead list,
    not a count of "how many limitations this document has" -- read
    each sentence directly."""
    lowered = text.lower()
    matches: list[BoundaryPhraseMatch] = []
    for phrase in _CLAIM_BOUNDARY_PHRASES:
        start = 0
        while True:
            idx = lowered.find(phrase, start)
            if idx == -1:
                break
            end = idx + len(phrase)
            matches.append(BoundaryPhraseMatch(
                pattern=phrase, matched_text=text[idx:end], start=idx, end=end,
                sentence=_sentence_window(text, idx, end),
            ))
            start = end
    return matches


@dataclass
class BoundaryPortabilityResult:
    source_boundary_phrases: list[BoundaryPhraseMatch] = field(default_factory=list)
    citation_text_word_count: int = 0
    citation_matched_terms: list[str] = field(default_factory=list)

    @property
    def source_has_boundary_language(self) -> bool:
        return len(self.source_boundary_phrases) > 0

    @property
    def citation_shows_limitation_trace(self) -> bool:
        return len(self.citation_matched_terms) > 0

    @property
    def flagged(self) -> bool:
        """True only when the source states a claim boundary AND the
        citation context shows no lexical trace of any limitation
        language at all. See module docstring: this is a lead, not
        proof of suppression -- a short or terse citation can
        legitimately fail this check without anything having been
        hidden."""
        return self.source_has_boundary_language and not self.citation_shows_limitation_trace

    def to_dict(self) -> dict:
        return {
            "source_boundary_phrases": [m.to_dict() for m in self.source_boundary_phrases],
            "source_has_boundary_language": self.source_has_boundary_language,
            "citation_text_word_count": self.citation_text_word_count,
            "citation_matched_terms": self.citation_matched_terms,
            "citation_shows_limitation_trace": self.citation_shows_limitation_trace,
            "flagged": self.flagged,
            "note": (
                "Purely lexical overlap, not a semantic check. A flag here means "
                "the source states a scope limitation and the citation text "
                "contains no matching term from a broad, low-precision indicator "
                "list -- it does not mean the limitation was suppressed. Absence "
                "is consistent with a short citation, a paraphrase that carries "
                "the same meaning in different words, or this checker's own "
                "recall gaps. Read both texts directly before concluding "
                "anything; this is a lead, not a verdict."
            ),
        }


def check_boundary_portability(source_text: str, citation_text: str) -> BoundaryPortabilityResult:
    """Compare a source document's own stated claim boundaries against
    a separate piece of text that cites or references that source.
    `citation_text` should be the citing context only (an abstract, a
    README's "prior work" section, a paragraph referencing the source)
    -- not the full source document itself, or every check will
    trivially pass."""
    source_matches = extract_claim_boundary_phrases(source_text)
    lowered_citation = citation_text.lower()
    matched_terms = [t for t in _LIMITATION_INDICATOR_TERMS if t in lowered_citation]
    return BoundaryPortabilityResult(
        source_boundary_phrases=source_matches,
        citation_text_word_count=len(citation_text.split()),
        citation_matched_terms=matched_terms,
    )
