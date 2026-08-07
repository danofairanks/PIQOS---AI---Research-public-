"""Scaffolding generator and structural linter for this repository's
`case_studies/` house format.

Quick start::

    from case_scaffold import CaseStudySpec, FrameworkRef, render_skeleton, lint_text

    spec = CaseStudySpec(
        date="2026-08-08", slug="example_specimen", title="An Example Specimen",
        framework_refs=[FrameworkRef("../papers/published/basin_attractors_v1.md", "§2.4", "Attractor 4")],
    )
    skeleton = render_skeleton(spec)
    print(lint_text(skeleton).warnings)  # unresolved TODOs -- expected on a fresh scaffold

Or from the command line::

    case-scaffold new --date 2026-08-08 --slug example_specimen --title "An Example Specimen" \\
        --framework "../papers/published/basin_attractors_v1.md:§2.4:Attractor 4"
    case-scaffold check case_studies/2026-08-08_example_specimen.md
    case-scaffold index-update --case-study case_studies/2026-08-08_example_specimen.md \\
        --date 2026-08-08 --framework-applied "Attractor 4" --summary "..."
"""

from .index import IndexRow, insert_row, parse_index_rows, render_index_row
from .lint import LintResult, lint_file, lint_text
from .template import (
    TODO_MARK, CaseStudySpec, FrameworkRef, default_filename, render_skeleton,
)

__all__ = [
    "IndexRow", "insert_row", "parse_index_rows", "render_index_row",
    "LintResult", "lint_file", "lint_text",
    "TODO_MARK", "CaseStudySpec", "FrameworkRef", "default_filename", "render_skeleton",
]

__version__ = "0.1.0"
