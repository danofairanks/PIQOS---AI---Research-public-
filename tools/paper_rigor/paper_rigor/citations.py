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
from .headings import find_section, iter_headings

_REFERENCES_NAME_RE = re.compile(r'^(?:references|bibliography|works cited|sources)$', re.IGNORECASE)
# A standalone "---" horizontal rule is this project's own convention
# for a major section break (used throughout CLAUDE.md and every real
# paper checked during tuning) -- References lists in practice end at
# the next one of these, not only at the next detected heading. Without
# this, a references section with no following heading (a real case:
# basin_attractors_v1.md's dated revision-log paragraphs follow
# directly after its reference list with no heading in between) reads
# all the way to end-of-document, and prose paragraphs get mis-split
# and counted as if they were bibliography entries. Not itself a
# "heading" concept, so it stays local here rather than living in
# headings.py.
_STANDALONE_DIVIDER_RE = re.compile(r'^---\s*$', re.MULTILINE)

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

# Self-referential citability claims: the paper asserting ITS OWN work
# rests on citable/documented research -- distinct from the paper
# describing a THIRD PARTY's work as peer-reviewed (a real false-
# positive caught during tuning: mirror_test_v1.md's table entry
# '"Sparks of AGI" (Bubeck et al.) | Peer-reviewed totalization' labels
# an external claim, not this document's own grounding). Deliberately
# narrower than a bare "peer-reviewed"/"published research" match for
# exactly that reason -- these phrases are shaped around a paper
# talking about its own sourcing ("grounded in ... research",
# "citable research", "extensively cited"), found verbatim in the real
# specimen that motivated this check (see README).
_CITABILITY_CLAIM_RE = re.compile(
    r'\bcitable research\b|\bdocumented,\s*citable\b|'
    r'\bground(?:ed|ing) in (?:documented|extensive|established)\s+research\b|'
    r'\bextensively cited\b|\bwell-documented framework\b|\bwell documented framework\b|'
    r'\bbase papers\b',
    re.IGNORECASE,
)

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


# A bare "References" line with no markdown and no numeric prefix, as
# PDF-to-text extraction often leaves it. Only these three names are
# accepted in the bare form ("Sources" alone on a line is too ordinary
# to treat as a heading), and the LAST occurrence is used so a table-
# of-contents line does not win over the real list at the end.
_BARE_REFERENCES_RE = re.compile(r'^[ \t]*(?:references|bibliography|works cited)[ \t]*$',
                                 re.IGNORECASE | re.MULTILINE)


def extract_references_section(text: str) -> str | None:
    """Returns the text under the first References/Bibliography/Works
    Cited/Sources heading (markdown `#` or a plain numbered heading --
    see `headings.py`), up to the next heading, a standalone `---`
    divider, or the end of the document. Falls back to a bare,
    unnumbered `References` / `Bibliography` / `Works cited` line (the
    last one in the document) when no such heading is detected. `None`
    if neither is found."""
    section = find_section(text, _REFERENCES_NAME_RE, extra_stop=_STANDALONE_DIVIDER_RE)
    if section is not None:
        return section
    bare = list(_BARE_REFERENCES_RE.finditer(text))
    if not bare:
        return None
    body_start = bare[-1].end()
    body_end = len(text)
    for h in iter_headings(text):
        if h.start >= body_start:
            body_end = h.start
            break
    stop = _STANDALONE_DIVIDER_RE.search(text, body_start, body_end)
    if stop:
        body_end = stop.start()
    return text[body_start:body_end]


# Reading-order text extracted from a PDF has no blank line between
# reference entries and wraps each entry over several lines. The
# splitter below closes an entry at a line that ends with a year (and
# optional period), a URL or a DOI -- the usual end of an entry -- and
# is only used when the blank-line split yields almost nothing.
_ENTRY_END_RE = re.compile(r'(?:\b(?:19|20)\d{2}[a-z]?\.?|https?://\S+|\bdoi:\S+)\s*$', re.IGNORECASE)
_PAGE_NUMBER_LINE_RE = re.compile(r'^\d{1,3}$')
_RUNNING_HEADER_MIN_REPEATS = 3
_LINE_SPLIT_MIN_ENDS_IN_BLOCK = 3

_INITIALS_FIRST_AUTHORS_RE = re.compile(
    r"^((?:[A-Z][A-Za-z]?\.(?:\s?[A-Z]\.)*(?:-[A-Z][a-z]?\.)?\s+[^\W\d_][\w'\u2019\-]+"
    r"(?:,\s+and\s+|,\s+|\s+and\s+|\s+&\s+)?)+)(?:et al\.)?",
)
_INITIALS_SURNAME_RE = re.compile(
    r"[A-Z][A-Za-z]?\.(?:\s?[A-Z]\.)*(?:-[A-Z][a-z]?\.)?\s+([^\W\d_][\w'\u2019\-]+)"
)


def _split_line_entries(section: str) -> list[str]:
    raw_lines = [ln.strip() for ln in section.splitlines()]
    counts: dict[str, int] = {}
    for ln in raw_lines:
        if len(ln) > 10:
            counts[ln] = counts.get(ln, 0) + 1
    entries: list[str] = []
    current: list[str] = []
    for ln in raw_lines:
        if not ln or _PAGE_NUMBER_LINE_RE.match(ln) or counts.get(ln, 0) >= _RUNNING_HEADER_MIN_REPEATS:
            continue
        current.append(ln)
        if _ENTRY_END_RE.search(ln):
            entries.append(" ".join(current))
            current = []
    if current:
        entries.append(" ".join(current))
    return entries


def _authors_of(block: str, *, initials_first: bool = False) -> list[str]:
    author_match = _AUTHOR_LIST_RE.match(block)
    if author_match:
        return _LASTNAME_RE.findall(author_match.group(1))
    if initials_first:
        initials_match = _INITIALS_FIRST_AUTHORS_RE.match(block)
        if initials_match:
            return _INITIALS_SURNAME_RE.findall(initials_match.group(1))
    return []


def _entry_from_block(block: str, *, reading_order: bool = False) -> CitationEntry:
    """`reading_order` is True only for entries recovered by the line-end
    heuristic (reading-order PDF text), where the initials-first author
    shape and a bare trailing year are the norm. Entries from blank-line
    blocks keep the stricter, original behaviour: a field that does not
    match the expected shape comes back as `None`/`[]`, never guessed."""
    year_match = _YEAR_RE.search(block)
    if year_match is None and reading_order:
        year_match = re.search(r'\b((?:19|20)\d{2})[a-z]?\b(?!.*\b(?:19|20)\d{2}\b)', block)
    url_match = _URL_RE.search(block)
    url = url_match.group(0).rstrip('.,)') if url_match else None
    return CitationEntry(
        raw=block, authors=_authors_of(block, initials_first=reading_order),
        year=year_match.group(1) if year_match else None,
        url=url, venue_type=_classify_venue(block, url),
    )


@dataclass
class ReferenceParse:
    """What the reference parser did, so a zero or a null downstream is
    never mistaken for a finding. `mode` is "blank_line" (entries
    separated by blank lines), "line_heuristic" (entries split by the
    year/URL line-end heuristic) or `None` (nothing parsed)."""
    section_found: bool
    n_entries: int
    mode: str | None
    warning: str | None

    def to_dict(self) -> dict:
        return {"section_found": self.section_found, "n_entries": self.n_entries,
                "mode": self.mode, "warning": self.warning}


def parse_references_detailed(text: str, *, min_word_count: int = 400) -> tuple[list[CitationEntry], ReferenceParse]:
    """Like `parse_references`, plus a `ReferenceParse` saying how the
    entries were obtained and whether the result should be trusted.
    `min_word_count` only decides whether a missing section is worth a
    warning (a short note is not expected to have a bibliography)."""
    section = extract_references_section(text)
    long_enough = len(text.split()) >= min_word_count
    if section is None:
        warning = ("no references section found: self-citation ratio and venue mix are unavailable, "
                   "not zero") if long_enough else None
        return [], ReferenceParse(section_found=False, n_entries=0, mode=None, warning=warning)

    blocks = [b.strip() for b in re.split(r'\n\s*\n', section.strip()) if b.strip()]
    mode = "blank_line"
    # Reading-order text: blocks are page-sized chunks (blank lines fall at
    # page breaks, not between entries), so several entry-ending lines sit
    # inside one block. In a normal blank-line-separated list each block is
    # one entry and holds about one such line.
    max_ends_in_block = max((sum(1 for ln in b.splitlines() if _ENTRY_END_RE.search(ln.strip()))
                             for b in blocks), default=0)
    if max_ends_in_block >= _LINE_SPLIT_MIN_ENDS_IN_BLOCK:
        line_blocks = _split_line_entries(section)
        if len(line_blocks) > len(blocks):
            blocks, mode = line_blocks, "line_heuristic"
    entries = [_entry_from_block(b, reading_order=(mode == "line_heuristic")) for b in blocks]
    if not entries:
        return [], ReferenceParse(section_found=True, n_entries=0, mode=None,
                                  warning="a references section was found but no entries could be parsed: "
                                          "self-citation ratio and venue mix are unavailable, not zero")
    warning = None
    if mode == "line_heuristic":
        warning = ("references were split by a line-end heuristic (no blank lines between entries): "
                   "counts and author fields are approximate")
    return entries, ReferenceParse(section_found=True, n_entries=len(entries), mode=mode, warning=warning)


def parse_references(text: str) -> list[CitationEntry]:
    """Best-effort. Returns `[]` if no references section is found --
    that is itself a reportable fact (see `scan.py` and
    `parse_references_detailed`), not an error."""
    return parse_references_detailed(text)[0]


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


@dataclass
class CitabilityClaimCheck:
    claims_citability: bool
    matched_phrases: list[str]
    n_references: int
    word_count: int
    applicable: bool

    @property
    def gap(self) -> bool:
        """A long paper that asserts its own grounding in citable/
        documented research while its own References section (or lack
        of one) parses to zero entries -- the paper's own citability
        claim and its own bibliography contradict each other, fully
        resolvable from the text alone, no external lookup needed to
        know it's contradictory (whether the claim is otherwise TRUE
        is a separate question this cannot answer)."""
        return self.applicable and self.claims_citability and self.n_references == 0

    def to_dict(self) -> dict:
        return {"claims_citability": self.claims_citability, "matched_phrases": self.matched_phrases,
                "n_references": self.n_references, "word_count": self.word_count,
                "applicable": self.applicable, "gap": self.gap}


def check_citability_claim(text: str, references: list[CitationEntry], *, min_word_count: int = 400) -> CitabilityClaimCheck:
    """Found via a real specimen (86KB, ~12,000 words, zero actual
    references, structured as a raw page-scan dump with no References
    heading at all) that asserted "the reference to base papers on
    Zenodo under Stephen Hope's authorship indicate the framework's
    grounding in documented, citable research" -- a citability claim
    about the document's OWN sourcing, contradicted by its own empty
    bibliography. `min_word_count` reuses the same "long enough that a
    real bibliography would be expected" judgment call as
    `disclaimer.py`'s limitations-section threshold, not a value taken
    from any style guide."""
    word_count = len(text.split())
    matches = [m.group(0) for m in _CITABILITY_CLAIM_RE.finditer(text)]
    return CitabilityClaimCheck(
        claims_citability=bool(matches),
        matched_phrases=sorted(set(matches)),
        n_references=len(references),
        word_count=word_count,
        applicable=word_count >= min_word_count,
    )
