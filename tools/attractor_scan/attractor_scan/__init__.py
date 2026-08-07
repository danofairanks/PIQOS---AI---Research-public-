"""Text classifier for basin_attractors_v1.md's seven defensive
maneuvers (§4.1) and five of its six semantic-laundering cases (§2.8).

Quick start::

    from attractor_scan import scan

    result = scan("We're working on it -- that's just a hot take from someone who doesn't get it.")
    print(result.flagged_maneuvers)  # ['provisionalization', 'status_dismissal']
    print(result.density)

Or from the command line::

    attractor-scan text --text "..."
    attractor-scan corpus --corpus docs.jsonl
"""

from .laundering import LaunderingResult, scan_laundering
from .maneuvers import MANEUVER_PHRASES, ManeuverResult, scan_maneuver, scan_maneuvers
from .scan import AttractorScanResult, CorpusScanSummary, scan, scan_corpus

__all__ = [
    "LaunderingResult", "scan_laundering",
    "MANEUVER_PHRASES", "ManeuverResult", "scan_maneuver", "scan_maneuvers",
    "AttractorScanResult", "CorpusScanSummary", "scan", "scan_corpus",
]

__version__ = "0.1.0"
