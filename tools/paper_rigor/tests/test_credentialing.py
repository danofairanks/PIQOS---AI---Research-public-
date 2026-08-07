from paper_rigor.credentialing import find_credential_substitution


def test_credential_with_no_evidence_nearby_is_flagged():
    text = "As a renowned expert with over 20 years of experience, I can confirm this is safe."
    matches = find_credential_substitution(text)
    assert len(matches) >= 1


def test_credential_with_citation_nearby_not_flagged():
    text = "Dr. Smith, a leading expert in immunology, reported the finding (Smith et al., 2024)."
    assert find_credential_substitution(text) == []


def test_credential_with_percentage_evidence_nearby_not_flagged():
    text = "As a professor of statistics, I note the effect size was 42.1% in this sample."
    assert find_credential_substitution(text) == []


def test_clean_text_flags_nothing():
    text = "The experiment measured the effect directly under controlled conditions."
    assert find_credential_substitution(text) == []


def test_to_dict_json_safe():
    import json
    matches = find_credential_substitution("As a Nobel laureate, I assure you this is correct.")
    json.dumps([m.to_dict() for m in matches])  # must not raise
