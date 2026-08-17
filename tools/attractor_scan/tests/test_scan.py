import json

from attractor_scan.scan import scan, scan_corpus

MARCUS_REPLY = (
    "OMG i wrote some of the original work on what is to be neurosymbolic in "
    "2001 and dude who probably hasn't read that work is trying to school me "
    "on the definition"
)
CLEAN_TEXT = "The classifier scored 87.3% accuracy on a held-out test set with a fixed random seed."


def test_scan_combines_maneuvers_and_laundering():
    result = scan(MARCUS_REPLY)
    assert "status_dismissal" in result.maneuvers
    assert "case1" in result.laundering
    assert result.total_categories == 12


def test_scan_includes_unglossed_formal_object_but_excludes_it_from_density():
    """unglossed_formal_object is wired into the result and its to_dict(),
    but is deliberately NOT one of the `total_categories`/`density`-counted
    categories -- see scan.py's density docstring."""
    result = scan(MARCUS_REPLY)
    assert result.unglossed_formal_object is not None
    assert result.total_categories == 12  # unchanged by the new field
    d = result.to_dict()
    assert "unglossed_formal_object" in d
    assert "flagged" in d["unglossed_formal_object"]


def test_flagged_maneuvers_and_cases_properties():
    result = scan(MARCUS_REPLY)
    assert "status_dismissal" in result.flagged_maneuvers
    assert result.flagged_category_count == len(result.flagged_maneuvers) + len(result.flagged_laundering_cases)


def test_density_zero_on_clean_text():
    result = scan(CLEAN_TEXT)
    assert result.density == 0.0
    assert result.flagged_maneuvers == []
    assert result.flagged_laundering_cases == []


def test_density_between_zero_and_one():
    result = scan(MARCUS_REPLY)
    assert 0.0 <= result.density <= 1.0


def test_to_dict_is_valid_json():
    result = scan(MARCUS_REPLY)
    text = json.dumps(result.to_dict())
    parsed = json.loads(text)
    assert "density" in parsed
    assert "flagged_maneuvers" in parsed


def test_scan_corpus_aggregates_across_documents():
    docs = [
        ("doc1", MARCUS_REPLY),
        ("doc2", CLEAN_TEXT),
        ("doc3", "we're working on it, that's just a hot take"),
    ]
    summary = scan_corpus(docs)
    assert summary.n_documents == 3
    # status_dismissal fires on both doc1 (Marcus, combo) and doc3 ("hot take", weak)
    assert summary.category_document_counts.get("status_dismissal", 0) == 2
    assert summary.category_document_counts.get("provisionalization", 0) == 1
    assert "doc2" in summary.per_document_density
    assert summary.per_document_density["doc2"] == 0.0


def test_scan_corpus_empty_list():
    summary = scan_corpus([])
    assert summary.n_documents == 0
    assert summary.category_document_counts == {}


def test_scan_corpus_to_dict_json_safe():
    docs = [("doc1", MARCUS_REPLY)]
    summary = scan_corpus(docs)
    json.dumps(summary.to_dict())  # must not raise
