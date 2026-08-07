from paper_rigor.falsifiability import check_falsifiability


def test_certainty_with_no_testable_marker_is_a_gap():
    text = "This conclusively demonstrates the effect, beyond any doubt."
    check = check_falsifiability(text)
    assert check.gap is True
    assert check.has_testable_markers is False


def test_certainty_with_testable_marker_present_is_not_a_gap():
    text = ("This conclusively demonstrates the effect. We test whether the "
            "prediction holds; if the observed rate falls below 5 percent, this claim fails.")
    check = check_falsifiability(text)
    assert check.gap is False
    assert check.has_testable_markers is True


def test_no_certainty_language_is_not_a_gap_even_without_testable_markers():
    text = "The results are consistent with the hypothesis in this sample."
    check = check_falsifiability(text)
    assert check.gap is False
    assert check.certainty_claims == []


def test_to_dict_json_safe():
    import json
    check = check_falsifiability("This proves the claim beyond any doubt.")
    json.dumps(check.to_dict())  # must not raise
