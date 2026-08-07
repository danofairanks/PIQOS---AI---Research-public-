"""Command-line interface: `verification-lint scan|scan-dir`."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .scan import scan_file, scan_paths


def _cmd_scan(args: argparse.Namespace) -> int:
    result = scan_file(args.path, min_word_count=args.min_word_count)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


def _cmd_scan_dir(args: argparse.Namespace) -> int:
    paths = sorted(Path(args.directory).rglob(args.pattern))
    results = scan_paths(paths, min_word_count=args.min_word_count)
    summary = {
        "n_files": len(results),
        "n_files_with_gaps": sum(1 for r in results if not r.ok),
        "total_gap_count": sum(r.gap_count for r in results),
        "files": [r.to_dict() for r in results if not args.only_gaps or not r.ok],
    }
    print(json.dumps(summary, indent=2))
    return 0 if summary["n_files_with_gaps"] == 0 else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="verification-lint",
                                 description="Scan markdown for unattributed quotes, uncited statistics, and missing disclaimer sections")
    sub = p.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="scan a single file")
    p_scan.add_argument("path")
    p_scan.add_argument("--min-word-count", type=int, default=400)
    p_scan.set_defaults(func=_cmd_scan)

    p_dir = sub.add_parser("scan-dir", help="scan every matching file in a directory tree")
    p_dir.add_argument("directory")
    p_dir.add_argument("--pattern", default="*.md")
    p_dir.add_argument("--min-word-count", type=int, default=400)
    p_dir.add_argument("--only-gaps", action="store_true", help="omit clean files from the output")
    p_dir.set_defaults(func=_cmd_scan_dir)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
