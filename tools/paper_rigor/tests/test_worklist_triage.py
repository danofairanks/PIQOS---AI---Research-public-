import json
import urllib.request
from io import BytesIO

import pytest

from paper_rigor.worklist_triage import (
    DEFAULT_MODEL,
    TriagedWorklistItem,
    WorklistTriageError,
    WorklistTriageResult,
    _call_groq_api,
    triage_worklist,
)

SAMPLE_WORKLIST = [
    {"kind": "uncited_empirical_claim", "item": "Research shows the model outperforms all baselines",
     "context": "...", "reason": "empirical-certainty language with no citation nearby"},
    {"kind": "credential_substitution", "item": "As a renowned expert with over 30 years of experience",
     "context": "...", "reason": "claim supported only by an appeal to credentials"},
]


def _groq_triage_response(entries: list[dict]) -> dict:
    return {"choices": [{"message": {"content": json.dumps({"triaged": entries})}}]}


def test_empty_worklist_returns_immediately_no_api_call(monkeypatch):
    """No GROQ_API_KEY set at all -- if this made a call it would raise."""
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    result = triage_worklist([])
    assert result.items == []
    json.dumps(result.to_dict())  # must not raise


def test_missing_api_key_raises_clear_error(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(WorklistTriageError, match="GROQ_API_KEY"):
        triage_worklist(SAMPLE_WORKLIST)


def test_successful_triage_merges_by_index(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "paper_rigor.worklist_triage._call_groq_api",
        lambda payload, api_key: _groq_triage_response([
            {"index": 0, "priority": "high", "suggested_check": "find the cited benchmark table"},
            {"index": 1, "priority": "low", "suggested_check": "check if credentials are named anywhere"},
        ]),
    )
    result = triage_worklist(SAMPLE_WORKLIST)
    assert len(result.items) == 2
    assert result.items[0].priority == "high"
    assert result.items[0].kind == "uncited_empirical_claim"  # original field preserved
    assert result.items[1].priority == "low"
    assert result.high_priority_items == [result.items[0]]


def test_never_invents_or_drops_items_count_mismatch_raises(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "paper_rigor.worklist_triage._call_groq_api",
        lambda payload, api_key: _groq_triage_response([
            {"index": 0, "priority": "high", "suggested_check": "x"},
        ]),  # only 1 entry for 2 input items
    )
    with pytest.raises(WorklistTriageError, match="refusing to guess"):
        triage_worklist(SAMPLE_WORKLIST)


def test_mismatched_indices_raises(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "paper_rigor.worklist_triage._call_groq_api",
        lambda payload, api_key: _groq_triage_response([
            {"index": 0, "priority": "high", "suggested_check": "x"},
            {"index": 5, "priority": "low", "suggested_check": "y"},  # index 5 doesn't exist
        ]),
    )
    with pytest.raises(WorklistTriageError, match="don't match the input indices"):
        triage_worklist(SAMPLE_WORKLIST)


def test_unrecognized_priority_raises(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "paper_rigor.worklist_triage._call_groq_api",
        lambda payload, api_key: _groq_triage_response([
            {"index": 0, "priority": "urgent!!", "suggested_check": "x"},
            {"index": 1, "priority": "low", "suggested_check": "y"},
        ]),
    )
    with pytest.raises(WorklistTriageError, match="unrecognized priority"):
        triage_worklist(SAMPLE_WORKLIST)


def test_malformed_response_raises_clear_error(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "paper_rigor.worklist_triage._call_groq_api",
        lambda payload, api_key: {"choices": []},
    )
    with pytest.raises(WorklistTriageError, match="Could not parse"):
        triage_worklist(SAMPLE_WORKLIST)


def test_missing_triaged_key_raises_clear_error(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "paper_rigor.worklist_triage._call_groq_api",
        lambda payload, api_key: {"choices": [{"message": {"content": json.dumps({"not_triaged": []})}}]},
    )
    with pytest.raises(WorklistTriageError, match="Could not parse"):
        triage_worklist(SAMPLE_WORKLIST)


def test_result_to_dict_is_json_safe_and_carries_disclaimer(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "paper_rigor.worklist_triage._call_groq_api",
        lambda payload, api_key: _groq_triage_response([
            {"index": 0, "priority": "medium", "suggested_check": "a"},
            {"index": 1, "priority": "medium", "suggested_check": "b"},
        ]),
    )
    result = triage_worklist(SAMPLE_WORKLIST)
    d = result.to_dict()
    json.dumps(d)  # must not raise
    assert d["source"] == "ai_advisory"
    assert "web access" in d["disclaimer"]
    assert d["high_priority_count"] == 0


def test_call_groq_api_sets_identifying_user_agent(monkeypatch):
    """Same regression class as the other two Groq-backed modules,
    applied proactively here from the start."""
    captured = {}

    class _FakeResponse(BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def fake_urlopen(request, timeout=None):
        captured["headers"] = dict(request.header_items())
        return _FakeResponse(json.dumps(_groq_triage_response([
            {"index": 0, "priority": "low", "suggested_check": "x"},
        ])).encode("utf-8"))

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    _call_groq_api({"model": DEFAULT_MODEL, "messages": []}, "test-key")

    user_agent = captured["headers"].get("User-agent", "")
    assert user_agent, "no User-Agent header was set at all"
    assert "python-urllib" not in user_agent.lower()
    assert "paper-rigor-worklist-triage" in user_agent


def test_result_is_a_dataclass_with_expected_fields():
    item = TriagedWorklistItem(
        kind="uncited_empirical_claim", item="x", context="c", reason="r",
        priority="high", suggested_check="check y",
    )
    result = WorklistTriageResult(items=[item], model=DEFAULT_MODEL)
    assert result.high_priority_items == [item]
    assert result.disclaimer
