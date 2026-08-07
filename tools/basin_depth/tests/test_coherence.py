import math

from basin_depth.coherence import (
    INV_E, decay_model, fit_exponential_decay, threshold_coherence_time,
)


def test_fit_recovers_known_decay_constant():
    """Generate gamma(tau) from the exact model with a known tau_c and
    confirm the fitter recovers it -- the load-bearing correctness
    check for the whole coherence-time-extraction step (protocol §5.1)."""
    true_A, true_tau_c, true_C = 0.7, 5.0, 0.1
    taus = list(range(1, 19))
    gamma = {t: true_A * math.exp(-t / true_tau_c) + true_C for t in taus}

    fit = fit_exponential_decay(gamma)

    assert not fit.censored
    assert abs(fit.tau_c - true_tau_c) < 0.1
    assert abs(fit.A - true_A) < 0.1
    assert abs(fit.C - true_C) < 0.1
    assert fit.r_squared > 0.99


def test_fit_recovers_long_but_finite_decay_constant():
    true_A, true_tau_c, true_C = 0.5, 25.0, 0.05
    taus = list(range(1, 19))
    gamma = {t: true_A * math.exp(-t / true_tau_c) + true_C for t in taus}

    fit = fit_exponential_decay(gamma)
    assert abs(fit.tau_c - true_tau_c) / true_tau_c < 0.15  # within 15% relative error


def test_fit_flags_censored_when_flat():
    """A gamma(tau) that never meaningfully decays within the observation
    window should saturate the tau_c upper bound and be flagged censored,
    not report a numerically enormous 'coherence time'."""
    taus = list(range(1, 19))
    gamma = {t: 0.95 for t in taus}  # essentially flat -> no real decay observable
    fit = fit_exponential_decay(gamma)
    assert fit.censored
    assert fit.tau_c <= 20.0 * max(taus) + 1e-6


def test_fit_falls_back_when_too_few_points():
    fit = fit_exponential_decay({1: 0.9, 2: 0.8})
    assert fit.censored
    assert fit.tau_c == 3.0  # max(tau) + 1


def test_threshold_method_matches_hand_computed_crossing():
    # gamma crosses below 1/e (~0.368) between tau=3 (0.4) and tau=4 (0.3)
    gamma = {1: 0.9, 2: 0.6, 3: 0.4, 4: 0.3, 5: 0.2}
    tau_c = threshold_coherence_time(gamma)
    assert tau_c == 4.0


def test_threshold_method_censored_when_never_crosses():
    gamma = {1: 0.9, 2: 0.8, 3: 0.7}
    tau_c = threshold_coherence_time(gamma)
    assert tau_c == 4.0  # max(tau) + 1


def test_decay_model_at_zero_is_A_plus_C():
    import numpy as np
    val = decay_model(np.array([0.0]), A=0.6, tau_c=3.0, C=0.1)
    assert abs(val[0] - 0.7) < 1e-9


def test_inv_e_constant():
    assert abs(INV_E - 1 / math.e) < 1e-12
