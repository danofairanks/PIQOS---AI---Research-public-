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
    ("papers/published/laundered_vocabulary_v1.md", False, 1, 1),
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


def test_known_bad_private_specimen_structural_gap():
    """Validated locally (not committed) against
    PIQOS-IsoAxiomV8-/papers/contamination/rem_capture.md -- a paper
    this project's own core/living_research_policy.md already
    documents as containing fabricated quotes attributed to named
    public figures. paper_rigor cannot detect quote fabrication (that
    needs reading primary sources, exactly the boundary its worklist
    exists for) but DOES catch the paper's own structural tell: a
    References section reading "[References would include citations
    to LeCun papers, ...]" instead of containing any. Skipped outside
    an environment with that private repo checked out alongside this
    one."""
    private_repo_specimen = REPO_ROOT.parent / "PIQOS-IsoAxiomV8-" / "papers" / "contamination" / "rem_capture.md"
    if not private_repo_specimen.is_file():
        pytest.skip("private repo specimen not available in this checkout")
    result = scan_file(private_repo_specimen)
    assert result.ok is False
    assert any("would include" in g.phrase for g in result.placeholder_gaps)


def test_citability_claim_without_references_on_a_real_unseen_specimen():
    """Validated locally (not committed) against a genuinely
    previously-unseen private-repo specimen from
    temp/papers/mimicry_instance_corpus/ -- an ~86KB / ~12,000-word
    paper (raw page-scan structure, no References heading anywhere)
    that asserts "the framework's grounding in documented, citable
    research" while containing zero actual references. This is the
    specimen that motivated citability_claim: the tool's first pass
    (before this check existed) came back almost entirely quiet on it
    -- structural_gap_count=1 (missing limitations only) -- because the
    paper's confident tone doesn't use ordinary academic certainty
    phrases; it invents its own register ("Sovereign Protocol,"
    "SEALED WITH THE 30-CROSSING KNOT") instead. This check closes that
    specific, real gap without pretending to catch invented terminology
    generally. Skipped outside an environment with the private repo
    checked out alongside this one."""
    private_repo_specimen = (
        REPO_ROOT.parent / "PIQOS-IsoAxiomV8-" / "temp" / "papers" / "mimicry_instance_corpus"
        / "the_transmission_of_humanity_topological_resonance.md"
    )
    if not private_repo_specimen.is_file():
        pytest.skip("private repo specimen not available in this checkout")
    result = scan_file(private_repo_specimen)
    assert result.citability_claim.gap is True
    assert result.citability_claim.n_references == 0
    assert result.structural_gap_count == 2  # missing limitations + citability claim


def test_to_dict_json_safe():
    import json
    result = scan_paper("Some clean prose with no issues at all here.")
    json.dumps(result.to_dict())  # must not raise
