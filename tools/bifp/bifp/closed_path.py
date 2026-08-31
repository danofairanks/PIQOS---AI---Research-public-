"""Closed-path / open-path evidence ledger for governance artifacts.

Operationalizes the defeat condition stated in `papers/drafts/
closed_path_confirmation_v1.md` §2: a governance artifact's own,
author-authored test suite establishes only an existential claim over
paths the author controls (P_closed) -- there exists a set of
author-chosen inputs on which the rule holds -- not the universal claim
over all paths (P_open) that a binding claim actually requires. This
module gives that distinction a structured, persistent record (mirroring
`audit.AuditSession`'s JSON-file pattern) and a text-heuristic lead
generator for prose that describes an artifact's evidence, following
`heuristics.py`'s existing contract exactly: every function here returns
matches or counts for a human or agent to read, never a verdict on
whether any artifact actually binds.

Generic by construction: nothing in this module or its tests refers to
any named project, repository, organization, or individual. Callers
supply their own free-text labels for whatever they are recording.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

#: The three recognized values for a fixture's outcome-derivation kind.
#: "asserted": the expected outcome is a literal constant chosen to
#:   match the artifact's own output on that input -- closed-path by
#:   the paper's §2 definition, regardless of how many such fixtures
#:   exist or how consistently they pass.
#: "derived": the expected outcome is computed from an independent
#:   specification of correct behavior, external to the artifact's own
#:   code -- open-path evidence.
#: "unknown": not yet classified -- the honest default, distinct from
#:   asserting either of the other two without having actually read
#:   the fixture.
DERIVATION_KINDS = ("asserted", "derived", "unknown")


@dataclass
class FixtureRecord:
    fixture_id: str
    outcome_derivation: str = "unknown"
    notes: str = ""

    def __post_init__(self) -> None:
        if self.outcome_derivation not in DERIVATION_KINDS:
            raise ValueError(
                f"outcome_derivation must be one of {DERIVATION_KINDS}, "
                f"got {self.outcome_derivation!r}"
            )

    def to_dict(self) -> dict:
        return {
            "fixture_id": self.fixture_id,
            "outcome_derivation": self.outcome_derivation,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FixtureRecord":
        return cls(
            fixture_id=d["fixture_id"],
            outcome_derivation=d.get("outcome_derivation", "unknown"),
            notes=d.get("notes", ""),
        )


@dataclass
class ClosedPathLedger:
    """A record of one artifact's fixture-by-fixture evidence
    classification. `artifact_label` is a free-text field the caller
    controls entirely -- this module never inspects, validates, or
    stores anything beyond what is explicitly passed in, so redaction
    (or not) is the caller's decision, not this tool's.
    """

    artifact_label: str
    fixtures: list[FixtureRecord] = field(default_factory=list)

    def add_fixture(self, fixture_id: str, outcome_derivation: str, *, notes: str = "") -> None:
        """Add or replace a fixture record (matching `fixture_id`
        replaces the prior record, so re-classifying a fixture on a
        second read doesn't create a duplicate)."""
        record = FixtureRecord(fixture_id=fixture_id, outcome_derivation=outcome_derivation, notes=notes)
        self.fixtures = [f for f in self.fixtures if f.fixture_id != fixture_id] + [record]

    def _count(self, kind: str) -> int:
        return sum(1 for f in self.fixtures if f.outcome_derivation == kind)

    @property
    def asserted_count(self) -> int:
        return self._count("asserted")

    @property
    def derived_count(self) -> int:
        return self._count("derived")

    @property
    def unknown_count(self) -> int:
        return self._count("unknown")

    @property
    def classified_count(self) -> int:
        """Fixtures actually read and classified as asserted or
        derived -- excludes "unknown", since an unread fixture is not
        evidence either way."""
        return self.asserted_count + self.derived_count

    @property
    def closed_path_ratio(self) -> float | None:
        """asserted / (asserted + derived), among fixtures actually
        classified. None if nothing has been classified yet -- a ratio
        of 0.0 (all derived) is a real, meaningful result and must not
        be confused with "not yet checked" (None)."""
        if self.classified_count == 0:
            return None
        return self.asserted_count / self.classified_count

    @property
    def flagged_fixture_ids(self) -> list[str]:
        """IDs of fixtures classified "asserted" -- a lead for review,
        not a claim that any of them is individually wrong; see
        closed_path_confirmation_v1.md §4 for how this project reads a
        classified-asserted fixture."""
        return [f.fixture_id for f in self.fixtures if f.outcome_derivation == "asserted"]

    def to_dict(self) -> dict:
        return {
            "artifact_label": self.artifact_label,
            "fixtures": [f.to_dict() for f in self.fixtures],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "ClosedPathLedger":
        return cls(
            artifact_label=d["artifact_label"],
            fixtures=[FixtureRecord.from_dict(f) for f in d.get("fixtures", [])],
        )

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "ClosedPathLedger":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


# --- Text heuristic: closed-path / open-path language in prose -----------
#
# A much coarser, recall-oriented lead generator for a README, paper, or
# report's own prose -- distinct from the FixtureRecord ledger above,
# which requires someone to have actually read the fixtures. This scans
# only for the *language an artifact uses to describe its own evidence*,
# not the evidence itself. A document that uses open-path language is
# not thereby proven to have open-path evidence, and a document with no
# matches either way is simply unclassified by this heuristic, not
# closed-path by default.

_CLOSED_PATH_PHRASES = [
    "in-process fixture", "in-memory", "self-authored", "author's own oracle",
    "authored by the repo owner", "closed loop", "closed-loop", "internal consistency",
    "tests pass by construction", "the tests were designed to pass",
]

_OPEN_PATH_PHRASES = [
    "independent red team", "independently reproduced", "third-party audit",
    "external reviewer", "adversarial party", "external contact",
    "cloned directly and", "independently cloned", "real-world deployment",
    "external optimizing policy", "counter-policy",
]


@dataclass
class LanguageMatch:
    pattern: str
    matched_text: str
    start: int
    end: int

    def to_dict(self) -> dict:
        return {"pattern": self.pattern, "text": self.matched_text, "start": self.start, "end": self.end}


@dataclass
class ClosedPathLanguageResult:
    closed_path_signals: list[LanguageMatch] = field(default_factory=list)
    open_path_signals: list[LanguageMatch] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "closed_path_signals": [m.to_dict() for m in self.closed_path_signals],
            "open_path_signals": [m.to_dict() for m in self.open_path_signals],
            "note": (
                "Lexical signal density in prose, not a fixture-level check -- "
                "see ClosedPathLedger for that. A document mentioning open-path "
                "language is not thereby shown to have open-path evidence, and "
                "a document with neither signal type is unclassified by this "
                "heuristic, not closed-path by default. Read every matched span "
                "directly; this is a lead, not a verdict."
            ),
        }


def _find_phrases(text: str, phrases: list[str]) -> list[LanguageMatch]:
    lowered = text.lower()
    matches = []
    for phrase in phrases:
        start = 0
        while True:
            idx = lowered.find(phrase, start)
            if idx == -1:
                break
            matches.append(LanguageMatch(phrase, text[idx:idx + len(phrase)], idx, idx + len(phrase)))
            start = idx + len(phrase)
    return matches


def scan_for_closed_path_language(text: str) -> ClosedPathLanguageResult:
    """Scan prose for language describing an artifact's own test
    evidence as closed-path or open-path. Purely lexical -- see
    module docstring and `ClosedPathLanguageResult.to_dict`'s "note"
    for what this does not establish."""
    return ClosedPathLanguageResult(
        closed_path_signals=_find_phrases(text, _CLOSED_PATH_PHRASES),
        open_path_signals=_find_phrases(text, _OPEN_PATH_PHRASES),
    )


_ASSERT_LITERAL_RE = re.compile(
    r"\bassert\w*\s*\(?\s*[\w.\[\]]+\s*==\s*"
    r"(?:true|false|-?\d+(?:\.\d+)?|\"[^\"]*\"|'[^']*')",
    re.IGNORECASE,
)


def scan_for_hardcoded_assertion_style(text: str) -> list[LanguageMatch]:
    """A narrow, generic code-shaped lexical check: flags assertion
    statements comparing directly against a literal (a boolean, a bare
    number, or a quoted string) rather than against a named variable or
    function call -- a *weak*, purely syntactic lead for "this fixture's
    expected value may be a hand-set constant rather than a derived
    computation" (closed_path_confirmation_v1.md §2's fixture-level
    check). This cannot distinguish a genuinely hardcoded expectation
    from a legitimate literal (many correct assertions compare against
    a real constant, e.g. `assert count == 3` when 3 is independently
    specified) -- read every match directly."""
    return [LanguageMatch("hardcoded_literal_assertion", m.group(0), m.start(), m.end())
            for m in _ASSERT_LITERAL_RE.finditer(text)]
