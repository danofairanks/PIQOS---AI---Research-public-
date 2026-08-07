import numpy as np

from basin_depth.autocorrelation import autocorrelation, cosine_similarity


def test_cosine_similarity_identical_vectors_is_one():
    v = np.array([1.0, 2.0, 3.0])
    assert abs(cosine_similarity(v, v) - 1.0) < 1e-9


def test_cosine_similarity_orthogonal_vectors_is_zero():
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert abs(cosine_similarity(a, b)) < 1e-9


def test_cosine_similarity_zero_vector_is_defined_as_zero():
    assert cosine_similarity(np.array([0.0, 0.0]), np.array([1.0, 1.0])) == 0.0


def test_autocorrelation_constant_signature_stays_at_one():
    """A vocabulary pool whose signature vector never changes across bins
    (the planted 'immune' behavior) should show gamma(tau) == 1.0 for
    every delay -- the pure conserved-current case."""
    fixed = np.array([1.0, 0.0, 0.0])
    quarters = [f"2020Q{i}" for i in range(1, 9)]
    signatures = {q: fixed for q in quarters}
    gamma = autocorrelation(signatures, quarters, max_tau=4)
    assert set(gamma.keys()) == {1, 2, 3, 4}
    for tau, val in gamma.items():
        assert abs(val - 1.0) < 1e-9


def test_autocorrelation_orthogonal_alternation_decays_at_odd_tau():
    """A signature that alternates between two orthogonal vectors every
    bin should show gamma(tau)==1 at even tau and gamma(tau)==0 at odd
    tau -- a clean, hand-checkable non-trivial case."""
    a, b = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    quarters = [f"2020Q{i}" for i in range(1, 9)]
    signatures = {q: (a if i % 2 == 0 else b) for i, q in enumerate(quarters)}
    gamma = autocorrelation(signatures, quarters, max_tau=4)
    assert abs(gamma[1]) < 1e-9
    assert abs(gamma[2] - 1.0) < 1e-9
    assert abs(gamma[3]) < 1e-9
    assert abs(gamma[4] - 1.0) < 1e-9


def test_autocorrelation_skips_missing_bins():
    fixed = np.array([1.0, 0.0])
    quarters = ["2020Q1", "2020Q2", "2020Q3"]
    # only Q1 and Q3 have a signature; Q2 is missing (no matching documents)
    signatures = {"2020Q1": fixed, "2020Q3": fixed}
    gamma = autocorrelation(signatures, quarters, max_tau=2)
    # tau=1 pairs (Q1,Q2) and (Q2,Q3), both touching the missing Q2 -> no valid pairs
    assert 1 not in gamma
    # tau=2 pairs (Q1,Q3), which both exist
    assert 2 in gamma
    assert abs(gamma[2] - 1.0) < 1e-9
