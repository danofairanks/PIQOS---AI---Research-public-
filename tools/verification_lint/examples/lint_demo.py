#!/usr/bin/env python3
"""Runnable demonstration of verification_lint: scan a deliberately
noisy synthetic document, then a cleaned-up version of the same
document, and show the gap count drop -- including the severe/
non-severe distinction that end-of-document sourcing produces.

    python3 examples/lint_demo.py

If run from a full repo checkout, also scans this project's own real
case_studies/ directory and prints the per-file severe-gap summary.
"""

from pathlib import Path

from verification_lint import scan_document, scan_paths

NOISY_DRAFT = """
# A Draft Specimen Note

The company's own spokesperson said something remarkable in a recent
appearance: "the system produces output that is completely reliable in
every conceivable circumstance and situation without exception whatsoever."
Nobody has checked this since.

Separately, the breach affected 17,600 accounts, or 94.37% of the user
base, at an estimated cost of $2.8B to remediate -- figures that appeared
in a single social media post and nowhere else.
"""

CLEANED_DRAFT = """
# A Draft Specimen Note

Per the company's Q3 investor call transcript (2026), a spokesperson
said: "the system produces output that is completely reliable in every
conceivable circumstance and situation without exception whatsoever."
This claim has not been independently verified.

The breach affected 17,600 accounts (94.37% of the user base), at an
estimated cost of $2.8B to remediate, according to the company's own
public disclosure filing.

## What This Note Does Not Claim

This note does not claim the $2.8B remediation estimate is accurate --
only that it is the figure the company itself disclosed.

*Sources: company Q3 investor call transcript, public disclosure filing.*
""" + (" filler-word" * 400)  # push over the disclaimer applicability threshold


def _print_result(label: str, result) -> None:
    print(f"--- {label} ---")
    print(f"  gap_count:        {result.gap_count}")
    print(f"  severe_gap_count: {result.severe_gap_count}")
    print(f"  ok:               {result.ok}")
    if result.unattributed_quotes:
        print(f"  unattributed quotes: {len(result.unattributed_quotes)}")
    if result.uncited_statistics:
        for s in result.uncited_statistics:
            print(f"    - {s.kind}: {s.value!r}")
    if result.disclaimer:
        print(f"  disclaimer gap:   {result.disclaimer.gap}")
    if result.sourcing:
        print(f"  has end sourcing: {result.sourcing.has_end_sourcing}")
    print()


def main() -> None:
    print("=== Step 1: a noisy first draft ===\n")
    _print_result("noisy draft", scan_document(NOISY_DRAFT))

    print("=== Step 2: the same claims, attributed and sourced ===\n")
    _print_result("cleaned draft", scan_document(CLEANED_DRAFT))

    repo_root = Path(__file__).resolve().parents[3]
    case_studies_dir = repo_root / "case_studies"
    if case_studies_dir.is_dir():
        print("=== Step 3: this repo's own real case_studies/ files ===\n")
        paths = sorted(case_studies_dir.glob("*.md"))
        results = scan_paths(paths)
        for r in sorted(results, key=lambda r: -r.severe_gap_count):
            flag = "SEVERE" if r.severe_gap_count else ("ok" if r.gap_count == 0 else "gaps (non-severe)")
            print(f"  {Path(r.path).name:60s} gap={r.gap_count:3d} severe={r.severe_gap_count:2d}  [{flag}]")
    else:
        print("(not run from a full repo checkout -- skipping the real-file scan)")


if __name__ == "__main__":
    main()
