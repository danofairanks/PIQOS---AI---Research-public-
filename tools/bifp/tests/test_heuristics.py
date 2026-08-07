from bifp.heuristics import (
    scan_for_prohibited_anthropomorphic_terms, scan_for_provisionalization,
    scan_for_status_dismissal, scan_text,
)

MARCUS_REPLY = (
    "OMG i wrote some of the original work on what is to be neurosymbolic in "
    "2001 and dude who probably hasn't read that work is trying to school me "
    "on the definition"
)


def test_status_dismissal_catches_real_marcus_specimen_at_combo_confidence():
    """Regression check against the real, previously-analyzed specimen this
    heuristic was built to catch automatically (narrative_defense_micro_macro
    §7 in this project's private tracking, promoted as a public case study)."""
    result = scan_for_status_dismissal(MARCUS_REPLY)
    assert result.flagged
    assert result.confidence == "combo"
    patterns = {m.pattern for m in result.matches}
    assert "credential_assertion" in patterns
    assert "dismiss_interlocutor" in patterns


def test_status_dismissal_no_match_on_substantive_reply():
    substantive = (
        "The original 2001 definition required a symbolic reasoning component "
        "with an explicit rule set, not just tool-calling. Here's the section "
        "of the paper where I define that, and here's why a coding harness "
        "doesn't satisfy it: [technical argument follows]."
    )
    result = scan_for_status_dismissal(substantive)
    assert not result.flagged
    assert result.confidence == "none"


def test_status_dismissal_weak_confidence_on_phrase_alone():
    text = "That's just a hot take, not a real argument."
    result = scan_for_status_dismissal(text)
    assert result.flagged
    assert result.confidence == "weak"


def test_provisionalization_matches_seed_phrases():
    text = "We're working on it and it's already being solved in the next release."
    result = scan_for_provisionalization(text)
    assert result.flagged
    assert result.confidence == "weak"
    assert len(result.matches) >= 2


def test_provisionalization_no_match_on_clean_text():
    result = scan_for_provisionalization("Here is the completed benchmark result.")
    assert not result.flagged


def test_anthropomorphic_terms_flags_unqualified_verbs():
    text = "The model understands the user's intent and believes the answer is correct."
    result = scan_for_prohibited_anthropomorphic_terms(text)
    assert result.flagged
    matched = {m.matched_text.lower() for m in result.matches}
    assert "understands" in matched
    assert "believes" in matched


def test_anthropomorphic_terms_no_match_on_clean_text():
    result = scan_for_prohibited_anthropomorphic_terms("The classifier's output layer produced a score of 0.87.")
    assert not result.flagged


def test_scan_text_runs_all_scanners():
    results = scan_text(MARCUS_REPLY)
    assert set(results.keys()) == {"provisionalization", "status_dismissal", "prohibited_anthropomorphic_terms"}
    assert results["status_dismissal"].flagged


def test_heuristic_result_to_dict_is_json_safe():
    import json
    result = scan_for_status_dismissal(MARCUS_REPLY)
    text = json.dumps(result.to_dict())
    assert "combo" in text
