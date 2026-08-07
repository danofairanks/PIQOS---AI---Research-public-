"""Command-line interface: `case-scaffold new|check|index-update`."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .index import insert_row, render_index_row
from .lint import lint_file
from .template import CaseStudySpec, FrameworkRef, default_filename, render_skeleton


def _parse_framework_arg(raw: str) -> FrameworkRef:
    """--framework "path.md:§2.4:Attractor 4 label" (label optional)."""
    parts = raw.split(":", 2)
    path = parts[0]
    section = parts[1] if len(parts) > 1 else ""
    label = parts[2] if len(parts) > 2 else ""
    return FrameworkRef(paper_path=path, section=section, label=label)


def _cmd_new(args: argparse.Namespace) -> int:
    spec = CaseStudySpec(
        date=args.date, slug=args.slug, title=args.title, subtitle=args.subtitle or "",
        framework_refs=[_parse_framework_arg(f) for f in (args.framework or [])],
        sources_note=args.sources or "",
        section_titles=args.section or None,
    )
    text = render_skeleton(spec)
    out_path = args.out or (Path("case_studies") / default_filename(spec))
    Path(out_path).write_text(text, encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)
    print(str(out_path))
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    result = lint_file(args.path, strict=args.strict, base_dir=args.base_dir)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


def _cmd_index_update(args: argparse.Namespace) -> int:
    readme_path = Path(args.readme)
    readme_text = readme_path.read_text(encoding="utf-8")
    filename = Path(args.case_study).name
    row = render_index_row(args.date, filename, args.framework_applied, args.summary)
    updated = insert_row(readme_text, row, args.date)
    readme_path.write_text(updated, encoding="utf-8")
    print(f"inserted row into {readme_path}", file=sys.stderr)
    print(row)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="case-scaffold",
                                 description="Scaffold and lint case_studies/ house-format files")
    sub = p.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="generate a new case-study skeleton")
    p_new.add_argument("--date", required=True, help="YYYY-MM-DD")
    p_new.add_argument("--slug", required=True, help="lowercase_underscore_slug")
    p_new.add_argument("--title", required=True)
    p_new.add_argument("--subtitle", default=None)
    p_new.add_argument("--framework", action="append",
                        help='repeatable: "path.md:§2.4:Attractor 4 label"')
    p_new.add_argument("--sources", default=None)
    p_new.add_argument("--section", action="append", help="repeatable: custom body section title")
    p_new.add_argument("--out", default=None, help="output path; defaults to case_studies/<date>_<slug>.md")
    p_new.set_defaults(func=_cmd_new)

    p_check = sub.add_parser("check", help="lint an existing case-study file")
    p_check.add_argument("path")
    p_check.add_argument("--strict", action="store_true", help="treat unresolved TODOs as errors")
    p_check.add_argument("--base-dir", default=None, help="base dir for resolving framework links (default: file's own dir)")
    p_check.set_defaults(func=_cmd_check)

    p_index = sub.add_parser("index-update", help="insert a row into case_studies/README.md's index table")
    p_index.add_argument("--readme", default="case_studies/README.md")
    p_index.add_argument("--case-study", required=True, help="path to the case-study file (only the filename is used)")
    p_index.add_argument("--date", required=True)
    p_index.add_argument("--framework-applied", required=True)
    p_index.add_argument("--summary", required=True)
    p_index.set_defaults(func=_cmd_index_update)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
