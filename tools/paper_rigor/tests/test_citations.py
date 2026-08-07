"""Citation parsing is validated against this repo's own real
`papers/published/basin_attractors_v1.md` References section (81
entries, APA-ish, blank-line-separated, mixed academic/legal/GitHub-
issue/self-published entry shapes) as ground truth, not just
constructed examples.
"""

from pathlib import Path

import pytest

from paper_rigor.citations import (
    CitationEntry, compute_self_citation, compute_venue_mix,
    find_uncited_empirical_claims, parse_references,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
BASIN_ATTRACTORS = REPO_ROOT / "papers" / "published" / "basin_attractors_v1.md"


def _skip_if_repo_layout_unavailable():
    if not BASIN_ATTRACTORS.is_file():
        pytest.skip(f"{BASIN_ATTRACTORS} not found; run tests from a full repo checkout")


def test_real_references_section_parses_to_known_count():
    """Regression test for a real bug: the first draft's section-end
    boundary only stopped at the next markdown heading, not at a
    standalone "---" divider. basin_attractors_v1.md's reference list
    is followed by dated revision-log paragraphs with no heading in
    between (only a "---" divider) -- without this fix, those prose
    paragraphs got mis-split and counted as if they were bibliography
    entries (112 "entries" instead of the real 81)."""
    _skip_if_repo_layout_unavailable()
    text = BASIN_ATTRACTORS.read_text(encoding="utf-8")
    entries = parse_references(text)
    assert len(entries) == 81


def test_real_references_venue_mix_matches_manual_count():
    _skip_if_repo_layout_unavailable()
    text = BASIN_ATTRACTORS.read_text(encoding="utf-8")
    entries = parse_references(text)
    mix = compute_venue_mix(entries)
    assert (mix.n_formal, mix.n_informal, mix.n_unknown, mix.n_total) == (28, 2, 51, 81)


def test_bare_domain_without_scheme_still_classified():
    """A real shape found during tuning: many references name a bare
    domain ("thehumanlineproject.org, as reported by...") with no
    "https://" scheme at all."""
    entry_text = "Some Org (2025). A report. someorg.arxiv.org, 2025."
    entries = parse_references(f"## References\n\n{entry_text}\n")
    assert entries[0].venue_type == "formal"


def test_extraction_stops_at_no_heading_but_horizontal_rule():
    text = (
        "## References\n\nSmith, J. (2020). A Paper. arxiv.org/abs/1234.\n\n"
        "---\n\n*Not a reference: this is a revision-log paragraph.*"
    )
    entries = parse_references(text)
    assert len(entries) == 1


def test_no_references_section_returns_empty_list_not_error():
    assert parse_references("Just some prose with no references heading at all.") == []


def test_self_citation_ratio_none_when_no_byline_given():
    entries = [CitationEntry(raw="x", authors=["Smith"], year="2020", url=None, venue_type="unknown")]
    result = compute_self_citation(entries, None)
    assert result.ratio is None


def test_self_citation_ratio_computed_when_byline_given():
    entries = [
        CitationEntry(raw="Smith, J. (2020). Prior work.", authors=["Smith"], year="2020", url=None, venue_type="unknown"),
        CitationEntry(raw="Jones, A. (2021). Other work.", authors=["Jones"], year="2021", url=None, venue_type="unknown"),
    ]
    result = compute_self_citation(entries, ["Smith"])
    assert result.ratio == 0.5
    assert result.n_self_cited == 1


def test_uncited_empirical_claim_flagged():
    claims = find_uncited_empirical_claims("Research shows that the intervention works. No further detail is given.")
    assert len(claims) == 1


def test_cited_empirical_claim_not_flagged():
    claims = find_uncited_empirical_claims("Research shows that the intervention works (Smith et al., 2024).")
    assert claims == []


def test_meta_framed_empirical_claim_not_flagged():
    """Regression test for a real specimen: mirror_test_v1.md lists
    "Economic studies showing low productivity impact -> 'Lag effect'"
    as an EXAMPLE of a dismissal maneuver, not as the paper's own
    empirical claim."""
    text = 'Dismissal maneuvers include: "Economic studies showing low productivity impact -> Lag effect"'
    assert find_uncited_empirical_claims(text) == []


def test_to_dict_json_safe():
    import json
    entries = parse_references("## References\n\nSmith, J. (2020). A Paper. https://arxiv.org/abs/1234\n")
    json.dumps([e.to_dict() for e in entries])  # must not raise
