#!/usr/bin/env python3
"""Runnable demonstration of attractor_scan against real specimens
already checked and written up elsewhere in this repository.

    python3 examples/scan_demo.py
"""

import json

from attractor_scan import scan

SPECIMENS = {
    "Marcus reply to Karapetyan (case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md)": (
        "OMG i wrote some of the original work on what is to be neurosymbolic in "
        "2001 and dude who probably hasn't read that work is trying to school me "
        "on the definition"
    ),
    "OpenAI blog framing after the Hugging Face breach "
    "(case_studies/2026-08-07_openai_huggingface_breach_singularity_reframe.md)": (
        "The primary lesson from this incident is that model security and safety "
        "must keep pace with rapidly advancing capabilities."
    ),
    "Musk quote-tweeting Anthropic's disclosure "
    "(basin_attractors_v1.md §2.8 Case 5's own cited example)": (
        "This will happen frequently as AI becomes smarter and more agentic."
    ),
    "Clean scientific text (negative control)": (
        "The classifier scored 87.3% accuracy on a held-out test set with a "
        "fixed random seed. Full code and data are in the supplementary materials."
    ),
}


def main() -> None:
    for label, text in SPECIMENS.items():
        result = scan(text)
        print(f"=== {label} ===")
        print(f"  text: {text!r}")
        print(f"  flagged maneuvers:  {result.flagged_maneuvers or '(none)'}")
        print(f"  flagged laundering: {result.flagged_laundering_cases or '(none)'}")
        print(f"  density: {result.density:.2f}\n")

    print("Full JSON for the first specimen:")
    first_text = next(iter(SPECIMENS.values()))
    print(json.dumps(scan(first_text).to_dict(), indent=2))


if __name__ == "__main__":
    main()
