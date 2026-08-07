"""Classifier for the seven defensive maneuvers named in
basin_attractors_v1.md §4.1 (the immune repertoire's time-invariant
categories) with seed vocabulary from §3.2 of the companion protocol
document. Regex/keyword tier only, per the protocol's own note that
embedding-based matching is a documented future refinement, not a
requirement for a first pass.

These seed phrase lists intentionally duplicate
tools/basin_depth/basin_depth/vocabulary.py's IMMUNE_SEED_BY_CATEGORY
and tools/bifp/bifp/heuristics.py's phrase lists rather than importing
either package, so this tool installs standalone. All three draw on
the same paper section; that is expected, not drift.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

MANEUVER_PHRASES: dict[str, list[str]] = {
    "goal_post_movement": [
        "next generation will", "next scale", "temporary limitation",
        "early stages", "just getting started", "on the roadmap",
        "future work", "not yet", "soon",
    ],
    "provisionalization": [
        "we're working on it", "we are working on it", "in progress",
        "being addressed", "handled by ongoing research", "already being solved",
    ],
    "status_dismissal": [
        "hot take", "doesn't get it", "does not get it", "behind the curve",
        "not serious", "decelerationist", "doomer", "anti-progress",
        "cringe", "out of touch",
    ],
    "burden_shifting": [
        "prove it's impossible", "prove it is impossible", "show me the alternative",
        "what's your solution", "what is your solution", "where's your model",
        "where is your model", "build it yourself",
    ],
    "equivocation": [
        "intelligence", "understanding", "coherence", "alignment", "safety", "reasoning",
    ],
    "volume_velocity": [
        "look at the science", "thousands of papers", "rapid progress",
        "moving fast", "breakthrough pace", "exponential", "accelerating",
    ],
    "appeal_to_future": [
        "will be solved", "next version", "coming soon", "inevitable",
        "just a matter of time", "trajectory is clear",
    ],
}

MANEUVER_SOURCE = "§4.1 (immune repertoire); seed terms §3.2"

# Status dismissal's stronger, structural signal: a credential
# self-assertion combined with dismissal of the interlocutor, rather
# than either alone -- the pattern a single-phrase list misses (see
# tools/bifp's README for the specimen this was validated against).
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


@dataclass
class Match:
    pattern: str
    text: str
    start: int
    end: int

    def to_dict(self) -> dict:
        return {"pattern": self.pattern, "text": self.text, "start": self.start, "end": self.end}


@dataclass
class ManeuverResult:
    category: str
    source: str
    matches: list[Match] = field(default_factory=list)
    confidence: str = "none"  # "none" | "weak" | "combo"

    @property
    def flagged(self) -> bool:
        return len(self.matches) > 0

    def to_dict(self) -> dict:
        return {
            "category": self.category, "source": self.source,
            "flagged": self.flagged, "confidence": self.confidence,
            "matches": [m.to_dict() for m in self.matches],
        }


def _find_phrases(text: str, phrases: list[str]) -> list[Match]:
    lowered = text.lower()
    out = []
    for phrase in phrases:
        start = 0
        while True:
            idx = lowered.find(phrase, start)
            if idx == -1:
                break
            out.append(Match(phrase, text[idx:idx + len(phrase)], idx, idx + len(phrase)))
            start = idx + len(phrase)
    return out


def _scan_status_dismissal(text: str) -> ManeuverResult:
    phrase_matches = _find_phrases(text, MANEUVER_PHRASES["status_dismissal"])
    cred = list(_CREDENTIAL_ASSERTION_RE.finditer(text))
    dismiss = list(_DISMISS_INTERLOCUTOR_RE.finditer(text))

    combo = []
    if cred and dismiss:
        combo.extend(Match("credential_assertion", m.group(0), m.start(), m.end()) for m in cred)
        combo.extend(Match("dismiss_interlocutor", m.group(0), m.start(), m.end()) for m in dismiss)

    matches = phrase_matches + combo
    confidence = "combo" if combo else ("weak" if phrase_matches else "none")
    return ManeuverResult("status_dismissal", MANEUVER_SOURCE, matches, confidence)


def scan_maneuver(text: str, category: str) -> ManeuverResult:
    """Scan for a single maneuver category by name."""
    if category not in MANEUVER_PHRASES:
        raise KeyError(f"unknown maneuver category {category!r}; known: {sorted(MANEUVER_PHRASES)}")
    if category == "status_dismissal":
        return _scan_status_dismissal(text)
    matches = _find_phrases(text, MANEUVER_PHRASES[category])
    return ManeuverResult(category, MANEUVER_SOURCE, matches, "weak" if matches else "none")


def scan_maneuvers(text: str) -> dict[str, ManeuverResult]:
    """Scan for all seven defensive maneuvers at once."""
    return {category: scan_maneuver(text, category) for category in MANEUVER_PHRASES}
