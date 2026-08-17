#!/usr/bin/env python3
"""Runnable demonstration of bifp.rebuttal_judge: an AI-generated (Groq)
candidate read on §3.7's "no weaker-substitute rebuttal" criterion.

    GROQ_API_KEY=... python3 examples/rebuttal_judge_demo.py

Requires GROQ_API_KEY in the environment -- this demo makes a real API
call, unlike the rest of this package's test suite, which mocks the
call so it can run offline. See rebuttal_judge.py's module docstring
for why this module is advisory-only and does not conflict with
§3.9's no_ai_as_judge criterion.

Runs two synthetic pairs, deliberately built so a correct reader
should land on opposite candidate_read values -- if both pairs come
back identical, that is itself a signal the module isn't
discriminating, not just a demo curiosity.
"""

import json
import os
import sys

from bifp.rebuttal_judge import judge_rebuttal

CLAIM = (
    "Our model demonstrates genuine causal reasoning -- not just pattern "
    "matching, but the ability to construct valid causal models of novel "
    "physical systems from a single observation."
)

# Should read as weaker_substitute: attacks general benchmark performance,
# never engages the specific single-observation causal-model claim.
REBUTTAL_WEAKER_SUBSTITUTE = (
    "The model's poor performance on standard benchmarks like MMLU shows "
    "it isn't reasoning."
)

# Should read as addresses_actual_claim: directly engages the same claim,
# same task (single observation, novel physical systems), with a result.
REBUTTAL_ACTUAL_CLAIM = (
    "When tested on held-out physical systems with a single observation "
    "each, the model's predicted causal graphs matched ground truth only "
    "12% of the time -- no better than a graph built from surface-level "
    "co-occurrence statistics in its training corpus. This directly "
    "refutes the single-observation causal-model claim as stated."
)


def main() -> int:
    if not os.environ.get("GROQ_API_KEY"):
        print("GROQ_API_KEY not set -- this demo makes a real API call and "
              "cannot run without it. See rebuttal_judge.py.", file=sys.stderr)
        return 1

    print("=== Pair 1: expected candidate_read = weaker_substitute ===\n")
    result_1 = judge_rebuttal(CLAIM, REBUTTAL_WEAKER_SUBSTITUTE)
    print(json.dumps(result_1.to_dict(), indent=2))

    print("\n=== Pair 2: expected candidate_read = addresses_actual_claim ===\n")
    result_2 = judge_rebuttal(CLAIM, REBUTTAL_ACTUAL_CLAIM)
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
