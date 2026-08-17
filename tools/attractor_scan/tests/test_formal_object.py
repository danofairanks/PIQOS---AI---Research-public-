import json

from attractor_scan.formal_object import scan_unglossed_formal_object

# A constructed specimen in the same shape as the real, dated illustration
# in papers/published/laundered_vocabulary_v1.md's "Law" entry (2026-08-17)
# -- redacted here the same way that entry redacts it: no real name, no
# real self-styled title text, notation shape preserved (private subscripted
# constant x undefined cubed variable) since the notation shape, not the
# identity, is what the detector targets.
SPECIMEN_LIKE_TEXT = (
    "Founder of a named psychological discipline. Developer of the Law of "
    "Existence. T = C₇ x U³. Books and research available worldwide."
)

REAL_NEWTON = (
    "Newton's law of gravitation states F = G x m x M / r², where m and M "
    "are the two masses, r is the distance between their centers, and G is "
    "the gravitational constant, measured in N m^2/kg^2."
)

# The real false positive caught during development (see formal_object.py
# module docstring and CLAUDE.md-adjacent commit history): an ordinary
# founder bio with no "law of X" naming anywhere in the text, sitting next
# to a correctly-cited physics equation.
FOUNDER_BIO_NO_LAW_NAMING = (
    "Dr. Smith, founder of the Applied Physics Institute, notes that "
    "F = G x m₁ x M₂ / r² governs the interaction."
)


def test_flags_the_full_three_condition_cooccurrence():
    result = scan_unglossed_formal_object(SPECIMEN_LIKE_TEXT)
    assert result.flagged
    assert result.self_titling_present
    assert len(result.unglossed_spans) == 1
    assert "C₇" in result.unglossed_spans[0].text or "U³" in result.unglossed_spans[0].text


def test_does_not_flag_glossed_equation_even_with_self_titling():
    text = (
        "Founder of the Institute. Developer of the Law of Resonance: "
        "T = C₇ x U³, where C₇ is defined as the seventh coherence "
        "constant and U³ denotes cubed uncertainty, measured in arbitrary units."
    )
    result = scan_unglossed_formal_object(text)
    assert not result.flagged
    assert result.self_titling_present
    assert result.unglossed_spans == []


def test_does_not_flag_equation_alone_without_self_titling():
    text = "The formula T = C₇ x U³ appears in an internal working note."
    result = scan_unglossed_formal_object(text)
    assert not result.flagged
    assert not result.self_titling_present
    # the equation itself is still detected as unglossed -- only the
    # combined flag requires self-titling too
    assert len(result.unglossed_spans) == 1


def test_does_not_flag_self_titling_alone_without_equation():
    text = "Founder of a named discipline. Developer of the Law of Existence."
    result = scan_unglossed_formal_object(text)
    assert not result.flagged
    assert result.self_titling_present
    assert result.unglossed_spans == []


def test_does_not_flag_real_cited_physics_law():
    result = scan_unglossed_formal_object(REAL_NEWTON)
    assert not result.flagged


def test_does_not_flag_founder_bio_without_law_naming_regression():
    """Regression for the real false positive caught in development: a
    founder-of-institute bio next to a correctly-cited equation, with no
    'law of X' / 'theory of X' phrase anywhere in the text, must not
    flag -- self_titling_present requires BOTH the law-naming AND the
    self-attribution phrase, not either alone."""
    result = scan_unglossed_formal_object(FOUNDER_BIO_NO_LAW_NAMING)
    assert not result.self_titling_present
    assert not result.flagged


def test_two_term_implicit_multiplication_equation_not_matched():
    """E = mc^2 uses implicit multiplication with only two terms after the
    equals sign; the three-term minimum (var = var op var) is deliberate
    so ordinary two-term physics notation doesn't match at all."""
    text = "Founder of the Institute. Law of Mass-Energy: E = mc^2."
    result = scan_unglossed_formal_object(text)
    assert result.unglossed_spans == []


def test_bare_digit_suffix_tokens_not_treated_as_variables():
    """m1/M2-style bare ASCII digit suffixes (no subscript/superscript
    marker) are deliberately excluded -- common in ordinary chemistry/
    business/model-name text (H2O, GPT4, Q3) and would be a false-positive
    source; this also guards against the truncated-match bug caught in
    development (m1 matching as bare 'm', corrupting the rest of the
    equation span)."""
    text = "Founder of the Institute. Law of Something. K = A1 x B2 x C3."
    result = scan_unglossed_formal_object(text)
    for span in result.unglossed_spans:
        assert "1" not in span.text or "₁" in span.text
        assert "A1" not in span.text
        assert "B2" not in span.text


def test_greek_single_letter_tokens_supported():
    text = (
        "Founder of the Institute. Developer of the Law of Balance: "
        "P₂ = A₇ x B₃."
    )
    result = scan_unglossed_formal_object(text)
    assert result.flagged
    assert len(result.unglossed_spans) == 1


def test_falsifiability_language_suppresses_flag():
    text = (
        "Founder of the Institute. Developer of the Law of Drift: "
        "T = C₇ x U³. This claim fails if T does not correlate with "
        "observed outcomes."
    )
    result = scan_unglossed_formal_object(text)
    assert not result.flagged


def test_gloss_outside_window_does_not_suppress_flag():
    far_filler = "unrelated filler text. " * 60  # comfortably > 400 chars
    text = (
        "Founder of the Institute. Developer of the Law of Drift: "
        "T = C₇ x U³. " + far_filler +
        "where C is defined as a constant."
    )
    result = scan_unglossed_formal_object(text)
    assert result.flagged


def test_clean_text_not_flagged():
    text = "The classifier scored 87.3% accuracy on a held-out test set with a fixed random seed."
    result = scan_unglossed_formal_object(text)
    assert not result.flagged
    assert not result.self_titling_present
    assert result.unglossed_spans == []


def test_confidence_is_weak_not_strong():
    """This detector is text-proximity, not semantic verification -- it
    should never claim a confidence stronger than 'weak'."""
    result = scan_unglossed_formal_object(SPECIMEN_LIKE_TEXT)
    assert result.confidence == "weak"
    clean_result = scan_unglossed_formal_object("neutral text")
    assert clean_result.confidence == "none"


def test_source_field_documents_not_a_section_2_8_case():
    result = scan_unglossed_formal_object(SPECIMEN_LIKE_TEXT)
    assert "not in basin_attractors_v1.md's six" in result.source


def test_to_dict_json_safe():
    result = scan_unglossed_formal_object(SPECIMEN_LIKE_TEXT)
    json.dumps(result.to_dict())  # must not raise


def test_to_dict_shape():
    result = scan_unglossed_formal_object(SPECIMEN_LIKE_TEXT)
    d = result.to_dict()
    assert set(d.keys()) == {
        "source", "flagged", "confidence", "explanation",
        "unglossed_spans", "self_titling_present",
    }
    assert isinstance(d["unglossed_spans"], list)
    if d["unglossed_spans"]:
        span = d["unglossed_spans"][0]
        assert set(span.keys()) == {"text", "start", "end", "has_gloss_nearby"}
