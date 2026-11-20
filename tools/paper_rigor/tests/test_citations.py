"""Citation parsing is validated against this repo's own real
`papers/published/basin_attractors_v1.md` References section (81
entries, APA-ish, blank-line-separated, mixed academic/legal/GitHub-
issue/self-published entry shapes) as ground truth, not just
constructed examples.
"""

from pathlib import Path

import pytest

from paper_rigor.citations import (
    CitationEntry, check_citability_claim, compute_self_citation, compute_venue_mix,
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


LONG_BODY = " ".join(["word"] * 450)


def test_citability_claim_with_zero_references_is_a_gap():
    """Regression test for a real, previously-unseen specimen (an
    ~86KB / ~12,000-word paper structured as a raw page-scan dump, no
    References heading anywhere) that asserted "the reference to base
    papers on Zenodo under Stephen Hope's authorship indicate the
    framework's grounding in documented, citable research" while
    containing zero actual references."""
    text = LONG_BODY + " The framework's grounding in documented, citable research is extensive."
    check = check_citability_claim(text, references=[])
    assert check.claims_citability is True
    assert check.gap is True


def test_citability_claim_with_real_references_not_a_gap():
    text = LONG_BODY + " This work is grounded in documented research."
    entries = parse_references("## References\n\nSmith, J. (2020). A Paper. https://arxiv.org/abs/1234\n")
    check = check_citability_claim(text, references=entries)
    assert check.claims_citability is True
    assert check.n_references == 1
    assert check.gap is False


def test_no_citability_claim_and_zero_references_not_a_gap():
    """Plenty of real, honest documents have no references section and
    never claim to -- that's not contradictory, so it's not flagged."""
    check = check_citability_claim(LONG_BODY, references=[])
    assert check.claims_citability is False
    assert check.gap is False


def test_short_document_not_applicable_even_with_claim_and_zero_refs():
    check = check_citability_claim("Documented, citable research supports this.", references=[])
    assert check.applicable is False
    assert check.gap is False


def test_third_party_peer_reviewed_label_not_flagged():
    """Regression test for a real false-positive risk found while
    designing this check: mirror_test_v1.md has a table row labeling a
    THIRD PARTY's paper '"Sparks of AGI" (Bubeck et al.) | Peer-reviewed
    totalization' -- describing someone else's work, not this
    document's own grounding. The narrower, self-referential phrase set
    ("citable research", "grounded in ... research") deliberately
    excludes a bare "peer-reviewed" match for this reason."""
    text = LONG_BODY + ' | "Sparks of AGI" (Bubeck et al.) | Peer-reviewed totalization |'
    check = check_citability_claim(text, references=[])
    assert check.claims_citability is False


def test_citability_claim_to_dict_json_safe():
    import json
    check = check_citability_claim(LONG_BODY + " citable research", references=[])
    json.dumps(check.to_dict())  # must not raise


# ---- reading-order (PDF-extracted) reference lists and parse reporting ----
# Constructed fixtures only; the real-document tests above are untouched.

from paper_rigor.citations import ReferenceParse, extract_references_section, parse_references_detailed


def _reading_order_doc(n_entries=12, with_page_noise=True):
    body = "Introduction\n\n" + " ".join(["Some body sentence about the topic."] * 60) + "\n\nReferences\n"
    entries = []
    for i in range(n_entries):
        name = ["Alder", "Brandt", "Castillo", "Dvorak", "Eriksen", "Fontaine"][i % 6]
        entries.append(
            f"A. {name}, B. Other{i}, and C. Third{i}. A study of topic number {i} in\n"
            f"constructed settings. Journal of Examples, {10 + i}:{100 + i}-{120 + i}, {2015 + (i % 8)}."
        )
        if with_page_noise and i % 4 == 3:
            entries.append(f"\n{20 + i}\n\n\x0cRunning Header Of The Paper\n")
    return body + "\n".join(entries) + "\n"


def test_bare_references_line_is_found_when_no_heading_is_detected():
    doc = _reading_order_doc()
    section = extract_references_section(doc)
    assert section is not None
    assert "Alder" in section and "Introduction" not in section


def test_bare_references_uses_last_occurrence_not_a_table_of_contents_line():
    doc = "Contents\nReferences\n\n" + _reading_order_doc()
    section = extract_references_section(doc)
    assert section is not None and section.lstrip().startswith("A. Alder")


def test_reading_order_entries_are_split_by_line_end_heuristic():
    entries, info = parse_references_detailed(_reading_order_doc(n_entries=12))
    assert info.section_found and info.mode == "line_heuristic"
    assert info.n_entries == len(entries) == 12
    assert info.warning and "approximate" in info.warning
    assert "Running Header" not in " ".join(e.raw for e in entries)


def test_reading_order_initials_first_authors_and_year_are_recovered():
    entries, _ = parse_references_detailed(_reading_order_doc(n_entries=12))
    first = entries[0]
    assert first.authors[:3] == ["Alder", "Other0", "Third0"]
    assert first.year == "2015"


def test_self_citation_ratio_works_on_reading_order_list():
    entries, _ = parse_references_detailed(_reading_order_doc(n_entries=12))
    result = compute_self_citation(entries, ["Alder"])
    assert result.n_references == 12 and result.n_self_cited == 2


def test_blank_line_lists_keep_original_behaviour_and_no_warning():
    doc = ("# Paper\n\n" + " ".join(["Body sentence."] * 120) + "\n\n## References\n\n"
           "Smith, J. (2020). A title. Journal. https://doi.org/10.1/x\n\n"
           "Jones, K. & Lee, M. (2021). Another title. Venue.\n")
    entries, info = parse_references_detailed(doc)
    assert info.mode == "blank_line" and info.warning is None and len(entries) == 2
    assert entries[1].authors == ["Jones", "Lee"]
    assert parse_references(doc)[0].raw == entries[0].raw


def test_blank_line_entries_do_not_get_initials_first_authors_guessed():
    doc = ("# Paper\n\n" + " ".join(["Body sentence."] * 120) + "\n\n## References\n\n"
           "A. Smith. Some Title. Journal of Things, 2020.\n\n"
           "B. Jones. Another Title. Journal of Things, 2021.\n")
    entries, info = parse_references_detailed(doc)
    assert info.mode == "blank_line"
    assert all(e.authors == [] for e in entries)  # original strictness: not guessed


def test_missing_references_in_a_long_text_warns_that_ratios_are_unavailable():
    doc = " ".join(["A sentence of plain prose."] * 200)
    entries, info = parse_references_detailed(doc)
    assert entries == [] and info.section_found is False
    assert info.warning and "unavailable" in info.warning


def test_missing_references_in_a_short_text_does_not_warn():
    _, info = parse_references_detailed("A short note with no bibliography.")
    assert info.warning is None


def test_section_found_but_empty_warns():
    doc = " ".join(["Body sentence."] * 120) + "\n\nReferences\n\n"
    entries, info = parse_references_detailed(doc)
    assert entries == [] and info.section_found is True and "unavailable" in (info.warning or "")


def test_reference_parse_to_dict_roundtrip():
    info = ReferenceParse(section_found=True, n_entries=3, mode="blank_line", warning=None)
    assert info.to_dict() == {"section_found": True, "n_entries": 3, "mode": "blank_line", "warning": None,
                              "highest_cited_number": None}


# ---- numbered "[n]" reference lists, under-split warning, reference-heading choice ----
# Constructed fixtures only.

def _numbered_doc(n=14, cited_up_to=None, table_after=True, smallcaps=True, noise=True):
    cited = cited_up_to or n
    body_sentences = []
    for i in range(1, cited + 1):
        body_sentences.append(f"Prior work reports a related effect [{i}] in a constructed setting.")
    body = "Introduction\n\n" + " ".join(body_sentences) + " " + " ".join(["More body prose here."] * 80)
    lines = ["\n\nReferences\n"]
    for i in range(1, n + 1):
        if smallcaps:
            names = f"[{i}] A LDER , A., VAN B ROEK , N., AND C ASTILLO , M. "
        else:
            names = f"[{i}] A. Alder, N. Van Broek, and M. Castillo. "
        lines.append(names + f"A study of constructed topic number {i}. Proceedings of Examples\n(Somewhere Place, {2015 + i % 8}), pp. 1-{10 + i}.")
        if noise and i % 5 == 0:
            lines.append(f"\n{20 + i}\n\n\x0cRunning Header Of The Paper\n")
    out = body + "\n".join(lines)
    if table_after:
        out += "\n\nTable 9: Something else\n[3] Row label that also starts with a bracketed number\n[1] another table row\n"
    return out


def test_numbered_list_is_split_on_markers_and_stops_at_a_table():
    entries, info = parse_references_detailed(_numbered_doc(n=16))
    assert info.mode == "numbered" and info.n_entries == len(entries) == 16
    assert info.warning is None
    assert info.highest_cited_number == 16
    assert "Row label" not in " ".join(e.raw for e in entries)
    assert "Running Header" not in " ".join(e.raw for e in entries)


def test_numbered_smallcaps_authors_are_recovered_for_self_citation():
    entries, _ = parse_references_detailed(_numbered_doc(n=12))
    assert entries[0].authors[:3] == ["Alder", "Broek", "Castillo"]
    result = compute_self_citation(entries, ["Broek"])
    assert result.n_references == 12 and result.n_self_cited == 12


def test_numbered_title_case_initials_first_authors_work_too():
    entries, _ = parse_references_detailed(_numbered_doc(n=12, smallcaps=False))
    assert entries[0].authors[:3] == ["Alder", "Broek", "Castillo"]


def test_under_split_list_warns_that_the_ratio_is_unreliable():
    # the text cites up to [30] but only 8 unnumbered entries exist
    body = "Introduction\n\n" + " ".join(f"A claim [{i}] is made here." for i in range(1, 31)) + " " + " ".join(["Body."] * 80)
    refs = "\n\nReferences\n\n" + "\n\n".join(f"Smith, J. ({2000 + i}). Title {i}. Journal." for i in range(8))
    entries, info = parse_references_detailed(body + refs)
    assert len(entries) == 8 and info.highest_cited_number == 30
    assert info.warning and "under-split" in info.warning


def test_no_under_split_warning_when_counts_agree_or_few_bracket_numbers_seen():
    entries, info = parse_references_detailed(_numbered_doc(n=16))
    assert info.warning is None
    short_body = "Introduction\n\n" + " ".join(["Body sentence with one cite [2]."] * 60)
    refs = "\n\nReferences\n\nSmith, J. (2020). T. Journal.\n\nJones, K. (2021). U. Venue.\n"
    _, info2 = parse_references_detailed(short_body + refs)
    assert info2.warning is None


def test_bare_references_column_header_before_the_real_list_does_not_win():
    doc = (_numbered_doc(n=14, table_after=False).replace(
        "Introduction\n\n", "Introduction\n\nTable 1: Something\nReferences\n[7, 9, 12]\n[3, 4]\nmore table text\n\n", 1))
    entries, info = parse_references_detailed(doc)
    assert info.mode == "numbered" and len(entries) == 14


def test_highest_cited_number_handles_lists_and_ranges():
    from paper_rigor.citations import _highest_bracketed_citation
    hi, n = _highest_bracketed_citation("see [3, 7] and [10-12] and [45]")
    assert hi == 45 and n == 6
