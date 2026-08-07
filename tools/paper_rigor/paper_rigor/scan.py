"""Unified paper scan. Splits findings into two kinds, matching the
distinction the tool was scoped around: `structural_gap_count` covers
what's fully resolved by reading the paper's own text (an author could
fix these without looking anything up); `external_verification_worklist`
covers what genuinely needs someone to check something outside the
paper (does citation X really say what's claimed, does this informal
source hold up, were these self-cited priors independently validated).
The worklist is the part meant for an MCP-connected agent with real
web search/fetch access to resolve -- see tools/research_mcp/.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .citations import (
    CitationEntry, SelfCitationResult, VenueMixResult, compute_self_citation,
    compute_venue_mix, find_uncited_empirical_claims, parse_references,
)
from .consensus import find_unsupported_consensus_claims
from .credentialing import find_credential_substitution
from .disclaimer import LimitationsCheck, check_limitations_section
from .falsifiability import FalsifiabilityCheck, check_falsifiability
from .placeholders import find_placeholder_issues

# Self-citation above this ratio, or any informal-venue reference,
# earns a worklist item rather than being silently counted only in the
# aggregate stat. Judgment calls, not values taken from any paper on
# citation practice -- tune per corpus.
SELF_CITATION_WORKLIST_THRESHOLD = 0.3


@dataclass
class PaperRigorResult:
    path: str
    placeholder_gaps: list = field(default_factory=list)
    labeled_placeholders: list = field(default_factory=list)
    falsifiability: FalsifiabilityCheck | None = None
    references: list[CitationEntry] = field(default_factory=list)
    self_citation: SelfCitationResult | None = None
    venue_mix: VenueMixResult | None = None
    uncited_empirical_claims: list = field(default_factory=list)
    credential_issues: list = field(default_factory=list)
    consensus_issues: list = field(default_factory=list)
    limitations: LimitationsCheck | None = None

    @property
    def structural_gap_count(self) -> int:
        count = len(self.placeholder_gaps)
        if self.falsifiability and self.falsifiability.gap:
            count += 1
        if self.limitations and self.limitations.gap:
            count += 1
        return count

    @property
    def external_verification_worklist(self) -> list[dict]:
        items = []
        for c in self.uncited_empirical_claims:
            items.append({"kind": "uncited_empirical_claim", "item": c.phrase,
                          "context": c.context, "reason": "empirical-certainty language with no citation nearby -- find and check the actual source"})
        for c in self.credential_issues:
            items.append({"kind": "credential_substitution", "item": c.phrase,
                          "context": c.context, "reason": "claim supported only by an appeal to credentials -- check whether the credential is real and whether independent evidence exists"})
        for c in self.consensus_issues:
            items.append({"kind": "unsupported_consensus_claim", "item": c.phrase,
                          "context": c.context, "reason": "consensus asserted with no citation -- check whether a survey/meta-analysis actually supports it"})
        for e in self.references:
            if e.venue_type == "informal":
                items.append({"kind": "informal_citation", "item": e.raw,
                              "context": e.raw, "reason": "cited source is a blog/social/press-release domain -- check whether the underlying claim holds up independently"})
        if self.self_citation and self.self_citation.ratio is not None and self.self_citation.ratio > SELF_CITATION_WORKLIST_THRESHOLD:
            items.append({
                "kind": "high_self_citation_ratio",
                "item": f"{self.self_citation.n_self_cited}/{self.self_citation.n_references} references are self-cited "
                        f"({self.self_citation.ratio:.0%})",
                "context": "; ".join(self.self_citation.self_cited_entries[:5]),
                "reason": "check whether these self-cited prior claims were independently validated, not just internally consistent",
            })
        return items

    @property
    def total_gap_count(self) -> int:
        return self.structural_gap_count + len(self.external_verification_worklist)

    @property
    def ok(self) -> bool:
        """Structural gaps only -- what the text itself already
        establishes. The worklist is leads for further work, not a
        pass/fail signal; a paper with a long, honest worklist and zero
        structural gaps is doing exactly what a rigorous paper should
        (making its citations checkable), not failing."""
        return self.structural_gap_count == 0

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "ok": self.ok,
            "structural_gap_count": self.structural_gap_count,
            "total_gap_count": self.total_gap_count,
            "placeholder_gaps": [g.to_dict() for g in self.placeholder_gaps],
            "labeled_placeholders": [g.to_dict() for g in self.labeled_placeholders],
            "falsifiability": self.falsifiability.to_dict() if self.falsifiability else None,
            "n_references": len(self.references),
            "self_citation": self.self_citation.to_dict() if self.self_citation else None,
            "venue_mix": self.venue_mix.to_dict() if self.venue_mix else None,
            "external_verification_worklist": self.external_verification_worklist,
            "limitations": self.limitations.to_dict() if self.limitations else None,
        }


def scan_paper(text: str, *, path: str = "<text>", byline_authors: list[str] | None = None,
               min_word_count: int = 400) -> PaperRigorResult:
    placeholder_result = find_placeholder_issues(text)
    references = parse_references(text)
    return PaperRigorResult(
        path=path,
        placeholder_gaps=placeholder_result["gaps"],
        labeled_placeholders=placeholder_result["labeled"],
        falsifiability=check_falsifiability(text),
        references=references,
        self_citation=compute_self_citation(references, byline_authors),
        venue_mix=compute_venue_mix(references),
        uncited_empirical_claims=find_uncited_empirical_claims(text),
        credential_issues=find_credential_substitution(text),
        consensus_issues=find_unsupported_consensus_claims(text),
        limitations=check_limitations_section(text, min_word_count=min_word_count),
    )


def scan_file(path: str | Path, *, byline_authors: list[str] | None = None,
              min_word_count: int = 400) -> PaperRigorResult:
    path = Path(path)
    return scan_paper(path.read_text(encoding="utf-8"), path=str(path),
                       byline_authors=byline_authors, min_word_count=min_word_count)
