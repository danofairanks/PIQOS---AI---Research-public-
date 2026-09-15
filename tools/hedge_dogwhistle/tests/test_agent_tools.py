import json

from hedge_dogwhistle.agent_tools import hedge_dogwhistle_scan_corpus, hedge_dogwhistle_scan_text


def test_scan_text_returns_json_safe_dict():
    result = hedge_dogwhistle_scan_text("I'm not saying anything, but the timing is suspicious.")
    json.dumps(result)
    assert result["has_paralipsis"] is True
    assert len(result["matches"]) == 1


def test_scan_corpus_returns_json_safe_dict():
    docs = [
        {"doc_id": "1", "text": "Far be it from me to accuse anyone."},
        {"doc_id": "2", "text": "The quarterly results are up 12%."},
    ]
    result = hedge_dogwhistle_scan_corpus(docs)
    json.dumps(result)
    assert result["n_documents"] == 2
    assert result["has_paralipsis_count"] == 1


def test_scan_corpus_malformed_document_returns_error():
    result = hedge_dogwhistle_scan_corpus([{"doc_id": "1"}])  # missing "text"
    assert "error" in result
