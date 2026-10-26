"""End-to-end scan validated against this repository's own real papers
and protocols (not just constructed examples), pinning exact
gap counts so a future change to any heuristic has to consciously
re-justify a shift in these numbers -- same discipline as
verification_lint's and case_scaffold's own test suites.
"""

from pathlib import Path

import pytest

from paper_rigor.scan import scan_file, scan_paper

REPO_ROOT = Path(__file__).resolve().parents[3]


def _skip_if_repo_layout_unavailable():
    if not (REPO_ROOT / "papers" / "published").is_dir():
        pytest.skip("papers/published/ not found; run tests from a full repo checkout")


@pytest.mark.parametrize("relpath,expect_ok,expect_structural,expect_total", [
    ("papers/published/basin_attractors_v1.md", True, 0, 2),
    ("papers/published/conjecture_tracker_v1.md", True, 0, 1),
    # Was (False, 1, 1) until credentialing.py's three matches on this file
    # (Founder of / founder of / Nobel laureate, all inside the "Law" entry's
    # own description OF the founder-of-discursivity pattern, not a claim the
    # document makes on its own behalf) were confirmed as false positives and
    # fixed at the detector level -- see credentialing.py's module docstring
    # and _shared.py's _STYLED_AS_RE. Independently corroborated externally
    # (2026-09-04): an outside reader ran this suite directly and reported
    # the identical stale-pin mismatch before this fix landed.
    ("papers/published/laundered_vocabulary_v1.md", True, 0, 0),
    ("papers/published/mirror_test_v1.md", False, 1, 1),
    ("protocols/elaboration_drift_prevalence_protocol_v1.md", True, 0, 0),
    ("protocols/noether_coherence_test_protocol_v1.md", True, 0, 0),
])
def test_real_document_gap_counts(relpath, expect_ok, expect_structural, expect_total):
    _skip_if_repo_layout_unavailable()
    result = scan_file(REPO_ROOT / relpath)
    assert result.ok is expect_ok, f"{relpath}: {result.to_dict()}"
    assert result.structural_gap_count == expect_structural, f"{relpath}: {result.placeholder_gaps}, {result.falsifiability}, {result.limitations}"
    assert result.total_gap_count == expect_total, f"{relpath}: {result.external_verification_worklist}"


def test_mirror_test_meta_framed_phrases_correctly_excluded():
    """mirror_test_v1.md contains "studies show[ing]" and "scientific
    consensus" as EXAMPLES within a description of rhetorical
    maneuvers/historical fallacies, not as the paper's own claims --
    both must NOT appear in the worklist (see _shared.py and
    test_citations.py/test_consensus.py's own regression tests for the
    isolated-unit version of this same check)."""
    _skip_if_repo_layout_unavailable()
    result = scan_file(REPO_ROOT / "papers/published/mirror_test_v1.md")
    worklist_items = [item["item"] for item in result.external_verification_worklist]
    assert not any("scientific consensus" in item.lower() and "cited as" not in item.lower() for item in worklist_items)


def test_constructed_bad_paper_flags_every_category():
    bad = (
        "As a renowned expert with over 30 years of experience, I can tell you this "
        "approach conclusively demonstrates artificial general intelligence, beyond any doubt. "
        "It is well known that no one disputes this. It is trivial to show the derivation; "
        "TODO: fill in proof. Research shows the model outperforms all baselines."
    ) + (" filler word" * 400)
    result = scan_paper(bad, byline_authors=["Smith"])
    assert result.ok is False
    assert result.structural_gap_count == 4  # 2 placeholder + falsifiability + limitations
    worklist_kinds = {item["kind"] for item in result.external_verification_worklist}
    assert worklist_kinds == {"uncited_empirical_claim", "credential_substitution", "unsupported_consensus_claim"}


def test_references_would_include_placeholder_is_a_structural_gap():
    """A References section that only says what it "would include" is a
    placeholder, not a bibliography. The scanner cannot detect fabricated
    quotes (that needs a primary source) but does catch this tell."""
    text = (
        "1. Introduction\n\n" + " ".join(["word"] * 450)
        + "\n\n## References\n\n[References would include citations to prior work, ...]\n"
    )
    result = scan_paper(text)
    assert result.ok is False
    assert any("would include" in g.phrase for g in result.placeholder_gaps)


def test_citability_claim_without_references_end_to_end():
    """A long document that asserts its grounding in "documented, citable
    research" while containing no references is flagged; its confident
    tone uses none of the ordinary academic certainty phrases."""
    text = (
        "1. Overview\n\n" + " ".join(["status"] * 450)
        + "\n\nThe framework's grounding in documented, citable research is established.\n"
    )
    result = scan_paper(text)
    assert result.citability_claim.gap is True
    assert result.citability_claim.n_references == 0


def test_plain_numbered_heading_paper_scans_clean_end_to_end():
    """End-to-end version of the headings-harness regression: a paper
    structured like a real PDF-extracted specimen (plain numbered
    headings, no markdown, no references section, no citability claim)
    with a genuine, substantive limitations section should scan clean
    -- confirming the harness fix, not just the isolated disclaimer.py
    unit, produces the correct overall result."""
    text = (
        "1. Introduction\n\n"
        + " ".join(["word"] * 450)
        + "\n\n7. Honest Limitations and Genuine Improvements\n\n"
          "One faculty that previously underperformed has been improved through a genuine upgrade.\n\n"
          "10. Conclusion\n\nWe have presented an integrated architecture.\n"
    )
    result = scan_paper(text)
    assert result.ok is True
    assert result.structural_gap_count == 0
    assert result.limitations.has_heading_section is True


def test_to_dict_json_safe():
    import json
    result = scan_paper("Some clean prose with no issues at all here.")
    json.dumps(result.to_dict())  # must not raise
