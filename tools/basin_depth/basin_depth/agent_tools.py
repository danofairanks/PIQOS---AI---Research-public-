"""Stable, JSON-in/JSON-out function surface for agent tool-calling.

Same contract as `bifp/agent_tools.py`: every function here takes and
returns only plain JSON-serializable types (str, bool, int, float,
dict, list, None), so this module can be wrapped directly as MCP tool
handlers without any adaptation layer. `tools/mcp_server/` does exactly
that -- see its README for the live, tested server.

This module is intentionally the only place in the package with this
constraint; `pipeline.py`, `corpus.py`, and friends are free to use
dataclasses internally. A `Document` list crosses this boundary as a
plain list of dicts (`doc_id`, `text`, `quarter`, optional `source`),
reconstructed into real `Document` objects on the way in.
"""

from __future__ import annotations

from .corpus import Document, bin_by_quarter, preprocess_corpus, quarter_range
from .pipeline import PipelineConfig, run_basin_depth, to_report_dict
from .vocabulary import derive_pools_from_corpus


def _docs_from_json(documents: list[dict]) -> list[Document]:
    return [
        Document(
            doc_id=str(d["doc_id"]),
            text=str(d["text"]),
            quarter=str(d["quarter"]),
            source=str(d.get("source", "")),
            metadata=dict(d.get("metadata", {})),
        )
        for d in documents
    ]


def basin_depth_demo(*, n_boot: int = 500) -> dict:
    """Run the pipeline against the bundled synthetic corpus (no
    network, no real corpus needed) and return the full JSON report.
    A quick way for an agent to confirm the tool works and see the
    report shape before bringing a real corpus."""
    from .examples_data import synthetic_corpus

    docs = synthetic_corpus()
    config = PipelineConfig(start_quarter="2018Q1", end_quarter="2026Q4",
                             n_boot=n_boot, min_tokens=15)
    result = run_basin_depth(docs, config)
    report = to_report_dict(result)
    report["note"] = "synthetic demo corpus -- not a real-world measurement"
    return report


def basin_depth_run(documents: list[dict], start_quarter: str, end_quarter: str, *,
                     backend: str = "termfreq", max_tau: int = 18, min_tokens: int = 100,
                     n_boot: int = 2000, run_permutation: bool = False, n_perm: int = 200) -> dict:
    """Run the full Noether-Temporal Coherence Test Protocol pipeline
    against a caller-supplied corpus and return the JSON report
    (protocol §11 primary + interpretation deliverables).

    `documents`: list of `{"doc_id": str, "text": str, "quarter": str,
    "source": str (optional), "metadata": dict (optional)}`.
    `backend`: "termfreq" (zero-dependency, default) or "embeddings"
    (requires sentence-transformers to be installed separately --
    returns an error dict rather than raising if it isn't).
    `run_permutation=True` re-embeds documents `n_perm` times and can
    be slow; leave it off unless you specifically need that test.
    """
    if backend not in ("termfreq", "embeddings"):
        return {"error": f"unknown backend {backend!r}; expected 'termfreq' or 'embeddings'"}

    embedding_backend = None
    if backend == "embeddings":
        try:
            from .embeddings import SentenceTransformerBackend
            embedding_backend = SentenceTransformerBackend()
        except ImportError as exc:
            return {"error": f"embeddings backend unavailable: {exc}"}

    try:
        docs = _docs_from_json(documents)
    except (KeyError, TypeError) as exc:
        return {"error": f"malformed document: {exc}"}

    config = PipelineConfig(
        start_quarter=start_quarter, end_quarter=end_quarter,
        backend=embedding_backend, max_tau=max_tau, min_tokens=min_tokens,
        n_boot=n_boot, run_permutation=run_permutation, n_perm=n_perm,
    )
    result = run_basin_depth(docs, config)
    return to_report_dict(result)


def basin_depth_derive_vocab(documents: list[dict], start_quarter: str, end_quarter: str) -> dict:
    """Empirically derive claim/immune/neutral vocabulary pools from a
    caller-supplied corpus (protocol Appendix A), instead of using the
    protocol's own AI-discourse seed lists. Useful when applying the
    protocol outside the AI-discourse domain it was written for."""
    try:
        docs = _docs_from_json(documents)
    except (KeyError, TypeError) as exc:
        return {"error": f"malformed document: {exc}"}

    docs = preprocess_corpus(docs)
    quarters = quarter_range(start_quarter, end_quarter)
    bins = bin_by_quarter(docs, quarters)
    pools, validations = derive_pools_from_corpus(bins, quarters)

    return {
        "pools": {name: sorted(pool.terms) for name, pool in pools.items()},
        "validation": {
            name: {"overlap": v.overlap, "threshold": v.threshold, "passed": v.passed,
                   "missing_from_derived": sorted(v.missing_from_derived)}
            for name, v in validations.items()
        },
    }
