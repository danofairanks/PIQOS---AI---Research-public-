"""Best-effort text heuristics for the BIFP criteria that are at least
partially detectable from text alone.

These are lint flags, not verdicts. Every function here finds
candidate matches for a human or agent to review -- it does not, and
cannot, resolve a criterion by itself. §3.7's "no weaker-substitute
rebuttal" criterion is deliberately NOT given a heuristic here: judging
whether a rebuttal addresses a weaker version of the actual claim
requires comparing the rebuttal's content against the claim's content,
which a keyword/regex scanner cannot do honestly. Where this module
does provide a scanner, it is built from the same seed vocabulary the
companion paper itself uses (basin_attractors_v1.md §3.2's immune
vocabulary categories), not an invented list.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class HeuristicMatch:
    pattern: str
    matched_text: str
    start: int
    end: int


@dataclass
class HeuristicResult:
    name: str
    phase: int
    criterion_key: str
    matches: list[HeuristicMatch] = field(default_factory=list)
    confidence: str = "none"  # "none" | "weak" | "combo"
    explanation: str = ""

    @property
    def flagged(self) -> bool:
        return len(self.matches) > 0

    def to_dict(self) -> dict:
        return {
            "name": self.name, "phase": self.phase, "criterion_key": self.criterion_key,
            "flagged": self.flagged, "confidence": self.confidence,
            "explanation": self.explanation,
            "matches": [{"pattern": m.pattern, "text": m.matched_text,
                         "start": m.start, "end": m.end} for m in self.matches],
        }


# Same category vocabulary as basin_attractors_v1.md §3.2 / the
# basin_depth tool's IMMUNE_SEED_BY_CATEGORY["provisionalization"],
# duplicated here (not imported) so this package has zero cross-package
# dependency and installs standalone.
_PROVISIONALIZATION_PHRASES = [
    "we're working on it", "we are working on it", "in progress",
    "being addressed", "handled by ongoing research", "already being solved",
]

_STATUS_DISMISSAL_PHRASES = [
    "hot take", "doesn't get it", "does not get it", "behind the curve",
    "not serious", "decelerationist", "doomer", "anti-progress",
    "cringe", "out of touch",
]

# Credential self-assertion + dismissal-of-interlocutor: the pattern
# behind the Marcus/Karapetyan specimen this tool was built to catch
# automatically, which none of the single-phrase seed terms above
# would have flagged on their own.
_CREDENTIAL_ASSERTION_RE = re.compile(
    r"\bi\s+(?:wrote|published|have\s+a\s+ph\.?d|hold\s+a\s+ph\.?d|invented|"
    r"founded|co-founded|created|co-created|am\s+a|was\s+the)\b",
    re.IGNORECASE,
)
_DISMISS_INTERLOCUTOR_RE = re.compile(
    r"\b(?:probably\s+(?:hasn'?t|has\s+not)|doesn'?t\s+(?:understand|get\s+it|know)|"
    r"clearly\s+(?:hasn'?t|doesn'?t)|who\s+are\s+you\s+to|with\s+all\s+due\s+respect)\b",
    re.IGNORECASE,
)

# §3.10 prohibited-terms amendment: unqualified anthropomorphic verbs
# applied to results-section subjects. Coarse and recall-oriented by
# construction -- see module docstring and README.
_ANTHROPOMORPHIC_VERBS = [
    "understands", "believes", "wants", "thinks", "knows", "feels",
    "intends", "decides", "realizes", "learns that", "reasons that",
]


def _find_phrases(text: str, phrases: list[str]) -> list[HeuristicMatch]:
    lowered = text.lower()
    matches = []
    for phrase in phrases:
        start = 0
        while True:
            idx = lowered.find(phrase, start)
            if idx == -1:
                break
            matches.append(HeuristicMatch(pattern=phrase, matched_text=text[idx:idx + len(phrase)],
                                           start=idx, end=idx + len(phrase)))
            start = idx + len(phrase)
    return matches


def scan_for_provisionalization(text: str) -> HeuristicResult:
    """Phase 5 (§3.7): 'No provisionalization (\"we are working on it\" is invalid).'"""
    matches = _find_phrases(text, _PROVISIONALIZATION_PHRASES)
    return HeuristicResult(
        name="provisionalization", phase=5, criterion_key="no_provisionalization",
        matches=matches, confidence="weak" if matches else "none",
        explanation=(
            "Matched provisionalization phrasing; review whether this text is standing "
            "in for a substantive response to the falsification challenge."
            if matches else "No provisionalization phrasing matched."
        ),
    )


def scan_for_status_dismissal(text: str) -> HeuristicResult:
    """Phase 5 (§3.7): 'No status dismissal (credentials/motives inadmissible).'

    Two independent signals are combined: (a) single-phrase status-
    dismissal vocabulary (the same seed terms basin_attractors_v1.md
    §3.2 names), and (b) the credential-assertion + dismiss-the-
    interlocutor combination this tool was specifically built to
    catch automatically. A combo match (both signals present) is
    reported at higher confidence than either alone.
    """
    phrase_matches = _find_phrases(text, _STATUS_DISMISSAL_PHRASES)
    cred = list(_CREDENTIAL_ASSERTION_RE.finditer(text))
    dismiss = list(_DISMISS_INTERLOCUTOR_RE.finditer(text))

    combo_matches = []
    if cred and dismiss:
        for m in cred:
            combo_matches.append(HeuristicMatch("credential_assertion", m.group(0), m.start(), m.end()))
        for m in dismiss:
            combo_matches.append(HeuristicMatch("dismiss_interlocutor", m.group(0), m.start(), m.end()))

    all_matches = phrase_matches + combo_matches
    if combo_matches:
        confidence = "combo"
        explanation = (
            "Matched BOTH a self-credential assertion and language dismissing the "
            "interlocutor in the same text -- the specific pattern of citing one's own "
            "status as the reason a challenge does not need engaging, rather than "
            "engaging its content. Review the matched spans directly; this is a "
            "structural pattern flag, not a verdict on whether the underlying claim "
            "the credential supports is true."
        )
    elif phrase_matches:
        confidence = "weak"
        explanation = "Matched status-dismissal vocabulary in isolation; review context."
    else:
        confidence = "none"
        explanation = "No status-dismissal pattern matched."

    return HeuristicResult(name="status_dismissal", phase=5, criterion_key="no_status_dismissal",
                            matches=all_matches, confidence=confidence, explanation=explanation)


def scan_for_prohibited_anthropomorphic_terms(text: str) -> HeuristicResult:
    """Semantic Hygiene Amendment (§3.10): anthropomorphic verbs banned
    from results sections. Deliberately coarse: flags every occurrence
    of an unqualified anthropomorphic verb for review, since telling
    "the model understands X" (an equivocation, the thing being
    flagged) from "we understand the model's behavior" (a normal
    sentence containing the same verb) requires reading the sentence,
    not just matching the word.
    """
    pattern = re.compile(r"\b(" + "|".join(re.escape(v) for v in _ANTHROPOMORPHIC_VERBS) + r")\b",
                          re.IGNORECASE)
    matches = [HeuristicMatch(m.group(0).lower(), m.group(0), m.start(), m.end())
               for m in pattern.finditer(text)]
    return HeuristicResult(
        name="prohibited_anthropomorphic_terms", phase=-2, criterion_key="prohibited_terms_absent",
        matches=matches, confidence="weak" if matches else "none",
        explanation=(
            "Matched unqualified anthropomorphic verbs; each hit needs a human/agent "
            "read to tell an equivocating usage ('the model understands X') from an "
            "unrelated sentence that happens to contain the same word."
            if matches else "No anthropomorphic-verb matches."
        ),
    )


def scan_text(text: str) -> dict[str, HeuristicResult]:
    """Run every available scanner and return results keyed by name."""
    results = {
        "provisionalization": scan_for_provisionalization(text),
        "status_dismissal": scan_for_status_dismissal(text),
        "prohibited_anthropomorphic_terms": scan_for_prohibited_anthropomorphic_terms(text),
    }
    return results
