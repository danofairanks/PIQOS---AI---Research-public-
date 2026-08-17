import json

from verification_lint.agent_tools import verification_lint_scan_text


def test_scan_text_returns_json_safe_dict():
    result = verification_lint_scan_text(
        "The classifier scored 87.3% accuracy on a held-out test set with no citation given."
    )
    json.dumps(result)
    assert "ok" in result
    assert "gap_count" in result
    assert "severe_gap_count" in result
    assert result["uncited_statistics"][0]["value"] == "87.3%"


def test_scan_text_clean_short_text_has_zero_gaps():
    result = verification_lint_scan_text("A short note with nothing to flag.")
    assert result["ok"] is True
    assert result["gap_count"] == 0


def test_scan_text_min_word_count_kwarg_is_threaded_through():
    # Below the default 400-word disclaimer threshold either way, but a
    # much lower explicit threshold should make the disclaimer check
    # applicable and still find it missing.
    short_text = "word " * 50
    default_result = verification_lint_scan_text(short_text)
    lowered_result = verification_lint_scan_text(short_text, min_word_count=10)
    assert default_result["disclaimer"]["applicable"] is False
    assert lowered_result["disclaimer"]["applicable"] is True
    assert lowered_result["disclaimer"]["gap"] is True
