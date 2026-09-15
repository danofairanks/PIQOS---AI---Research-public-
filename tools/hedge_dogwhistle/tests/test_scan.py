import json

from hedge_dogwhistle.scan import scan, scan_corpus


def test_scan_returns_result_with_expected_shape():
    result = scan("I'm not saying anything, but the timing is suspicious.")
    d = result.to_dict()
    assert "matches" in d
    assert "has_paralipsis" in d
    assert "text_with_hedges_removed" in d
    json.dumps(d)


def test_scan_corpus_aggregates():
    documents = [
        ("1", "I'm not saying anything, but the timing is suspicious."),
        ("2", "The quarterly results show a 12% increase in revenue."),
        ("3", "Far be it from me to accuse anyone. Not to suggest otherwise, though."),
    ]
    summary = scan_corpus(documents)
    assert summary.n_documents == 3
    assert summary.has_paralipsis_count == 2
    assert summary.total_matches == 3
    json.dumps(summary.to_dict())


def test_scan_corpus_empty():
    summary = scan_corpus([])
    assert summary.n_documents == 0
    assert summary.to_dict()["has_paralipsis_frequency"] == 0.0
