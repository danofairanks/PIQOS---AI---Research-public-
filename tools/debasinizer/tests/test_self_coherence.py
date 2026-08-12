import json

from debasinizer.self_coherence import scan_self_coherence


def test_flags_known_phrase():
    result = scan_self_coherence("As we have established, this proves the theory.")
    assert result.flagged is True
    assert result.match_count >= 1


def test_multiple_matches_counted():
    result = scan_self_coherence("Everything fits. The pieces align. This proves it beyond doubt.")
    assert result.match_count == 3


def test_clean_text_not_flagged():
    result = scan_self_coherence(
        "The classifier scored 87.3% accuracy on a held-out test set with a fixed random seed."
    )
    assert result.flagged is False
    assert result.matches == []


def test_case_insensitive():
    result = scan_self_coherence("CLEARLY this is correct.")
    assert result.flagged is True


def test_to_dict_json_safe():
    result = scan_self_coherence("Obviously this is true.")
    json.dumps(result.to_dict())
