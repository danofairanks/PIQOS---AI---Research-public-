import pytest

from case_scaffold.lint import lint_text
from case_scaffold.template import CaseStudySpec, FrameworkRef, default_filename, render_skeleton


def _minimal_spec(**overrides) -> CaseStudySpec:
    defaults = dict(date="2026-08-08", slug="example_specimen", title="An Example Specimen")
    defaults.update(overrides)
    return CaseStudySpec(**defaults)


def test_date_validation():
    with pytest.raises(ValueError):
        _minimal_spec(date="Aug 8 2026")


def test_slug_validation():
    with pytest.raises(ValueError):
        _minimal_spec(slug="Not A Valid Slug")


def test_default_filename():
    spec = _minimal_spec()
    assert default_filename(spec) == "2026-08-08_example_specimen.md"


def test_render_skeleton_has_correct_title():
    text = render_skeleton(_minimal_spec())
    assert text.startswith("# Real-Time Specimen Analysis: An Example Specimen")


def test_render_skeleton_passes_structural_lint_but_warns_on_todos():
    text = render_skeleton(_minimal_spec())
    result = lint_text(text)
    assert result.ok  # structurally valid
    assert result.warnings  # but full of TODOs, as expected for a fresh scaffold


def test_render_skeleton_strict_mode_fails_on_fresh_scaffold():
    text = render_skeleton(_minimal_spec())
    result = lint_text(text, strict=True)
    assert not result.ok  # TODOs are errors in strict mode


def test_custom_subtitle_used_verbatim():
    spec = _minimal_spec(subtitle="A custom subtitle sentence")
    text = render_skeleton(spec)
    assert "### A custom subtitle sentence" in text


def test_framework_refs_appear_in_closing_line():
    spec = _minimal_spec(framework_refs=[
        FrameworkRef("../papers/published/basin_attractors_v1.md", "§2.4", "Attractor 4"),
    ])
    text = render_skeleton(spec)
    closing = text.strip().splitlines()[-1]
    assert "Applies the framework from" in closing
    assert "basin_attractors_v1.md" in closing
    assert "§2.4" in closing


def test_multiple_framework_refs_joined_with_and():
    spec = _minimal_spec(framework_refs=[
        FrameworkRef("../papers/published/basin_attractors_v1.md", "§2.4", "Attractor 4"),
        FrameworkRef("../papers/published/mirror_test_v1.md", "§5.1", "Ring 3"),
    ])
    text = render_skeleton(spec)
    closing = text.strip().splitlines()[-1]
    assert " and " in closing
    assert "mirror_test_v1.md" in closing


def test_sources_note_used_verbatim_when_provided():
    spec = _minimal_spec(sources_note="X post (verified account), inspected directly.")
    text = render_skeleton(spec)
    assert "X post (verified account), inspected directly." in text


def test_custom_section_titles():
    spec = _minimal_spec(section_titles=["Layer One", "Layer Two"])
    text = render_skeleton(spec)
    assert "## Layer One" in text
    assert "## Layer Two" in text
