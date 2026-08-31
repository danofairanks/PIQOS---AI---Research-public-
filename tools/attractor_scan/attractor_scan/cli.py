"""Command-line interface: `attractor-scan text|corpus`."""

from __future__ import annotations

import argparse
import json
import sys

from .claim_boundary import check_boundary_portability
from .scan import scan, scan_corpus
from .visual_proof_judge import DEFAULT_MODEL, VisualProofJudgeError, judge_visual_proof


def _cmd_text(args: argparse.Namespace) -> int:
    if args.file:
        text = open(args.file, encoding="utf-8").read()
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()
    result = scan(text)
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def _cmd_corpus(args: argparse.Namespace) -> int:
    documents = []
    with open(args.corpus, encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            documents.append((str(obj.get("id", i)), obj["text"]))
    summary = scan_corpus(documents)
    print(json.dumps(summary.to_dict(), indent=2))
    return 0


def _cmd_visual_proof(args: argparse.Namespace) -> int:
    try:
        result = judge_visual_proof(args.claim, image_path=args.image, model=args.model)
    except VisualProofJudgeError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 1
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def _cmd_claim_boundary(args: argparse.Namespace) -> int:
    source_text = open(args.source_file, encoding="utf-8").read() if args.source_file else args.source_text
    citation_text = (
        open(args.citation_file, encoding="utf-8").read() if args.citation_file else args.citation_text
    )
    if source_text is None or citation_text is None:
        print(json.dumps({"error": "both a source and a citation text/file are required"}, indent=2))
        return 1
    result = check_boundary_portability(source_text, citation_text)
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="attractor-scan",
                                 description="Classifier for basin_attractors_v1.md's defensive maneuvers and semantic-laundering cases")
    sub = p.add_subparsers(dest="command", required=True)

    p_text = sub.add_parser("text", help="scan a single piece of text")
    p_text.add_argument("--text", default=None)
    p_text.add_argument("--file", default=None, help="read text from this file instead of --text/stdin")
    p_text.set_defaults(func=_cmd_text)

    p_corpus = sub.add_parser("corpus", help="scan a JSONL corpus ({\"id\":..., \"text\":...} per line) and aggregate")
    p_corpus.add_argument("--corpus", required=True)
    p_corpus.set_defaults(func=_cmd_corpus)

    p_visual = sub.add_parser(
        "visual-proof",
        help="get an AI-generated (Groq vision) candidate read on Case 6 for one image + claim "
             "(advisory only, single-specimen research aid -- requires GROQ_API_KEY)",
    )
    p_visual.add_argument("--claim", required=True)
    p_visual.add_argument("--image", required=True, help="path to a local image file")
    p_visual.add_argument("--model", default=DEFAULT_MODEL)
    p_visual.set_defaults(func=_cmd_visual_proof)

    p_boundary = sub.add_parser(
        "claim-boundary",
        help="check whether a source document's stated limitations show any lexical trace "
             "in a separate citation/reference text (two-document comparison; lead, not a verdict)",
    )
    p_boundary.add_argument("--source-text", default=None)
    p_boundary.add_argument("--source-file", default=None, help="read source text from this file instead of --source-text")
    p_boundary.add_argument("--citation-text", default=None)
    p_boundary.add_argument("--citation-file", default=None, help="read citation text from this file instead of --citation-text")
    p_boundary.set_defaults(func=_cmd_claim_boundary)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
