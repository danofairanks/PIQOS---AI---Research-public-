from paper_rigor.placeholders import find_placeholder_issues


def test_hand_wave_phrase_is_flagged():
    result = find_placeholder_issues("It is trivial to show the model is correct.")
    kinds = [g.kind for g in result["gaps"]]
    assert "hand_wave" in kinds


def test_unlabeled_marker_is_flagged():
    result = find_placeholder_issues("TODO: insert benchmark numbers here.")
    kinds = [g.kind for g in result["gaps"]]
    assert "unlabeled_marker" in kinds


def test_references_would_include_is_flagged():
    """Regression test for a real specimen: a References section whose
    entire content was "[References would include citations to LeCun
    papers, ...]" -- describing what a bibliography would contain
    instead of containing one, while the body cited specific dated
    statements as if sourced. Found in a known-fabricated private-repo
    paper already flagged by this project's own living_research_policy.md."""
    text = "## References\n\n[References would include citations to relevant papers.]"
    result = find_placeholder_issues(text)
    phrases = [g.phrase for g in result["gaps"]]
    assert any("would include" in p for p in phrases)


def test_honest_labeled_placeholder_not_counted_as_gap():
    text = "This value is EMPIRICAL_FILL_IN, pending calibration on real hardware."
    result = find_placeholder_issues(text)
    assert result["gaps"] == []
    assert len(result["labeled"]) == 2  # EMPIRICAL_FILL_IN + "pending calibration"


def test_clean_text_flags_nothing():
    text = "We measured the effect directly and report the confidence interval below."
    result = find_placeholder_issues(text)
    assert result["gaps"] == []
    assert result["labeled"] == []


def test_to_dict_json_safe():
    import json
    result = find_placeholder_issues("It is trivial to show this. TODO: cite source.")
    json.dumps([g.to_dict() for g in result["gaps"]])  # must not raise
