"""Parse and update case_studies/README.md's index table.

The table's own format (verified directly against the real file, not
assumed): a `| Date | Specimen | Framework applied | Summary |` header,
a separator row, one row per case study in date order, ending right
before the line "Update this index in the same commit that adds a
case study."
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_ANCHOR_LINE = "Update this index in the same commit that adds a case study."
_ROW_RE = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|")


@dataclass
class IndexRow:
    date: str
    raw: str  # the full markdown table row


def parse_index_rows(readme_text: str) -> list[IndexRow]:
    rows = []
    for line in readme_text.splitlines():
        m = _ROW_RE.match(line)
        if m:
            rows.append(IndexRow(date=m.group(1), raw=line))
    return rows


def render_index_row(date: str, filename: str, framework_applied: str, summary: str) -> str:
    link = f"[`{filename}`]({filename})"
    # pipe characters inside cell content would break the table; escape defensively
    framework_applied = framework_applied.replace("|", "\\|")
    summary = summary.replace("|", "\\|")
    return f"| {date} | {link} | {framework_applied} | {summary} |"


def insert_row(readme_text: str, new_row: str, date: str) -> str:
    """Insert `new_row` into the index table in date order (matching
    the file's existing ascending-date convention), immediately before
    the anchor line. Raises ValueError if the anchor line isn't found
    -- fail loudly rather than silently appending somewhere wrong."""
    if _ANCHOR_LINE not in readme_text:
        raise ValueError(f"could not find anchor line {_ANCHOR_LINE!r} in README text")

    lines = readme_text.splitlines()
    rows = parse_index_rows(readme_text)
    later_rows = [r for r in rows if r.date > date]

    anchor_idx = next(i for i, l in enumerate(lines) if _ANCHOR_LINE in l)

    if later_rows:
        # insert immediately before the first row whose date is later than the new one
        insert_before_raw = later_rows[0].raw
        insert_idx = next(i for i, l in enumerate(lines) if l == insert_before_raw)
        lines.insert(insert_idx, new_row)
    else:
        # append after the last existing row, before the anchor (skipping blank lines)
        idx = anchor_idx - 1
        while idx > 0 and not lines[idx].strip():
            idx -= 1
        lines.insert(idx + 1, new_row)

    return "\n".join(lines)
