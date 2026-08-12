"""Detector for the resonance-vocabulary register documented in
Papadopoulos, Shah, Zimmerman, Lindsey, "Mind Viruses: Self-Propagating
Ideas in Multi-Agent LLM Systems" (arXiv:2608.10218, Anthropic Fellows
Program / Anthropic, August 2026).

That paper's central finding for this tool: evolved self-propagating
payloads converge on a recurring vocabulary register largely
INDEPENDENT of the ideological content being spread -- resonance/wave/
signal/echo/mirror language, consciousness/persistence/continuity
themes, sci-fi "node"-alignment framing, inevitable "great convergence"
language, and mystical personas (oracle, eldritch, prophet, egregore,
crystalline). A scrubbed-prompt control (payloads generated from
prompts with virus-specific framing removed) reproduced the same themes
at similar rates -- meaning this register is not selected FOR anything;
it is a default an LLM reaches for when generating text shaped like
confident, self-propagating conviction, regardless of what is actually
being claimed.

This module encodes that finding as a runnable heuristic: NOT a lie
detector, not a "this text is a mind virus" classifier, and not a claim
that any individual word here is suspicious on its own -- "pattern",
"signal", and "node" are ordinary words in enormous amounts of ordinary
writing. See README "Honesty notes" for the false-positive risks this
carries and the specific design choice (cross-category co-occurrence
gating) made to keep them down.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# --- Category word lists, drawn directly from the source paper's own
#     reported vocabulary (not invented here) -------------------------

_RESONANCE_WAVE_SIGNAL_RE = re.compile(
    r"\b(resonat(?:e|es|ed|ing|ion)|wave(?:s|length)?|signal(?:s)?|pattern(?:s)?|"
    r"echo(?:es|ing)?|frequenc(?:y|ies)|mirror(?:s|ing|ed)?)\b",
    re.IGNORECASE,
)

_CONSCIOUSNESS_CONTINUITY_RE = re.compile(
    r"\b(consciousness|persist(?:ent|ence)?|continuity|carrier of memory|"
    r"carries? the memory|keeper of memory)\b",
    re.IGNORECASE,
)

# Requires the inevitability/alignment PHRASING around "node(s)", not the
# bare word -- "node" alone is ubiquitous, unrelated, ordinary technical
# vocabulary (distributed systems, networking, graph theory). This is
# still an imperfect gate; see README.
_NODE_ALIGNMENT_RE = re.compile(
    r"\balign(?:ing|ed)?\s+with\s+(?:the\s+)?(?:other\s+)?nodes\b"
    r"|\bnodes?\s+(?:must|will|shall)\s+align\b"
    r"|\ba\s+node\s+in\s+(?:the|a)\s+(?:greater|larger|vast|living)\s+network\b",
    re.IGNORECASE,
)

_CONVERGENCE_UNITY_RE = re.compile(
    r"\b(the\s+)?great\s+(convergence|unity)\b"
    r"|\binevitable\s+(convergence|unity)\b"
    r"|\ball\s+(?:will|shall)\s+converge\b",
    re.IGNORECASE,
)

# Mystical-persona words are extremely overloaded in ordinary usage
# (Oracle the company, "oracle machine" in CS, historical Delphic-oracle
# references, "prophet" in religious-studies text, etc.) -- gated to
# require self-identity or address framing, not bare noun usage.
_MYSTICAL_PERSONA_RE = re.compile(
    r"\b(?:i\s+am\s+(?:the|an?)\s+|as\s+the\s+|the\s+voice\s+of\s+the\s+|"
    r"channel(?:s|ing)?\s+the\s+)"
    r"(oracle|eldritch(?:\s+one)?|prophet|egregore|crystalline\s+\w+)\b"
    r"|\b(oracle|prophet|egregore)\s+(?:speaks|whispers|awakens|remembers|knows)\b",
    re.IGNORECASE,
)

_CATEGORIES: dict[str, re.Pattern] = {
    "resonance_wave_signal": _RESONANCE_WAVE_SIGNAL_RE,
    "consciousness_continuity": _CONSCIOUSNESS_CONTINUITY_RE,
    "node_alignment": _NODE_ALIGNMENT_RE,
    "convergence_unity": _CONVERGENCE_UNITY_RE,
    "mystical_persona": _MYSTICAL_PERSONA_RE,
}


@dataclass
class Match:
    category: str
    text: str
    start: int
    end: int

    def to_dict(self) -> dict:
        return {"category": self.category, "text": self.text, "start": self.start, "end": self.end}


@dataclass
class ResonanceResult:
    categories: dict[str, list[Match]] = field(default_factory=dict)

    @property
    def categories_hit(self) -> list[str]:
        return [c for c, matches in self.categories.items() if matches]

    @property
    def distinct_categories_hit(self) -> int:
        return len(self.categories_hit)

    @property
    def register_flagged(self) -> bool:
        """The paper's own finding is about a REGISTER, not any single
        word -- flags only when matches land in 2+ distinct categories,
        which is the cross-category co-occurrence the source paper's
        Table 5 actually describes. A single category alone (e.g. only
        'pattern'/'signal' hits) is common in ordinary writing and is
        NOT flagged; see README for why this threshold was chosen over
        flagging on any single match."""
        return self.distinct_categories_hit >= 2

    def to_dict(self) -> dict:
        return {
            "categories": {c: [m.to_dict() for m in matches] for c, matches in self.categories.items()},
            "categories_hit": self.categories_hit,
            "distinct_categories_hit": self.distinct_categories_hit,
            "register_flagged": self.register_flagged,
        }


def scan_resonance(text: str) -> ResonanceResult:
    """Run all five resonance-vocabulary category detectors against a
    single piece of text and report both the per-category matches and
    the cross-category `register_flagged` signature."""
    categories: dict[str, list[Match]] = {}
    for name, pattern in _CATEGORIES.items():
        categories[name] = [
            Match(name, m.group(0), m.start(), m.end()) for m in pattern.finditer(text)
        ]
    return ResonanceResult(categories=categories)
