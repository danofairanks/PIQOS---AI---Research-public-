import pytest

from case_scaffold.index import insert_row, parse_index_rows, render_index_row

SAMPLE_README = """# Case Studies

## Index

| Date | Specimen | Framework applied | Summary |
|---|---|---|---|
| 2026-07-27 | [`2026-07-27_a.md`](2026-07-27_a.md) | Attractor 1 | First summary. |
| 2026-08-01 | [`2026-08-01_b.md`](2026-08-01_b.md) | Attractor 2 | Second summary. |

Update this index in the same commit that adds a case study.
"""


def test_parse_index_rows_finds_all_dated_rows():
    rows = parse_index_rows(SAMPLE_README)
    assert [r.date for r in rows] == ["2026-07-27", "2026-08-01"]


def test_render_index_row_format():
    row = render_index_row("2026-08-08", "2026-08-08_c.md", "Attractor 3", "Third summary.")
    assert row == "| 2026-08-08 | [`2026-08-08_c.md`](2026-08-08_c.md) | Attractor 3 | Third summary. |"


def test_render_index_row_escapes_pipes():
    row = render_index_row("2026-08-08", "x.md", "A | B", "Summary with | pipe")
    assert "\\|" in row


def test_insert_row_appends_when_latest_date():
    row = render_index_row("2026-08-08", "2026-08-08_c.md", "Attractor 3", "Third summary.")
    updated = insert_row(SAMPLE_README, row, "2026-08-08")
    rows = parse_index_rows(updated)
    assert [r.date for r in rows] == ["2026-07-27", "2026-08-01", "2026-08-08"]


def test_insert_row_in_the_middle_by_date():
    row = render_index_row("2026-07-29", "2026-07-29_mid.md", "Attractor X", "Middle summary.")
    updated = insert_row(SAMPLE_README, row, "2026-07-29")
    rows = parse_index_rows(updated)
    assert [r.date for r in rows] == ["2026-07-27", "2026-07-29", "2026-08-01"]


def test_insert_row_before_anchor_line():
    row = render_index_row("2026-08-08", "2026-08-08_c.md", "Attractor 3", "Third summary.")
    updated = insert_row(SAMPLE_README, row, "2026-08-08")
    lines = updated.splitlines()
    anchor_idx = next(i for i, l in enumerate(lines) if "Update this index" in l)
    row_idx = next(i for i, l in enumerate(lines) if "2026-08-08_c.md" in l)
    assert row_idx < anchor_idx


def test_insert_row_raises_without_anchor_line():
    with pytest.raises(ValueError):
        insert_row("no anchor here", "| row |", "2026-08-08")


def test_insert_row_does_not_lose_existing_rows():
    row = render_index_row("2026-08-08", "2026-08-08_c.md", "Attractor 3", "Third summary.")
    updated = insert_row(SAMPLE_README, row, "2026-08-08")
    assert "2026-07-27_a.md" in updated
    assert "2026-08-01_b.md" in updated
