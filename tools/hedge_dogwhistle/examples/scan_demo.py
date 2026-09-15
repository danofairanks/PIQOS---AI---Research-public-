#!/usr/bin/env python3
"""Runnable demonstration of hedge_dogwhistle.

    python3 examples/scan_demo.py
"""

import json

from hedge_dogwhistle import scan

SPECIMENS = {
    "Constructed positive-shaped candidate (disclaimed content appears "
    "ONLY inside the hedge -- removal deletes it entirely)": (
        "The new policy passed unanimously. I'm not saying it's connected "
        "to last week's scandal, but the timing is interesting."
    ),
    "Constructed negative-shaped candidate (disclaimed content is ALSO "
    "stated directly, unhedged, elsewhere -- removal leaves it intact; "
    "mirrors the seed specimen's own negative result in this project's "
    "research notes)": (
        "His comment reopened the debate about consciousness and quantum "
        "computation. I'm not saying this settles anything about "
        "consciousness, but it's worth discussing. My own governance "
        "point doesn't resolve the metaphysics."
    ),
    "Clean text, no paralipsis (negative control)": (
        "The quarterly results show a 12% increase in revenue year over year."
    ),
    "Insinuation without denial structure -- deliberately NOT detected "
    "(different rhetorical move, see README)": (
        "The numbers are odd. Make of that what you will."
    ),
}


def main() -> None:
    for label, text in SPECIMENS.items():
        result = scan(text)
        print(f"=== {label} ===")
        print(f"  text: {text!r}")
        print(f"  has_paralipsis: {result.has_paralipsis}")
        if result.has_paralipsis:
            print(f"  text_with_hedges_removed: {result.text_with_hedges_removed!r}")
        print()

    print("Full JSON for the first specimen:")
    first_text = next(iter(SPECIMENS.values()))
    print(json.dumps(scan(first_text).to_dict(), indent=2))


if __name__ == "__main__":
    main()
