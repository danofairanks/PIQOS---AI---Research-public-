from verification_lint.sourcing import check_sourcing


def test_no_sourcing_signal_at_all():
    check = check_sourcing("A plain document with no closing sources line and no framework citation.")
    assert check.has_sources_statement is False
    assert check.has_framework_citation is False
    assert check.has_end_sourcing is False


def test_sources_colon_line_detected():
    """This project's real convention: an italic closing line naming
    every source inspected, e.g. "Sources: X post..., OpenAI's own blog
    post..." rather than inline per-claim citation."""
    text = "Some analysis body text.\n\n*Sources: the original X post, the company blog announcement.*"
    check = check_sourcing(text)
    assert check.has_sources_statement is True
    assert check.has_end_sourcing is True


def test_source_singular_also_detected():
    text = "Body text here.\n\nSource: the primary announcement thread."
    check = check_sourcing(text)
    assert check.has_sources_statement is True


def test_applies_the_framework_from_detected():
    text = "This case study applies the framework from Basin Attractors v1 (§4)."
    check = check_sourcing(text)
    assert check.has_framework_citation is True
    assert check.has_end_sourcing is True


def test_applies_the_framework_from_is_case_insensitive():
    text = "This piece Applies The Framework From the Noether-Temporal Coherence paper."
    check = check_sourcing(text)
    assert check.has_framework_citation is True


def test_word_sourced_alone_does_not_match_sources_colon_pattern():
    """The pattern requires "source(s):" with a following colon-space,
    not just the bare word "sourced" appearing anywhere -- a looser
    match would produce false positives on ordinary prose."""
    text = "This claim is well sourced and documented across three separate posts."
    check = check_sourcing(text)
    assert check.has_sources_statement is False


def test_to_dict_json_safe():
    import json
    check = check_sourcing("Sources: a, b, c.")
    json.dumps(check.to_dict())  # must not raise
