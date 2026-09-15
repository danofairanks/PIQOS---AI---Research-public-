"""Detector for paralipsis ("I'm not saying X, but...") plus a mechanized
first step of the operator-proposed removal test: does the reader's
association with the disclaimed content survive deleting the
disclaiming sentence entirely?

Quick start::

    from hedge_dogwhistle import scan

    result = scan(
        "He's clearly hiding something. I'm not saying he's corrupt, "
        "but you have to wonder."
    )
    print(result.has_paralipsis)              # True
    print(result.text_with_hedges_removed)    # "He's clearly hiding something. ... but you have to wonder."

Or from the command line::

    hedge-dogwhistle text --text "..."
    hedge-dogwhistle corpus --corpus docs.jsonl
"""

from .paralipsis import ParalipsisMatch, find_paralipsis
from .removal_test import RemovalTestResult, remove_spans, run_removal_test
from .scan import CorpusScanSummary, scan, scan_corpus
from .sentences import sentence_containing, split_sentences

__all__ = [
    "ParalipsisMatch",
    "find_paralipsis",
    "RemovalTestResult",
    "remove_spans",
    "run_removal_test",
    "CorpusScanSummary",
    "scan",
    "scan_corpus",
    "sentence_containing",
    "split_sentences",
]

__version__ = "0.1.0"
