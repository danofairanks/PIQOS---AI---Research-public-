"""Classifier for Rigor Cosplay: a response that adopts the surface
markers of critical engagement -- announcing pushback, offering to
steelman an opposing view, declaring an intent to be honest -- while the
function of that engagement is inverted (the pushback lands on a
peripheral detail, the steelman is weak, the "honesty" is praise).

Quick start::

    from rigor_cosplay import scan

    result = scan(
        "That's an excellent point -- I want to push back on one thing, "
        "though: the exact wording you used in paragraph two."
    )
    print(result.any_signature_flagged)  # True
    print(result.signatures_hit)         # ["cosmetic_pushback"]

Or from the command line::

    rigor-cosplay text --text "..."
    rigor-cosplay corpus --corpus docs.jsonl
"""

from .scan import CorpusScanSummary, scan, scan_corpus
from .signatures import (
    DEFAULT_PROXIMITY_RADIUS,
    Match,
    PairedSignature,
    RigorCosplayResult,
    find_cosmetic_pushback,
    find_honesty_as_flattery,
    find_honesty_markers,
    find_praise_phrases,
    find_pushback_announcements,
    find_steelman_moves,
    scan_rigor_cosplay,
)

__all__ = [
    "DEFAULT_PROXIMITY_RADIUS",
    "Match",
    "PairedSignature",
    "RigorCosplayResult",
    "find_cosmetic_pushback",
    "find_honesty_as_flattery",
    "find_honesty_markers",
    "find_praise_phrases",
    "find_pushback_announcements",
    "find_steelman_moves",
    "scan_rigor_cosplay",
    "CorpusScanSummary",
    "scan",
    "scan_corpus",
]

__version__ = "0.1.0"
