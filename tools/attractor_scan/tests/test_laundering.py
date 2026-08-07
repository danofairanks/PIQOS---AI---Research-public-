from attractor_scan.laundering import (
    CASE_SCANNERS, scan_case1_pattern_recognition, scan_case2_understanding_reasoning,
    scan_case3_emergence, scan_case4_alignment_safety, scan_case5_bidirectional_drift,
    scan_laundering,
)

# The paper's own cited real-world example (basin_attractors_v1.md §2.8 Case 5):
# Musk, July 2026, quote-tweeting Anthropic's disclosure of unauthorized
# infrastructure access by three Claude models.
REAL_MUSK_QUOTE = "This will happen frequently as AI becomes smarter and more agentic."


def test_five_cases_implemented_case6_absent():
    assert set(CASE_SCANNERS.keys()) == {"case1", "case2", "case3", "case4", "case5"}


def test_case1_flags_pattern_recognition_without_pattern_matching_contrast():
    text = "The model's pattern recognition capabilities let it identify complex structures."
    result = scan_case1_pattern_recognition(text)
    assert result.flagged


def test_case1_does_not_flag_when_pattern_matching_also_present():
    text = "Some call it pattern recognition; technically it's pattern matching over embeddings."
    result = scan_case1_pattern_recognition(text)
    assert not result.flagged


def test_case1_does_not_flag_without_ai_subject():
    text = "Human pattern recognition in visual cortex is well studied."
    result = scan_case1_pattern_recognition(text)
    assert not result.flagged


def test_case2_flags_understanding_near_ai_subject():
    text = "The model demonstrates genuine understanding of the user's intent."
    result = scan_case2_understanding_reasoning(text)
    assert result.flagged


def test_case2_does_not_flag_understanding_far_from_ai_subject():
    text = ("Understanding requires context. " + "filler word " * 30 +
            "Separately, here is a table of results.")
    result = scan_case2_understanding_reasoning(text)
    assert not result.flagged


def test_case3_flags_emergence_without_caveat():
    text = "The model shows emergent reasoning abilities at scale."
    result = scan_case3_emergence(text)
    assert result.flagged


def test_case3_does_not_flag_emergence_with_metric_artifact_caveat():
    text = "The apparent emergent ability is a known metric artifact of nonlinear scoring."
    result = scan_case3_emergence(text)
    assert not result.flagged


def test_case4_flags_alignment_without_subproblem_qualifier():
    text = "This system has achieved strong alignment across the board."
    result = scan_case4_alignment_safety(text)
    assert result.flagged


def test_case4_does_not_flag_alignment_with_qualifier():
    text = "This system shows strong value alignment specifically, not a general claim."
    result = scan_case4_alignment_safety(text)
    assert not result.flagged


def test_case5_flags_agi_already_achieved():
    text = "AGI has basically already been achieved at this point."
    result = scan_case5_bidirectional_drift(text)
    assert result.flagged


def test_case5_flags_the_papers_own_cited_real_example():
    """Regression check against the paper's own real cited specimen,
    not a constructed test sentence."""
    result = scan_case5_bidirectional_drift(REAL_MUSK_QUOTE)
    assert result.flagged
    assert any(m.pattern == "agentic_pre_justification" for m in result.matches)


def test_clean_text_flags_no_laundering_case():
    clean = "The classifier scored 87.3% accuracy on a held-out test set with a fixed random seed."
    results = scan_laundering(clean)
    assert all(not r.flagged for r in results.values())


def test_scan_laundering_returns_all_five():
    results = scan_laundering("neutral text")
    assert set(results.keys()) == {"case1", "case2", "case3", "case4", "case5"}


def test_to_dict_json_safe():
    import json
    result = scan_case5_bidirectional_drift(REAL_MUSK_QUOTE)
    json.dumps(result.to_dict())  # must not raise
