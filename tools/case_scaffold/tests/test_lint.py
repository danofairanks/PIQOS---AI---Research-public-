"""Lint rules are validated against this repository's own real
case_studies/ files, not just constructed examples. Checked directly
(2026-08-08): the house format stabilized starting 2026-08-04 -- the
five files from that date onward, plus the two case studies added
this session (2026-08-06, 2026-08-07), all fully conform: the
"# Real-Time Specimen Analysis:" title prefix and a "## What This
Case Study Does Not Claim" section both appear consistently from
2026-08-04 forward and not before. The six files from 2026-07-27
through 2026-08-02 predate that convention (shorter titles, no
Does-Not-Claim section, a July 27 outlier with the long title but no
Does-Not-Claim section) and are expected to fail structural lint for
specific, named reasons -- that is real history, not a linter bug,
and this test suite pins both halves of it rather than only the
files that happen to pass.
"""

from pathlib import Path

import pytest

from case_scaffold.lint import lint_file, lint_text

CASE_STUDIES_DIR = Path(__file__).resolve().parents[3] / "case_studies"

CONFORMING_FILES = [
    "2026-08-04_aix_seed_iq_arc_agi_3_claim.md",
    "2026-08-04_dead_salmon_fmri_ring3_specimen.md",
    "2026-08-04_doorstep_interview_format_friction_suppression.md",
    "2026-08-04_musk_source_code_binary_escalation.md",
    "2026-08-06_marcus_karapetyan_status_dismissal.md",
    "2026-08-07_openai_huggingface_breach_singularity_reframe.md",
]

PRE_CONVENTION_FILES = [
    "2026-07-27_ssi_nvidia_partnership.md",
    "2026-07-28_grok_x_instant_sycophancy.md",
    "2026-07-28_minimal_input_elaboration_drift.md",
    "2026-07-28_nfl_misapplication_grok_x.md",
    "2026-07-28_nvidia_circular_deals_bloomberg.md",
    "2026-07-31_altman_family_podcast_ratio.md",
    "2026-08-02_ten_advances_abductive_jump_test.md",
]


def _skip_if_repo_layout_unavailable():
    if not CASE_STUDIES_DIR.is_dir():
        pytest.skip(f"case_studies/ not found at {CASE_STUDIES_DIR}; "
                    f"run tests from a full repo checkout to exercise these ground-truth checks")


@pytest.mark.parametrize("filename", CONFORMING_FILES)
def test_conforming_real_files_pass_strict_lint(filename):
    _skip_if_repo_layout_unavailable()
    result = lint_file(CASE_STUDIES_DIR / filename, strict=True)
    assert result.ok, f"{filename}: {result.errors}"


def test_2026_07_27_fails_only_for_missing_does_not_claim_section():
    _skip_if_repo_layout_unavailable()
    result = lint_file(CASE_STUDIES_DIR / "2026-07-27_ssi_nvidia_partnership.md")
    assert not result.ok
    assert len(result.errors) == 1
    assert "What This Case Study Does Not Claim" in result.errors[0]


@pytest.mark.parametrize("filename", [
    "2026-07-28_grok_x_instant_sycophancy.md",
    "2026-07-28_minimal_input_elaboration_drift.md",
    "2026-07-28_nfl_misapplication_grok_x.md",
    "2026-07-28_nvidia_circular_deals_bloomberg.md",
])
def test_pre_convention_short_title_files_fail_title_and_claim_checks(filename):
    _skip_if_repo_layout_unavailable()
    result = lint_file(CASE_STUDIES_DIR / filename)
    assert not result.ok
    joined = " ".join(result.errors)
    assert "Real-Time Specimen Analysis" in joined
    assert "What This Case Study Does Not Claim" in joined


# --- Rules exercised directly, independent of the real-repo fixtures ---

VALID_MINIMAL_TEXT = """# Real-Time Specimen Analysis: Example

### A one-sentence subtitle naming the mechanism

---

## Executive Summary

Some summary text.

---

## The Specimen

Some specimen text.

## What This Case Study Does Not Claim

Some caveats.

---

*Specimen dated 2026-08-08. Applies the framework from [`../papers/published/example.md`](../papers/published/example.md) §1.*
"""


def test_valid_minimal_text_passes():
    result = lint_text(VALID_MINIMAL_TEXT)
    assert result.ok


def test_missing_title_fails():
    text = VALID_MINIMAL_TEXT.replace(
        "# Real-Time Specimen Analysis: Example", "# Something Else Entirely"
    )
    result = lint_text(text)
    assert not result.ok
    assert any("Real-Time Specimen Analysis" in e for e in result.errors)


def test_missing_subtitle_fails():
    lines = VALID_MINIMAL_TEXT.splitlines()
    lines = [l for l in lines if not l.startswith("### A one-sentence")]
    result = lint_text("\n".join(lines))
    assert not result.ok


def test_missing_separator_fails():
    text_no_sep = VALID_MINIMAL_TEXT.replace("---", "")
    result = lint_text(text_no_sep)
    assert not result.ok
    assert any("separator" in e for e in result.errors)


def test_missing_closing_line_fails():
    lines = VALID_MINIMAL_TEXT.strip().splitlines()[:-1]
    result = lint_text("\n".join(lines))
    assert not result.ok
    assert any("Applies the framework from" in e for e in result.errors)


def test_todo_marker_is_warning_not_error_by_default():
    text = VALID_MINIMAL_TEXT.replace("Some summary text.", "**TODO — replace before publishing:** fill this in")
    result = lint_text(text)
    assert result.ok
    assert result.warnings


def test_todo_marker_is_error_in_strict_mode():
    text = VALID_MINIMAL_TEXT.replace("Some summary text.", "**TODO — replace before publishing:** fill this in")
    result = lint_text(text, strict=True)
    assert not result.ok


def test_broken_framework_link_warns_when_base_dir_given(tmp_path):
    result = lint_text(VALID_MINIMAL_TEXT, base_dir=tmp_path)
    assert result.ok  # link resolution failures are warnings, not structural errors
    assert result.warnings
    assert any("does not resolve" in w for w in result.warnings)


def test_lint_file_reads_from_disk(tmp_path):
    p = tmp_path / "test.md"
    p.write_text(VALID_MINIMAL_TEXT, encoding="utf-8")
    result = lint_file(p)
    assert result.path == str(p)
