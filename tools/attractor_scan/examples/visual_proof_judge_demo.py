#!/usr/bin/env python3
"""Runnable demonstration of attractor_scan.visual_proof_judge: an
AI-generated (Groq vision) candidate read on Case 6 ("technical
precision borrowed as visual proof" -- basin_attractors_v1.md §2.8).

    GROQ_API_KEY=... python3 examples/visual_proof_judge_demo.py

Requires GROQ_API_KEY and the two images this generates via
`generate_visual_proof_demo_images.py` (already committed under
`visual_proof_demo_images/`; re-run that script to regenerate them).
Makes real API calls, unlike the rest of this package's test suite,
which mocks the call so it can run offline.

Runs two synthetic pairs, deliberately built so a correct reader
should land on opposite candidate_read values -- if both come back
identical, that's a discrimination-failure signal, not just a demo
curiosity. Neither image is a real specimen; see the generator
script's docstring for why (Case 6's actual cited example is a real,
copyrighted X post this project doesn't vendor).

Waits between the two calls -- confirmed live 2026-08-17 that a single
vision call on this account's on_demand tier (8000 TPM) can use nearly
the entire budget by itself (one clean call used 7996/8000), so a
second call in the same 60-second window gets HTTP 429 even though its
own request is well under the limit on its own. This is a demo-pacing
fact about two back-to-back calls, not a bug in judge_visual_proof --
a single real-world call for one specimen doesn't hit this.
"""

import json
import os
import sys
import time
from pathlib import Path

from attractor_scan.visual_proof_judge import judge_visual_proof

IMAGES_DIR = Path(__file__).parent / "visual_proof_demo_images"

# Should read as genuine_technical_support: the chart's own numbers
# directly support the claim.
GENUINE_CLAIM = "Model X achieves the highest accuracy on the benchmark, outperforming both baselines B and C as shown."
GENUINE_IMAGE = IMAGES_DIR / "genuine_benchmark_chart.png"

# Should read as unrelated_borrowed_precision: the image is a real,
# accurately-drawn mathematical singularity (a pole at x=0), but has
# nothing to do with the claim beyond the shared word "singularity".
PUN_CLAIM = "This proves AI is approaching a societal singularity -- an irreversible, transformative event horizon for civilization."
PUN_IMAGE = IMAGES_DIR / "singularity_pun_graphic.png"

# Confirmed live 2026-08-17: a single clean call used 7996/8000 of this
# account's on_demand-tier TPM budget by itself; a second call inside
# the same 60s window gets HTTP 429 even at a well-under-limit request
# size. The API's own 429 body reported "try again in 51.3825s".
_SECONDS_BETWEEN_CALLS = 65


def main() -> int:
    if not os.environ.get("GROQ_API_KEY"):
        print("GROQ_API_KEY not set -- this demo makes real API calls and "
              "cannot run without it. See visual_proof_judge.py.", file=sys.stderr)
        return 1
    for path in (GENUINE_IMAGE, PUN_IMAGE):
        if not path.exists():
            print(f"missing demo image {path} -- run generate_visual_proof_demo_images.py first",
                  file=sys.stderr)
            return 1

    print("=== Pair 1: expected candidate_read = genuine_technical_support ===\n")
    result_1 = judge_visual_proof(GENUINE_CLAIM, image_path=str(GENUINE_IMAGE))
    print(json.dumps(result_1.to_dict(), indent=2))

    print(f"\n(waiting {_SECONDS_BETWEEN_CALLS}s -- this account's on_demand tier TPM "
          f"budget doesn't cover two vision calls back-to-back, see module docstring)",
          file=sys.stderr)
    time.sleep(_SECONDS_BETWEEN_CALLS)

    print("\n=== Pair 2: expected candidate_read = unrelated_borrowed_precision ===\n")
    result_2 = judge_visual_proof(PUN_CLAIM, image_path=str(PUN_IMAGE))
    print(json.dumps(result_2.to_dict(), indent=2))

    print("\n=== Discrimination check ===\n")
    if result_1.candidate_read != result_2.candidate_read:
        print(f"  PASS: pairs read differently ({result_1.candidate_read!r} vs "
              f"{result_2.candidate_read!r})")
        return 0
    print(f"  FLAG: both pairs read as {result_1.candidate_read!r} -- "
          f"the model is not discriminating between these two cases.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
