import json

from paper_rigor.agent_tools import paper_rigor_scan, paper_rigor_triage_worklist


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


def test_triage_worklist_missing_key_returns_error_dict_not_exception(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    worklist = [{"kind": "uncited_empirical_claim", "item": "x", "context": "c", "reason": "r"}]
    result = paper_rigor_triage_worklist(worklist)
    assert "error" in result
    assert "GROQ_API_KEY" in result["error"]


def test_triage_worklist_empty_is_json_safe_no_key_needed(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    result = paper_rigor_triage_worklist([])
    json.dumps(result)  # must not raise
    assert result["items"] == []


def test_triage_worklist_end_to_end_with_real_scan_output(monkeypatch):
    """Confirms the two functions actually compose: a real scan's
    worklist shape feeds cleanly into triage."""
    bad = ("As a renowned expert with over 30 years of experience, research shows "
           "this outperforms all baselines.") + (" filler word" * 400)
    scan_result = paper_rigor_scan(bad)
    worklist = scan_result["external_verification_worklist"]
    assert len(worklist) >= 1

    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "paper_rigor.worklist_triage._call_groq_api",
        lambda payload, api_key: {
            "choices": [{"message": {"content": json.dumps({
                "triaged": [
                    {"index": i, "priority": "medium", "suggested_check": "check it"}
                    for i in range(len(worklist))
                ]
            })}}]
        },
    )
    result = paper_rigor_triage_worklist(worklist)
    json.dumps(result)  # must not raise
    assert len(result["items"]) == len(worklist)
