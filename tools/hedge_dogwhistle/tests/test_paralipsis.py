from hedge_dogwhistle.paralipsis import find_paralipsis


def test_im_not_saying_matches():
    matches = find_paralipsis("I'm not saying he's corrupt, but you have to wonder.")
    assert len(matches) == 1
    assert "not saying" in matches[0].text.lower()


def test_far_be_it_from_me_matches():
    matches = find_paralipsis("Far be it from me to point fingers, but the numbers are odd.")
    assert len(matches) == 1


def test_not_to_suggest_matches():
    matches = find_paralipsis("Not to suggest anything, but he left right after the meeting.")
    assert len(matches) == 1


def test_no_comment_on_whether_matches():
    matches = find_paralipsis("No comment on whether the funds were misused.")
    assert len(matches) == 1


def test_clean_text_no_matches():
    matches = find_paralipsis(
        "The quarterly results show a 12% increase in revenue year over year."
    )
    assert matches == []


def test_match_includes_containing_sentence():
    text = "He's clearly hiding something. I'm not saying he's corrupt, but you have to wonder."
    matches = find_paralipsis(text)
    assert len(matches) == 1
    assert matches[0].sentence == "I'm not saying he's corrupt, but you have to wonder."


def test_multiple_matches_in_one_text():
    text = (
        "I'm not saying it's fraud. Far be it from me to accuse anyone directly."
    )
    matches = find_paralipsis(text)
    assert len(matches) == 2


def test_make_of_that_what_you_will_not_included():
    # deliberately out of scope -- insinuation without a denial structure
    matches = find_paralipsis("The numbers are odd. Make of that what you will.")
    assert matches == []


def test_to_dict_json_safe():
    import json

    matches = find_paralipsis("I'm not saying anything, but the timing is suspicious.")
    json.dumps([m.to_dict() for m in matches])
