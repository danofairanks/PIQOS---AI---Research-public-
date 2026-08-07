"""End-to-end orchestration: corpus -> basin-depth metric.

Wires together corpus.py, vocabulary.py, embeddings.py,
autocorrelation.py, coherence.py, and stats.py into the single
measurement the protocol's §11 calls for: B = tau_c_immune / tau_c_claim,
with its supporting statistical tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .autocorrelation import autocorrelation
from .coherence import CoherenceFit, fit_exponential_decay, threshold_coherence_time
from .corpus import Document, bin_by_quarter, preprocess_corpus
from .embeddings import EmbeddingBackend, TermFrequencyBackend, compute_signatures
from .stats import (
    BootstrapResult, PermutationResult, block_bootstrap_delta,
    cohens_d, interpret_cohens_d, permutation_test,
)
from .vocabulary import VocabPool, default_ai_discourse_pools


@dataclass
class PipelineConfig:
    start_quarter: str
    end_quarter: str
    vocab_pools: dict[str, VocabPool] | None = None  # None -> default_ai_discourse_pools()
    backend: EmbeddingBackend | None = None  # None -> TermFrequencyBackend()
    max_tau: int = 18
    min_tokens: int = 100
    dedup_threshold: float = 0.85
    n_boot: int = 2000
    run_permutation: bool = False  # opt-in: re-embeds documents n_perm times, can be slow
    n_perm: int = 200
    seed: int | None = 0


@dataclass
class BasinDepthResult:
    quarters: list[str]
    tau_c_fits: dict[str, CoherenceFit]  # per pool: "claim", "immune", "neutral"
    tau_c_threshold: dict[str, float]
    delta_tau_c: float
    basin_depth: float
    interpretation: str
    bootstrap: BootstrapResult
    permutation: PermutationResult | None
    cohens_d: float
    cohens_d_interpretation: str
    n_docs_used: int
    gamma: dict[str, dict[int, float]] = field(default_factory=dict)


def interpret_basin_depth(B: float) -> str:
    """Protocol §11.2 interpretation table."""
    if B <= 1:
        return "no evidence of deep basin"
    if B <= 2:
        return "weak basin"
    if B <= 5:
        return "moderate basin"
    return "deep basin"


def run_basin_depth(docs: list[Document], config: PipelineConfig) -> BasinDepthResult:
    """Run the full protocol pipeline (§2 preprocessing through §6
    statistical testing) and return the basin-depth result.

    `docs` should already be timestamped with `Document.quarter`
    labels; this function applies length filtering and deduplication
    (§2.1), then everything downstream of corpus ingestion.
    """
    from .corpus import quarter_range

    quarters = quarter_range(config.start_quarter, config.end_quarter)
    vocab_pools = config.vocab_pools or default_ai_discourse_pools()
    backend = config.backend or TermFrequencyBackend()

    clean_docs = preprocess_corpus(docs, min_tokens=config.min_tokens, dedup_threshold=config.dedup_threshold)
    bins = bin_by_quarter(clean_docs, quarters)

    signatures = compute_signatures(bins, quarters, vocab_pools, backend)

    gamma: dict[str, dict[int, float]] = {}
    tau_c_fits: dict[str, CoherenceFit] = {}
    tau_c_threshold: dict[str, float] = {}
    for name in vocab_pools:
        g = autocorrelation(signatures[name], quarters, config.max_tau)
        gamma[name] = g
        tau_c_fits[name] = fit_exponential_decay(g)
        tau_c_threshold[name] = threshold_coherence_time(g)

    delta_tau_c = tau_c_fits["immune"].tau_c - tau_c_fits["claim"].tau_c
    basin_depth = (
        tau_c_fits["immune"].tau_c / tau_c_fits["claim"].tau_c
        if tau_c_fits["claim"].tau_c > 0 else float("inf")
    )

    bootstrap = block_bootstrap_delta(
        signatures, quarters, config.max_tau,
        pool_a="immune", pool_b="claim", n_boot=config.n_boot, seed=config.seed,
    )

    permutation: PermutationResult | None = None
    if config.run_permutation:
        permutation = permutation_test(
            clean_docs, quarters, vocab_pools, backend, config.max_tau,
            observed_delta=delta_tau_c, pool_a="immune", pool_b="claim",
            n_perm=config.n_perm, seed=config.seed,
        )

    d = cohens_d(bootstrap.tau_c_a_samples, bootstrap.tau_c_b_samples)

    return BasinDepthResult(
        quarters=quarters,
        tau_c_fits=tau_c_fits,
        tau_c_threshold=tau_c_threshold,
        delta_tau_c=delta_tau_c,
        basin_depth=basin_depth,
        interpretation=interpret_basin_depth(basin_depth),
        bootstrap=bootstrap,
        permutation=permutation,
        cohens_d=d,
        cohens_d_interpretation=interpret_cohens_d(d),
        n_docs_used=len(clean_docs),
        gamma=gamma,
    )


def _json_safe(obj):
    """Recursively replace NaN/Infinity with None so the report is valid
    under strict JSON parsers (Python's json module permits NaN by
    default, but many other languages' JSON parsers reject it)."""
    if isinstance(obj, float):
        return None if (obj != obj or obj in (float("inf"), float("-inf"))) else obj
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    return obj


def to_report_dict(result: BasinDepthResult) -> dict:
    """JSON-serializable summary of a BasinDepthResult (protocol §11
    primary + interpretation deliverables)."""
    return _json_safe({
        "quarters": {"start": result.quarters[0], "end": result.quarters[-1], "n": len(result.quarters)},
        "n_docs_used": result.n_docs_used,
        "tau_c": {
            name: {
                "exponential_fit": fit.tau_c,
                "stderr": fit.tau_c_stderr,
                "r_squared": fit.r_squared,
                "censored": fit.censored,
                "threshold_method": result.tau_c_threshold[name],
            }
            for name, fit in result.tau_c_fits.items()
        },
        "delta_tau_c": result.delta_tau_c,
        "basin_depth": result.basin_depth,
        "interpretation": result.interpretation,
        "bootstrap": {
            "p_value": result.bootstrap.p_value,
            "ci_95": result.bootstrap.ci_95,
            "n_boot": result.bootstrap.n_boot,
        },
        "permutation": (
            {"p_value": result.permutation.p_value, "n_perm": result.permutation.n_perm}
            if result.permutation else None
        ),
        "cohens_d": result.cohens_d,
        "cohens_d_interpretation": result.cohens_d_interpretation,
    })
