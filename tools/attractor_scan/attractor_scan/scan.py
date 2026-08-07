"""Unified scan combining the maneuver and semantic-laundering
classifiers, plus a simple corpus-level aggregation helper.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .laundering import LaunderingResult, scan_laundering
from .maneuvers import ManeuverResult, scan_maneuvers


@dataclass
class AttractorScanResult:
    maneuvers: dict[str, ManeuverResult]
    laundering: dict[str, LaunderingResult]

    @property
    def flagged_maneuvers(self) -> list[str]:
        return [k for k, v in self.maneuvers.items() if v.flagged]

    @property
    def flagged_laundering_cases(self) -> list[str]:
        return [k for k, v in self.laundering.items() if v.flagged]

    @property
    def total_categories(self) -> int:
        return len(self.maneuvers) + len(self.laundering)

    @property
    def flagged_category_count(self) -> int:
        return len(self.flagged_maneuvers) + len(self.flagged_laundering_cases)

    @property
    def density(self) -> float:
        """Fraction of the 12 implemented categories (7 maneuvers + 5
        laundering cases) that flagged at least one match. A single
        summary scalar for corpus-level comparison; NOT a claim that a
        higher density means a text is more 'captured' -- see README."""
        if self.total_categories == 0:
            return 0.0
        return self.flagged_category_count / self.total_categories

    def to_dict(self) -> dict:
        return {
            "maneuvers": {k: v.to_dict() for k, v in self.maneuvers.items()},
            "laundering": {k: v.to_dict() for k, v in self.laundering.items()},
            "flagged_maneuvers": self.flagged_maneuvers,
            "flagged_laundering_cases": self.flagged_laundering_cases,
            "density": self.density,
        }


def scan(text: str) -> AttractorScanResult:
    """Run every implemented maneuver and semantic-laundering scanner
    against a single piece of text."""
    return AttractorScanResult(maneuvers=scan_maneuvers(text), laundering=scan_laundering(text))


@dataclass
class CorpusScanSummary:
    n_documents: int
    category_document_counts: dict[str, int] = field(default_factory=dict)  # category -> # docs with a flag
    category_match_counts: dict[str, int] = field(default_factory=dict)     # category -> total match count
    per_document_density: dict[str, float] = field(default_factory=dict)    # doc_id -> density

    def to_dict(self) -> dict:
        return {
            "n_documents": self.n_documents,
            "category_document_counts": self.category_document_counts,
            "category_document_frequency": {
                k: (v / self.n_documents if self.n_documents else 0.0)
                for k, v in self.category_document_counts.items()
            },
            "category_match_counts": self.category_match_counts,
            "per_document_density": self.per_document_density,
        }


def scan_corpus(documents: list[tuple[str, str]]) -> CorpusScanSummary:
    """Scan a list of (doc_id, text) pairs and aggregate category
    frequency across the corpus. This is deliberately simple --
    counting, not statistics -- see tools/basin_depth for the actual
    significance-tested measurement this project ships; this function
    is a quick first-pass survey, not a substitute for it.
    """
    summary = CorpusScanSummary(n_documents=len(documents))
    for doc_id, text in documents:
        result = scan(text)
        summary.per_document_density[doc_id] = result.density
        for category in list(result.maneuvers) + list(result.laundering):
            flagged = (result.maneuvers.get(category) or result.laundering.get(category)).flagged
            matches = len((result.maneuvers.get(category) or result.laundering.get(category)).matches)
            summary.category_match_counts[category] = summary.category_match_counts.get(category, 0) + matches
            if flagged:
                summary.category_document_counts[category] = summary.category_document_counts.get(category, 0) + 1
    return summary
