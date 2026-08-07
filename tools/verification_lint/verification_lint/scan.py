"""Unified document scan combining the quote, statistic, and disclaimer
checks, plus a directory-level aggregation helper for CI use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .disclaimer import DisclaimerCheck, check_disclaimer
from .quotes import QuoteFinding, find_unattributed_quotes
from .sourcing import SourcingCheck, check_sourcing
from .statistics import StatFinding, find_uncited_statistics


@dataclass
class VerificationLintResult:
    path: str
    unattributed_quotes: list[QuoteFinding] = field(default_factory=list)
    uncited_statistics: list[StatFinding] = field(default_factory=list)
    disclaimer: DisclaimerCheck | None = None
    sourcing: SourcingCheck | None = None

    @property
    def gap_count(self) -> int:
        count = len(self.unattributed_quotes) + len(self.uncited_statistics)
        if self.disclaimer and self.disclaimer.gap:
            count += 1
        return count

    @property
    def severe_gap_count(self) -> int:
        """Gap count when the document has NO end-of-document sourcing
        statement to fall back on -- i.e. these items genuinely have no
        citation anywhere, not just none nearby. Use this, not
        `gap_count`, as the primary CI signal; see README."""
        if self.sourcing and self.sourcing.has_end_sourcing:
            return 1 if (self.disclaimer and self.disclaimer.gap) else 0
        return self.gap_count

    @property
    def ok(self) -> bool:
        return self.severe_gap_count == 0

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "ok": self.ok,
            "gap_count": self.gap_count,
            "severe_gap_count": self.severe_gap_count,
            "unattributed_quotes": [q.to_dict() for q in self.unattributed_quotes],
            "uncited_statistics": [s.to_dict() for s in self.uncited_statistics],
            "disclaimer": self.disclaimer.to_dict() if self.disclaimer else None,
            "sourcing": self.sourcing.to_dict() if self.sourcing else None,
        }


def scan_document(text: str, *, path: str = "<text>", min_word_count: int = 400) -> VerificationLintResult:
    return VerificationLintResult(
        path=path,
        unattributed_quotes=find_unattributed_quotes(text),
        uncited_statistics=find_uncited_statistics(text),
        disclaimer=check_disclaimer(text, min_word_count=min_word_count),
        sourcing=check_sourcing(text),
    )


def scan_file(path: str | Path, *, min_word_count: int = 400) -> VerificationLintResult:
    path = Path(path)
    return scan_document(path.read_text(encoding="utf-8"), path=str(path), min_word_count=min_word_count)


def scan_paths(paths: list[str | Path], *, min_word_count: int = 400) -> list[VerificationLintResult]:
    return [scan_file(p, min_word_count=min_word_count) for p in paths]
