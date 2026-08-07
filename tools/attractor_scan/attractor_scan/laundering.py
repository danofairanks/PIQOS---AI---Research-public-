"""Classifier for the semantic-laundering cases named in
basin_attractors_v1.md §2.8 (Attractor 8).

Five of the paper's six named cases are implemented as generalizable
text patterns. **Case 6 ("A Term's Own Technical Precision Borrowed as
Visual Proof for Its Unrelated Hype Meaning") is deliberately NOT
implemented here.** The paper's own example for that case is a
specific image (a math-formula collage captioned "math Singularity")
being read as visual support for an unrelated hype claim via pun --
that is a cross-modal, single-instance rhetorical move, not a
generalizable text pattern, and building a keyword scanner that
pretended to detect it would be exactly the kind of unearned precision
this whole project's research is built to catch elsewhere. If a
second, independently-checkable instance of the pun-as-evidence move
turns up, it belongs in a case study, not a keyword list.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_AI_SUBJECT_RE = re.compile(r"\b(model|llm|ai|neural network|system|transformer|chatbot)\b", re.IGNORECASE)


@dataclass
class Match:
    pattern: str
    text: str
    start: int
    end: int

    def to_dict(self) -> dict:
        return {"pattern": self.pattern, "text": self.text, "start": self.start, "end": self.end}


@dataclass
class LaunderingResult:
    case: str
    name: str
    source: str
    matches: list[Match] = field(default_factory=list)
    confidence: str = "none"
    explanation: str = ""

    @property
    def flagged(self) -> bool:
        return len(self.matches) > 0

    def to_dict(self) -> dict:
        return {
            "case": self.case, "name": self.name, "source": self.source,
            "flagged": self.flagged, "confidence": self.confidence,
            "explanation": self.explanation,
            "matches": [m.to_dict() for m in self.matches],
        }


def _finditer_matches(pattern: re.Pattern, text: str, label: str) -> list[Match]:
    return [Match(label, m.group(0), m.start(), m.end()) for m in pattern.finditer(text)]


# --- Case 1: Pattern Recognition vs. Pattern Matching -----------------

_PATTERN_RECOGNITION_RE = re.compile(r"\bpattern recognition\b", re.IGNORECASE)
_PATTERN_MATCHING_RE = re.compile(r"\bpattern matching\b", re.IGNORECASE)


def scan_case1_pattern_recognition(text: str) -> LaunderingResult:
    """§2.8 Case 1: describing model operation as 'pattern recognition'
    (a cognitive-science term implying meaning-making) rather than
    'pattern matching' (the algorithmic, correlation-only description)
    upgrades the claim without argument. Flags 'pattern recognition'
    applied near an AI-subject word when 'pattern matching' is absent
    from the same text (i.e. the distinction was never drawn)."""
    pr_matches = _finditer_matches(_PATTERN_RECOGNITION_RE, text, "pattern_recognition")
    pm_present = bool(_PATTERN_MATCHING_RE.search(text))
    ai_subject_present = bool(_AI_SUBJECT_RE.search(text))
    flagged_matches = pr_matches if (pr_matches and ai_subject_present and not pm_present) else []
    return LaunderingResult(
        "case1", "Pattern Recognition vs. Pattern Matching", "§2.8 Case 1",
        flagged_matches, confidence="weak" if flagged_matches else "none",
        explanation=(
            "'Pattern recognition' used for an AI subject with no 'pattern matching' "
            "distinction drawn anywhere in the text -- review whether the more precise, "
            "algorithmic term would change the claim's force."
            if flagged_matches else "No unqualified pattern-recognition usage matched."
        ),
    )


# --- Case 2: "Understanding" and "Reasoning" ---------------------------

_UNDERSTANDING_REASONING_RE = re.compile(r"\b(understanding|reasoning|understands|reasons)\b", re.IGNORECASE)
_QUALIFIER_WINDOW = 60  # characters of proximity counted as "near" the AI-subject word


def scan_case2_understanding_reasoning(text: str) -> LaunderingResult:
    """§2.8 Case 2: 'understanding'/'reasoning' used to describe model
    operation without operationalization -- the technical-meaning to
    benchmark-meaning to narrative-meaning laundering chain the paper
    names. Flags occurrences within `_QUALIFIER_WINDOW` characters of
    an AI-subject word (i.e. actually describing the system, not used
    in an unrelated sentence)."""
    matches = []
    for m in _UNDERSTANDING_REASONING_RE.finditer(text):
        window_start = max(0, m.start() - _QUALIFIER_WINDOW)
        window_end = min(len(text), m.end() + _QUALIFIER_WINDOW)
        if _AI_SUBJECT_RE.search(text[window_start:window_end]):
            matches.append(Match("understanding_reasoning", m.group(0), m.start(), m.end()))
    return LaunderingResult(
        "case2", '"Understanding" and "Reasoning"', "§2.8 Case 2",
        matches, confidence="weak" if matches else "none",
        explanation=(
            "Matched unqualified understanding/reasoning language describing an AI "
            "subject -- review whether this means 'generated intermediate tokens' / "
            "'scored above chance' or is claiming the technical, human-cognition sense."
            if matches else "No unqualified understanding/reasoning usage matched near an AI subject."
        ),
    )


# --- Case 3: "Emergence" -----------------------------------------------

_EMERGENCE_RE = re.compile(r"\bemergen(?:t|ce)\b", re.IGNORECASE)
_METRIC_ARTIFACT_CAVEAT_RE = re.compile(
    r"\b(metric artifact|nonlinear (?:scoring|metric)|measurement artifact|scale threshold)\b",
    re.IGNORECASE,
)


def scan_case3_emergence(text: str) -> LaunderingResult:
    """§2.8 Case 3: 'emergence' used in its physics sense (ontologically
    novel macroscopic properties) when what's actually meant is a sharp
    benchmark-performance jump at a scale threshold -- often a metric
    artifact (Schaeffer et al. 2023), not a phase transition. Flags
    'emergen(t/ce)' near an AI subject with no metric-artifact caveat
    anywhere in the text."""
    em_matches = _finditer_matches(_EMERGENCE_RE, text, "emergence")
    ai_subject_present = bool(_AI_SUBJECT_RE.search(text))
    caveat_present = bool(_METRIC_ARTIFACT_CAVEAT_RE.search(text))
    flagged_matches = em_matches if (em_matches and ai_subject_present and not caveat_present) else []
    return LaunderingResult(
        "case3", '"Emergence"', "§2.8 Case 3",
        flagged_matches, confidence="weak" if flagged_matches else "none",
        explanation=(
            "'Emergen(t/ce)' applied to an AI subject with no metric-artifact caveat -- "
            "review whether this claims a genuine phase transition or a benchmark-score "
            "jump that nonlinear scoring can produce without one."
            if flagged_matches else "No unqualified emergence usage matched."
        ),
    )


# --- Case 4: "Alignment" and "Safety" ----------------------------------

_ALIGNMENT_SAFETY_RE = re.compile(r"\b(alignment|safety)\b", re.IGNORECASE)
_SUBPROBLEM_QUALIFIERS = [
    "task reliability", "task-reliability", "takeover avoidance", "value alignment",
    "bias mitigation", "helpfulness", "harmlessness", "harmless", "helpful",
]


def scan_case4_alignment_safety(text: str) -> LaunderingResult:
    """§2.8 Case 4: 'alignment' has been compressed to cover at least
    six distinct problems (task-reliability, takeover avoidance, value
    alignment, bias mitigation, helpfulness, harmlessness); progress on
    one gets reported as progress on all. Flags 'alignment'/'safety'
    mentions with none of the six sub-problem terms present anywhere
    in the text -- i.e. the claim never specifies which problem it
    actually means."""
    as_matches = _finditer_matches(_ALIGNMENT_SAFETY_RE, text, "alignment_safety")
    lowered = text.lower()
    qualifier_present = any(q in lowered for q in _SUBPROBLEM_QUALIFIERS)
    flagged_matches = as_matches if (as_matches and not qualifier_present) else []
    return LaunderingResult(
        "case4", '"Alignment" and "Safety"', "§2.8 Case 4",
        flagged_matches, confidence="weak" if flagged_matches else "none",
        explanation=(
            "'Alignment'/'safety' mentioned without specifying which of the six "
            "distinct sub-problems is meant -- review whether the claim generalizes "
            "across sub-problems it never actually measured."
            if flagged_matches else "Alignment/safety usage was accompanied by a sub-problem qualifier, or absent."
        ),
    )


# --- Case 5: Bidirectional Drift ("AGI" down / "Agentic" up) ----------

_AGI_ACHIEVED_RE = re.compile(
    r"\bagi\b[^.?!]{0,50}\b(already|basically|effectively|whoosh(?:ed)?|achieved|is\s+here)\b"
    r"|\b(already|basically|effectively|achieved)\b[^.?!]{0,50}\bagi\b",
    re.IGNORECASE,
)
_AGENTIC_INEVITABLE_RE = re.compile(
    r"\bagentic\b[^.?!]{0,60}\b(inevitable|will happen(?: (?:frequently|often|more))?|"
    r"as ai becomes|cost of progress)\b"
    r"|\b(will happen(?: (?:frequently|often|more))?|inevitable|as ai becomes|cost of progress)\b"
    r"[^.?!]{0,60}\bagentic\b",
    re.IGNORECASE,
)


def scan_case5_bidirectional_drift(text: str) -> LaunderingResult:
    """§2.8 Case 5: the same news cycle can move related terms in
    opposite directions for different narrative needs -- 'AGI' diluted
    downward until it can be claimed already achieved; 'agentic'
    inflated upward into a pre-justification for failures ('this will
    happen more as AI becomes more agentic'). Flags both directions;
    each is weaker/noisier than Cases 1-4 by construction (matching a
    directional claim from short-range co-occurrence, not a single
    fixed phrase) -- treat matches as illustrative leads, not findings."""
    agi_matches = _finditer_matches(_AGI_ACHIEVED_RE, text, "agi_already_achieved")
    agentic_matches = _finditer_matches(_AGENTIC_INEVITABLE_RE, text, "agentic_pre_justification")
    matches = agi_matches + agentic_matches
    return LaunderingResult(
        "case5", "Bidirectional Drift (AGI down / Agentic up)", "§2.8 Case 5",
        matches, confidence="weak" if matches else "none",
        explanation=(
            "Matched language moving 'AGI' toward already-achieved or 'agentic' toward "
            "inevitable-failure framing. This is the noisiest scanner in the package -- "
            "short-range co-occurrence, not a fixed phrase -- review every match directly."
            if matches else "No bidirectional-drift pattern matched."
        ),
    )


CASE_SCANNERS = {
    "case1": scan_case1_pattern_recognition,
    "case2": scan_case2_understanding_reasoning,
    "case3": scan_case3_emergence,
    "case4": scan_case4_alignment_safety,
    "case5": scan_case5_bidirectional_drift,
}


def scan_laundering(text: str) -> dict[str, LaunderingResult]:
    """Run all five implemented semantic-laundering case scanners."""
    return {case: scanner(text) for case, scanner in CASE_SCANNERS.items()}
