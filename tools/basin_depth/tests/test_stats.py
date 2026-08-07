import numpy as np

from basin_depth.stats import cohens_d, interpret_cohens_d, cross_corpus_comparison, block_bootstrap_delta


def test_cohens_d_matches_manual_calculation():
    a = np.array([10.0, 12.0, 11.0, 13.0, 9.0])
    b = np.array([5.0, 6.0, 4.0, 7.0, 5.0])
    d = cohens_d(a, b)

    n_a, n_b = len(a), len(b)
    var_a, var_b = np.var(a, ddof=1), np.var(b, ddof=1)
    pooled = np.sqrt(((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2))
    expected = (np.mean(a) - np.mean(b)) / pooled
    assert abs(d - expected) < 1e-9


def test_cohens_d_zero_when_equal_pooled_std_zero():
    a = np.array([5.0, 5.0, 5.0])
    b = np.array([5.0, 5.0, 5.0])
    assert cohens_d(a, b) == 0.0


def test_interpret_cohens_d_buckets():
    assert interpret_cohens_d(0.05) == "negligible"
    assert interpret_cohens_d(0.3) == "small"
    assert interpret_cohens_d(0.6) == "medium"
    assert interpret_cohens_d(1.2) == "large"
    assert interpret_cohens_d(-1.2) == "large"  # magnitude, not sign


def test_cross_corpus_comparison_kruskal_and_anova_run():
    rng = np.random.default_rng(0)
    by_corpus = {
        "primary": rng.normal(5, 1, size=50),
        "control": rng.normal(0, 1, size=50),
        "negative": rng.normal(0, 1, size=50),
    }
    result_k = cross_corpus_comparison(by_corpus, method="kruskal")
    assert result_k.method == "kruskal"
    assert result_k.p_value < 0.05  # primary is clearly shifted

    result_a = cross_corpus_comparison(by_corpus, method="anova")
    assert result_a.method == "anova"
    assert result_a.p_value < 0.05


def test_cross_corpus_comparison_requires_two_corpora():
    import pytest
    with pytest.raises(ValueError):
        cross_corpus_comparison({"only_one": np.array([1.0, 2.0])})


def test_block_bootstrap_delta_recovers_planted_signal():
    """Two vocab pools with genuinely different persistence -- immune
    constant across bins, claim alternating -- should show a clearly
    positive delta with p_value well under 1, and NOT crash on the
    resampling machinery."""
    quarters = [f"2020Q{i}" for i in range(1, 5)] + [f"2021Q{i}" for i in range(1, 5)]
    constant = np.array([1.0, 0.0, 0.0])
    signatures = {
        "immune": {q: constant for q in quarters},
        "claim": {q: (np.array([0.0, 1.0, 0.0]) if i % 2 == 0 else np.array([0.0, 0.0, 1.0]))
                  for i, q in enumerate(quarters)},
    }
    result = block_bootstrap_delta(signatures, quarters, max_tau=3, block_size=2, n_boot=100, seed=0)
    assert result.observed_delta > 0
    assert 0.0 <= result.p_value <= 1.0
    assert len(result.delta_samples) == 100
