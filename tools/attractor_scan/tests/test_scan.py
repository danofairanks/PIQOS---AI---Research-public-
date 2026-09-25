import json
from pathlib import Path

import pytest

from attractor_scan.scan import scan, scan_corpus

REPO_ROOT = Path(__file__).resolve().parents[3]

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


def _skip_if_repo_layout_unavailable():
    if not (REPO_ROOT / "papers" / "drafts").is_dir():
        pytest.skip("papers/drafts/ not found; run tests from a full repo checkout")


def test_real_document_case2_excludes_own_arxiv_citation():
    """Regression pin for the false positive this package found in its own
    real-document check (see laundering.py's `_in_arxiv_citation` comment):
    scanning topology_with_no_exit_v1.md §6 previously flagged the word
    'Reasoning' inside a cited paper's own title --
    "...Interpretation of Reasoning Operations in LLMs" (arXiv:2509.04753v1)
    -- as an unqualified first-person AI-reasoning claim under case2. That
    citation is not this document's own assertion. Same defect class, same
    fix shape, as paper_rigor/credentialing.py's meta-framing suppression
    (see this repo's CLAUDE.md "Fixed 2026-09-04" entry) -- ported here
    rather than re-derived, since attractor_scan had no real-document
    regression coverage at all before this test."""
    _skip_if_repo_layout_unavailable()
    text = (REPO_ROOT / "papers" / "drafts" / "topology_with_no_exit_v1.md").read_text()
    result = scan(text)
    case2 = result.laundering["case2"]
    assert case2.flagged is False
    assert case2.matches == []


def test_real_document_case3_excludes_own_table_row_title():
    """Regression pin for the false positive this package found scanning
    papers/drafts/ssa_r5.3.8_review/countermodel_analysis_v1.md: a cited
    source paper's own title, reproduced verbatim in the paper's citation
    table ("...A Structural Condition for Residual Emergence Under Bounded
    State Trajectories"), was flagged as an unqualified AI-emergence claim
    under case3 purely because an unrelated AI-subject word ("model")
    appeared elsewhere in the document -- case3 has no proximity window at
    all, unlike case2, so this false-positive shape is broader than
    case2's citation-only fix. See laundering.py's `_in_markdown_table_row`
    comment for the exact shape."""
    _skip_if_repo_layout_unavailable()
    text = (
        REPO_ROOT / "papers" / "drafts" / "ssa_r5.3.8_review"
        / "countermodel_analysis_v1.md"
    ).read_text()
    result = scan(text)
    case3 = result.laundering["case3"]
    assert case3.flagged is False
    assert case3.matches == []
