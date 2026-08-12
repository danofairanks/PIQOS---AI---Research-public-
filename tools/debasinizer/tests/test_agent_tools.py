import json

from debasinizer.agent_tools import debasinizer_scan_corpus, debasinizer_scan_text


def test_scan_text_returns_json_safe_dict():
    result = debasinizer_scan_text("The signal resonates with consciousness across every node.")
    json.dumps(result)
    assert "register_flagged" in result
    assert "self_coherence" in result


def test_scan_corpus_returns_json_safe_dict():
    docs = [
        {"doc_id": "1", "text": "As we have established, this proves it."},
        {"doc_id": "2", "text": "The classifier scored 87.3% accuracy."},
    ]
    result = debasinizer_scan_corpus(docs)
    json.dumps(result)
    assert result["n_documents"] == 2
    assert result["self_coherence_flagged_count"] == 1


def test_scan_corpus_malformed_document_returns_error():
    result = debasinizer_scan_corpus([{"doc_id": "1"}])  # missing "text"
    assert "error" in result
