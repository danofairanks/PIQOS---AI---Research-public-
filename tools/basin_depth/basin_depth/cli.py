"""Command-line interface: `basin-depth run|demo|vocab`."""

from __future__ import annotations

import argparse
import json
import sys

from .corpus import load_csv, load_jsonl, quarter_range, bin_by_quarter, preprocess_corpus
from .pipeline import PipelineConfig, run_basin_depth, to_report_dict
from .vocabulary import default_ai_discourse_pools, derive_pools_from_corpus


def _cmd_run(args: argparse.Namespace) -> int:
    if args.corpus.endswith(".jsonl"):
        docs = load_jsonl(args.corpus)
    else:
        docs = load_csv(args.corpus)

    backend = None
    if args.backend == "embeddings":
        from .embeddings import SentenceTransformerBackend
        backend = SentenceTransformerBackend()

    config = PipelineConfig(
        start_quarter=args.start, end_quarter=args.end,
        backend=backend, max_tau=args.max_tau, min_tokens=args.min_tokens,
        n_boot=args.n_boot, run_permutation=args.permutation, n_perm=args.n_perm,
    )
    result = run_basin_depth(docs, config)
    report = to_report_dict(result)

    text = json.dumps(report, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote report to {args.out}", file=sys.stderr)
    print(text)
    return 0


def _cmd_demo(args: argparse.Namespace) -> int:
    from .examples_data import synthetic_corpus
    docs = synthetic_corpus()
    # Synthetic demo documents are short by construction; the protocol's
    # own min_tokens=100 default is calibrated for real abstracts/articles,
    # not toy sentences, so the demo explicitly relaxes it rather than
    # padding documents with filler that would swamp the planted signal.
    config = PipelineConfig(start_quarter="2018Q1", end_quarter="2026Q4",
                             n_boot=args.n_boot, min_tokens=15)
    result = run_basin_depth(docs, config)
    print(json.dumps(to_report_dict(result), indent=2))
    print(
        f"\nbasin depth B = {result.basin_depth:.2f} -> {result.interpretation} "
        f"(synthetic demo corpus; not a real-world measurement)",
        file=sys.stderr,
    )
    return 0


def _cmd_vocab_derive(args: argparse.Namespace) -> int:
    if args.corpus.endswith(".jsonl"):
        docs = load_jsonl(args.corpus)
    else:
        docs = load_csv(args.corpus)
    docs = preprocess_corpus(docs)
    quarters = quarter_range(args.start, args.end)
    bins = bin_by_quarter(docs, quarters)
    pools, validations = derive_pools_from_corpus(bins, quarters)

    out = {
        "pools": {name: sorted(pool.terms) for name, pool in pools.items()},
        "validation": {
            name: {"overlap": v.overlap, "threshold": v.threshold, "passed": v.passed,
                   "missing_from_derived": sorted(v.missing_from_derived)}
            for name, v in validations.items()
        },
    }
    text = json.dumps(out, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="basin-depth",
                                 description="Noether-Temporal Coherence Test Protocol reference implementation")
    sub = p.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="run the full pipeline against a corpus file")
    p_run.add_argument("--corpus", required=True, help="path to a .jsonl or .csv corpus file")
    p_run.add_argument("--start", required=True, help="start quarter, e.g. 2018Q1")
    p_run.add_argument("--end", required=True, help="end quarter, e.g. 2026Q4")
    p_run.add_argument("--backend", choices=["termfreq", "embeddings"], default="termfreq")
    p_run.add_argument("--max-tau", type=int, default=18)
    p_run.add_argument("--min-tokens", type=int, default=100,
                        help="protocol §2.1 default is 100; lower for small/short test corpora")
    p_run.add_argument("--n-boot", type=int, default=2000)
    p_run.add_argument("--permutation", action="store_true",
                        help="also run the (slower) permutation test")
    p_run.add_argument("--n-perm", type=int, default=200)
    p_run.add_argument("--out", default=None, help="write JSON report to this path")
    p_run.set_defaults(func=_cmd_run)

    p_demo = sub.add_parser("demo", help="run the pipeline against a bundled synthetic corpus (no network needed)")
    p_demo.add_argument("--n-boot", type=int, default=500)
    p_demo.set_defaults(func=_cmd_demo)

    p_vocab = sub.add_parser("vocab", help="vocabulary pool tools")
    vocab_sub = p_vocab.add_subparsers(dest="vocab_command", required=True)
    p_derive = vocab_sub.add_parser("derive", help="empirically derive claim/immune pools from a corpus (Appendix A)")
    p_derive.add_argument("--corpus", required=True)
    p_derive.add_argument("--start", required=True)
    p_derive.add_argument("--end", required=True)
    p_derive.add_argument("--out", default=None)
    p_derive.set_defaults(func=_cmd_vocab_derive)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
