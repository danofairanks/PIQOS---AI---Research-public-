import base64
import json
import urllib.request
from io import BytesIO

import pytest

from attractor_scan.visual_proof_judge import (
    DEFAULT_MODEL,
    VisualProofJudgeError,
    VisualProofJudgeResult,
    _call_groq_api,
    judge_visual_proof,
)

# A real, minimal 1x1 transparent PNG -- valid image bytes, not a stub.
_TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def _groq_response(content_obj: dict) -> dict:
    return {"choices": [{"message": {"content": json.dumps(content_obj)}}]}


def test_missing_api_key_raises_clear_error(monkeypatch, tmp_path):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    with pytest.raises(VisualProofJudgeError, match="GROQ_API_KEY"):
        judge_visual_proof("claim", image_path=str(img))


def test_requires_exactly_one_image_source(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    with pytest.raises(VisualProofJudgeError, match="exactly one"):
        judge_visual_proof("claim")  # neither image_path nor image_bytes
    with pytest.raises(VisualProofJudgeError, match="exactly one"):
        judge_visual_proof("claim", image_path="a.png", image_bytes=_TINY_PNG, media_type="image/png")


def test_unreadable_image_path_raises_clear_error(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    with pytest.raises(VisualProofJudgeError, match="could not read image_path"):
        judge_visual_proof("claim", image_path="/nonexistent/path/x.png")


def test_image_bytes_without_media_type_raises(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    with pytest.raises(VisualProofJudgeError, match="media_type"):
        judge_visual_proof("claim", image_bytes=_TINY_PNG)


def test_image_path_with_unknown_suffix_requires_media_type(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    img = tmp_path / "x.bin"
    img.write_bytes(_TINY_PNG)
    with pytest.raises(VisualProofJudgeError, match="could not infer media type"):
        judge_visual_proof("claim", image_path=str(img))


def test_image_path_media_type_inferred_from_suffix(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    seen = {}

    def fake_call(payload, api_key):
        seen["payload"] = payload
        return _groq_response({
            "image_description": "a small image", "candidate_read": "unclear",
            "reasoning": "", "borrowed_term": None, "self_reported_confidence": "low",
        })

    monkeypatch.setattr("attractor_scan.visual_proof_judge._call_groq_api", fake_call)
    judge_visual_proof("claim", image_path=str(img))
    image_content = seen["payload"]["messages"][1]["content"][1]
    assert image_content["image_url"]["url"].startswith("data:image/png;base64,")


def test_payload_sets_explicit_max_completion_tokens_within_account_tpm_budget(monkeypatch, tmp_path):
    """Regression test for two live findings, both confirmed 2026-08-17:
    (1) HTTP 400 json_validate_failed with an empty failed_generation
    on the harder of two live specimens -- a reasoning-capable model
    can exhaust an unset default token budget on reasoning before
    emitting the JSON answer; (2) HTTP 413 rate_limit_exceeded when
    max_completion_tokens was set to the model's own advertised cap
    (16384) -- this account's on_demand tier has an 8000 TPM budget,
    and providers reserve max_completion_tokens against it up front.
    Pins that some explicit value is set (finding 1) while staying
    well under the account's real cap once image+prompt overhead is
    added (finding 2) -- 4096 leaves that headroom."""
    monkeypatch.setenv("GROQ_API_KEY", "k")
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    seen = {}

    def fake_call(payload, api_key):
        seen["payload"] = payload
        return _groq_response({
            "image_description": "x", "candidate_read": "unclear", "reasoning": "",
            "borrowed_term": None, "self_reported_confidence": "low",
        })

    monkeypatch.setattr("attractor_scan.visual_proof_judge._call_groq_api", fake_call)
    judge_visual_proof("claim", image_path=str(img))
    max_tokens = seen["payload"].get("max_completion_tokens", 0)
    assert 1024 <= max_tokens <= 6000


def test_image_bytes_path_used_directly(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    seen = {}

    def fake_call(payload, api_key):
        seen["payload"] = payload
        return _groq_response({
            "image_description": "a small image", "candidate_read": "unclear",
            "reasoning": "", "borrowed_term": None, "self_reported_confidence": "low",
        })

    monkeypatch.setattr("attractor_scan.visual_proof_judge._call_groq_api", fake_call)
    judge_visual_proof("claim", image_bytes=_TINY_PNG, media_type="image/png")
    image_content = seen["payload"]["messages"][1]["content"][1]
    assert image_content["image_url"]["url"].startswith("data:image/png;base64,")


def test_genuine_support_read_is_not_flagged(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    monkeypatch.setattr(
        "attractor_scan.visual_proof_judge._call_groq_api",
        lambda payload, api_key: _groq_response({
            "image_description": "a benchmark results table",
            "candidate_read": "genuine_technical_support",
            "reasoning": "the table's own numbers directly support the claim",
            "borrowed_term": None, "self_reported_confidence": "high",
        }),
    )
    result = judge_visual_proof("the model beats the benchmark", image_path=str(img))
    assert result.flagged is False
    assert result.candidate_read == "genuine_technical_support"


def test_unrelated_borrowed_precision_is_flagged(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    monkeypatch.setattr(
        "attractor_scan.visual_proof_judge._call_groq_api",
        lambda payload, api_key: _groq_response({
            "image_description": "a collage of unrelated math formulas",
            "candidate_read": "unrelated_borrowed_precision",
            "reasoning": "the formulas have nothing to do with the AGI claim; only 'singularity' links them",
            "borrowed_term": "singularity", "self_reported_confidence": "medium",
        }),
    )
    result = judge_visual_proof("math Singularity", image_path=str(img))
    assert result.flagged is True
    assert result.borrowed_term == "singularity"


def test_result_to_dict_is_json_safe_and_carries_disclaimer(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    monkeypatch.setattr(
        "attractor_scan.visual_proof_judge._call_groq_api",
        lambda payload, api_key: _groq_response({
            "image_description": "x", "candidate_read": "unclear", "reasoning": "",
            "borrowed_term": None, "self_reported_confidence": "low",
        }),
    )
    result = judge_visual_proof("claim", image_path=str(img))
    d = result.to_dict()
    json.dumps(d)  # must not raise
    assert d["source"] == "ai_advisory"
    assert d["case"] == "6"
    assert "case study" in d["disclaimer"]


def test_unrecognized_candidate_read_raises(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    monkeypatch.setattr(
        "attractor_scan.visual_proof_judge._call_groq_api",
        lambda payload, api_key: _groq_response({
            "image_description": "x", "candidate_read": "definitely_fake",
            "reasoning": "", "borrowed_term": None, "self_reported_confidence": "high",
        }),
    )
    with pytest.raises(VisualProofJudgeError, match="unrecognized candidate_read"):
        judge_visual_proof("claim", image_path=str(img))


def test_malformed_response_raises_clear_error(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    monkeypatch.setattr(
        "attractor_scan.visual_proof_judge._call_groq_api",
        lambda payload, api_key: {"choices": []},
    )
    with pytest.raises(VisualProofJudgeError, match="Could not parse"):
        judge_visual_proof("claim", image_path=str(img))


def test_call_groq_api_sets_identifying_user_agent(monkeypatch):
    """Same regression class as tools/bifp's rebuttal_judge test: Groq's
    edge bot-fights requests carrying Python's bare default urllib UA.
    Exercises the actual Request object _call_groq_api builds."""
    captured = {}

    class _FakeResponse(BytesIO):
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def fake_urlopen(request, timeout=None):
        captured["headers"] = dict(request.header_items())
        return _FakeResponse(json.dumps({
            "choices": [{"message": {"content": json.dumps({
                "image_description": "x", "candidate_read": "unclear", "reasoning": "",
                "borrowed_term": None, "self_reported_confidence": "low",
            })}}]
        }).encode("utf-8"))

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    _call_groq_api({"model": DEFAULT_MODEL, "messages": []}, "test-key")

    user_agent = captured["headers"].get("User-agent", "")
    assert user_agent, "no User-Agent header was set at all"
    assert "python-urllib" not in user_agent.lower()
    assert "attractor-scan-visual-proof-judge" in user_agent


def test_result_is_a_dataclass_with_expected_fields():
    result = VisualProofJudgeResult(
        claim_text="c", image_description="d", candidate_read="genuine_technical_support",
        reasoning="ok", borrowed_term=None, self_reported_confidence="high", model=DEFAULT_MODEL,
    )
    assert result.flagged is False
    assert result.disclaimer
