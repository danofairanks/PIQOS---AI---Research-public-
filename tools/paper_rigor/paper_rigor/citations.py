"""Citation-shape checks: self-citation ratio, formal-vs-informal
sourcing mix, and uncited empirical-certainty claims. Deliberately
does NOT attempt to verify that a citation supports the claim it's
attached to -- that requires reading the cited work, which is exactly
the boundary `scan.py`'s external-verification worklist exists for
(see README). Everything here is computable from the paper's own text.

Reference-list parsing is best-effort against one real, common shape:
an APA-ish "## References" section with blank-line-separated entries
("Lastname, F., Lastname2, F2. & Lastname3, F3. (Year). Title. Venue.
URL."). Tuned against this repo's own `basin_attractors_v1.md`
references section, which also includes non-academic entries (a court
case citation, a GitHub issue, a self-published PDF) the parser must
degrade gracefully on rather than crash on -- author/year/URL fields
come back as `None` when unparseable, they are never guessed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ._shared import has_meta_framing_nearby

_REFERENCES_HEADER_RE = re.compile(
    r'^#{1,3}\s*(references|bibliography|works cited|sources)\s*$',
    re.IGNORECASE | re.MULTILINE,
)
_ANY_HEADER_RE = re.compile(r'^#{1,3}\s+\S', re.MULTILINE)
# A standalone "---" horizontal rule is this project's own convention
# for a major section break (used throughout CLAUDE.md and every real
# paper checked during tuning) -- References lists in practice end at
# the next one of these, not only at the next markdown heading. Without
# this, a references section with no following heading (a real case:
# basin_attractors_v1.md's dated revision-log paragraphs follow
# directly after its reference list with no heading in between) reads
# all the way to end-of-document, and prose paragraphs get mis-split
# and counted as if they were bibliography entries.
_SECTION_BREAK_RE = re.compile(r'^#{1,3}\s+\S|^---\s*$', re.MULTILINE)

_AUTHOR_LIST_RE = re.compile(
    r'^([A-Z][A-Za-z\'-]+(?:,\s*[A-Z]\.(?:[A-Z]\.)?){1,3}'
    r'(?:,?\s*(?:&|and)\s*[A-Z][A-Za-z\'-]+(?:,\s*[A-Z]\.(?:[A-Z]\.)?){1,3})*'
    r'(?:,?\s*et al\.)?)',
)
_LASTNAME_RE = re.compile(r'\b([A-Z][A-Za-z\'-]{2,})\b')
_YEAR_RE = re.compile(r'\((\d{4})(?:[/,]\s*\d{4})?')
_URL_RE = re.compile(r'https?://\S+')

FORMAL_DOMAIN_MARKERS = [
    "arxiv.org", "doi.org", "nature.com", "science.org", "pmc.ncbi",
    "ncbi.nlm.nih.gov", ".edu/", "aclanthology.org", "openreview.net",
    "acm.org", "ieee.org", "springer.com", "sciencedirect.com",
]
INFORMAL_DOMAIN_MARKERS = [
    "medium.com", "substack.com", "twitter.com", "x.com", "linkedin.com",
    "businesswire.com", "prnewswire.com", "reddit.com", "facebook.com",
    "tiktok.com",
]
FORMAL_VENUE_TEXT_MARKERS = [
    "arxiv", "icml", "iclr", "neurips", "acl ", "emnlp", "doi:",
]

# Inline in-body citation shapes: "(Author, 2026)", "(Author & Other, 2026)",
# a footnote marker, or a bare URL -- any of these counts as "some
# citation-shaped evidence is present nearby," same proximity-heuristic
# contract as verification_lint's statistics.py/quotes.py.
_INLINE_CITATION_SIGNALS = [
    re.compile(r'\([A-Z][A-Za-z\'-]+(?:\s*(?:&|and|,)\s*[A-Z][A-Za-z\'-]+)*,?\s*\d{4}[a-z]?\)'),
    re.compile(r'\[\^?\d+\]'),
    _URL_RE,
    re.compile(r'\bet al\.'),
]

EMPIRICAL_CLAIM_MARKERS = [
    "research shows", "research demonstrates", "studies confirm", "studies show",
    "experiments demonstrate", "experiments show", "data shows", "data demonstrates",
    "evidence shows", "researchers found", "scientists confirm", "studies have shown",
]
_EMPIRICAL_CLAIM_RE = re.compile("|".join(re.escape(p) for p in EMPIRICAL_CLAIM_MARKERS), re.IGNORECASE)

CONTEXT_CHARS = 150


@dataclass
class CitationEntry:
    raw: str
    authors: list[str]  # best-effort last names; empty if unparseable
    year: str | None
    url: str | None
    venue_type: str  # "formal" | "informal" | "unknown"

    def to_dict(self) -> dict:
        return {"raw": self.raw, "authors": self.authors, "year": self.year,
                "url": self.url, "venue_type": self.venue_type}


def _classify_venue(entry_text: str, url: str | None) -> str:
    lowered = entry_text.lower()
    # Real references often name a domain without a full scheme'd URL
    # ("thehumanlineproject.org, as reported by Vice" -- no "https://").
    # Check domain markers against the raw entry text too, not only a
    # parsed URL's netloc -- caught during tuning against this repo's
    # own basin_attractors_v1.md references, more than half of which
    # cite a bare domain this way.
    if any(d in lowered for d in FORMAL_DOMAIN_MARKERS):
        return "formal"
    if any(d in lowered for d in INFORMAL_DOMAIN_MARKERS):
        return "informal"
    if any(m in lowered for m in FORMAL_VENUE_TEXT_MARKERS):
        return "formal"
    return "unknown"


def extract_references_section(text: str) -> str | None:
    """Returns the text under the first References/Bibliography/Works
    Cited/Sources heading, up to the next heading of any level, or the
    end of the document. `None` if no such heading is found."""
    m = _REFERENCES_HEADER_RE.search(text)
    if not m:
        return None
    rest = text[m.end():]
    next_break = _SECTION_BREAK_RE.search(rest)
    return rest[:next_break.start()] if next_break else rest


def parse_references(text: str) -> list[CitationEntry]:
    """Best-effort. Returns `[]` if no references section is found --
    that is itself a reportable fact (see `scan.py`), not an error."""
    section = extract_references_section(text)
    if section is None:
        return []

    entries = []
    for block in re.split(r'\n\s*\n', section.strip()):
        block = block.strip()
        if not block:
            continue
        author_match = _AUTHOR_LIST_RE.match(block)
        authors = _LASTNAME_RE.findall(author_match.group(1)) if author_match else []
        year_match = _YEAR_RE.search(block)
        url_match = _URL_RE.search(block)
        url = url_match.group(0).rstrip('.,)') if url_match else None
        entries.append(CitationEntry(
            raw=block, authors=authors,
            year=year_match.group(1) if year_match else None,
            url=url, venue_type=_classify_venue(block, url),
        ))
    return entries


@dataclass
class SelfCitationResult:
    ratio: float | None  # None if no byline authors were supplied
    n_references: int
    n_self_cited: int
    self_cited_entries: list[str]

    def to_dict(self) -> dict:
        return {"ratio": self.ratio, "n_references": self.n_references,
                "n_self_cited": self.n_self_cited, "self_cited_entries": self.self_cited_entries}


def compute_self_citation(entries: list[CitationEntry], byline_authors: list[str] | None) -> SelfCitationResult:
    """`byline_authors` is the paper's own declared author last names,
    supplied by the caller -- deliberately not auto-extracted from the
    document header, which is unreliable across formats (this repo's
    own `basin_attractors_v1.md` has no individual byline at all, just
    "Research Memo"). Pass `None` or `[]` when the paper has no
    individual byline; `ratio` comes back `None` rather than a
    meaningless 0.0 in that case."""
    if not byline_authors or not entries:
        return SelfCitationResult(ratio=None, n_references=len(entries), n_self_cited=0, self_cited_entries=[])
    byline_lower = {a.lower() for a in byline_authors}
    self_cited = [e for e in entries if any(a.lower() in byline_lower for a in e.authors)]
    return SelfCitationResult(
        ratio=len(self_cited) / len(entries),
        n_references=len(entries), n_self_cited=len(self_cited),
        self_cited_entries=[e.raw for e in self_cited],
    )


@dataclass
class VenueMixResult:
    n_formal: int
    n_informal: int
    n_unknown: int
    n_total: int

    @property
    def informal_ratio(self) -> float:
        return self.n_informal / self.n_total if self.n_total else 0.0

    def to_dict(self) -> dict:
        return {"n_formal": self.n_formal, "n_informal": self.n_informal,
                "n_unknown": self.n_unknown, "n_total": self.n_total,
                "informal_ratio": self.informal_ratio}


def compute_venue_mix(entries: list[CitationEntry]) -> VenueMixResult:
    n_formal = sum(1 for e in entries if e.venue_type == "formal")
    n_informal = sum(1 for e in entries if e.venue_type == "informal")
    n_unknown = sum(1 for e in entries if e.venue_type == "unknown")
    return VenueMixResult(n_formal=n_formal, n_informal=n_informal, n_unknown=n_unknown, n_total=len(entries))


@dataclass
class UncitedEmpiricalClaim:
    phrase: str
    start: int
    end: int
    context: str

    def to_dict(self) -> dict:
        return {"phrase": self.phrase, "start": self.start, "end": self.end, "context": self.context}


def find_uncited_empirical_claims(text: str, *, window: int = CONTEXT_CHARS) -> list[UncitedEmpiricalClaim]:
    """"Research shows..." / "studies confirm..." with no citation-
    shaped signal (an (Author, Year), a footnote marker, a URL, or
    "et al.") within `window` characters either side. Same proximity-
    heuristic contract as verification_lint -- a lead, not a verdict;
    does not check whether a found citation actually supports the
    claim."""
    out = []
    for m in _EMPIRICAL_CLAIM_RE.finditer(text):
        if has_meta_framing_nearby(text, m.start(), m.end()):
            continue
        start, end = max(0, m.start() - window), min(len(text), m.end() + window)
        context = text[start:end]
        if not any(sig.search(context) for sig in _INLINE_CITATION_SIGNALS):
            out.append(UncitedEmpiricalClaim(phrase=m.group(0), start=m.start(), end=m.end(), context=context))
    return out
