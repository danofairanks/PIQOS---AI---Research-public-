"""Unified scan entry point plus a simple corpus-level aggregation
helper. Same shape as `debasinizer.scan` / `rigor_cosplay.scan`
elsewhere in this repository.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .removal_test import RemovalTestResult, run_removal_test


def scan(text: str) -> RemovalTestResult:
    """Find paralipsis constructions in `text` and mechanize the first
    step of the removal test (see `removal_test.py`)."""
    return run_removal_test(text)


@dataclass
class CorpusScanSummary:
    n_documents: int
    has_paralipsis_count: int = 0
    total_matches: int = 0

    def to_dict(self) -> dict:
        return {
            "n_documents": self.n_documents,
            "has_paralipsis_count": self.has_paralipsis_count,
            "has_paralipsis_frequency": (
                self.has_paralipsis_count / self.n_documents if self.n_documents else 0.0
            ),
            "total_matches": self.total_matches,
        }


def scan_corpus(documents: list[tuple[str, str]]) -> CorpusScanSummary:
    """Scan a list of (doc_id, text) pairs and aggregate flag frequency
    across the corpus. Counting, not statistics -- see `tools/basin_depth`
    for the significance-tested measurement this project ships."""
    summary = CorpusScanSummary(n_documents=len(documents))
    for _doc_id, text in documents:
        result = scan(text)
        if result.has_paralipsis:
            summary.has_paralipsis_count += 1
        summary.total_matches += len(result.matches)
    return summary
