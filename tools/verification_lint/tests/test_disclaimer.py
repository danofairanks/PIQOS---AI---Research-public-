from verification_lint.disclaimer import check_disclaimer

LONG_BODY_NO_DISCLAIMER = " ".join(["word"] * 450)
LONG_BODY_WITH_DISCLAIMER = LONG_BODY_NO_DISCLAIMER + " This case study does not claim anything beyond what is shown."
LONG_BODY_WITH_TRACKER_PHRASING = LONG_BODY_NO_DISCLAIMER + " What this tracker does NOT yet establish is discussed below."


def test_short_document_not_applicable():
    check = check_disclaimer("A short note, no formal scoping needed here.")
    assert check.applicable is False
    assert check.gap is False


def test_long_document_with_no_disclaimer_is_a_gap():
    check = check_disclaimer(LONG_BODY_NO_DISCLAIMER)
    assert check.applicable is True
    assert check.present is False
    assert check.gap is True


def test_long_document_with_case_study_style_disclaimer_not_a_gap():
    check = check_disclaimer(LONG_BODY_WITH_DISCLAIMER)
    assert check.present is True
    assert check.gap is False


def test_long_document_with_tracker_style_disclaimer_not_a_gap():
    """Grounded in the real second phrasing used in this repo:
    papers/published/conjecture_tracker_v1.md's "What this tracker does
    NOT yet establish" heading, distinct from the case-study heading."""
    check = check_disclaimer(LONG_BODY_WITH_TRACKER_PHRASING)
    assert check.present is True
    assert check.gap is False


def test_min_word_count_is_configurable():
    text = " ".join(["word"] * 50)
    check_default = check_disclaimer(text)
    assert check_default.applicable is False
    check_lowered = check_disclaimer(text, min_word_count=10)
    assert check_lowered.applicable is True
    assert check_lowered.gap is True


def test_word_count_reported_accurately():
    check = check_disclaimer(LONG_BODY_NO_DISCLAIMER)
    assert check.word_count == 450
    assert check.min_word_count == 400


def test_to_dict_json_safe():
    import json
    check = check_disclaimer(LONG_BODY_NO_DISCLAIMER)
    json.dumps(check.to_dict())  # must not raise
