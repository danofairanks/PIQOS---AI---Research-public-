"""Significance testing and effect size.

Implements protocol §6: block bootstrap (Method A), permutation test
(Method B), cross-corpus ANOVA/Kruskal-Wallis (Method C), and Cohen's d.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats as scipy_stats

from .autocorrelation import autocorrelation
from .coherence import fit_exponential_decay
from .corpus import Document, bin_by_quarter
from .embeddings import EmbeddingBackend, compute_signatures
from .vocabulary import VocabPool


@dataclass
class BootstrapResult:
    observed_delta: float
    delta_samples: np.ndarray
    tau_c_a_samples: np.ndarray
    tau_c_b_samples: np.ndarray
    p_value: float
    ci_95: tuple[float, float]
    n_boot: int


def _blocked_resample(quarters: list[str], block_size: int, n: int, rng: np.random.Generator) -> list[str]:
    """Resample a quarter sequence in contiguous blocks (with replacement),
    concatenated to length >= n, then truncated to exactly n."""
    blocks = [quarters[i:i + block_size] for i in range(0, len(quarters), block_size)]
    out: list[str] = []
    while len(out) < n:
        idx = rng.integers(0, len(blocks))
        out.extend(blocks[idx])
    return out[:n]


def block_bootstrap_delta(
    signatures: dict[str, dict[str, np.ndarray]],
    quarters: list[str],
    max_tau: int,
    *,
    pool_a: str = "immune",
    pool_b: str = "claim",
    block_size: int = 4,
    n_boot: int = 2000,
    seed: int | None = 0,
) -> BootstrapResult:
    """Protocol §6.3 Method A.

    Resamples time bins with replacement in contiguous blocks of
    `block_size` quarters, recomputes gamma_V(tau) and tau_c_V for
    each bootstrap sample from the *already-computed* signature
    vectors (no re-embedding needed — that is the whole point of
    resampling the bin order rather than the documents), and reports
    the fraction of bootstrap deltas <= 0 as the p-value, per the
    protocol's own definition.
    """
    rng = np.random.default_rng(seed)

    observed_gamma_a = autocorrelation(signatures[pool_a], quarters, max_tau)
    observed_gamma_b = autocorrelation(signatures[pool_b], quarters, max_tau)
    observed_delta = fit_exponential_decay(observed_gamma_a).tau_c - fit_exponential_decay(observed_gamma_b).tau_c

    delta_samples = np.empty(n_boot)
    a_samples = np.empty(n_boot)
    b_samples = np.empty(n_boot)
    for i in range(n_boot):
        resampled = _blocked_resample(quarters, block_size, len(quarters), rng)
        gamma_a = autocorrelation(signatures[pool_a], resampled, max_tau)
        gamma_b = autocorrelation(signatures[pool_b], resampled, max_tau)
        tau_a = fit_exponential_decay(gamma_a).tau_c
        tau_b = fit_exponential_decay(gamma_b).tau_c
        a_samples[i] = tau_a
        b_samples[i] = tau_b
        delta_samples[i] = tau_a - tau_b

    p_value = float(np.mean(delta_samples <= 0))
    ci_95 = (float(np.percentile(delta_samples, 2.5)), float(np.percentile(delta_samples, 97.5)))

    return BootstrapResult(
        observed_delta=observed_delta, delta_samples=delta_samples,
        tau_c_a_samples=a_samples, tau_c_b_samples=b_samples,
        p_value=p_value, ci_95=ci_95, n_boot=n_boot,
    )


@dataclass
class PermutationResult:
    observed_delta: float
    permuted_deltas: np.ndarray
    p_value: float
    n_perm: int


def permutation_test(
    docs: list[Document],
    quarters: list[str],
    vocab_pools: dict[str, VocabPool],
    backend: EmbeddingBackend,
    max_tau: int,
    observed_delta: float,
    *,
    pool_a: str = "immune",
    pool_b: str = "claim",
    n_perm: int = 500,
    seed: int | None = 0,
) -> PermutationResult:
    """Protocol §6.3 Method B: pool all documents, randomly reassign to
    bins preserving bin sizes, recompute tau_c_immune/tau_c_claim, and
    report the fraction of permutations with delta >= observed delta.

    This re-embeds documents on every permutation and is the
    computationally heaviest of the three significance tests;
    `n_perm` defaults lower than `n_boot` for that reason.
    """
    rng = np.random.default_rng(seed)
    bin_sizes = [len(bin_by_quarter(docs, quarters).get(q, [])) for q in quarters]
    pool_subset = {k: v for k, v in vocab_pools.items() if k in (pool_a, pool_b)}

    permuted_deltas = np.empty(n_perm)
    for i in range(n_perm):
        shuffled = list(docs)
        rng.shuffle(shuffled)
        reassigned: list[Document] = []
        cursor = 0
        for q, size in zip(quarters, bin_sizes):
            for d in shuffled[cursor:cursor + size]:
                reassigned.append(Document(doc_id=d.doc_id, text=d.text, quarter=q,
                                            source=d.source, metadata=d.metadata))
            cursor += size

        perm_bins = bin_by_quarter(reassigned, quarters)
        sigs = compute_signatures(perm_bins, quarters, pool_subset, backend)
        gamma_a = autocorrelation(sigs[pool_a], quarters, max_tau)
        gamma_b = autocorrelation(sigs[pool_b], quarters, max_tau)
        tau_a = fit_exponential_decay(gamma_a).tau_c
        tau_b = fit_exponential_decay(gamma_b).tau_c
        permuted_deltas[i] = tau_a - tau_b

    p_value = float(np.mean(permuted_deltas >= observed_delta))
    return PermutationResult(observed_delta=observed_delta, permuted_deltas=permuted_deltas,
                              p_value=p_value, n_perm=n_perm)


@dataclass
class ANOVAResult:
    statistic: float
    p_value: float
    method: str  # "anova" or "kruskal"


def cross_corpus_comparison(delta_by_corpus: dict[str, np.ndarray], *, method: str = "kruskal") -> ANOVAResult:
    """Protocol §6.3 Method C: compare Delta-tau_c distributions (e.g. the
    bootstrap delta_samples from `block_bootstrap_delta`) across corpora
    via one-way ANOVA or Kruskal-Wallis. Kruskal-Wallis is the default
    since bootstrap delta distributions are not guaranteed normal.
    """
    samples = list(delta_by_corpus.values())
    if len(samples) < 2:
        raise ValueError("cross_corpus_comparison needs at least two corpora")
    if method == "anova":
        stat, p = scipy_stats.f_oneway(*samples)
    elif method == "kruskal":
        stat, p = scipy_stats.kruskal(*samples)
    else:
        raise ValueError(f"unknown method {method!r}, expected 'anova' or 'kruskal'")
    return ANOVAResult(statistic=float(stat), p_value=float(p), method=method)


def cohens_d(a_samples: np.ndarray, b_samples: np.ndarray) -> float:
    """Protocol §6.4: d = (tau_c_immune - tau_c_claim) / sigma_pooled,
    using the pooled standard deviation from bootstrap samples.
    """
    n_a, n_b = len(a_samples), len(b_samples)
    var_a, var_b = np.var(a_samples, ddof=1), np.var(b_samples, ddof=1)
    pooled_var = ((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2)
    pooled_std = float(np.sqrt(pooled_var))
    if pooled_std == 0:
        return 0.0
    return float((np.mean(a_samples) - np.mean(b_samples)) / pooled_std)


def interpret_cohens_d(d: float) -> str:
    """Protocol §6.4 interpretation table."""
    ad = abs(d)
    if ad < 0.2:
        return "negligible"
    if ad < 0.5:
        return "small"
    if ad < 0.8:
        return "medium"
    return "large"
