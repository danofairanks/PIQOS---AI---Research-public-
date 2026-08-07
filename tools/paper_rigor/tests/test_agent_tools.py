import json

from paper_rigor.agent_tools import paper_rigor_scan


def test_scan_is_json_safe_and_has_expected_shape():
    result = paper_rigor_scan("Some clean prose with no issues at all here.")
    json.dumps(result)  # must not raise
    assert "ok" in result
    assert "structural_gap_count" in result
    assert "external_verification_worklist" in result


def test_scan_with_byline_authors_computes_self_citation():
    text = "## References\n\nSmith, J. (2020). Prior work. arxiv.org/abs/1234\n"
    result = paper_rigor_scan(text, byline_authors=["Smith"])
    assert result["self_citation"]["ratio"] == 1.0


def test_scan_without_byline_authors_self_citation_ratio_is_null():
    text = "## References\n\nSmith, J. (2020). Prior work. arxiv.org/abs/1234\n"
    result = paper_rigor_scan(text)
    assert result["self_citation"]["ratio"] is None


def test_scan_flags_constructed_bad_paper():
    bad = "It is trivial to show this. TODO: fill in proof. " + (" filler word" * 400)
    result = paper_rigor_scan(bad)
    assert result["ok"] is False
    assert result["structural_gap_count"] >= 1
