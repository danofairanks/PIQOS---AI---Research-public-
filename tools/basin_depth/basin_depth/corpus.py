"""Corpus ingestion, deduplication, length filtering, and quarterly binning.

Implements protocol §2 (Corpus Specification) and Appendix A, Step 1.
This module is deliberately source-agnostic: it consumes a generic
timestamped-document format (JSONL or CSV) rather than shipping
scrapers for any specific source (arXiv, lab blogs, earnings calls,
...). Bring your own corpus; this module handles what every corpus
needs regardless of where it came from.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Document:
    """A single timestamped text document."""

    doc_id: str
    text: str
    quarter: str  # e.g. "2023Q1"
    source: str = ""
    metadata: dict = field(default_factory=dict)

    @property
    def tokens(self) -> list[str]:
        return _tokenize(self.text)


_TOKEN_RE = re.compile(r"[a-z0-9']+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


def quarter_of(d: date) -> str:
    return f"{d.year}Q{(d.month - 1) // 3 + 1}"


def parse_quarter(value: str) -> tuple[int, int]:
    """Parse '2023Q1' -> (2023, 1). Raises ValueError on malformed input."""
    m = re.fullmatch(r"(\d{4})Q([1-4])", value.strip())
    if not m:
        raise ValueError(f"not a quarter string like '2023Q1': {value!r}")
    return int(m.group(1)), int(m.group(2))


def quarter_index(value: str) -> int:
    """Linear index of a quarter for ordering/arithmetic (year*4 + q)."""
    year, q = parse_quarter(value)
    return year * 4 + (q - 1)


def quarter_range(start: str, end: str) -> list[str]:
    """Ordered list of quarter labels from start to end, inclusive."""
    start_idx, end_idx = quarter_index(start), quarter_index(end)
    if end_idx < start_idx:
        raise ValueError(f"end quarter {end!r} precedes start quarter {start!r}")
    out = []
    for idx in range(start_idx, end_idx + 1):
        year, q0 = divmod(idx, 4)
        out.append(f"{year}Q{q0 + 1}")
    return out


def load_jsonl(path: str | Path, *, text_field: str = "text",
                quarter_field: str = "quarter", id_field: str = "id",
                source_field: str = "source") -> list[Document]:
    """Load documents from a JSONL file, one JSON object per line.

    Each object must have at least a text field and a quarter field
    (either an explicit '2023Q1'-style string, or the loader will try
    `date_field` if `quarter_field` is absent — see `load_jsonl_with_dates`
    for the date-based variant).
    """
    docs: list[Document] = []
    with open(path, encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            docs.append(
                Document(
                    doc_id=str(obj.get(id_field, i)),
                    text=obj[text_field],
                    quarter=obj[quarter_field],
                    source=obj.get(source_field, ""),
                    metadata={k: v for k, v in obj.items()
                              if k not in {text_field, quarter_field, id_field, source_field}},
                )
            )
    return docs


def load_csv(path: str | Path, *, text_col: str = "text",
             quarter_col: str = "quarter", id_col: str | None = None,
             source_col: str | None = None) -> list[Document]:
    """Load documents from a CSV file with headers."""
    docs: list[Document] = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader):
            docs.append(
                Document(
                    doc_id=row[id_col] if id_col else str(i),
                    text=row[text_col],
                    quarter=row[quarter_col],
                    source=row[source_col] if source_col else "",
                )
            )
    return docs


def filter_by_length(docs: list[Document], *, min_tokens: int = 100) -> list[Document]:
    """Protocol §2.1 exclusion criterion: drop documents under min_tokens."""
    return [d for d in docs if len(d.tokens) >= min_tokens]


def _shingles(text: str, k: int = 5) -> set[str]:
    toks = _tokenize(text)
    if len(toks) < k:
        return {" ".join(toks)} if toks else set()
    return {" ".join(toks[i:i + k]) for i in range(len(toks) - k + 1)}


def jaccard_similarity(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def deduplicate(docs: list[Document], *, threshold: float = 0.85, shingle_k: int = 5) -> list[Document]:
    """Near-duplicate removal via k-shingle Jaccard similarity.

    Protocol §2.1 specifies MinHash LSH at threshold 0.85; this is an
    exact O(n^2) shingle-Jaccard implementation of the same
    acceptance criterion. It is correct at any corpus size and fast
    enough for corpora up to a few thousand documents; for larger
    corpora, swap in a MinHash/LSH index behind the same
    `deduplicate()` signature without changing any downstream code.
    """
    kept: list[Document] = []
    kept_shingles: list[set[str]] = []
    for d in docs:
        sh = _shingles(d.text, shingle_k)
        is_dup = any(jaccard_similarity(sh, existing) >= threshold for existing in kept_shingles)
        if not is_dup:
            kept.append(d)
            kept_shingles.append(sh)
    return kept


def bin_by_quarter(docs: list[Document], quarters: list[str] | None = None) -> dict[str, list[Document]]:
    """Group documents by quarter. If `quarters` is given, every quarter
    in that list is present in the output (possibly with an empty list),
    preserving the caller's ordering downstream via `quarters`.
    """
    bins: dict[str, list[Document]] = {}
    if quarters:
        for q in quarters:
            bins[q] = []
    for d in docs:
        bins.setdefault(d.quarter, []).append(d)
    return bins


def preprocess_corpus(
    docs: list[Document],
    *,
    min_tokens: int = 100,
    dedup_threshold: float = 0.85,
) -> list[Document]:
    """Apply protocol §2.1 inclusion/exclusion pipeline: length filter then dedup."""
    docs = filter_by_length(docs, min_tokens=min_tokens)
    docs = deduplicate(docs, threshold=dedup_threshold)
    return docs
