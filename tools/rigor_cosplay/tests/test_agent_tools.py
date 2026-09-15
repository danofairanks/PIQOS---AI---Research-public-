import json

from rigor_cosplay.agent_tools import rigor_cosplay_scan_corpus, rigor_cosplay_scan_text


def test_scan_text_returns_json_safe_dict():
    result = rigor_cosplay_scan_text("That's an excellent point -- I want to push back on one thing.")
    json.dumps(result)
    assert result["any_signature_flagged"] is True
    assert "cosmetic_pushback" in result["signatures_hit"]


def test_scan_corpus_returns_json_safe_dict():
    docs = [
        {"doc_id": "1", "text": "Let me steelman the opposing view."},
        {"doc_id": "2", "text": "Plain disagreement on the merits."},
    ]
    result = rigor_cosplay_scan_corpus(docs)
    json.dumps(result)
    assert result["n_documents"] == 2
    assert result["any_flagged_count"] == 1


def test_scan_corpus_malformed_document_returns_error():
    result = rigor_cosplay_scan_corpus([{"doc_id": "1"}])  # missing "text"
    assert "error" in result
