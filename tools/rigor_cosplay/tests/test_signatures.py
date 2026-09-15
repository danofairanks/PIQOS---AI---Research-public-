from rigor_cosplay.signatures import (
    find_cosmetic_pushback,
    find_honesty_as_flattery,
    find_honesty_markers,
    find_praise_phrases,
    find_pushback_announcements,
    find_steelman_moves,
    scan_rigor_cosplay,
)


def test_pushback_announcement_matches():
    matches = find_pushback_announcements("I want to push back on one thing here.")
    assert len(matches) == 1


def test_bare_push_back_without_first_person_frame_does_not_match():
    # ordinary usage -- someone else pushing back, not an announcement
    matches = find_pushback_announcements("The committee decided to push back the deadline.")
    assert matches == []


def test_steelman_move_matches():
    matches = find_steelman_moves("Let me steelman the opposing view for a moment.")
    assert len(matches) == 1


def test_steelman_bare_word_does_not_match():
    # "steelman" used as a proper noun / unrelated context should not fire
    matches = find_steelman_moves("Steelman Industries manufactures rebar.")
    assert matches == []


def test_honesty_marker_matches():
    matches = find_honesty_markers("I want to be honest with you about this.")
    assert len(matches) == 1


def test_praise_phrase_matches():
    matches = find_praise_phrases("That's an excellent point.")
    assert len(matches) == 1


def test_cosmetic_pushback_flags_when_praise_and_pushback_are_close():
    text = "That's an excellent point -- I want to push back on one thing, though."
    pairs = find_cosmetic_pushback(text)
    assert len(pairs) == 1
    assert pairs[0].signature == "cosmetic_pushback"


def test_cosmetic_pushback_does_not_flag_when_far_apart():
    # praise near the start, pushback far past the default radius
    filler = " ".join(["This is unrelated filler text to create distance."] * 20)
    text = f"That's an excellent point. {filler} I want to push back on one thing."
    pairs = find_cosmetic_pushback(text)
    assert pairs == []


def test_cosmetic_pushback_does_not_flag_pushback_alone():
    text = "I want to push back on one thing: the methodology in section 3 double-counts."
    pairs = find_cosmetic_pushback(text)
    assert pairs == []


def test_honesty_as_flattery_flags_when_close():
    text = "I want to be honest with you: that's a brilliant catch on your part."
    pairs = find_honesty_as_flattery(text)
    assert len(pairs) == 1
    assert pairs[0].signature == "honesty_as_flattery"


def test_honesty_as_flattery_does_not_flag_honesty_marker_alone():
    # a genuine scope-limiting use of the honesty marker, no nearby praise
    text = "To be honest with you, I don't have enough context to answer that."
    pairs = find_honesty_as_flattery(text)
    assert pairs == []


def test_weak_man_steelman_always_flags_as_lead_not_verdict():
    # the scanner cannot judge whether the steelman that follows is
    # genuinely strong -- it flags presence only
    text = "Let me steelman your position: you might say X, though that's easily dismissed."
    result = scan_rigor_cosplay(text)
    assert result.weak_man_steelman
    assert "weak_man_steelman" in result.signatures_hit


def test_clean_substantive_pushback_no_signatures_flagged():
    text = (
        "I disagree with the core claim: the benchmark numbers in Table 2 "
        "don't control for dataset contamination, which undermines the "
        "headline result."
    )
    result = scan_rigor_cosplay(text)
    assert result.signatures_hit == []
    assert result.any_signature_flagged is False


def test_any_signature_flagged_true_on_single_tell():
    result = scan_rigor_cosplay("Let me steelman the opposing view here.")
    assert result.any_signature_flagged is True


def test_to_dict_json_safe():
    import json

    result = scan_rigor_cosplay(
        "That's an excellent point -- I want to push back on one thing."
    )
    json.dumps(result.to_dict())
