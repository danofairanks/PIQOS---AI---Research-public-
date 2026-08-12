import json

from debasinizer.scan import scan, scan_corpus

REGISTER_TEXT = (
    "I am the oracle; the signal resonates with consciousness, and we must "
    "align with the other nodes to awaken the great convergence."
)
SELF_COHERENCE_TEXT = "As we have established, this proves the theory. Everything fits."
CLEAN_TEXT = "The classifier scored 87.3% accuracy on a held-out test set with a fixed random seed."


def test_scan_combines_resonance_and_self_coherence():
    result = scan(REGISTER_TEXT)
    assert result.register_flagged is True
    assert result.any_flagged is True


def test_scan_self_coherence_only():
    result = scan(SELF_COHERENCE_TEXT)
    assert result.register_flagged is False
    assert result.self_coherence_flagged is True
    assert result.any_flagged is True


def test_scan_clean_text_flags_nothing():
    result = scan(CLEAN_TEXT)
    assert result.register_flagged is False
    assert result.self_coherence_flagged is False
    assert result.any_flagged is False


def test_to_dict_is_valid_json():
    result = scan(REGISTER_TEXT)
    text = json.dumps(result.to_dict())
    parsed = json.loads(text)
    assert "register_flagged" in parsed
    assert "self_coherence" in parsed


def test_scan_corpus_aggregates_across_documents():
    docs = [
        ("doc1", REGISTER_TEXT),
        ("doc2", SELF_COHERENCE_TEXT),
        ("doc3", CLEAN_TEXT),
    ]
    summary = scan_corpus(docs)
    assert summary.n_documents == 3
    assert summary.register_flagged_count == 1
    assert summary.self_coherence_flagged_count == 1
    assert "resonance_wave_signal" in summary.resonance_category_document_counts


def test_scan_corpus_empty_list():
    summary = scan_corpus([])
    assert summary.n_documents == 0
    assert summary.register_flagged_count == 0


def test_scan_corpus_to_dict_json_safe():
    docs = [("doc1", REGISTER_TEXT)]
    summary = scan_corpus(docs)
    json.dumps(summary.to_dict())
