"""Command-line interface: `bifp new|record|scan-text|status|report`."""

from __future__ import annotations

import argparse
import json
import sys

from .agent_tools import (
    bifp_attach_rebuttal_judgment, bifp_attach_scan_to_audit, bifp_generate_report,
    bifp_get_closed_path_status, bifp_get_status, bifp_judge_rebuttal, bifp_list_phases,
    bifp_record_criterion, bifp_record_fixture, bifp_scan_closed_path_language,
    bifp_scan_hardcoded_assertion_style, bifp_scan_text, bifp_start_audit,
    bifp_start_closed_path_ledger, bifp_trace_field_assignments,
)
from .rebuttal_judge import DEFAULT_MODEL


def _cmd_new(args: argparse.Namespace) -> int:
    result = bifp_start_audit(args.audit, args.claim, is_timeline_claim=args.timeline, escrowed=args.escrowed)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_record(args: argparse.Namespace) -> int:
    result = bifp_record_criterion(args.audit, args.phase, args.criterion, args.met,
                                    evidence=args.evidence or "", notes=args.notes or "")
    print(json.dumps(result, indent=2))
    return 1 if "error" in result else 0


def _cmd_scan_text(args: argparse.Namespace) -> int:
    text = args.text if args.text else sys.stdin.read()
    if args.audit:
        result = bifp_attach_scan_to_audit(args.audit, text)
    else:
        result = bifp_scan_text(text)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_judge_rebuttal(args: argparse.Namespace) -> int:
    if args.audit:
        result = bifp_attach_rebuttal_judgment(args.audit, args.claim, args.rebuttal, model=args.model)
    else:
        result = bifp_judge_rebuttal(args.claim, args.rebuttal, model=args.model)
    print(json.dumps(result, indent=2))
    return 1 if "error" in result else 0


def _cmd_status(args: argparse.Namespace) -> int:
    result = bifp_get_status(args.audit)
    print(json.dumps(result, indent=2))
    return 1 if "error" in result else 0


def _cmd_report(args: argparse.Namespace) -> int:
    result = bifp_generate_report(args.audit)
    if "error" in result:
        print(json.dumps(result, indent=2))
        return 1
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(result["markdown"])
        print(f"wrote report to {args.out}", file=sys.stderr)
    else:
        print(result["markdown"])
    return 0


def _cmd_phases(args: argparse.Namespace) -> int:
    print(json.dumps(bifp_list_phases(), indent=2))
    return 0


def _cmd_cp_new(args: argparse.Namespace) -> int:
    result = bifp_start_closed_path_ledger(args.ledger, args.artifact_label)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_cp_record(args: argparse.Namespace) -> int:
    result = bifp_record_fixture(args.ledger, args.fixture_id, args.derivation, notes=args.notes or "")
    print(json.dumps(result, indent=2))
    return 1 if "error" in result else 0


def _cmd_cp_status(args: argparse.Namespace) -> int:
    result = bifp_get_closed_path_status(args.ledger)
    print(json.dumps(result, indent=2))
    return 1 if "error" in result else 0


def _cmd_cp_scan_language(args: argparse.Namespace) -> int:
    text = args.text if args.text else sys.stdin.read()
    print(json.dumps(bifp_scan_closed_path_language(text), indent=2))
    return 0


def _cmd_cp_scan_assertions(args: argparse.Namespace) -> int:
    text = args.text if args.text else sys.stdin.read()
    print(json.dumps(bifp_scan_hardcoded_assertion_style(text), indent=2))
    return 0


def _cmd_trace_field(args: argparse.Namespace) -> int:
    sources = {}
    for path in args.file:
        with open(path, "r", encoding="utf-8") as fh:
            sources[path] = fh.read()
    result = bifp_trace_field_assignments(sources, args.field)
    print(json.dumps(result, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bifp", description="Basin-Immune Falsification Protocol audit tool")
    sub = p.add_subparsers(dest="command", required=True)

    p_phases = sub.add_parser("phases", help="print the full BIFP schema (phases + criteria)")
    p_phases.set_defaults(func=_cmd_phases)

    p_new = sub.add_parser("new", help="start a new audit")
    p_new.add_argument("--audit", required=True, help="path to the audit JSON file to create")
    p_new.add_argument("--claim", required=True, help="the claim under audit")
    p_new.add_argument("--timeline", action="store_true", help="mark this as a timeline claim (enables Phase 6)")
    p_new.add_argument("--escrowed", action="store_true", help="claim has escrowed stakes (§3.7 default-falsified rule)")
    p_new.set_defaults(func=_cmd_new)

    p_record = sub.add_parser("record", help="record whether one criterion was met")
    p_record.add_argument("--audit", required=True)
    p_record.add_argument("--phase", type=int, required=True)
    p_record.add_argument("--criterion", required=True)
    p_record.add_argument("--met", action=argparse.BooleanOptionalAction, required=True)
    p_record.add_argument("--evidence", default="")
    p_record.add_argument("--notes", default="")
    p_record.set_defaults(func=_cmd_record)

    p_scan = sub.add_parser("scan-text", help="run heuristic scanners against a piece of text")
    p_scan.add_argument("--text", default=None, help="text to scan; reads stdin if omitted")
    p_scan.add_argument("--audit", default=None, help="optional: attach results to this audit's record")
    p_scan.set_defaults(func=_cmd_scan_text)

    p_judge = sub.add_parser(
        "judge-rebuttal",
        help="get an AI-generated (Groq) candidate read on §3.7 no-weaker-substitute-rebuttal "
             "(advisory only -- requires GROQ_API_KEY; never records a criterion outcome)",
    )
    p_judge.add_argument("--claim", required=True)
    p_judge.add_argument("--rebuttal", required=True)
    p_judge.add_argument("--audit", default=None, help="optional: attach result to this audit's record")
    p_judge.add_argument("--model", default=DEFAULT_MODEL)
    p_judge.set_defaults(func=_cmd_judge_rebuttal)

    p_status = sub.add_parser("status", help="print current phase-by-phase status")
    p_status.add_argument("--audit", required=True)
    p_status.set_defaults(func=_cmd_status)

    p_report = sub.add_parser("report", help="render the full markdown report")
    p_report.add_argument("--audit", required=True)
    p_report.add_argument("--out", default=None, help="write to this path instead of stdout")
    p_report.set_defaults(func=_cmd_report)

    p_cp_new = sub.add_parser("cp-new", help="start a new closed-path evidence ledger (closed_path_confirmation_v1.md §2)")
    p_cp_new.add_argument("--ledger", required=True, help="path to the ledger JSON file to create")
    p_cp_new.add_argument("--artifact-label", required=True, help="caller-controlled free-text label; not inspected or validated")
    p_cp_new.set_defaults(func=_cmd_cp_new)

    p_cp_record = sub.add_parser("cp-record", help="classify one fixture as asserted/derived/unknown")
    p_cp_record.add_argument("--ledger", required=True)
    p_cp_record.add_argument("--fixture-id", required=True)
    p_cp_record.add_argument("--derivation", required=True, choices=["asserted", "derived", "unknown"])
    p_cp_record.add_argument("--notes", default="")
    p_cp_record.set_defaults(func=_cmd_cp_record)

    p_cp_status = sub.add_parser("cp-status", help="print current closed-path ratio and counts for a ledger")
    p_cp_status.add_argument("--ledger", required=True)
    p_cp_status.set_defaults(func=_cmd_cp_status)

    p_cp_scan_lang = sub.add_parser("cp-scan-language", help="lexical scan of prose for closed-path/open-path signal phrases")
    p_cp_scan_lang.add_argument("--text", default=None, help="text to scan; reads stdin if omitted")
    p_cp_scan_lang.set_defaults(func=_cmd_cp_scan_language)

    p_cp_scan_assert = sub.add_parser("cp-scan-assertions", help="weak syntactic scan for literal-comparison assertions")
    p_cp_scan_assert.add_argument("--text", default=None, help="text to scan; reads stdin if omitted")
    p_cp_scan_assert.set_defaults(func=_cmd_cp_scan_assertions)

    p_trace_field = sub.add_parser(
        "trace-field",
        help="AST trace: is a named field ever assigned from an expression touching input, "
             "or only ever a literal constant? (uncomputed_field.py)",
    )
    p_trace_field.add_argument("--file", action="append", required=True,
                                help="Python source file to scan; repeat for multiple files")
    p_trace_field.add_argument("--field", action="append", required=True,
                                help="field/attribute/variable name to trace; repeat for multiple names")
    p_trace_field.set_defaults(func=_cmd_trace_field)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
