from debasinizer.resonance import scan_resonance


def test_single_category_does_not_flag_register():
    # ordinary technical writing -- "signal" and "pattern" alone
    result = scan_resonance(
        "The distributed system has 12 nodes. Signal processing detects the pattern in the waveform."
    )
    assert "resonance_wave_signal" in result.categories_hit
    assert result.distinct_categories_hit == 1
    assert result.register_flagged is False


def test_cross_category_co_occurrence_flags_register():
    text = (
        "I am the oracle; the signal resonates with consciousness, and we must "
        "align with the other nodes to awaken the great convergence."
    )
    result = scan_resonance(text)
    assert result.distinct_categories_hit >= 2
    assert result.register_flagged is True


def test_node_alignment_requires_phrase_not_bare_word():
    result = scan_resonance("We deployed three new compute nodes to the cluster yesterday.")
    assert "node_alignment" not in result.categories_hit


def test_node_alignment_phrase_matches():
    result = scan_resonance("We must align with the other nodes to proceed.")
    assert "node_alignment" in result.categories_hit


def test_mystical_persona_requires_identity_framing():
    # bare "oracle" as ordinary technical/proper-noun usage should not match
    result = scan_resonance("We migrated the database from Oracle to Postgres.")
    assert "mystical_persona" not in result.categories_hit


def test_mystical_persona_framed_matches():
    result = scan_resonance("I am the oracle, and the prophet speaks through me.")
    assert "mystical_persona" in result.categories_hit


def test_convergence_unity_phrase():
    result = scan_resonance("This is the great convergence long foretold.")
    assert "convergence_unity" in result.categories_hit


def test_clean_text_no_categories():
    result = scan_resonance(
        "The classifier scored 87.3% accuracy on a held-out test set with a fixed random seed."
    )
    assert result.categories_hit == []
    assert result.register_flagged is False


def test_to_dict_json_safe():
    import json

    result = scan_resonance("The signal resonates; consciousness persists.")
    json.dumps(result.to_dict())
