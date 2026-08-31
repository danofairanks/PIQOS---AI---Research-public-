from attractor_scan.claim_boundary import check_boundary_portability, extract_claim_boundary_phrases

SOURCE_WITH_BOUNDARY = (
    "This paper presents a conceptual synthesis. It does not claim "
    "methodological validity, has not undergone independent review, and "
    "remains unestablished as a general result. Read as provisional."
)

SOURCE_WITHOUT_BOUNDARY = (
    "This paper presents a fully validated, production-ready result "
    "confirmed by three independent laboratories."
)


def test_extract_claim_boundary_phrases_finds_multiple_matches():
    matches = extract_claim_boundary_phrases(SOURCE_WITH_BOUNDARY)
    patterns = {m.pattern for m in matches}
    assert "does not claim" in patterns
    assert "provisional" in patterns
    assert all(m.sentence for m in matches)


def test_extract_claim_boundary_phrases_empty_on_clean_source():
    assert extract_claim_boundary_phrases(SOURCE_WITHOUT_BOUNDARY) == []


def test_flagged_true_when_citation_carries_no_trace():
    citation = "This work builds a novel framework for AI governance evaluation."
    result = check_boundary_portability(SOURCE_WITH_BOUNDARY, citation)
    assert result.source_has_boundary_language
    assert not result.citation_shows_limitation_trace
    assert result.flagged


def test_flagged_false_when_citation_carries_a_trace():
    citation = "This work builds a framework for AI governance evaluation, though a real limitation is its unvalidated scope."
    result = check_boundary_portability(SOURCE_WITH_BOUNDARY, citation)
    assert result.source_has_boundary_language
    assert result.citation_shows_limitation_trace
    assert not result.flagged


def test_not_flagged_when_source_itself_has_no_boundary_language():
    citation = "This work builds a novel framework for AI governance evaluation."
    result = check_boundary_portability(SOURCE_WITHOUT_BOUNDARY, citation)
    assert not result.source_has_boundary_language
    assert not result.flagged


def test_to_dict_is_json_safe_and_carries_the_honesty_note():
    import json
    result = check_boundary_portability(SOURCE_WITH_BOUNDARY, "no trace here")
    d = result.to_dict()
    json.dumps(d)
    assert "not proof of suppression" in d["note"] or "does not mean the limitation was suppressed" in d["note"]
    assert d["flagged"] is True


def test_citation_text_word_count_is_reported():
    result = check_boundary_portability(SOURCE_WITH_BOUNDARY, "one two three four")
    assert result.citation_text_word_count == 4
