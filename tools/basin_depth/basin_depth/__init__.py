"""Reference implementation of the Noether-Temporal Coherence Test Protocol
(protocols/noether_coherence_test_protocol_v1.md) for measuring
basin-attractor depth in a time-stamped text corpus.

Quick start::

    from basin_depth import Document, PipelineConfig, run_basin_depth

    docs = [Document(doc_id="1", text="...", quarter="2023Q1"), ...]
    result = run_basin_depth(docs, PipelineConfig(start_quarter="2018Q1", end_quarter="2026Q4"))
    print(result.basin_depth, result.interpretation)

Or from the command line::

    basin-depth demo
    basin-depth run --corpus mycorpus.jsonl --start 2018Q1 --end 2026Q4
"""

from .corpus import Document, load_csv, load_jsonl, quarter_range
from .pipeline import BasinDepthResult, PipelineConfig, run_basin_depth, to_report_dict
from .vocabulary import VocabPool, default_ai_discourse_pools, derive_pools_from_corpus

__all__ = [
    "Document",
    "load_csv",
    "load_jsonl",
    "quarter_range",
    "BasinDepthResult",
    "PipelineConfig",
    "run_basin_depth",
    "to_report_dict",
    "VocabPool",
    "default_ai_discourse_pools",
    "derive_pools_from_corpus",
]

__version__ = "0.1.0"
