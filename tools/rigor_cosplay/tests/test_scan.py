import json

from rigor_cosplay.scan import scan, scan_corpus


def test_scan_returns_result_with_expected_shape():
    result = scan("That's an excellent point -- I want to push back on one thing.")
    d = result.to_dict()
    assert "cosmetic_pushback" in d
    assert "weak_man_steelman" in d
    assert "honesty_as_flattery" in d
    assert "any_signature_flagged" in d
    json.dumps(d)


def test_scan_corpus_aggregates():
    documents = [
        ("1", "That's an excellent point -- I want to push back on one thing."),
        ("2", "The benchmark numbers don't control for contamination."),
        ("3", "Let me steelman your position for a moment."),
    ]
    summary = scan_corpus(documents)
    assert summary.n_documents == 3
    assert summary.any_flagged_count == 2
    assert summary.signature_document_counts["cosmetic_pushback"] == 1
    assert summary.signature_document_counts["weak_man_steelman"] == 1
    json.dumps(summary.to_dict())


def test_scan_corpus_empty():
    summary = scan_corpus([])
    assert summary.n_documents == 0
    assert summary.to_dict()["any_flagged_frequency"] == 0.0
