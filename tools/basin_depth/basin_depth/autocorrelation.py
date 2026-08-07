"""Autocorrelation of bin-level signature vectors.

Implements protocol §4.3 (embedding-based autocorrelation) and §4.4
(term-frequency autocorrelation, the mandated robustness check).
"""

from __future__ import annotations

import numpy as np

from .corpus import Document
from .vocabulary import VocabPool


def cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    nu, nv = np.linalg.norm(u), np.linalg.norm(v)
    if nu == 0 or nv == 0:
        return 0.0
    return float(np.dot(u, v) / (nu * nv))


def autocorrelation(
    signatures: dict[str, np.ndarray], ordered_quarters: list[str], max_tau: int
) -> dict[int, float]:
    """Protocol §4.3: gamma_V(tau) = cos_sim(s_V(t), s_V(t+tau)) averaged
    over all valid t, for tau = 1..max_tau. Quarters with no signature
    (no matching documents that bin) are skipped as "invalid t" for
    that tau, per the protocol's own "averaged over all valid t"
    language — this keeps sparse bins from silently zeroing out the
    correlation instead of just being excluded from the average.
    """
    gamma: dict[int, float] = {}
    for tau in range(1, max_tau + 1):
        corrs = []
        for i in range(len(ordered_quarters) - tau):
            qt, qtau = ordered_quarters[i], ordered_quarters[i + tau]
            if qt in signatures and qtau in signatures:
                corrs.append(cosine_similarity(signatures[qt], signatures[qtau]))
        if corrs:
            gamma[tau] = float(np.mean(corrs))
    return gamma


def term_frequency_vector(
    docs_in_bin: list[Document], term_order: list[str]
) -> np.ndarray:
    """Normalized frequency distribution over `term_order` for one bin,
    protocol §4.4 step 1-2: f_V(t) then p_V(t) = f_V(t) / sum(f_V(t))."""
    counts = np.zeros(len(term_order), dtype=np.float64)
    total_tokens = 0
    for d in docs_in_bin:
        toks = d.tokens
        total_tokens += len(toks)
        tokset_text = d.text.lower()
        for i, term in enumerate(term_order):
            if " " in term or "-" in term:
                counts[i] += tokset_text.count(term)
            else:
                counts[i] += toks.count(term)
    s = counts.sum()
    if s == 0:
        return counts  # all-zero; caller treats this bin as having no signal
    return counts / s


def term_frequency_autocorrelation(
    bins: dict[str, list[Document]],
    ordered_quarters: list[str],
    vocab: VocabPool,
    max_tau: int,
) -> dict[int, float]:
    """Protocol §4.4: dot-product similarity between normalized
    term-frequency distributions p_V(t) and p_V(t+tau), as the
    interpretable non-embedding robustness check.
    """
    term_order = sorted(vocab.terms)
    p_by_quarter: dict[str, np.ndarray] = {}
    for q in ordered_quarters:
        vec = term_frequency_vector(bins.get(q, []), term_order)
        if vec.sum() > 0:
            p_by_quarter[q] = vec

    gamma: dict[int, float] = {}
    for tau in range(1, max_tau + 1):
        dots = []
        for i in range(len(ordered_quarters) - tau):
            qt, qtau = ordered_quarters[i], ordered_quarters[i + tau]
            if qt in p_by_quarter and qtau in p_by_quarter:
                dots.append(float(np.dot(p_by_quarter[qt], p_by_quarter[qtau])))
        if dots:
            gamma[tau] = float(np.mean(dots))
    return gamma
