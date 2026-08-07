#!/usr/bin/env python3
"""Runnable demonstration of paper_rigor: scan a deliberately bad
constructed paragraph, then this repo's own real
papers/published/basin_attractors_v1.md, showing the
structural_gap_count vs. external_verification_worklist split.

    python3 examples/rigor_demo.py
"""

from pathlib import Path

from paper_rigor import scan_file, scan_paper

BAD_PARAGRAPH = (
    "As a renowned expert with over 30 years of experience, I can tell you this "
    "approach conclusively demonstrates artificial general intelligence, beyond "
    "any doubt. It is well known that no one disputes this. It is trivial to show "
    "the derivation; TODO: fill in proof. Research shows the model outperforms "
    "all baselines."
) + (" filler word" * 400)  # push over the 400-word limitations-section threshold


def _print_result(label: str, result) -> None:
    print(f"--- {label} ---")
    print(f"  ok:                    {result.ok}")
    print(f"  structural_gap_count:  {result.structural_gap_count}  (fixable by rereading the paper's own text)")
    print(f"  total_gap_count:       {result.total_gap_count}")
    if result.placeholder_gaps:
        print(f"  placeholder gaps:      {[(g.kind, g.phrase) for g in result.placeholder_gaps]}")
    if result.falsifiability and result.falsifiability.gap:
        print(f"  falsifiability gap:    certainty language with no stated test condition")
    if result.limitations and result.limitations.gap:
        print(f"  limitations gap:       no 'does not claim' phrase or Limitations heading found")
    if result.citability_claim and result.citability_claim.gap:
        print(f"  citability claim gap:  claims '{result.citability_claim.matched_phrases}' but 0 references parsed")
    if result.external_verification_worklist:
        print(f"  external_verification_worklist ({len(result.external_verification_worklist)} items -- needs a real web search/fetch to resolve):")
        for item in result.external_verification_worklist:
            print(f"    - [{item['kind']}] {item['item'][:70]}")
    print()


def main() -> None:
    print("=== Step 1: a deliberately bad constructed paragraph ===\n")
    _print_result("bad paragraph", scan_paper(BAD_PARAGRAPH, byline_authors=["Smith"]))

    repo_root = Path(__file__).resolve().parents[3]
    real_paper = repo_root / "papers" / "published" / "basin_attractors_v1.md"
    if real_paper.is_file():
        print("=== Step 2: this repo's own real basin_attractors_v1.md ===\n")
        result = scan_file(real_paper)
        _print_result("basin_attractors_v1.md", result)
        print(f"  ({result.venue_mix.n_total} references parsed: "
              f"{result.venue_mix.n_formal} formal, {result.venue_mix.n_informal} informal, "
              f"{result.venue_mix.n_unknown} unclassifiable)")
    else:
        print("(not run from a full repo checkout -- skipping the real-paper scan)")

    print("\n=== Step 3: a paper that claims citability but has zero references ===\n")
    print("(constructed here -- the real specimen that motivated this check is a private-repo\n"
          " document; see README 'A real bug this tool's own tuning surfaced, round two')\n")
    citability_bad = (
        "This framework's grounding in documented, citable research is extensive. "
        "The base papers underlying this work establish its rigor beyond question."
    ) + (" filler word" * 400)
    _print_result("citability-without-references", scan_paper(citability_bad))


if __name__ == "__main__":
    main()
