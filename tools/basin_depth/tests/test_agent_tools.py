import json

from basin_depth.agent_tools import basin_depth_demo, basin_depth_derive_vocab, basin_depth_run


def _small_corpus() -> list[dict]:
    quarters = ["2020Q1"] * 5 + ["2020Q2"] * 5 + ["2020Q3"] * 5
    return [
        {"doc_id": str(i), "text": "this is a test document about coherence and drift " * 20, "quarter": q}
        for i, q in enumerate(quarters)
    ]


def test_demo_is_json_safe_and_has_expected_shape():
    report = basin_depth_demo(n_boot=100)
    json.dumps(report)  # must not raise
    assert "basin_depth" in report
    assert "interpretation" in report
    assert "synthetic" in report["note"]


def test_run_against_caller_supplied_corpus_is_json_safe():
    report = basin_depth_run(_small_corpus(), "2020Q1", "2020Q3", n_boot=50, min_tokens=10)
    json.dumps(report)  # must not raise
    assert "basin_depth" in report
    assert report["n_docs_used"] > 0


def test_run_unknown_backend_returns_error_dict_not_exception():
    result = basin_depth_run(_small_corpus(), "2020Q1", "2020Q3", backend="bogus")
    assert "error" in result


def test_run_malformed_document_returns_error_dict_not_exception():
    result = basin_depth_run([{"doc_id": "1", "text": "no quarter field here"}], "2020Q1", "2020Q3")
    assert "error" in result


def test_derive_vocab_is_json_safe():
    result = basin_depth_derive_vocab(_small_corpus(), "2020Q1", "2020Q3")
    json.dumps(result)  # must not raise
    assert "pools" in result
    assert "validation" in result


def test_derive_vocab_malformed_document_returns_error_dict():
    result = basin_depth_derive_vocab([{"doc_id": "1"}], "2020Q1", "2020Q3")
    assert "error" in result
