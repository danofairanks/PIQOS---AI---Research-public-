from verification_lint.quotes import find_unattributed_quotes

LONG_UNATTRIBUTED = (
    "The system produces output that is completely reliable in every conceivable "
    "circumstance and situation without exception whatsoever."
)


def test_short_scare_quote_not_flagged():
    """Below the 40-char threshold -- a definitional term, not a claim
    needing attribution. This was the dominant false-positive source in
    the first draft (e.g. "neurosymbolic AI", "coding harness and tool
    calls" from the real Marcus case study)."""
    text = 'Karapetyan\'s objection to "neurosymbolic AI" is structurally the same request.'
    findings = find_unattributed_quotes(text)
    assert findings == []


def test_long_quote_with_no_nearby_signal_is_flagged():
    text = f'The report claims: "{LONG_UNATTRIBUTED}" and moves on without further comment.'
    findings = find_unattributed_quotes(text)
    assert len(findings) == 1
    assert LONG_UNATTRIBUTED in findings[0].quote


def test_quote_attributed_by_named_speaker_verb_not_flagged():
    text = f'Gary Marcus wrote: "{LONG_UNATTRIBUTED}" in a reply on X.'
    findings = find_unattributed_quotes(text)
    assert findings == []


def test_quote_attributed_by_section_citation_not_flagged():
    text = f'Checked against BIFP\'s own criteria (§3.7, Phase 5): "{LONG_UNATTRIBUTED}" and nothing else.'
    findings = find_unattributed_quotes(text)
    assert findings == []


def test_quote_attributed_by_markdown_link_not_flagged():
    text = f'Per [the source](https://example.com/post), the claim reads: "{LONG_UNATTRIBUTED}" verbatim.'
    findings = find_unattributed_quotes(text)
    assert findings == []


def test_quote_attributed_by_year_not_flagged():
    text = f'In a 2026 interview the claim was: "{LONG_UNATTRIBUTED}" without further comment.'
    findings = find_unattributed_quotes(text)
    assert findings == []


def test_repeated_quote_only_flagged_once_and_only_if_never_attributed():
    text = (
        f'First mention, attributed: Gary Marcus wrote "{LONG_UNATTRIBUTED}" on X. '
        f'Later, the same quote reappears without nearby signal: '
        + "filler " * 60 +
        f'"{LONG_UNATTRIBUTED}" is worth revisiting.'
    )
    findings = find_unattributed_quotes(text)
    # attributed once anywhere in the document -> not flagged even where it repeats unattributed
    assert findings == []


def test_two_different_unattributed_quotes_both_flagged():
    other = "A completely different substantive claim that is also long enough to count as a real quote here."
    text = f'"{LONG_UNATTRIBUTED}" appears here. Later, "{other}" appears too, both with no attribution nearby.'
    findings = find_unattributed_quotes(text)
    assert len(findings) == 2


def test_curly_quotes_also_detected():
    # Deliberately avoids the word "reads" here -- that's one of this
    # module's own attribution signals (see test_quote_attributed_by_
    # verb_reads_not_flagged below), so it would mask the thing this
    # test exists to isolate: that curly quotes are matched at all.
    text = f"The following appears verbatim with zero named source: “{LONG_UNATTRIBUTED}” and nothing more."
    findings = find_unattributed_quotes(text)
    assert len(findings) == 1


def test_quote_attributed_by_verb_reads_not_flagged():
    """"reads" is treated as an attribution verb (e.g. "the document
    reads: ...") even without a named speaker -- a deliberately loose
    signal tuned against this repo's real files. Documented here so the
    tradeoff (fewer false positives, some real gaps missed) is visible
    rather than silently encoded only in the regex."""
    text = f'The claim reads: "{LONG_UNATTRIBUTED}" and moves on without further comment.'
    findings = find_unattributed_quotes(text)
    assert findings == []


def test_to_dict_json_safe():
    import json
    text = f'"{LONG_UNATTRIBUTED}" appears with no attribution anywhere nearby at all.'
    findings = find_unattributed_quotes(text)
    json.dumps([f.to_dict() for f in findings])  # must not raise
