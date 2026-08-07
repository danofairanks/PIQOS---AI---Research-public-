from basin_depth.corpus import (
    Document, deduplicate, filter_by_length, jaccard_similarity,
    quarter_index, quarter_range, bin_by_quarter, parse_quarter,
)


def test_parse_quarter_roundtrip():
    assert parse_quarter("2023Q1") == (2023, 1)
    assert parse_quarter("1999Q4") == (1999, 4)


def test_quarter_range_inclusive():
    qs = quarter_range("2023Q3", "2024Q2")
    assert qs == ["2023Q3", "2023Q4", "2024Q1", "2024Q2"]


def test_quarter_range_single():
    assert quarter_range("2020Q1", "2020Q1") == ["2020Q1"]


def test_quarter_index_orders_correctly():
    assert quarter_index("2020Q1") < quarter_index("2020Q4") < quarter_index("2021Q1")


def test_jaccard_similarity_basic():
    assert jaccard_similarity({"a", "b"}, {"a", "b"}) == 1.0
    assert jaccard_similarity({"a"}, {"b"}) == 0.0
    assert jaccard_similarity(set(), set()) == 1.0
    assert jaccard_similarity({"a", "b", "c"}, {"b", "c", "d"}) == 2 / 4


def test_filter_by_length():
    docs = [
        Document("1", "one two three", "2020Q1"),
        Document("2", " ".join(["word"] * 200), "2020Q1"),
    ]
    kept = filter_by_length(docs, min_tokens=100)
    assert [d.doc_id for d in kept] == ["2"]


def test_deduplicate_removes_near_identical():
    base = "the quick brown fox jumps over the lazy dog many times in a row here"
    docs = [
        Document("1", base, "2020Q1"),
        Document("2", base + " extra", "2020Q1"),  # near-duplicate
        Document("3", "completely different content about an unrelated topic entirely", "2020Q1"),
    ]
    deduped = deduplicate(docs, threshold=0.85)
    ids = {d.doc_id for d in deduped}
    assert "1" in ids
    assert "3" in ids
    assert len(deduped) == 2  # doc 2 dropped as a near-duplicate of doc 1


def test_bin_by_quarter_preserves_requested_quarters():
    docs = [Document("1", "x", "2020Q1"), Document("2", "y", "2020Q3")]
    bins = bin_by_quarter(docs, quarters=quarter_range("2020Q1", "2020Q4"))
    assert set(bins.keys()) == {"2020Q1", "2020Q2", "2020Q3", "2020Q4"}
    assert len(bins["2020Q1"]) == 1
    assert len(bins["2020Q2"]) == 0
