from paper_rigor.consensus import find_unsupported_consensus_claims


def test_unsupported_consensus_claim_is_flagged():
    matches = find_unsupported_consensus_claims("It is well known that this approach works best in all cases.")
    assert len(matches) == 1


def test_consensus_claim_with_citation_not_flagged():
    matches = find_unsupported_consensus_claims("It is well known that this approach works best (see the 2023 meta-analysis).")
    assert matches == []


def test_consensus_claim_with_survey_reference_not_flagged():
    matches = find_unsupported_consensus_claims("There is broad consensus on this point, as a recent survey confirmed.")
    assert matches == []


def test_meta_framed_consensus_claim_not_flagged():
    """Regression test for a real specimen (mirror_test_v1.md, a
    Lysenkoism case study): "the absence of published criticism was
    then cited as evidence of scientific consensus" describes a
    historical fallacious move; it is not the paper's own claim of
    consensus."""
    text = "The absence of published criticism was then cited as evidence of scientific consensus."
    assert find_unsupported_consensus_claims(text) == []


def test_clean_text_flags_nothing():
    text = "Three independent studies produced conflicting results on this question."
    assert find_unsupported_consensus_claims(text) == []


def test_to_dict_json_safe():
    import json
    matches = find_unsupported_consensus_claims("Everyone agrees this is true.")
    json.dumps([m.to_dict() for m in matches])  # must not raise
