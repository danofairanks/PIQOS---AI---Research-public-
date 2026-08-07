"""A bundled synthetic corpus for `basin-depth demo`.

This is NOT real AI discourse. It is a deliberately constructed
toy corpus that plants the effect the protocol predicts for a
captured field — rotating, era-specific claim vocabulary against a
small, constant set of immune-maneuver phrases repeated unchanged in
every quarter — purely so that a fresh install has something runnable
in seconds, with no network access and no real corpus required. Use
`basin-depth run --corpus yours.jsonl ...` for an actual measurement.
"""

from __future__ import annotations

import random

from .corpus import Document, quarter_range
from .vocabulary import IMMUNE_SEED_BY_CATEGORY, NEUTRAL_SEED

# Protocol §3.1's own era table, kept as explicit per-era buckets here
# (rather than the flattened CLAIM_SEED) because the synthetic
# generator needs to know *which* claim terms are live in which era.
_ERA_CLAIM_TERMS: dict[tuple[int, int], list[str]] = {
    (2018, 2020): ["artificial general intelligence", "transformative ai", "gpt-3",
                   "few-shot learning", "bert", "scaling laws"],
    (2021, 2022): ["chatgpt", "sparks of agi", "emergent abilities", "alignment problem",
                   "large language model", "prompt engineering"],
    (2023, 2023): ["gpt-4", "multimodal", "frontier model", "reasoning",
                   "constitutional ai", "rlhf"],
    (2024, 2024): ["o1", "reasoning model", "agentic ai", "superintelligence",
                   "ai scientist", "test-time compute"],
    (2025, 2026): ["singularity", "event horizon", "gentle singularity", "asi",
                   "recursive self-improvement", "mars colonies ai"],
}

_IMMUNE_TERMS = [t for terms in IMMUNE_SEED_BY_CATEGORY.values() for t in terms][:8]
_FILLER = [
    "the field continues to develop rapidly this quarter",
    "researchers and commentators discussed the implications at length",
    "industry observers noted several developments worth tracking",
    "the discourse this period covered a range of related topics",
    "several publications addressed related questions during this window",
    "public commentary on the subject remained active throughout the period",
    "a number of contributors weighed in with their own perspectives",
    "coverage of the topic appeared across multiple outlets this quarter",
    "the conversation touched on both technical and social dimensions",
    "responses to prior developments continued to circulate widely",
]


def _claim_terms_for_year(year: int) -> list[str]:
    for (lo, hi), terms in _ERA_CLAIM_TERMS.items():
        if lo <= year <= hi:
            return terms
    return _ERA_CLAIM_TERMS[(2025, 2026)]


def _make_doc(doc_id: str, quarter: str, kind: str, rng: random.Random) -> Document:
    year = int(quarter[:4])
    filler_sentences = rng.sample(_FILLER, k=3)
    neutral = rng.sample(sorted(NEUTRAL_SEED), k=3)

    if kind == "claim":
        term_choices = _claim_terms_for_year(year)
    else:
        term_choices = _IMMUNE_TERMS
    # repeat each chosen term twice, the way a real document tends to
    # reference its own core topic more than once, so the term signal
    # is not swamped by the surrounding filler sentences
    terms = rng.sample(term_choices, k=min(4, len(term_choices))) * 2

    words = filler_sentences + terms + neutral
    rng.shuffle(words)
    text = ". ".join(words) + f". this document is document {doc_id} for {quarter}."
    return Document(doc_id=doc_id, text=text, quarter=quarter, source="synthetic")


def synthetic_corpus(*, docs_per_quarter: int = 8, seed: int = 0) -> list[Document]:
    """Deterministic synthetic corpus spanning 2018Q1-2026Q4 with a
    planted basin-depth signal (see module docstring)."""
    rng = random.Random(seed)
    quarters = quarter_range("2018Q1", "2026Q4")
    docs: list[Document] = []
    for q in quarters:
        for i in range(docs_per_quarter):
            kind = "claim" if i % 2 == 0 else "immune"
            docs.append(_make_doc(f"{q}-{i}", q, kind, rng))
    return docs
