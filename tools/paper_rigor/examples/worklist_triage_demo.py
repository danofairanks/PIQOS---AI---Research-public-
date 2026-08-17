#!/usr/bin/env python3
"""Runnable demonstration of paper_rigor.worklist_triage: an
AI-generated (Groq) priority + suggested_check for each item in a real
external_verification_worklist.

    GROQ_API_KEY=... python3 examples/worklist_triage_demo.py

Requires GROQ_API_KEY -- this demo makes a real API call, unlike the
rest of this package's test suite, which mocks the call so it can run
offline. Reuses rigor_demo.py's own constructed BAD_PARAGRAPH specimen
(not a new example) since it already produces a real, varied
three-kind worklist (uncited empirical claim, credential substitution,
unsupported consensus claim) -- exactly the mix a triage pass should
be able to differentiate.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from rigor_demo import BAD_PARAGRAPH  # noqa: E402

from paper_rigor import scan_paper
from paper_rigor.worklist_triage import triage_worklist


def main() -> int:
    if not os.environ.get("GROQ_API_KEY"):
        print("GROQ_API_KEY not set -- this demo makes a real API call and "
              "cannot run without it. See worklist_triage.py.", file=sys.stderr)
        return 1

    scan_result = scan_paper(BAD_PARAGRAPH, byline_authors=["Smith"])
    worklist = scan_result.external_verification_worklist
    print(f"=== scan_paper found {len(worklist)} worklist items ===\n")
    for item in worklist:
        print(f"  [{item['kind']}] {item['item'][:70]}")

    print("\n=== Triage (Groq) ===\n")
    # triage_worklist() itself already raises WorklistTriageError on any
    # count/index mismatch (see the offline test suite), so reaching this
    # line at all already confirms nothing was invented or dropped.
    triage = triage_worklist(worklist)
    print(json.dumps(triage.to_dict(), indent=2))

    print("\n=== Differentiation check ===\n")
    checks = {i.suggested_check for i in triage.items}
    priorities = [i.priority for i in triage.items]
    if len(checks) == len(triage.items) and len(set(priorities)) > 1:
        print(f"  PASS: {len(triage.items)} items got distinct suggested_check text and "
              f"more than one priority level ({sorted(set(priorities))}) -- not a "
              f"degenerate identical-output pass")
        return 0
    print(f"  FLAG: suggested_check text or priority levels look degenerate "
          f"(priorities: {priorities})")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
