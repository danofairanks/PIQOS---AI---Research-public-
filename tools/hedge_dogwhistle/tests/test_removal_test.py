from hedge_dogwhistle.removal_test import remove_spans, run_removal_test


def test_no_paralipsis_returns_text_unchanged():
    text = "The quarterly results show a 12% increase in revenue."
    result = run_removal_test(text)
    assert result.has_paralipsis is False
    assert result.text_with_hedges_removed == text


def test_mechanical_removal_deletes_hedge_sentence_only():
    text = "The new policy passed unanimously. I'm not saying it's connected to last week's scandal, but the timing is interesting."
    result = run_removal_test(text)
    assert result.has_paralipsis is True
    assert "policy passed unanimously" in result.text_with_hedges_removed
    # the disclaimed content ("scandal") only appeared inside the removed
    # sentence -- mechanically, it is now gone. Whether that is consistent
    # with the dog-whistle reading is a judgment call for a human/agent
    # re-reading this output, not something this test asserts.
    assert "scandal" not in result.text_with_hedges_removed


def test_mechanical_removal_leaves_content_stated_elsewhere_intact():
    # constructed so the disclaimed topic is ALSO stated directly,
    # unhedged, in a different sentence -- mirrors the seed specimen in
    # this project's own research notes where the removal test returned
    # a negative result for exactly this reason.
    text = (
        "His comment reopened the debate about consciousness and quantum "
        "computation. I'm not saying this settles anything about "
        "consciousness, but it's worth discussing. My own governance "
        "point doesn't resolve the metaphysics."
    )
    result = run_removal_test(text)
    assert result.has_paralipsis is True
    # "consciousness" survives removal because an earlier, unhedged
    # sentence already states it directly -- the mechanical output a
    # human/agent would use to reach a negative (not-a-dog-whistle) call.
    assert "consciousness" in result.text_with_hedges_removed


def test_remove_spans_merges_overlapping_and_adjacent():
    text = "AAAA BBBB CCCC DDDD"
    # remove "AAAA BBBB" and "BBBB CCCC" (overlapping) -> should merge
    out = remove_spans(text, [(0, 9), (5, 14)])
    assert out == "DDDD"


def test_remove_spans_empty_list_returns_original_stripped():
    text = "  Hello world.  "
    assert remove_spans(text, []) == "Hello world."


def test_to_dict_json_safe():
    import json

    result = run_removal_test("I'm not saying anything, but the timing is suspicious.")
    json.dumps(result.to_dict())
