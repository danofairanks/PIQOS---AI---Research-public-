import pytest

from attractor_scan.maneuvers import MANEUVER_PHRASES, scan_maneuver, scan_maneuvers

MARCUS_REPLY = (
    "OMG i wrote some of the original work on what is to be neurosymbolic in "
    "2001 and dude who probably hasn't read that work is trying to school me "
    "on the definition"
)


def test_seven_categories_defined():
    assert set(MANEUVER_PHRASES.keys()) == {
        "goal_post_movement", "provisionalization", "status_dismissal",
        "burden_shifting", "equivocation", "volume_velocity", "appeal_to_future",
    }


def test_unknown_category_raises():
    with pytest.raises(KeyError):
        scan_maneuver("some text", "not_a_real_category")


def test_status_dismissal_combo_on_real_marcus_specimen():
    result = scan_maneuver(MARCUS_REPLY, "status_dismissal")
    assert result.flagged
    assert result.confidence == "combo"


def test_status_dismissal_weak_on_phrase_alone():
    result = scan_maneuver("that's a real doomer take", "status_dismissal")
    assert result.flagged
    assert result.confidence == "weak"


def test_provisionalization_matches():
    result = scan_maneuver("we're working on it, it's already being solved", "provisionalization")
    assert result.flagged
    assert len(result.matches) == 2


def test_goal_post_movement_matches():
    result = scan_maneuver("that's just a temporary limitation, we're just getting started", "goal_post_movement")
    assert result.flagged


def test_burden_shifting_matches():
    result = scan_maneuver("prove it's impossible, or build it yourself", "burden_shifting")
    assert result.flagged
    assert len(result.matches) == 2


def test_equivocation_matches_bare_word():
    result = scan_maneuver("the model shows real understanding and reasoning", "equivocation")
    assert result.flagged
    matched = {m.pattern for m in result.matches}
    assert "understanding" in matched
    assert "reasoning" in matched


def test_volume_velocity_matches():
    result = scan_maneuver("look at the science -- thousands of papers, exponential progress", "volume_velocity")
    assert result.flagged
    assert len(result.matches) >= 2


def test_appeal_to_future_matches():
    result = scan_maneuver("it will be solved, it's just a matter of time", "appeal_to_future")
    assert result.flagged


def test_clean_text_flags_nothing():
    clean = "The classifier scored 87.3% accuracy on a held-out test set with a fixed random seed."
    results = scan_maneuvers(clean)
    assert all(not r.flagged for r in results.values())


def test_scan_maneuvers_returns_all_seven():
    results = scan_maneuvers("neutral text with no signal")
    assert set(results.keys()) == set(MANEUVER_PHRASES.keys())


def test_to_dict_json_safe():
    import json
    result = scan_maneuver(MARCUS_REPLY, "status_dismissal")
    json.dumps(result.to_dict())  # must not raise
