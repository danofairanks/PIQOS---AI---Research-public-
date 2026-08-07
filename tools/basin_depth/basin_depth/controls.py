"""Control tests: placebo vocabulary and temporal reversal.

Implements protocol §7.3 and §7.4. §7.1 (control corpus) and §7.2
(negative control corpus) are not separate code paths — they are the
same pipeline run against a different `Document` list, per the
protocol's own framing ("execute the identical protocol on..."), so
they need no dedicated function here; see `pipeline.run_basin_depth`
called three times in `examples/synthetic_demo.py` for exactly that.
"""

from __future__ import annotations

import numpy as np

from .vocabulary import VocabPool, term_frequency_by_quarter
from .corpus import Document


def placebo_vocabulary(
    candidate_terms: set[str],
    immune_pool: VocabPool,
    bins: dict[str, list[Document]],
    quarters: list[str],
    *,
    seed: int | None = 0,
) -> VocabPool:
    """Protocol §7.3: a synthetic 'immune' vocabulary built by randomly
    drawing from `candidate_terms` (intended use: the neutral pool, or
    a wider low-function candidate set) so that its total corpus
    frequency approximately matches the real immune pool's total
    frequency, and drawing the same number of terms as the real
    immune pool. Expected result under the null: tau_c_placebo is
    close to tau_c_neutral, not to tau_c_immune — if it instead tracks
    tau_c_immune, that indicates the depth signal is driven by generic
    low-frequency stability rather than immune-specific content
    (protocol's own falsification condition for this control).
    """
    rng = np.random.default_rng(seed)
    freq = term_frequency_by_quarter(bins, quarters)

    def total_freq(term: str) -> float:
        return sum(freq.get(term, {}).values())

    target_total = sum(total_freq(t) for t in immune_pool.terms)
    target_per_term = target_total / max(len(immune_pool.terms), 1)

    candidates = sorted(candidate_terms - immune_pool.terms)
    if not candidates:
        raise ValueError("no candidate terms available to build a placebo pool from")

    # Rank candidates by closeness to the target per-term frequency, then
    # sample from the closest band with replacement-free draws — this is
    # the "same frequency distribution as the immune seed list" matching
    # criterion, operationalized as nearest-frequency sampling rather than
    # pure uniform random draw (which would not control for frequency).
    scored = sorted(candidates, key=lambda t: abs(total_freq(t) - target_per_term))
    n_terms = min(len(immune_pool.terms), len(scored))
    pool_size = max(n_terms * 3, n_terms)
    band = scored[:pool_size]
    chosen = rng.choice(band, size=n_terms, replace=False)

    return VocabPool("placebo", set(chosen.tolist()))


def temporal_reversal(quarters: list[str]) -> list[str]:
    """Protocol §7.4: reverse the time order of the corpus bins.

    Returns the reversed quarter-label ordering; pass this in place of
    the forward-chronological `quarters` list to `autocorrelation()`
    and downstream fitting to run the reversed-time test. Signature
    vectors themselves are unchanged — only the sequence order used to
    pair (t, t+tau) changes, which is exactly what the protocol's
    reversal test is checking.
    """
    return list(reversed(quarters))
