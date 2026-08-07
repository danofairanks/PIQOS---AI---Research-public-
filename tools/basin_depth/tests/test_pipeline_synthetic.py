import json

from basin_depth.corpus import Document
from basin_depth.pipeline import PipelineConfig, run_basin_depth, to_report_dict
from basin_depth.vocabulary import VocabPool


def _tiny_corpus() -> list[Document]:
    """A hand-built corpus small enough to run instantly, with the same
    planted-signal shape as the CLI demo: 'stable' vocabulary repeats
    every quarter, 'shifting' vocabulary rotates. Each document is given
    a unique quarter/index marker so `deduplicate()` (a real, protocol-
    mandated preprocessing step) does not collapse the deliberately
    repeated stable-vocabulary documents across quarters into a single
    surviving copy -- exactly the trap real near-duplicate detection is
    supposed to catch, so the fixture has to avoid it honestly rather
    than by disabling dedup for the test."""
    docs = []
    quarters = [f"2020Q{i}" for i in range(1, 5)] + [f"2021Q{i}" for i in range(1, 5)]
    for i, q in enumerate(quarters):
        shifting_term = "alpha term" if i % 2 == 0 else "beta term"
        for j in range(4):
            stable_text = (f"stable phrase stable phrase filler words here to pad "
                            f"this synthetic document out a little further, marker {q}-{j}")
            shifting_text = (f"{shifting_term} {shifting_term} filler words here to pad "
                              f"this synthetic document out a little further, marker {q}-{j}")
            docs.append(Document(f"{q}-stable-{j}", stable_text, q))
            docs.append(Document(f"{q}-shift-{j}", shifting_text, q))
    return docs


def _tiny_pools() -> dict[str, VocabPool]:
    return {
        "claim": VocabPool("claim", {"alpha term", "beta term"}),
        "immune": VocabPool("immune", {"stable phrase"}),
        "neutral": VocabPool("neutral", {"filler"}),
    }


def test_pipeline_runs_end_to_end_and_produces_sane_types():
    config = PipelineConfig(
        start_quarter="2020Q1", end_quarter="2021Q4",
        vocab_pools=_tiny_pools(), max_tau=4, min_tokens=5, n_boot=30,
    )
    result = run_basin_depth(_tiny_corpus(), config)

    assert result.n_docs_used > 0
    assert set(result.tau_c_fits.keys()) == {"claim", "immune", "neutral"}
    assert isinstance(result.basin_depth, float)
    assert result.interpretation in {
        "no evidence of deep basin", "weak basin", "moderate basin", "deep basin",
    }
    assert 0.0 <= result.bootstrap.p_value <= 1.0


def test_pipeline_immune_persists_longer_than_claim_on_planted_signal():
    """The core qualitative prediction the protocol tests for: on a
    corpus where immune vocabulary never changes and claim vocabulary
    rotates by era, tau_c_immune should exceed tau_c_claim, i.e.
    basin_depth > 1. The 8-quarter/max_tau=4 tiny fixture used
    elsewhere in this file is too short a window for the exponential
    fit to discriminate real decay from the tau_c upper-bound cap
    (both saturate it), so this test uses the same bundled
    synthetic corpus the CLI's `basin-depth demo` runs against, which
    spans the full 36-quarter window the protocol itself specifies."""
    from basin_depth.examples_data import synthetic_corpus

    config = PipelineConfig(
        start_quarter="2018Q1", end_quarter="2026Q4",
        max_tau=12, min_tokens=15, n_boot=30,
    )
    result = run_basin_depth(synthetic_corpus(), config)
    assert result.tau_c_fits["immune"].tau_c > result.tau_c_fits["claim"].tau_c
    assert result.basin_depth > 1.0


def test_report_dict_is_valid_strict_json_no_nan_literal():
    config = PipelineConfig(
        start_quarter="2020Q1", end_quarter="2021Q4",
        vocab_pools=_tiny_pools(), max_tau=4, min_tokens=5, n_boot=10,
    )
    result = run_basin_depth(_tiny_corpus(), config)
    report = to_report_dict(result)
    text = json.dumps(report)
    assert "NaN" not in text
    assert "Infinity" not in text
    # round-trips cleanly
    assert json.loads(text) == report


def test_pipeline_with_permutation_test_runs():
    config = PipelineConfig(
        start_quarter="2020Q1", end_quarter="2021Q4",
        vocab_pools=_tiny_pools(), max_tau=3, min_tokens=5, n_boot=10,
        run_permutation=True, n_perm=5,
    )
    result = run_basin_depth(_tiny_corpus(), config)
    assert result.permutation is not None
    assert result.permutation.n_perm == 5
    assert 0.0 <= result.permutation.p_value <= 1.0
