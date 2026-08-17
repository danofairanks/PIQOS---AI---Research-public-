"""Command-line interface: `paper-rigor scan`."""

from __future__ import annotations

import argparse
import json

from .scan import scan_file
from .worklist_triage import DEFAULT_MODEL, WorklistTriageError, triage_worklist


def _cmd_scan(args: argparse.Namespace) -> int:
    authors = [a.strip() for a in args.authors.split(",")] if args.authors else None
    result = scan_file(args.path, byline_authors=authors, min_word_count=args.min_word_count)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


def _cmd_triage(args: argparse.Namespace) -> int:
    authors = [a.strip() for a in args.authors.split(",")] if args.authors else None
    result = scan_file(args.path, byline_authors=authors, min_word_count=args.min_word_count)
    try:
        triage = triage_worklist(result.external_verification_worklist, model=args.model)
    except WorklistTriageError as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 1
    print(json.dumps(triage.to_dict(), indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="paper-rigor",
                                 description="Domain-agnostic paper-rigor scanner: placeholders, falsifiability, "
                                             "self-citation, credentialing, consensus claims, citation-type mix")
    sub = p.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="scan a single paper")
    p_scan.add_argument("path")
    p_scan.add_argument("--authors", default=None,
                         help="comma-separated author last names, for self-citation ratio (omit if anonymous)")
    p_scan.add_argument("--min-word-count", type=int, default=400)
    p_scan.set_defaults(func=_cmd_scan)

    p_triage = sub.add_parser(
        "triage-worklist",
        help="scan a paper, then get an AI-generated (Groq) priority + suggested_check for each "
             "external_verification_worklist item (advisory only -- requires GROQ_API_KEY)",
    )
    p_triage.add_argument("path")
    p_triage.add_argument("--authors", default=None)
    p_triage.add_argument("--min-word-count", type=int, default=400)
    p_triage.add_argument("--model", default=DEFAULT_MODEL)
    p_triage.set_defaults(func=_cmd_triage)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
