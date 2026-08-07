#!/usr/bin/env python3
"""Runnable demonstration of the basin_depth library, using the bundled
synthetic corpus -- no network access, no real corpus, no GPU required.

    python3 examples/synthetic_demo.py

For a real measurement, replace `synthetic_corpus()` with your own
`Document` list loaded via `basin_depth.load_jsonl` / `load_csv`, or
just use the CLI: `basin-depth run --corpus yours.jsonl --start ... --end ...`
"""

from basin_depth import PipelineConfig, run_basin_depth, to_report_dict
from basin_depth.examples_data import synthetic_corpus


def main() -> None:
    docs = synthetic_corpus()
    print(f"Synthetic corpus: {len(docs)} documents, 2018Q1-2026Q4\n")

    config = PipelineConfig(
        start_quarter="2018Q1",
        end_quarter="2026Q4",
        min_tokens=15,  # relaxed from the protocol's real-corpus default of 100
        n_boot=500,
    )
    result = run_basin_depth(docs, config)

    print("Coherence times (quarters):")
    for name, fit in result.tau_c_fits.items():
        flag = " [saturated observation window]" if fit.censored else ""
        print(f"  tau_c_{name:8s} = {fit.tau_c:8.2f}  (R^2={fit.r_squared:.3f}){flag}")

    print(f"\ndelta_tau_c (immune - claim) = {result.delta_tau_c:.2f}")
    print(f"basin_depth B                = {result.basin_depth:.2f}")
    print(f"interpretation                -> {result.interpretation}")
    print(f"bootstrap p-value             = {result.bootstrap.p_value:.3f}")
    print(f"Cohen's d                     = {result.cohens_d:.2f} ({result.cohens_d_interpretation})")

    print("\nThis is a synthetic corpus constructed to demonstrate the pipeline,")
    print("NOT a real measurement of AI discourse. See ../README.md and the")
    print("protocol document for how to point this at a real, timestamped corpus.")

    import json
    print("\nFull report (JSON):")
    print(json.dumps(to_report_dict(result), indent=2))


if __name__ == "__main__":
    main()
