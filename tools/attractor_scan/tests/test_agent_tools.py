import base64
import json

from attractor_scan.agent_tools import (
    attractor_scan_corpus, attractor_scan_judge_visual_proof, attractor_scan_text,
)

_TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)

MUSK_QUOTE = "This will happen frequently as AI becomes smarter and more agentic"
CLEAN_TEXT = "The classifier scored 87.3% accuracy on a held-out test set with a fixed random seed."
STATUS_DISMISSAL_TEXT = "we are still working on it, that is just a hot take"


def test_scan_text_is_json_safe():
    result = attractor_scan_text(MUSK_QUOTE)
    json.dumps(result)  # must not raise
    assert "maneuvers" in result
    assert "laundering" in result
    assert "unglossed_formal_object" in result


def test_scan_text_flags_the_papers_own_cited_example():
    """Same real specimen attractor_scan's own test suite validates
    against -- Case 5's real-world cited Musk quote, kept here as a
    cross-check that the JSON-facing wrapper doesn't lose the finding."""
    result = attractor_scan_text(MUSK_QUOTE)
    assert "case5" in result["flagged_laundering_cases"]


def test_scan_text_clean_control_flags_nothing():
    result = attractor_scan_text(CLEAN_TEXT)
    assert result["flagged_maneuvers"] == []
    assert result["flagged_laundering_cases"] == []
    assert result["density"] == 0.0


def test_scan_corpus_is_json_safe():
    documents = [
        {"doc_id": "1", "text": STATUS_DISMISSAL_TEXT},
        {"doc_id": "2", "text": CLEAN_TEXT},
    ]
    result = attractor_scan_corpus(documents)
    json.dumps(result)  # must not raise
    assert result["n_documents"] == 2


def test_scan_corpus_malformed_document_returns_error_dict_not_exception():
    result = attractor_scan_corpus([{"doc_id": "1"}])  # missing "text"
    assert "error" in result


def test_scan_corpus_empty_list_is_json_safe():
    result = attractor_scan_corpus([])
    json.dumps(result)  # must not raise
    assert result["n_documents"] == 0


def test_judge_visual_proof_missing_key_returns_error_dict_not_exception(monkeypatch, tmp_path):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    result = attractor_scan_judge_visual_proof("claim", str(img))
    assert "error" in result
    assert "GROQ_API_KEY" in result["error"]


def test_judge_visual_proof_is_json_safe(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    img = tmp_path / "x.png"
    img.write_bytes(_TINY_PNG)
    monkeypatch.setattr(
        "attractor_scan.visual_proof_judge._call_groq_api",
        lambda payload, api_key: {
            "choices": [{"message": {"content": json.dumps({
                "image_description": "a formula collage",
                "candidate_read": "unrelated_borrowed_precision",
                "reasoning": "no real connection to the claim",
                "borrowed_term": "singularity", "self_reported_confidence": "medium",
            })}}]
        },
    )
    result = attractor_scan_judge_visual_proof("math Singularity", str(img))
    json.dumps(result)  # must not raise
    assert result["source"] == "ai_advisory"
    assert result["flagged"] is True


def test_judge_visual_proof_unreadable_image_returns_error_dict(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "k")
    result = attractor_scan_judge_visual_proof("claim", "/nonexistent/x.png")
    assert "error" in result
