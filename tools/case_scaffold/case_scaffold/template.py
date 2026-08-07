"""Generate a new case-study markdown skeleton in this repository's
house format, derived directly from the structure shared by all 13
existing files in case_studies/ (verified in lint.py's own tests
against those real files, not just described here).

The generator does not fabricate content. Every place that needs real
research -- the specimen quote, what was checked, the sources list --
is left as a visible, greppable TODO marker rather than filled with
plausible-sounding placeholder prose. A file this tool produces is
meant to fail `case_scaffold.lint.lint_file(..., strict=True)` until a
human or agent has actually done the work; that is a feature, not a
rough edge to smooth over.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

TODO_MARK = "**TODO — replace before publishing:**"


@dataclass(frozen=True)
class FrameworkRef:
    """One paper/section this case study applies."""

    paper_path: str  # relative to case_studies/, e.g. "../papers/published/basin_attractors_v1.md"
    section: str = ""  # e.g. "§2.4"
    label: str = ""  # e.g. "Attractor 4 — Post-Hoc Governance"

    def as_markdown_link(self) -> str:
        name = self.paper_path.rsplit("/", 1)[-1]
        return f"[`{self.paper_path}`]({self.paper_path})"

    def as_closing_citation(self) -> str:
        link = self.as_markdown_link()
        tail = " ".join(x for x in [self.section, f"({self.label})" if self.label else ""] if x)
        return f"{link} {tail}".rstrip()


@dataclass
class CaseStudySpec:
    date: str  # "2026-08-08"
    slug: str  # "some_specimen_slug" -- lowercase, underscore-separated
    title: str  # H1 text after "Real-Time Specimen Analysis: "
    subtitle: str = ""  # H3 line; TODO placeholder if empty
    framework_refs: list[FrameworkRef] = field(default_factory=list)
    sources_note: str = ""  # filled into the closing line if provided, else a TODO
    section_titles: list[str] | None = None  # custom body section headers; default skeleton if None

    def __post_init__(self):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", self.date):
            raise ValueError(f"date must be YYYY-MM-DD, got {self.date!r}")
        if not re.fullmatch(r"[a-z0-9_]+", self.slug):
            raise ValueError(f"slug must be lowercase/digits/underscores only, got {self.slug!r}")


DEFAULT_SECTIONS = [
    "The Specimen: What Was Posted",
    "Checked Against Primary Sources",
]


def default_filename(spec: CaseStudySpec) -> str:
    return f"{spec.date}_{spec.slug}.md"


def _closing_line(spec: CaseStudySpec) -> str:
    sources = spec.sources_note or f"{TODO_MARK} list every source actually inspected, not just linked."
    if spec.framework_refs:
        refs = " and ".join(r.as_closing_citation() for r in spec.framework_refs)
        framework_clause = f"Applies the framework from {refs}."
    else:
        # Structurally this must still read as a citation line (the lint
        # check for "Applies the framework from" + a markdown link is a
        # STRUCTURAL requirement, not a completeness one) -- the TODO
        # marker flags it as unresolved without breaking that shape.
        framework_clause = (
            f"Applies the framework from {TODO_MARK} cite the specific paper(s) and "
            f"section(s) this case study applies, e.g. "
            f"[`../papers/published/basin_attractors_v1.md`](../papers/published/basin_attractors_v1.md) §N."
        )
    return f"*Specimen dated {spec.date}. Sources: {sources} {framework_clause}*"


def render_skeleton(spec: CaseStudySpec) -> str:
    sections = spec.section_titles if spec.section_titles is not None else DEFAULT_SECTIONS

    parts: list[str] = []
    parts.append(f"# Real-Time Specimen Analysis: {spec.title}")
    parts.append("")
    subtitle = spec.subtitle or (
        f"### {TODO_MARK} one sentence naming the specific mechanism this specimen "
        f"demonstrates, not a generic description of the topic"
    )
    parts.append(subtitle if subtitle.startswith("###") else f"### {subtitle}")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("## Executive Summary")
    parts.append("")
    parts.append(
        f"{TODO_MARK} 3-6 sentences. State what was posted/claimed, what checking it "
        f"against primary sources actually found, and the one specific finding that "
        f"makes this specimen worth logging -- not a restatement of the topic."
    )
    parts.append("")
    parts.append("---")
    parts.append("")

    for title in sections:
        parts.append(f"## {title}")
        parts.append("")
        parts.append(
            f"{TODO_MARK} quote the specimen verbatim where possible (exact text, "
            f"not paraphrase), name the source precisely (platform, account, date, "
            f"verified status), and state plainly what checking it against a primary "
            f"source found -- including if the check came back inconclusive."
        )
        parts.append("")

    parts.append("## What This Case Study Does Not Claim")
    parts.append("")
    parts.append(
        f"{TODO_MARK} at minimum, state what this does NOT establish about intent "
        f"(bad faith vs. ordinary error), what remains unverified or out of scope, "
        f"and any claim adjacent to this one that this specimen does not extend to."
    )
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append(_closing_line(spec))
    parts.append("")
    return "\n".join(parts)
