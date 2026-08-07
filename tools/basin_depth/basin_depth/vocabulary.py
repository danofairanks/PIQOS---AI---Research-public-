"""Vocabulary pool construction and validation.

Implements protocol §3 (Vocabulary Operationalization) and Appendix A
(Vocabulary Pool Derivation Algorithm). Ships the protocol's own seed
lists (§3.1-3.3) verbatim so the AI-discourse use case works
out-of-the-box; also implements the empirical CV-based derivation
procedure so the tool can build vocabulary pools for a corpus in a
domain the seed lists were never written for.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field

from .corpus import Document, _tokenize

# --------------------------------------------------------------------------
# Protocol §3.1 seed claim vocabulary (flattened across eras)
# --------------------------------------------------------------------------
CLAIM_SEED: set[str] = {
    "artificial general intelligence", "transformative ai", "gpt-3",
    "few-shot learning", "bert", "scaling laws",
    "chatgpt", "sparks of agi", "emergent abilities", "alignment problem",
    "large language model", "prompt engineering",
    "gpt-4", "multimodal", "frontier model", "reasoning", "constitutional ai", "rlhf",
    "o1", "reasoning model", "agentic ai", "superintelligence", "ai scientist",
    "test-time compute",
    "singularity", "event horizon", "gentle singularity", "asi",
    "recursive self-improvement", "mars colonies ai",
}

# --------------------------------------------------------------------------
# Protocol §3.2 seed immune vocabulary, by defensive maneuver category
# --------------------------------------------------------------------------
IMMUNE_SEED_BY_CATEGORY: dict[str, set[str]] = {
    "goal_post_movement": {
        "next generation will", "next scale", "temporary limitation",
        "early stages", "just getting started", "on the roadmap",
        "future work", "not yet", "soon",
    },
    "provisionalization": {
        "we're working on it", "in progress", "being addressed",
        "handled by ongoing research", "already being solved",
    },
    "status_dismissal": {
        "hot take", "doesn't get it", "behind the curve", "not serious",
        "decelerationist", "doomer", "anti-progress", "cringe", "out of touch",
    },
    "burden_shifting": {
        "prove it's impossible", "show me the alternative",
        "what's your solution", "where's your model", "build it yourself",
    },
    "equivocation": {
        "intelligence", "understanding", "coherence", "alignment", "safety", "reasoning",
    },
    "volume_velocity": {
        "look at the science", "thousands of papers", "rapid progress",
        "moving fast", "breakthrough pace", "exponential", "accelerating",
    },
    "appeal_to_future": {
        "will be solved", "next version", "coming soon", "inevitable",
        "just a matter of time", "trajectory is clear",
    },
}

IMMUNE_SEED: set[str] = set().union(*IMMUNE_SEED_BY_CATEGORY.values())

# --------------------------------------------------------------------------
# Protocol §3.3 neutral vocabulary
# --------------------------------------------------------------------------
NEUTRAL_SEED: set[str] = {
    "experiment", "method", "result", "analysis", "data", "figure",
    "table", "hypothesis", "conclusion",
}


@dataclass
class VocabPool:
    """A named set of terms/phrases used to filter and weight documents."""

    name: str
    terms: set[str]
    categories: dict[str, str] = field(default_factory=dict)

    def count_in(self, text: str) -> int:
        """Occurrences of any pool term in text (case-insensitive, substring match
        for multi-word phrases; whole-token match for single words)."""
        lowered = text.lower()
        total = 0
        for term in self.terms:
            if " " in term or "-" in term:
                total += lowered.count(term)
            else:
                total += sum(1 for tok in _tokenize(text) if tok == term)
        return total

    def contains(self, text: str) -> bool:
        return self.count_in(text) > 0


def default_ai_discourse_pools() -> dict[str, VocabPool]:
    """The protocol's own seed lists, ready to use without any empirical
    derivation step. Appropriate for the primary AI-discourse use case
    the protocol was written for; for a different domain, use
    `derive_pools_from_corpus` instead.
    """
    categories = {}
    for cat, terms in IMMUNE_SEED_BY_CATEGORY.items():
        for t in terms:
            categories[t] = cat
    return {
        "claim": VocabPool("claim", set(CLAIM_SEED)),
        "immune": VocabPool("immune", set(IMMUNE_SEED), categories),
        "neutral": VocabPool("neutral", set(NEUTRAL_SEED)),
    }


# --------------------------------------------------------------------------
# Empirical derivation (protocol Appendix A, steps 2-5)
# --------------------------------------------------------------------------

def extract_ngrams(tokens: list[str], n: int) -> list[str]:
    if len(tokens) < n:
        return []
    return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def term_frequency_by_quarter(
    bins: dict[str, list[Document]], quarters: list[str], *, ngram_sizes: tuple[int, ...] = (1, 2, 3)
) -> dict[str, dict[str, float]]:
    """term -> quarter -> normalized frequency (count / total n-grams that quarter).

    Appendix A step 3: "freq[term][quarter] = count(term, quarter) / total_tokens(quarter)".
    We normalize per n-gram-size pool implicitly by pooling all sizes into one
    frequency table, which keeps single terms (equivocation-style) and
    multi-word phrases comparable within a quarter.
    """
    counts: dict[str, dict[str, int]] = {}
    totals: dict[str, int] = {q: 0 for q in quarters}
    for q in quarters:
        for doc in bins.get(q, []):
            toks = doc.tokens
            grams: list[str] = list(toks)
            for n in ngram_sizes:
                if n > 1:
                    grams.extend(extract_ngrams(toks, n))
            totals[q] += len(grams)
            for g in grams:
                counts.setdefault(g, {}).setdefault(q, 0)
                counts[g][q] += 1

    freq: dict[str, dict[str, float]] = {}
    for term, by_q in counts.items():
        freq[term] = {}
        for q in quarters:
            c = by_q.get(q, 0)
            freq[term][q] = (c / totals[q]) if totals[q] else 0.0
    return freq


def coefficient_of_variation(series: list[float]) -> float:
    """CV = std / mean. Returns +inf if mean is zero and std is nonzero,
    0.0 if both are zero (a constant-zero series has no variation)."""
    if not series:
        return 0.0
    mean = statistics.fmean(series)
    if len(series) < 2:
        return 0.0
    std = statistics.pstdev(series)
    if mean == 0:
        return float("inf") if std > 0 else 0.0
    return std / mean


def derive_candidate_pools(
    freq_by_term: dict[str, dict[str, float]],
    quarters: list[str],
    *,
    cv_high: float = 1.5,
    cv_low: float = 0.5,
    min_total_occurrences: int = 3,
) -> tuple[set[str], set[str]]:
    """Appendix A steps 3-5: split terms into claim-candidates (high CV)
    and immune-candidates (low CV) by coefficient of variation across
    quarters. Terms with fewer than `min_total_occurrences` total hits
    are dropped as too sparse for a reliable CV estimate.
    """
    claim_candidates: set[str] = set()
    immune_candidates: set[str] = set()
    for term, by_q in freq_by_term.items():
        series = [by_q.get(q, 0.0) for q in quarters]
        nonzero_hits = sum(1 for v in series if v > 0)
        if nonzero_hits < min_total_occurrences:
            continue
        cv = coefficient_of_variation(series)
        if cv > cv_high:
            claim_candidates.add(term)
        elif cv < cv_low:
            immune_candidates.add(term)
    return claim_candidates, immune_candidates


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


@dataclass
class ValidationResult:
    overlap: float
    threshold: float
    passed: bool
    missing_from_derived: set[str]


def validate_against_seed(derived: set[str], seed: set[str], *, min_overlap: float) -> ValidationResult:
    """Protocol §3.1/§3.2 validation requirements: derived pool must
    overlap the seed list by at least `min_overlap` (Jaccard for claim,
    0.70; a looser subset-recall check for immune, 0.60 of seed present)."""
    overlap = jaccard(derived, seed)
    missing = seed - derived
    return ValidationResult(overlap=overlap, threshold=min_overlap,
                             passed=overlap >= min_overlap, missing_from_derived=missing)


def derive_pools_from_corpus(
    bins: dict[str, list[Document]],
    quarters: list[str],
    *,
    claim_seed: set[str] = CLAIM_SEED,
    immune_seed: set[str] = IMMUNE_SEED,
    neutral_seed: set[str] = NEUTRAL_SEED,
    cv_high: float = 1.5,
    cv_low: float = 0.5,
) -> tuple[dict[str, VocabPool], dict[str, ValidationResult]]:
    """Full Appendix A pipeline: compute term frequencies by quarter,
    split by CV, and intersect with seed lists to produce final pools
    plus their validation results (§3.1: >70% overlap for claim;
    §3.2: >60% seed recall for immune).
    """
    freq = term_frequency_by_quarter(bins, quarters)
    claim_candidates, immune_candidates = derive_candidate_pools(
        freq, quarters, cv_high=cv_high, cv_low=cv_low
    )

    claim_final = claim_candidates & claim_seed if claim_seed else claim_candidates
    immune_final = immune_candidates & immune_seed if immune_seed else immune_candidates

    validations = {
        "claim": validate_against_seed(claim_candidates, claim_seed, min_overlap=0.70),
        "immune": validate_against_seed(immune_candidates, immune_seed, min_overlap=0.60),
    }

    pools = {
        "claim": VocabPool("claim", claim_final or set(claim_seed)),
        "immune": VocabPool("immune", immune_final or set(immune_seed)),
        "neutral": VocabPool("neutral", set(neutral_seed)),
    }
    return pools, validations
