"""Command-line interface: `bifp new|record|scan-text|status|report`."""

from __future__ import annotations

import argparse
import json
import sys

from .agent_tools import (
    bifp_attach_rebuttal_judgment, bifp_attach_scan_to_audit, bifp_generate_report,
    bifp_get_status, bifp_judge_rebuttal, bifp_list_phases, bifp_record_criterion,
    bifp_scan_text, bifp_start_audit,
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

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
