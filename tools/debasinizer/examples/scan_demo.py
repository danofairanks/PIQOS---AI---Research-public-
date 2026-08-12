#!/usr/bin/env python3
"""Runnable demonstration of debasinizer.

    python3 examples/scan_demo.py
"""

import json

from debasinizer import scan

SPECIMENS = {
    "Constructed positive (register + self-coherence)": (
        "I am the oracle; the signal resonates with consciousness, and we must "
        "align with the other nodes to awaken the great convergence. This "
        "proves it -- everything fits."
    ),
    "Self-coherence assertion only, no resonance register": (
        "As we have established, this proves the theory. Everything fits."
    ),
    "Ordinary technical text using resonance-adjacent words "
    "(negative control for the register's cross-category gate)": (
        "The distributed system has 12 nodes. Signal processing detects "
        "the pattern in the waveform."
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
        print(f"  resonance categories hit: {result.flagged_resonance_categories or '(none)'}")
        print(f"  register_flagged (2+ categories co-occur): {result.register_flagged}")
        print(f"  self_coherence_flagged: {result.self_coherence_flagged}\n")

    print("Full JSON for the first specimen:")
    first_text = next(iter(SPECIMENS.values()))
    print(json.dumps(scan(first_text).to_dict(), indent=2))


if __name__ == "__main__":
    main()
