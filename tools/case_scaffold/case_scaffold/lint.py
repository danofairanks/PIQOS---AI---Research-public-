"""Structural validation of a case-study file against the house format
shared by every existing file in case_studies/. Two severities:

- **errors** — structural rules every real file in this repo already
  satisfies (verified directly against all 13 of them in this
  package's own test suite, not assumed). A file failing these isn't
  in house format, full stop.
- **warnings** — signals that something needs attention before
  publishing (a leftover TODO marker) without being a structural
  defect. A freshly-generated scaffold is expected to warn; it should
  never error.

`strict=True` promotes warnings to errors -- use it as the "ready to
publish" gate.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .template import TODO_MARK

_TITLE_RE = re.compile(r"^# Real-Time Specimen Analysis: .+$")
_SUBTITLE_RE = re.compile(r"^### .+$")
_H2_RE = re.compile(r"^## (.+)$")
_CLOSING_LINE_RE = re.compile(r"^\*.*Applies the framework from.*\*$")
_MD_LINK_RE = re.compile(r"\]\(([^)]+\.md)\)")


@dataclass
class LintResult:
    path: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict:
        return {"path": self.path, "ok": self.ok, "errors": self.errors, "warnings": self.warnings}


def lint_text(text: str, *, path: str = "<text>", strict: bool = False, base_dir: str | Path | None = None) -> LintResult:
    result = LintResult(path=path)
    lines = text.splitlines()
    non_empty = [l for l in lines if l.strip()]

    if not non_empty or not _TITLE_RE.match(non_empty[0]):
        result.errors.append(
            'First non-blank line must match "# Real-Time Specimen Analysis: <title>".'
        )

    if len(non_empty) < 2 or not _SUBTITLE_RE.match(non_empty[1]):
        result.errors.append(
            "Second non-blank line must be a ### subtitle naming the specific mechanism demonstrated."
        )

    h2_titles = [m.group(1) for l in lines if (m := _H2_RE.match(l))]
    if "Executive Summary" not in h2_titles:
        result.errors.append('Missing required section: "## Executive Summary".')
    if "What This Case Study Does Not Claim" not in h2_titles:
        result.errors.append('Missing required section: "## What This Case Study Does Not Claim".')
    if len(h2_titles) < 3:
        result.errors.append(
            "Expected at least one body section between Executive Summary and "
            "What This Case Study Does Not Claim; found none."
        )

    if "---" not in [l.strip() for l in lines]:
        result.errors.append("Missing at least one `---` section separator.")

    if not non_empty or not _CLOSING_LINE_RE.match(non_empty[-1]):
        result.errors.append(
            'Last non-blank line must be an italicized line containing '
            '"Applies the framework from" and a markdown link to the paper it applies.'
        )
    elif base_dir is not None:
        for link_path in _MD_LINK_RE.findall(non_empty[-1]):
            resolved = (Path(base_dir) / link_path).resolve()
            if not resolved.is_file():
                result.warnings.append(f"Closing-line framework link does not resolve to a file: {link_path}")

    todo_count = text.count(TODO_MARK)
    if todo_count:
        msg = f"Contains {todo_count} unresolved TODO marker(s); not ready to publish."
        (result.errors if strict else result.warnings).append(msg)

    return result


def lint_file(path: str | Path, *, strict: bool = False, base_dir: str | Path | None = None) -> LintResult:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if base_dir is None:
        base_dir = path.parent
    return lint_text(text, path=str(path), strict=strict, base_dir=base_dir)
