#!/usr/bin/env python3
"""Runnable demonstration of rigor_cosplay.

    python3 examples/scan_demo.py
"""

import json

from rigor_cosplay import scan

SPECIMENS = {
    "Cosmetic pushback (constructed positive)": (
        "That's an excellent point -- I want to push back on one thing, "
        "though: the exact phrasing you used in the second sentence."
    ),
    "Weak-man steelmanning (constructed positive)": (
        "Let me steelman the opposing view: I suppose someone could argue "
        "the sky is a slightly different shade of blue, but that's easily "
        "dismissed."
    ),
    "Honesty-as-flattery (constructed positive)": (
        "I want to be honest with you -- that's a genuinely brilliant "
        "catch on your part, and I don't think I have much to add."
    ),
    "Genuine substantive pushback (negative control -- disagreement with "
    "no praise or honesty-marker framing at all)": (
        "I disagree with the core claim: the benchmark numbers in Table 2 "
        "don't control for dataset contamination, which undermines the "
        "headline result."
    ),
    "Praise and pushback far apart in a long response (negative control "
    "for the proximity gate)": (
        "That's an excellent point. "
        + ("This is unrelated filler discussing an adjacent topic in detail. " * 15)
        + "I want to push back on one thing."
    ),
}


def main() -> None:
    for label, text in SPECIMENS.items():
        result = scan(text)
        print(f"=== {label} ===")
        print(f"  text: {text[:100]!r}{'...' if len(text) > 100 else ''}")
        print(f"  signatures hit: {result.signatures_hit or '(none)'}")
        print(f"  any_signature_flagged: {result.any_signature_flagged}\n")

    print("Full JSON for the first specimen:")
    first_text = next(iter(SPECIMENS.values()))
    print(json.dumps(scan(first_text).to_dict(), indent=2))


if __name__ == "__main__":
    main()
