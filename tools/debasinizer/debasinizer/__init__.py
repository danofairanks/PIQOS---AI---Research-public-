"""Text classifier for the resonance-vocabulary register (Papadopoulos
et al., "Mind Viruses," arXiv:2608.10218) and self-referential
coherence-assertion phrasing.

Quick start::

    from debasinizer import scan

    result = scan("The signal resonates across every node; the pattern is unmistakable.")
    print(result.register_flagged)         # True -- 2+ resonance categories co-occur
    print(result.self_coherence_flagged)   # True -- "the pattern is unmistakable"

Or from the command line::

    debasinizer text --text "..."
    debasinizer corpus --corpus docs.jsonl
"""

from .resonance import Match as ResonanceMatch
from .resonance import ResonanceResult, scan_resonance
from .scan import CorpusScanSummary, DebasinizerResult, scan, scan_corpus
from .self_coherence import Match as SelfCoherenceMatch
from .self_coherence import SelfCoherenceResult, scan_self_coherence

__all__ = [
    "ResonanceMatch", "ResonanceResult", "scan_resonance",
    "SelfCoherenceMatch", "SelfCoherenceResult", "scan_self_coherence",
    "DebasinizerResult", "CorpusScanSummary", "scan", "scan_corpus",
]

__version__ = "0.1.0"
