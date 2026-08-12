"""Unified scan combining the resonance-register and self-coherence
classifiers, plus a simple corpus-level aggregation helper. Same shape
as `attractor_scan.scan` elsewhere in this repository.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .resonance import ResonanceResult, scan_resonance
from .self_coherence import SelfCoherenceResult, scan_self_coherence


@dataclass
class DebasinizerResult:
    resonance: ResonanceResult
    self_coherence: SelfCoherenceResult

    @property
    def flagged_resonance_categories(self) -> list[str]:
        return self.resonance.categories_hit

    @property
    def register_flagged(self) -> bool:
        """True when 2+ distinct resonance categories co-occur -- the
        cross-category signature the source paper's own findings
        describe. See `resonance.ResonanceResult.register_flagged`."""
        return self.resonance.register_flagged

    @property
    def self_coherence_flagged(self) -> bool:
        return self.self_coherence.flagged

    @property
    def any_flagged(self) -> bool:
        return self.register_flagged or self.self_coherence_flagged

    def to_dict(self) -> dict:
        return {
            "resonance": self.resonance.to_dict(),
            "self_coherence": self.self_coherence.to_dict(),
            "register_flagged": self.register_flagged,
            "self_coherence_flagged": self.self_coherence_flagged,
            "any_flagged": self.any_flagged,
        }


def scan(text: str) -> DebasinizerResult:
    """Run the resonance-register and self-coherence-assertion
    detectors against a single piece of text."""
    return DebasinizerResult(resonance=scan_resonance(text), self_coherence=scan_self_coherence(text))


@dataclass
class CorpusScanSummary:
    n_documents: int
    register_flagged_count: int = 0
    self_coherence_flagged_count: int = 0
    resonance_category_document_counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "n_documents": self.n_documents,
            "register_flagged_count": self.register_flagged_count,
            "register_flagged_frequency": (
                self.register_flagged_count / self.n_documents if self.n_documents else 0.0
            ),
            "self_coherence_flagged_count": self.self_coherence_flagged_count,
            "self_coherence_flagged_frequency": (
                self.self_coherence_flagged_count / self.n_documents if self.n_documents else 0.0
            ),
            "resonance_category_document_counts": self.resonance_category_document_counts,
        }


def scan_corpus(documents: list[tuple[str, str]]) -> CorpusScanSummary:
    """Scan a list of (doc_id, text) pairs and aggregate flag frequency
    across the corpus. Counting, not statistics -- see
    `tools/basin_depth` for the significance-tested measurement this
    project ships; this function is a quick first-pass survey."""
    summary = CorpusScanSummary(n_documents=len(documents))
    for _doc_id, text in documents:
        result = scan(text)
        if result.register_flagged:
            summary.register_flagged_count += 1
        if result.self_coherence_flagged:
            summary.self_coherence_flagged_count += 1
        for category in result.flagged_resonance_categories:
            summary.resonance_category_document_counts[category] = (
                summary.resonance_category_document_counts.get(category, 0) + 1
            )
    return summary
