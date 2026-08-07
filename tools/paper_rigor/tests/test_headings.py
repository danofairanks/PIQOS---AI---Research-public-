import re

from paper_rigor.headings import find_section, has_heading_matching, iter_headings

# Verbatim real headings from a PDF-extracted specimen used to
# validate this module -- see headings.py's own module docstring and
# README "A harness, not another patch".
REAL_PLAIN_HEADINGS_DOC = (
    "1. Introduction\n"
    "Some introductory prose that mentions 1. a first point and 2. a second point inline.\n\n"
    "5.2 Elite Cognitive Stress Test: Fifteen Faculties (60/60)\n"
    "Body text describing the stress test in detail across several sentences.\n\n"
    "7. Honest Limitations and Genuine Improvements\n"
    "One faculty that previously underperformed has been improved through a genuine upgrade.\n\n"
    "10. Conclusion\n"
    "We have presented an integrated architecture.\n"
)


def test_markdown_headings_detected():
    text = "# Title\n\n## Section One\n\nBody text.\n\n### Subsection\n\nMore text.\n"
    headings = iter_headings(text)
    assert [h.text for h in headings] == ["Title", "Section One", "Subsection"]
    assert [h.level for h in headings] == [1, 2, 3]


def test_plain_numbered_headings_detected_in_document_order():
    headings = iter_headings(REAL_PLAIN_HEADINGS_DOC)
    texts = [h.text for h in headings]
    assert texts == [
        "Introduction",
        "Elite Cognitive Stress Test: Fifteen Faculties (60/60)",
        "Honest Limitations and Genuine Improvements",
        "Conclusion",
    ]
    assert all(h.level is None for h in headings)


def test_plain_headings_do_not_false_positive_on_inline_numbered_references():
    """"1. a first point and 2. a second point inline" sits inside a
    body sentence, not on its own line -- must not be detected as two
    extra headings."""
    headings = iter_headings(REAL_PLAIN_HEADINGS_DOC)
    assert len(headings) == 4


def test_mixed_markdown_and_plain_document_both_detected():
    text = "# Real Markdown Title\n\nBody.\n\n7. A Plain Numbered Heading\n\nMore body.\n"
    headings = iter_headings(text)
    assert [h.text for h in headings] == ["Real Markdown Title", "A Plain Numbered Heading"]


def test_find_section_returns_body_up_to_next_heading():
    body = find_section(REAL_PLAIN_HEADINGS_DOC, re.compile(r"elite cognitive", re.IGNORECASE))
    assert body is not None
    assert "stress test in detail" in body
    assert "Honest Limitations" not in body  # stopped at the next heading


def test_find_section_returns_none_when_no_matching_heading():
    assert find_section(REAL_PLAIN_HEADINGS_DOC, re.compile(r"nonexistent section")) is None


def test_find_section_extra_stop_pattern():
    text = "## References\n\nSmith, J. (2020). A Paper.\n\n---\n\n*Not a reference.*"
    body = find_section(text, re.compile(r"^references$", re.IGNORECASE),
                         extra_stop=re.compile(r"^---\s*$", re.MULTILINE))
    assert "Smith" in body
    assert "Not a reference" not in body


def test_has_heading_matching_substring_not_full_phrase():
    """Regression test for the real specimen: a heading titled
    "Honest Limitations and Genuine Improvements" must match a search
    for "limitations" even though the heading text is not equal to
    any fixed limitations phrase."""
    assert has_heading_matching(REAL_PLAIN_HEADINGS_DOC, re.compile(r"\blimitations\b", re.IGNORECASE)) is True


def test_has_heading_matching_false_when_absent():
    assert has_heading_matching(REAL_PLAIN_HEADINGS_DOC, re.compile(r"\bmethodology\b", re.IGNORECASE)) is False


def test_to_dict_json_safe():
    import json
    headings = iter_headings("# A Heading\n\nBody.")
    json.dumps([h.to_dict() for h in headings])  # must not raise
