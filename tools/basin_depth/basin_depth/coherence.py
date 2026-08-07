"""Coherence time extraction from an autocorrelation function.

Implements protocol §5: exponential decay model fitting (primary) and
the 1/e threshold method (robustness check).
"""

from __future__ import annotations

import math
import warnings
from dataclasses import dataclass

import numpy as np
from scipy.optimize import OptimizeWarning, curve_fit

INV_E = 1.0 / math.e


def decay_model(tau: np.ndarray, A: float, tau_c: float, C: float) -> np.ndarray:
    """gamma_V(tau) = A * exp(-tau / tau_c) + C  (protocol §5.1)."""
    return A * np.exp(-tau / tau_c) + C


@dataclass
class CoherenceFit:
    A: float
    tau_c: float
    C: float
    tau_c_stderr: float | None
    r_squared: float
    censored: bool = False  # True if the fit could not be constrained (too few points)

    def confidence_interval(self, z: float = 1.0) -> tuple[float, float]:
        """z=1.0 -> 1-sigma CI per protocol §11.1 ('confidence intervals')."""
        if self.tau_c_stderr is None:
            return (self.tau_c, self.tau_c)
        return (self.tau_c - z * self.tau_c_stderr, self.tau_c + z * self.tau_c_stderr)


def fit_exponential_decay(gamma: dict[int, float]) -> CoherenceFit:
    """Protocol §5.1: nonlinear least squares fit of gamma_V(tau) = A*exp(-tau/tau_c) + C,
    with constraints A > 0, tau_c > 0, 0 <= C < 0.3.

    Falls back to a censored fit (tau_c = max(tau) + 1, per §5.2's
    censoring convention) if there are fewer than 3 data points to fit,
    or if the optimizer cannot converge within the bounds.
    """
    taus = np.array(sorted(gamma.keys()), dtype=np.float64)
    gammas = np.array([gamma[int(t)] for t in taus], dtype=np.float64)

    if len(taus) < 3:
        max_tau = float(taus.max()) if len(taus) else 1.0
        return CoherenceFit(A=float(gammas[0]) if len(gammas) else 0.0,
                             tau_c=max_tau + 1, C=0.0, tau_c_stderr=None,
                             r_squared=float("nan"), censored=True)

    max_tau = float(taus.max())
    # tau_c is unconstrained above by the protocol text, but an unbounded
    # upper bound lets curve_fit diverge to numerically meaningless values
    # (thousands of quarters) whenever gamma(tau) is nearly flat across the
    # observation window. Cap at a large multiple of the observation window
    # itself: still reads as "did not decohere within the window we can see"
    # (which is the correct interpretation of a flat curve), without
    # reporting a physically nonsensical number. Fits that saturate this
    # bound are flagged `censored=True`, the same flag used for the
    # too-few-points fallback below.
    tau_c_cap = 20.0 * max_tau
    p0 = [max(gammas[0] - gammas[-1], 0.1), max(taus[len(taus) // 2], 1.0), max(min(gammas[-1], 0.29), 0.0)]
    bounds = ([1e-6, 1e-6, 0.0], [np.inf, tau_c_cap, 0.3 - 1e-9])
    try:
        with warnings.catch_warnings():
            # A fit that saturates the tau_c bound (near-flat gamma, no
            # real decay in the window) legitimately has an ill-conditioned
            # covariance matrix; that condition is already surfaced via the
            # `censored` flag below, so the warning would be noise, not signal.
            warnings.filterwarnings("ignore", category=OptimizeWarning)
            popt, pcov = curve_fit(decay_model, taus, gammas, p0=p0, bounds=bounds, maxfev=10000)
    except (RuntimeError, ValueError):
        return CoherenceFit(A=float(gammas[0]), tau_c=max_tau + 1, C=0.0,
                             tau_c_stderr=None, r_squared=float("nan"), censored=True)

    A, tau_c, C = popt
    stderr = float(np.sqrt(np.diag(pcov))[1]) if np.all(np.isfinite(pcov)) else None

    residuals = gammas - decay_model(taus, *popt)
    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((gammas - np.mean(gammas)) ** 2))
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    return CoherenceFit(A=float(A), tau_c=float(tau_c), C=float(C),
                         tau_c_stderr=stderr, r_squared=r_squared,
                         censored=bool(tau_c >= 0.999 * tau_c_cap))


def threshold_coherence_time(gamma: dict[int, float], threshold: float = INV_E) -> float:
    """Protocol §5.2: smallest tau such that gamma_V(tau) < threshold
    (default 1/e). If it never drops below threshold, return
    max(tau) + 1 (censored), matching the protocol's convention.
    """
    if not gamma:
        return float("nan")
    for tau in sorted(gamma.keys()):
        if gamma[tau] < threshold:
            return float(tau)
    return float(max(gamma.keys()) + 1)
