"""Unified scan entry point plus a simple corpus-level aggregation
helper. Same shape as `debasinizer.scan` / `attractor_scan.scan`
elsewhere in this repository.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .signatures import DEFAULT_PROXIMITY_RADIUS, RigorCosplayResult, scan_rigor_cosplay


def scan(text: str, *, radius: int = DEFAULT_PROXIMITY_RADIUS) -> RigorCosplayResult:
    """Run the three Rigor Cosplay signature detectors against a single
    piece of text."""
    return scan_rigor_cosplay(text, radius=radius)


@dataclass
class CorpusScanSummary:
    n_documents: int
    any_flagged_count: int = 0
    signature_document_counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "n_documents": self.n_documents,
            "any_flagged_count": self.any_flagged_count,
            "any_flagged_frequency": (
                self.any_flagged_count / self.n_documents if self.n_documents else 0.0
            ),
            "signature_document_counts": self.signature_document_counts,
        }


def scan_corpus(
    documents: list[tuple[str, str]], *, radius: int = DEFAULT_PROXIMITY_RADIUS
) -> CorpusScanSummary:
    """Scan a list of (doc_id, text) pairs and aggregate flag frequency
    across the corpus. Counting, not statistics -- see `tools/basin_depth`
    for the significance-tested measurement this project ships."""
    summary = CorpusScanSummary(n_documents=len(documents))
    for _doc_id, text in documents:
        result = scan(text, radius=radius)
        if result.any_signature_flagged:
            summary.any_flagged_count += 1
        for signature in result.signatures_hit:
            summary.signature_document_counts[signature] = (
                summary.signature_document_counts.get(signature, 0) + 1
            )
    return summary
