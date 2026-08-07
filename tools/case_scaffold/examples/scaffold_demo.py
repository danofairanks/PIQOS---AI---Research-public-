#!/usr/bin/env python3
"""Runnable demonstration of case_scaffold: generate a skeleton, show
it failing strict lint (expected -- it's full of TODOs), fill in the
TODOs the way a contributor would, then show it passing.

    python3 examples/scaffold_demo.py
"""

from case_scaffold import CaseStudySpec, FrameworkRef, lint_text, render_skeleton


def main() -> None:
    spec = CaseStudySpec(
        date="2026-08-08",
        slug="demo_specimen",
        title="A Demo Specimen",
        subtitle="A one-line X post makes an unfalsifiable claim and nobody checks the number",
        framework_refs=[
            FrameworkRef("../papers/published/basin_attractors_v1.md", "§2.5",
                          "Attractor 5 — The Formal-Looking Literature Is Mostly Valid"),
        ],
        sources_note="X post (verified account), inspected directly per the operator's capture.",
    )

    print("=== Step 1: generate the skeleton ===\n")
    skeleton = render_skeleton(spec)
    print(skeleton)

    print("=== Step 2: lint it -- structurally valid, but full of TODOs ===\n")
    result = lint_text(skeleton)
    print(f"  structurally ok: {result.ok}")
    print(f"  warnings: {len(result.warnings)}")
    for w in result.warnings:
        print(f"    - {w}")

    print("\n=== Step 3: strict mode treats those same TODOs as blocking ===\n")
    strict_result = lint_text(skeleton, strict=True)
    print(f"  ready to publish: {strict_result.ok}")

    print("\n=== Step 4: a filled-in version (what a contributor produces) passes strict ===\n")
    filled = skeleton
    filled = filled.replace(
        "**TODO — replace before publishing:** 3-6 sentences. State what was "
        "posted/claimed, what checking it against primary sources actually found, "
        "and the one specific finding that makes this specimen worth logging -- "
        "not a restatement of the topic.",
        "A LinkedIn post claims a benchmark result that, checked directly against "
        "the cited paper, does not appear anywhere in it. The number is real, the "
        "attribution is not.",
    )
    # (a real contributor would fill in every remaining TODO the same way;
    # this demo fills only enough to show the mechanism, not a full worked example)
    remaining = filled.count("TODO — replace before publishing")
    print(f"  (demo leaves {remaining} TODOs unfilled -- see the two real case studies "
          f"this session wrote by hand for full worked examples: "
          f"case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md and "
          f"case_studies/2026-08-07_openai_huggingface_breach_singularity_reframe.md)")


if __name__ == "__main__":
    main()
