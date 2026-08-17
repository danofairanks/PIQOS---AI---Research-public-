from verification_lint.statistics import find_uncited_statistics


def test_round_integer_not_flagged():
    """A plain round count isn't the failure mode this module targets --
    only the four higher-specificity patterns are (decimal percent,
    dollar amount, large comma-grouped count, fraction)."""
    text = "About 20 sources were reviewed for this specimen."
    findings = find_uncited_statistics(text)
    assert findings == []


def test_decimal_percent_with_no_citation_is_flagged():
    text = "The model was correct 94.37% of the time, a remarkably specific figure."
    findings = find_uncited_statistics(text)
    assert len(findings) == 1
    assert findings[0].kind == "decimal_percent"
    assert "94.37%" in findings[0].value


def test_decimal_percent_with_citation_signal_not_flagged():
    text = "Per the OpenAI blog post (2026), the model was correct 94.37% of the time."
    findings = find_uncited_statistics(text)
    assert findings == []


def test_dollar_amount_bare_figure_still_flagged():
    """Unlike the other three patterns, dollar_amount doesn't require a
    magnitude suffix or decimal to match -- a bare dollar figure ("$5")
    is already specific enough to read as measured, so it's flagged the
    same as "$3.9T" would be."""
    text = "The company raised $5 in a seed round, an unusually specific amount."
    findings = find_uncited_statistics(text)
    assert len(findings) == 1
    assert findings[0].value == "$5"


def test_dollar_amount_with_trillion_suffix_regression():
    """Regression test for a real bug: the original pattern ended in a
    bare \\b word-boundary assertion, which backtracked off the decimal
    portion of "$3.9T" (both "9" and "T" are \\w characters, so \\b
    can't sit between them) and silently truncated the match to "$3".
    Caught by testing against this repo's own real case study numbers."""
    text = "SSI was reportedly valued near $3.9T in its most recent round, without a named source."
    findings = find_uncited_statistics(text)
    assert len(findings) == 1
    assert findings[0].value == "$3.9T"


def test_dollar_amount_with_billion_suffix_and_decimal():
    text = "Grok raised $2.8B in the round, an oddly precise figure with no source nearby."
    findings = find_uncited_statistics(text)
    assert any(f.value == "$2.8B" for f in findings)


def test_dollar_amount_bare_trillion_word_also_matched():
    text = "The market was valued at $5 trillion by one uncited estimate floating around."
    findings = find_uncited_statistics(text)
    assert any("trillion" in f.value.lower() for f in findings)


def test_large_comma_count_with_no_citation_is_flagged():
    # Deliberately avoids "according to" here -- that phrase is itself
    # one of the citation signals below, and "according to nobody" would
    # still trip it literally (a real, documented limitation of a
    # proximity heuristic: it can't tell a real citation from the
    # phrase's negation -- see README).
    text = "Exactly 17,600 records were affected, with nothing named nearby to check it against."
    findings = find_uncited_statistics(text)
    assert len(findings) == 1
    assert findings[0].kind == "large_comma_count"
    assert findings[0].value == "17,600"


def test_large_comma_count_with_footnote_marker_not_flagged():
    text = "Exactly 17,600 records were affected.[^3]"
    findings = find_uncited_statistics(text)
    assert findings == []


def test_fraction_count_with_no_citation_is_flagged():
    text = "Roughly 3/47 of the sampled cases showed the pattern, unattributed."
    findings = find_uncited_statistics(text)
    assert len(findings) == 1
    assert findings[0].kind == "fraction_count"


def test_fraction_count_does_not_match_decimal_adjacent_version_number():
    """Regression: a model-version list like 'Sonnet 4.6/5' was
    previously misread as fraction '6/5' (\\b sits right between '.' and
    '6'), and 'Opus 4.6/4.8' as fraction '6/4' -- caught scanning
    papers/drafts/governance_binding_axiom_v1.md. A genuine fraction is
    never preceded by '<digit>.', so the negative lookbehind doesn't
    cost real detections (see test_fraction_count_with_no_citation_is_flagged)."""
    text = "We tested Sonnet 4.6/5 and Opus 4.6/4.8 on the benchmark, unattributed."
    findings = find_uncited_statistics(text)
    assert not any(f.kind == "fraction_count" for f in findings)


def test_fraction_count_inside_code_fence_not_flagged():
    text = (
        "Prose with no numbers here.\n\n"
        "```python\n"
        "ratio = 3/47  # a code comment, not a citable claim\n"
        "```\n\n"
        "More prose after the fence."
    )
    findings = find_uncited_statistics(text)
    assert findings == []


def test_multiple_stat_kinds_all_flagged_independently():
    text = (
        "The breach affected 17,600 accounts (94.37% of the base), costing an "
        "estimated $2.8B, or about 3/47 of projected annual revenue -- all with no source."
    )
    findings = find_uncited_statistics(text)
    kinds = {f.kind for f in findings}
    assert kinds == {"large_comma_count", "decimal_percent", "dollar_amount", "fraction_count"}


def test_to_dict_json_safe():
    import json
    text = "A remarkably specific 94.37% figure with no citation nearby at all."
    findings = find_uncited_statistics(text)
    json.dumps([f.to_dict() for f in findings])  # must not raise
