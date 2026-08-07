from basin_depth.controls import placebo_vocabulary, temporal_reversal
from basin_depth.corpus import Document, bin_by_quarter, quarter_range
from basin_depth.vocabulary import VocabPool


def test_temporal_reversal_reverses_order():
    quarters = quarter_range("2020Q1", "2020Q4")
    reversed_qs = temporal_reversal(quarters)
    assert reversed_qs == list(reversed(quarters))
    assert reversed_qs != quarters


def test_placebo_vocabulary_disjoint_from_immune_pool():
    quarters = quarter_range("2020Q1", "2020Q2")
    docs = [
        Document("1", "alpha beta gamma delta epsilon zeta eta theta", "2020Q1"),
        Document("2", "alpha beta gamma delta epsilon zeta eta theta", "2020Q2"),
    ]
    bins = bin_by_quarter(docs, quarters)
    immune = VocabPool("immune", {"alpha", "beta"})
    candidates = {"gamma", "delta", "epsilon", "zeta", "eta", "theta"}

    placebo = placebo_vocabulary(candidates, immune, bins, quarters, seed=0)
    assert placebo.terms.isdisjoint(immune.terms)
    assert placebo.terms.issubset(candidates)
    assert len(placebo.terms) == min(len(immune.terms), len(candidates))


def test_placebo_vocabulary_raises_on_empty_candidates():
    import pytest
    quarters = quarter_range("2020Q1", "2020Q1")
    bins = bin_by_quarter([], quarters)
    immune = VocabPool("immune", {"alpha"})
    with pytest.raises(ValueError):
        placebo_vocabulary(set(), immune, bins, quarters)
