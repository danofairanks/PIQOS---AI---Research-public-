# basin-depth

Reference implementation of the [Noether-Temporal Coherence Test
Protocol](../../protocols/noether_coherence_test_protocol_v1.md)
(v1.0), the operational falsification test derived in
[`basin_attractors_v1.md`](../../papers/published/basin_attractors_v1.md)
§4-5. It measures whether the *defensive/immune vocabulary* of a
field's discourse (goal-post movement, provisionalization, status
dismissal, ...) persists longer, autocorrelation-wise, than the
field's *surface claim vocabulary* — the falsifiable signature the
paper predicts for a "captured" epistemic field, and predicts should
be absent (or much smaller) in a self-correcting one.

**This tool does not assume the answer.** Run it against a corpus and
it reports a number, `B = tau_c_immune / tau_c_claim`, with bootstrap
and permutation significance tests. `B <= 1` is a real, printable
result — it means the corpus you fed it shows no evidence of a deep
basin. Nothing in this codebase nudges the output toward confirming
the hypothesis; see [Honesty notes](#honesty-notes-what-this-tool-does-not-do) below.

## Install

```bash
cd tools/basin_depth
pip install -e .            # numpy + scipy only, no heavy deps
pip install -e ".[embeddings]"  # optional: adds sentence-transformers for §4.1's real embedding backend
```

Requires Python >= 3.10.

## 60-second demo (no corpus, no network required)

```bash
basin-depth demo
# or:
python3 examples/synthetic_demo.py
```

This runs the full pipeline against a bundled, deliberately-constructed
synthetic corpus (rotating era-specific "claim" vocabulary against a
constant set of "immune" phrases repeated unchanged every quarter) so
you can see the whole measurement — autocorrelation, exponential decay
fit, bootstrap test, Cohen's d, the final `B` — working end to end
before pointing it at anything real. **It is a toy corpus, not a
measurement of anything.**

## Running it on your own corpus

The library is deliberately source-agnostic: it does not ship
scrapers for arXiv, lab blogs, or earnings calls (protocol §2.1's
source list). Bring your own corpus as JSONL or CSV:

```jsonl
{"id": "doc1", "text": "full document text here...", "quarter": "2023Q1", "source": "arxiv"}
{"id": "doc2", "text": "...", "quarter": "2023Q1", "source": "blog"}
```

```bash
basin-depth run \
  --corpus mycorpus.jsonl \
  --start 2018Q1 --end 2026Q4 \
  --backend termfreq \
  --n-boot 2000 \
  --out report.json
```

- `--backend termfreq` (default): zero-dependency hashed bag-of-words
  embedding. This is the protocol's §4.4 "term-frequency alternative,"
  used here as the light default rather than as only a robustness check.
- `--backend embeddings`: protocol §4.1's actual `all-MiniLM-L6-v2`
  sentence-transformer embeddings. Requires the `[embeddings]` extra.
- `--permutation`: also runs protocol §6.3 Method B (re-embeds the
  corpus per permutation; slow — off by default, on for a full
  publication-grade run).

Or as a library:

```python
from basin_depth import Document, PipelineConfig, run_basin_depth, to_report_dict

docs = [Document(doc_id="1", text="...", quarter="2023Q1"), ...]
result = run_basin_depth(docs, PipelineConfig(start_quarter="2018Q1", end_quarter="2026Q4"))
print(result.basin_depth, result.interpretation)
print(to_report_dict(result))  # JSON-serializable full report
```

## What's implemented, mapped to the protocol document

| Protocol section | Module | Status |
|---|---|---|
| §2 Corpus Specification (ingestion, dedup, length filter) | `corpus.py` | Implemented (source-agnostic: JSONL/CSV in, not per-source scrapers) |
| §3 Vocabulary Operationalization | `vocabulary.py` | Protocol's own seed lists shipped verbatim; empirical CV-based derivation (Appendix A) implemented for other domains |
| §4 Autocorrelation (embedding + term-frequency) | `embeddings.py`, `autocorrelation.py` | Both methods implemented |
| §5 Coherence Time Extraction (exponential fit + threshold) | `coherence.py` | Both methods implemented |
| §6 Statistical Test (bootstrap, permutation, cross-corpus, Cohen's d) | `stats.py` | All three significance methods + effect size implemented |
| §7 Control Tests (placebo vocabulary, temporal reversal) | `controls.py` | Implemented as composable functions — run them by calling the pipeline with a placebo/reversed input, same as §7.1/§7.2's "identical protocol, different corpus" framing |
| §11 Output (basin-depth metric + interpretation) | `pipeline.py` | `run_basin_depth()` returns the full `BasinDepthResult`; `to_report_dict()` for JSON |

## Honesty notes — what this tool does NOT do

- **It does not source a real corpus for you.** §2.1's arXiv/blog/
  earnings-call pipeline is real infrastructure work (rate limits,
  HTML parsing per source, Wayback Machine snapshotting for
  reproducibility per §9.1) that this release does not include. The
  measurement engine is complete and tested; corpus acquisition is
  explicitly left to the caller.
- **`basin-depth demo`'s output is not a finding.** The synthetic
  corpus plants the signal on purpose so the pipeline has something to
  show. Reporting `demo`'s `B` value as if it said anything about real
  AI discourse would be exactly the kind of unearned precision this
  project's own research elsewhere is built to catch.
- **A high `B` does not, by itself, prove a field is "captured."**
  Protocol §7 exists precisely because a naive reading of `B` can be
  an artifact of vocabulary-frequency stability rather than genuine
  immune-structure persistence — run the placebo-vocabulary and
  temporal-reversal controls (§7.3-7.4) before treating a result as
  more than a first pass, and see §10 (protocol document) for the
  full limitations list (single-field validation, English-only,
  vocabulary-pool sensitivity, embedding-model bias, correlation-not-
  causation).
- **The term-frequency backend (this tool's default) is a lower-fidelity
  stand-in for real sentence embeddings.** The protocol treats
  embedding-based autocorrelation as primary and term-frequency as a
  robustness check (§4.4); this tool inverts which one is the
  zero-config default purely for installability, not because
  term-frequency is claimed to be equally accurate. Use
  `--backend embeddings` for anything you intend to report.
- **Reproducibility (§9) is your responsibility for your own corpus.**
  This tool fixes random seeds internally (`seed=0` default throughout)
  so its own computations are deterministic given identical input, but
  it does not archive source documents, compute document hashes, or
  timestamp-verify a corpus for you — do that before publishing a result.

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

43 tests cover: corpus preprocessing (dedup, length filtering, quarter
arithmetic), vocabulary CV derivation and seed-list validation,
autocorrelation on hand-computable synthetic signatures (constant
signal → γ≡1; orthogonal alternation → known period-2 pattern),
exponential-decay-constant recovery against planted ground truth,
Cohen's d against a manual calculation, and end-to-end pipeline runs
including the qualitative claim the protocol exists to test
(tau_c_immune > tau_c_claim on a corpus built to have that property).

## License

MIT, same as the rest of this repository.
