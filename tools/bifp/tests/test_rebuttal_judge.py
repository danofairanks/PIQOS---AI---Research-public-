import json

import pytest

from bifp.rebuttal_judge import (
    DEFAULT_MODEL,
    RebuttalJudgeError,
    RebuttalJudgeResult,
    judge_rebuttal,
)


def _groq_response(content_obj: dict) -> dict:
    """Shape a fake Groq chat-completions response body."""
    return {"choices": [{"message": {"content": json.dumps(content_obj)}}]}


def test_missing_api_key_raises_clear_error(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(RebuttalJudgeError, match="GROQ_API_KEY"):
        judge_rebuttal("claim", "rebuttal")


def test_api_key_from_env_is_used(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key-from-env")
    seen = {}

    def fake_call(payload, api_key):
        seen["api_key"] = api_key
        seen["payload"] = payload
        return _groq_response({
            "candidate_read": "addresses_actual_claim",
            "reasoning": "matches scope",
            "weakened_restatement_quote": None,
            "self_reported_confidence": "high",
        })

    monkeypatch.setattr("bifp.rebuttal_judge._call_groq_api", fake_call)
    result = judge_rebuttal("claim text", "rebuttal text")
    assert seen["api_key"] == "test-key-from-env"
    assert seen["payload"]["model"] == DEFAULT_MODEL
    assert "claim text" in seen["payload"]["messages"][1]["content"]
    assert result.candidate_read == "addresses_actual_claim"
    assert result.flagged is False


def test_explicit_api_key_overrides_env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "env-key")
    seen = {}

    def fake_call(payload, api_key):
        seen["api_key"] = api_key
        return _groq_response({
            "candidate_read": "unclear", "reasoning": "", "weakened_restatement_quote": None,
            "self_reported_confidence": "low",
        })

    monkeypatch.setattr("bifp.rebuttal_judge._call_groq_api", fake_call)
    judge_rebuttal("c", "r", api_key="explicit-key")
    assert seen["api_key"] == "explicit-key"


def test_weaker_substitute_read_is_flagged(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "bifp.rebuttal_judge._call_groq_api",
        lambda payload, api_key: _groq_response({
            "candidate_read": "weaker_substitute",
            "reasoning": "rebuttal targets a narrower claim",
            "weakened_restatement_quote": "some easier claim",
            "self_reported_confidence": "medium",
        }),
    )
    result = judge_rebuttal("the strong original claim", "a rebuttal of something easier")
    assert result.flagged is True
    assert result.weakened_restatement_quote == "some easier claim"


def test_result_to_dict_is_json_safe_and_carries_disclaimer(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "bifp.rebuttal_judge._call_groq_api",
        lambda payload, api_key: _groq_response({
            "candidate_read": "unclear", "reasoning": "ambiguous target",
            "weakened_restatement_quote": None, "self_reported_confidence": "low",
        }),
    )
    result = judge_rebuttal("c", "r")
    d = result.to_dict()
    json.dumps(d)  # must not raise
    assert d["source"] == "ai_advisory"
    assert d["phase"] == 5
    assert d["criterion_key"] == "no_weaker_substitute_rebuttal"
    assert "no_ai_as_judge" in d["disclaimer"]
    assert "record()" in d["disclaimer"]


def test_unrecognized_candidate_read_raises(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "bifp.rebuttal_judge._call_groq_api",
        lambda payload, api_key: _groq_response({
            "candidate_read": "definitely_true",  # not a valid value
            "reasoning": "", "weakened_restatement_quote": None, "self_reported_confidence": "high",
        }),
    )
    with pytest.raises(RebuttalJudgeError, match="unrecognized candidate_read"):
        judge_rebuttal("c", "r")


def test_malformed_response_raises_clear_error(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "bifp.rebuttal_judge._call_groq_api",
        lambda payload, api_key: {"choices": []},  # missing expected shape
    )
    with pytest.raises(RebuttalJudgeError, match="Could not parse"):
        judge_rebuttal("c", "r")


def test_non_json_content_raises_clear_error(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(
        "bifp.rebuttal_judge._call_groq_api",
        lambda payload, api_key: {"choices": [{"message": {"content": "not json"}}]},
    )
    with pytest.raises(RebuttalJudgeError, match="Could not parse"):
        judge_rebuttal("c", "r")


def test_custom_model_is_passed_through(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    seen = {}

    def fake_call(payload, api_key):
        seen["model"] = payload["model"]
        return _groq_response({
            "candidate_read": "unclear", "reasoning": "", "weakened_restatement_quote": None,
            "self_reported_confidence": "low",
        })

    monkeypatch.setattr("bifp.rebuttal_judge._call_groq_api", fake_call)
    result = judge_rebuttal("c", "r", model="llama-3.1-8b-instant")
    assert seen["model"] == "llama-3.1-8b-instant"
    assert result.model == "llama-3.1-8b-instant"


def test_result_is_a_dataclass_with_expected_fields():
    result = RebuttalJudgeResult(
        claim_text="c", rebuttal_text="r", candidate_read="addresses_actual_claim",
        reasoning="ok", weakened_restatement_quote=None, self_reported_confidence="high",
        model=DEFAULT_MODEL,
    )
    assert result.flagged is False
    assert result.disclaimer  # non-empty default
