# case-scaffold

Scaffolding generator and structural linter for this repository's
[`case_studies/`](../../case_studies/) house format. Every real
case study in this repo shares the same structure — title, subtitle,
Executive Summary, one or more body sections, "What This Case Study
Does Not Claim," and a sourced closing line naming the framework
applied. This tool turns that shared structure into something you can
generate and check, instead of having to reverse-engineer it by
reading thirteen files.

## Install

```bash
cd tools/case_scaffold
pip install -e .
pip install -e ".[dev]"
```

Zero runtime dependencies. Requires Python >= 3.10.

## What this tool does NOT do

**It does not write your case study.** `case-scaffold new` produces
structure with visible `**TODO — replace before publishing:**`
markers everywhere real research is required — the specimen quote,
what checking it found, the sources actually inspected. A generated
file is designed to fail `case-scaffold check --strict` until a human
or agent has done that work. Nothing here fabricates plausible-sounding
analysis to fill the gaps; that would defeat the entire discipline this
project's case studies exist to demonstrate.

## Generate a skeleton

```bash
case-scaffold new \
  --date 2026-08-08 \
  --slug demo_specimen \
  --title "A Demo Specimen" \
  --subtitle "One sentence naming the specific mechanism this specimen demonstrates" \
  --framework "../papers/published/basin_attractors_v1.md:§2.5:Attractor 5 label" \
  --sources "X post (verified account), inspected directly." \
  --out case_studies/2026-08-08_demo_specimen.md
```

`--framework` is repeatable (a case study can apply more than one
paper/section, and several real ones do). `--section` is repeatable
too, for custom body-section titles beyond the two-section default.

```bash
python3 examples/scaffold_demo.py
```

walks through generation, linting (structurally valid, but flagged
with pending TODOs), and strict-mode gating end to end.

## Lint an existing (or in-progress) file

```bash
case-scaffold check case_studies/2026-08-08_demo_specimen.md            # structural check only
case-scaffold check case_studies/2026-08-08_demo_specimen.md --strict   # also fail on unresolved TODOs
```

Exit code 0/1, so this composes into CI: run non-strict on every PR to
catch structural drift, or strict right before a file is meant to be final.

## Update the index

```bash
case-scaffold index-update \
  --case-study case_studies/2026-08-08_demo_specimen.md \
  --date 2026-08-08 \
  --framework-applied "Attractor 5" \
  --summary "One-sentence summary for the table."
```

Inserts a row into `case_studies/README.md`'s table in date order —
the same convention that file's own text asks contributors to follow
("Update this index in the same commit that adds a case study"),
done by the tool instead of by hand.

## A real finding this tool's own test suite surfaced

Linting all 13 real files in `case_studies/` (not just the ones this
tool was built to match) shows the house format **stabilized starting
2026-08-04**. The five files from that date forward, plus the two
case studies added this session (2026-08-06, 2026-08-07), all fully
conform: the `# Real-Time Specimen Analysis:` title prefix and the
`## What This Case Study Does Not Claim` section both appear
consistently from 2026-08-04 on and not before. The six files from
2026-07-27 through 2026-08-02 predate that convention — shorter
titles, no Does-Not-Claim section — and fail structural lint for
specific, named reasons pinned directly in `tests/test_lint.py`.

That's not a linter bug to work around. `case-scaffold` targets the
format the project actually converged on and wants new contributions
to match; the older files are real history, not malformed data, and
this tool doesn't try to retroactively rewrite them or pretend the
convention was always there.

## Design notes

- **Structural validity and completeness are checked separately, on
  purpose.** A freshly generated scaffold passes non-strict lint (it
  has the right shape) while failing strict lint (it's full of
  TODOs). `--strict` is the "ready to publish" gate; plain `check` is
  the "is this even in house format" gate. Treat them as two different
  questions, not two severities of the same one.
- **The closing-line citation clause is structurally required even
  before you know which framework section applies.** If you generate
  a skeleton with no `--framework` yet, the closing line still reads
  as a valid citation line (`"Applies the framework from **TODO**..."`)
  rather than omitting the phrase entirely — the TODO marks it
  unresolved without breaking the shape the structural checker looks
  for. This was a real bug in the first draft, caught by this
  package's own test suite before shipping (see `test_template.py`'s
  `test_render_skeleton_passes_structural_lint_but_warns_on_todos`).
- **Framework-link resolution is a warning, not an error**, even in
  strict mode — a case study written against a paper that hasn't been
  committed yet, or checked from a directory that isn't the real repo
  layout, shouldn't hard-fail. Use `--base-dir` to point the checker
  at the real `case_studies/` directory when you want that check to
  mean something.

## Development

```bash
pip install -e ".[dev]"
pytest tests/ -q
```

39 tests, including: the full skeleton-generation/lint round trip,
index-table parsing and date-ordered insertion, and — the strongest
grounding in this package — lint rules validated directly against all
13 real files in `case_studies/`, with the pre-2026-08-04 convention
gap pinned as an explicit, named test rather than silently ignored.

## License

MIT, same as the rest of this repository.
