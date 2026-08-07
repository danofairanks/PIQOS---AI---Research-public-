from paper_rigor.disclaimer import check_limitations_section

LONG_BODY = " ".join(["word"] * 450)


def test_short_document_not_applicable():
    check = check_limitations_section("A short note.")
    assert check.applicable is False
    assert check.gap is False


def test_long_document_with_neither_signal_is_a_gap():
    check = check_limitations_section(LONG_BODY)
    assert check.gap is True
    assert check.has_inline_phrase is False
    assert check.has_heading_section is False


def test_inline_phrase_signal_reused_from_verification_lint():
    text = LONG_BODY + " This paper does not claim anything beyond what is shown."
    check = check_limitations_section(text)
    assert check.has_inline_phrase is True
    assert check.gap is False


def test_limitations_heading_signal_recognized():
    """Regression test for a real specimen: protocols/noether_coherence_
    test_protocol_v1.md has a full "## 10. LIMITATIONS AND SCOPE
    CAVEATS" section that verification_lint's inline-phrase-only check
    (tuned for a different, narrower house convention) does not
    recognize -- this heading check is what closes that gap."""
    text = LONG_BODY + "\n\n## 10. LIMITATIONS AND SCOPE CAVEATS\n\nSome caveats here."
    check = check_limitations_section(text)
    assert check.has_heading_section is True
    assert check.has_inline_phrase is False
    assert check.gap is False


def test_bare_limitations_heading_recognized():
    text = LONG_BODY + "\n\n## Limitations\n\nSome caveats here."
    check = check_limitations_section(text)
    assert check.has_heading_section is True


def test_threats_to_validity_heading_recognized():
    text = LONG_BODY + "\n\n## Threats to Validity\n\nSome caveats here."
    check = check_limitations_section(text)
    assert check.has_heading_section is True


def test_to_dict_json_safe():
    import json
    check = check_limitations_section(LONG_BODY)
    json.dumps(check.to_dict())  # must not raise
