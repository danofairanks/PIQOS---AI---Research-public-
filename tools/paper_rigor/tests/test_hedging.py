"""Hedge-density check. Constructed fixtures only (no counts pinned
against this repo's own mutable papers; see the repo CLAUDE.md note on
that failure class). The threshold itself was chosen against this
repo's papers; that calibration is documented in the README and is not
re-asserted here."""

from paper_rigor.hedging import (
    HEDGE_TERMS, LEAD_SHARE_THRESHOLD, MIN_SENTENCES, MIN_THESIS_SENTENCES, check_hedge_density,
)
from paper_rigor.scan import scan_paper


def _para(sentences):
    return " ".join(sentences)


HEDGED = [
    "This approach may reduce the error rate in some settings.",
    "It could potentially generalise to related problems.",
    "The effect might possibly depend on scale.",
    "Such a system may arguably be easier to govern.",
    "It is not inconceivable that the pattern holds more widely.",
    "A related mechanism could perhaps explain part of the gap.",
    "These results may point toward a broader trend.",
    "The method might also help in other domains.",
]
PLAIN = [
    "We collected 200 samples from the public archive.",
    "Each sample was labelled by two annotators.",
    "The classifier uses a fixed vocabulary of 5000 tokens.",
    "Training ran for 40 epochs on one machine.",
    "The table lists the three settings we compared.",
    "Section 4 describes the labelling protocol.",
    "The appendix gives every hyperparameter.",
    "Figure 2 shows the loss over time.",
]


def _doc(intro, body, tail=""):
    return f"# Title\n\n## 1. Introduction\n\n{_para(intro)}\n\n## 2. Methods\n\n{_para(body)}\n\n{tail}"


def test_heavily_hedged_intro_without_testable_language_is_a_lead():
    text = _doc(HEDGED, PLAIN * 4)
    r = check_hedge_density(text)
    assert r.applicable and r.thesis_section_found
    assert r.thesis_n_sentences >= MIN_THESIS_SENTENCES
    assert r.thesis_share >= LEAD_SHARE_THRESHOLD
    assert r.lead is True
    assert r.thesis_examples  # shows which sentences


def test_same_hedging_with_testable_condition_is_not_a_lead():
    text = _doc(HEDGED, PLAIN * 4, tail="This claim fails if the effect disappears at larger scale.")
    r = check_hedge_density(text)
    assert r.has_testable_markers is True
    assert r.lead is False


def test_plainly_stated_intro_is_not_a_lead():
    text = _doc(PLAIN, HEDGED * 3 + PLAIN)
    r = check_hedge_density(text)
    assert r.thesis_share == 0.0
    assert r.lead is False
    assert r.share > 0.3  # body hedging alone does not make a lead


def test_short_text_is_not_applicable():
    r = check_hedge_density("# T\n\n## Introduction\n\nThis may work. It could help.")
    assert r.applicable is False and r.lead is False
    assert MIN_SENTENCES > 4


def test_month_may_and_fixed_phrases_are_not_hedges():
    text = _doc(["We started in May 2026 and finished soon after that date.",
                 "Please report problems as soon as possible to the team.",
                 "This is impossible to verify from the archive alone."] + PLAIN * 2, PLAIN * 4)
    r = check_hedge_density(text)
    assert r.n_hedged == 0


def test_a_sentence_with_several_hedges_counts_once():
    r = check_hedge_density(_doc(["It may perhaps possibly help in some cases."] + PLAIN * 2, PLAIN * 4))
    assert r.thesis_n_hedged == 1


def test_references_section_is_excluded():
    refs = "\n\n## References\n\n" + "\n\n".join(f"Author{i}, A. (2020). It may {i} appear in print. Venue." for i in range(60))
    r = check_hedge_density(_doc(PLAIN * 2, PLAIN * 4, tail=refs))
    assert r.n_hedged == 0


def test_hard_wrapped_sentences_are_joined():
    wrapped = "\n".join(["This approach may reduce the", "error rate in some settings."] * 1)
    text = "# T\n\n## Introduction\n\n" + wrapped + "\n\n" + _para(PLAIN * 5)
    r = check_hedge_density(text)
    assert r.thesis_n_hedged == 1


def test_not_counted_as_a_structural_gap_and_present_in_scan_dict():
    hedged = scan_paper(_doc(HEDGED, PLAIN * 4))
    plain = scan_paper(_doc(PLAIN, PLAIN * 4))
    d = hedged.to_dict()
    assert d["hedge_density"]["lead"] is True
    assert d["hedge_density"]["lead_share_threshold"] == LEAD_SHARE_THRESHOLD
    assert plain.to_dict()["hedge_density"]["lead"] is False
    # a lead alone changes neither the structural gap count nor `ok`
    assert hedged.structural_gap_count == plain.structural_gap_count
    assert hedged.ok == plain.ok


def test_hedge_terms_are_lowercase_words():
    assert all(t == t.lower() for t in HEDGE_TERMS)
