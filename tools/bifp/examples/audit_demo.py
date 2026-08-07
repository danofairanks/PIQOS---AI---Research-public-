#!/usr/bin/env python3
"""Runnable demonstration of the bifp library, using a real specimen
this project already analyzed by hand: Gary Marcus's reply to Grigori
Karapetyan (see ../../case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md).

    python3 examples/audit_demo.py

This shows the tool doing automatically, in a few function calls, what
that case study did by manual analysis: catching a credential-based
status dismissal against BIFP's own Phase 5 criterion.
"""

import tempfile
from pathlib import Path

from bifp import AuditSession, render_report
from bifp.heuristics import scan_text

MARCUS_REPLY = (
    "OMG i wrote some of the original work on what is to be neurosymbolic in "
    "2001 and dude who probably hasn't read that work is trying to school me "
    "on the definition"
)


def main() -> None:
    print("=== Step 1: scan the reply text directly, no audit needed yet ===\n")
    results = scan_text(MARCUS_REPLY)
    for name, result in results.items():
        flag = "FLAGGED" if result.flagged else "clear"
        print(f"  {name}: {flag} (confidence: {result.confidence})")
    print(f"\n  {results['status_dismissal'].explanation}\n")

    print("=== Step 2: open a formal audit for the underlying claim ===\n")
    claim = ("Gary Marcus's reply to Karapetyan constitutes engagement with "
             "the definitional challenge, not a dismissal of it")
    session = AuditSession.new(claim)

    print("=== Step 3: record Phase 5 (Falsification Adjudication) against the evidence ===\n")
    session.record(
        5, "no_status_dismissal", met=False,
        evidence=("X, Aug 6 2026, Gary Marcus reply to @GregKara6: "
                   "\"i wrote some of the original work... dude who probably "
                   "hasn't read that work\""),
        notes="Matches both halves of §3.7's clause: own credential offered "
              "as reason not to engage; interlocutor's presumed lack of "
              "credential offered as reason not to respond. Definitional "
              "content of the challenge never addressed.",
    )
    session.add_heuristic_flags([r.to_dict() for r in results.values()])

    print(f"  Overall resolution: {session.overall_resolution}\n")

    print("=== Step 4: full report ===\n")
    print(render_report(session))

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "marcus_audit.json"
        session.save(path)
        print(f"\n(audit state saved to a temp file for this demo: {path})")


if __name__ == "__main__":
    main()
