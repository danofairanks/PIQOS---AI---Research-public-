"""End-to-end scan validated against this repository's own real
case_studies/ files, not just constructed examples. Checked directly
(2026-08-07): a naive proximity-only detector reads this project's real
convention -- one italic "Sources: ..." line at the close of a document,
rather than inline per-claim citation -- as riddled with gaps (214
total across 14 files in an early draft). The `sourcing.py` module and
the `severe_gap_count` distinction exist specifically to correct for
that: `gap_count` is the raw heuristic surface (useful as a checklist),
`severe_gap_count` is what should gate CI, and it only stays nonzero
where a document has neither end-sourcing nor a disclaimer to fall back
on. The five real files pinned as severe below independently
corroborate case_scaffold's separately-derived PRE_CONVENTION_FILES
finding: the house format (title prefix, Does-Not-Claim section)
stabilized 2026-08-04, and four case studies plus the case_studies/
index page predate it.
"""

from pathlib import Path

import pytest

from verification_lint import scan_file

REPO_ROOT = Path(__file__).resolve().parents[3]
CASE_STUDIES_DIR = REPO_ROOT / "case_studies"


def _skip_if_repo_layout_unavailable():
    if not CASE_STUDIES_DIR.is_dir():
        pytest.skip(f"case_studies/ not found at {CASE_STUDIES_DIR}; "
                    f"run tests from a full repo checkout to exercise these ground-truth checks")


def test_marcus_case_study_has_zero_gaps():
    """The most heavily-tuned-against specimen: named sources, section
    citations, and short scare-quotes throughout -- exactly the shape
    the quote/statistic detectors were calibrated not to false-positive on."""
    _skip_if_repo_layout_unavailable()
    result = scan_file(CASE_STUDIES_DIR / "2026-08-06_marcus_karapetyan_status_dismissal.md")
    assert result.gap_count == 0
    assert result.severe_gap_count == 0
    assert result.ok


def test_openai_breach_case_study_has_four_non_severe_gaps():
    """Has end-of-document sourcing, so its flagged items -- originally
    one (a large comma-grouped count with no *proximate* citation) --
    are real but non-severe: checklist items to verify against the
    sources line, not hard failures. The 2026-08-27 primary-source
    addendum appended to this same file (per its own "Sourcing tier,
    stated precisely" section) legitimately introduced three more of
    the same shape -- a second, separate mention of the 17,600 count,
    a decimal-percent range (0.2% to 3.5-4%), and a direct quote
    ("would have flagged most of the dangerous actions") whose
    attribution ("OpenAI's own report states that...") sits in the
    same compound sentence but outside quotes.py's proximity window --
    all covered by the addendum's own end-of-document sources line,
    same as the original gap. Was pinned at gap_count == 1 until an
    outside reader (2026-09-04) ran this suite directly and reported
    the resulting stale-pin mismatch (4 actual vs. 1 expected);
    confirmed here by reading each of the three new matches directly,
    not just accepting the count."""
    _skip_if_repo_layout_unavailable()
    result = scan_file(CASE_STUDIES_DIR / "2026-08-07_openai_huggingface_breach_singularity_reframe.md")
    assert result.gap_count == 4
    assert result.severe_gap_count == 0
    assert result.ok
    assert result.sourcing.has_end_sourcing is True


@pytest.mark.parametrize("filename", [
    "2026-07-27_ssi_nvidia_partnership.md",
    "2026-07-28_grok_x_instant_sycophancy.md",
    "2026-07-28_minimal_input_elaboration_drift.md",
    "2026-07-28_nfl_misapplication_grok_x.md",
])
def test_pre_convention_files_have_exactly_one_severe_gap(filename):
    """These four predate the 2026-08-04 house-format convention and
    have no "What This Case Study Does Not Claim" section -- the same
    real historical fact case_scaffold's lint suite pins independently.
    Each has end-sourcing, so the single severe gap is the missing
    disclaimer, not an uncited quote or statistic."""
    _skip_if_repo_layout_unavailable()
    result = scan_file(CASE_STUDIES_DIR / filename)
    assert result.severe_gap_count == 1
    assert not result.ok
    assert result.disclaimer.gap is True
    assert result.sourcing.has_end_sourcing is True


def test_nvidia_circular_deals_has_gaps_but_none_severe():
    """Also pre-convention by file naming, but distinct from the four
    above: it has both end-sourcing AND a disclaimer-style section, so
    despite 11 raw quote/statistic gaps none of them are severe."""
    _skip_if_repo_layout_unavailable()
    result = scan_file(CASE_STUDIES_DIR / "2026-07-28_nvidia_circular_deals_bloomberg.md")
    assert result.gap_count > 0
    assert result.severe_gap_count == 0
    assert result.ok


def test_case_studies_index_page_is_severe():
    """case_studies/README.md is a table-of-contents index, not a
    specimen analysis -- it has neither a disclaimer section nor an
    end-sourcing statement, so every flagged item stays severe. This is
    a correct read: an index page listing many case studies legitimately
    is not itself sourced the way an analysis is."""
    _skip_if_repo_layout_unavailable()
    result = scan_file(CASE_STUDIES_DIR / "README.md")
    assert result.severe_gap_count > 0
    assert not result.ok
    assert result.sourcing.has_end_sourcing is False


def test_conforming_files_are_clean_or_only_non_severe():
    """The remaining 2026-08-04-onward files (beyond Marcus and the
    OpenAI breach file, already covered above) should never surface a
    severe gap -- they all carry both the Does-Not-Claim section and
    end-sourcing."""
    _skip_if_repo_layout_unavailable()
    for filename in [
        "2026-08-04_aix_seed_iq_arc_agi_3_claim.md",
        "2026-08-04_dead_salmon_fmri_ring3_specimen.md",
        "2026-08-04_doorstep_interview_format_friction_suppression.md",
        "2026-08-04_musk_source_code_binary_escalation.md",
    ]:
        result = scan_file(CASE_STUDIES_DIR / filename)
        assert result.severe_gap_count == 0, f"{filename}: unexpected severe gap"


def test_to_dict_json_safe():
    import json
    _skip_if_repo_layout_unavailable()
    result = scan_file(CASE_STUDIES_DIR / "2026-08-06_marcus_karapetyan_status_dismissal.md")
    json.dumps(result.to_dict())  # must not raise
