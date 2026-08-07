"""Detect whether a document has a blanket end-of-document sourcing
statement, this project's own actual citation convention.

Checked directly against this repo's own case_studies/ files: they do
not cite a source next to every number in the body text. They state
the finding, then close with one italic line naming every source
inspected ("Sources: X post..., OpenAI's own blog post..."). A
per-claim proximity scanner (quotes.py, statistics.py) would read every
one of those documents as riddled with unsourced claims, which is a
wrong conclusion about a document that is, in fact, sourced -- just
sourced in aggregate rather than inline. This module names that
convention explicitly so the rest of the tool's output can be read
correctly: "no proximate citation" is not the same claim as "uncited,"
and a document with end-sourcing should have its per-item findings
read as a checklist to verify against that source list, not as a
verdict that the document cites nothing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_SOURCES_LINE_RE = re.compile(r'\bsources?:\s', re.IGNORECASE)
_APPLIES_FRAMEWORK_RE = re.compile(r'applies the framework from', re.IGNORECASE)


@dataclass
class SourcingCheck:
    has_sources_statement: bool
    has_framework_citation: bool

    @property
    def has_end_sourcing(self) -> bool:
        return self.has_sources_statement or self.has_framework_citation

    def to_dict(self) -> dict:
        return {
            "has_sources_statement": self.has_sources_statement,
            "has_framework_citation": self.has_framework_citation,
            "has_end_sourcing": self.has_end_sourcing,
        }


def check_sourcing(text: str) -> SourcingCheck:
    return SourcingCheck(
        has_sources_statement=bool(_SOURCES_LINE_RE.search(text)),
        has_framework_citation=bool(_APPLIES_FRAMEWORK_RE.search(text)),
    )
