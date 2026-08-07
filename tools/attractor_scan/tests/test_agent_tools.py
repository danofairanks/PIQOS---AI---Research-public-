import json

from attractor_scan.agent_tools import attractor_scan_corpus, attractor_scan_text

MUSK_QUOTE = "This will happen frequently as AI becomes smarter and more agentic"
CLEAN_TEXT = "The classifier scored 87.3% accuracy on a held-out test set with a fixed random seed."
STATUS_DISMISSAL_TEXT = "we are still working on it, that is just a hot take"


def test_scan_text_is_json_safe():
    result = attractor_scan_text(MUSK_QUOTE)
    json.dumps(result)  # must not raise
    assert "maneuvers" in result
    assert "laundering" in result


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
