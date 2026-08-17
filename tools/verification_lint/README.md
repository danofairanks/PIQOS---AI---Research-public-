# verification-lint

A content-level evidentiary-gap scanner: flags direct quotes with no
nearby attribution, high-precision numbers with no nearby citation, and
documents missing a "what this does not claim" scoping section. This is
the "no exemption by source" discipline this project applies by hand to
every case study, encoded as a heuristic you can run — a lead generator
for a human or agent review pass, not a verdict.

## Install

```bash
cd tools/verification_lint
pip install -e .
pip install -e ".[dev]"   # adds pytest
```

Zero runtime dependencies. Requires Python >= 3.10.

## 30-second demo, against real specimens already in this repo

```bash
python3 examples/lint_demo.py
```

Scans a deliberately noisy synthetic draft, then a cleaned-up version of
the same draft with the quote attributed and the numbers sourced, and
(if run from a full repo checkout) this project's own real
`case_studies/` files — printing each file's gap count next to its
severe-gap count so the two numbers are never confused.

## What this tool does

Three independent checks, each a proximity heuristic over plain text:

- **`quotes.py`** — flags a quoted span of 40+ characters with no
  attribution signal (named-speaker verb, platform name, `@handle`,
  markdown link, year, proper name, `§` section reference, `Phase N`,
  an acronym, or a parenthetical containing a digit) within 250
  characters on either side. Below 40 characters, a quote reads as a
  scare-quoted term ("neurosymbolic AI") rather than a claim — those
  are not flagged. A quote's exact text is only ever flagged once per
  document: once attributed anywhere, a later unattributed repetition
  of the same phrase is not re-flagged.
- **`statistics.py`** — flags four shapes of high-precision number with
  no citation signal (`per`, `according to`, `source:`, `cited in`,
  `published`, a markdown link, an `(Author, 2026)`-style parenthetical,
  or a `[^n]` footnote marker) within 150 characters: a decimal
  percentage (`94.37%`), a dollar amount (`$5`, `$2.8B`, `$3.9T`), a
  large comma-grouped count (`17,600`), or a fraction (`3/47`). A round
  integer ("about 20 sources") is not flagged — only the shapes above,
  which is where unearned precision tends to hide.
- **`disclaimer.py`** — a document-level (not per-claim) check for
  whether the text ever scopes its own claims, matching either of this
  repo's two real headings: "What This Case Study Does Not Claim" and
  "What this tracker does NOT yet establish." Only applies to documents
  at or above `min_word_count` (default 400) — short notes don't need a
  formal scoping section.

A fourth module, **`sourcing.py`**, exists to correct a real
miscalibration the first two checks produced — see below.

## Why `severe_gap_count`, not just `gap_count`

The first draft of this tool, run against this repo's own 14
`case_studies/` files, reported **214 total gaps** — including false
positives on files that are, by hand-review, well sourced. The root
cause: this project's real citation convention is a single italic
closing line naming every source inspected —

> *Sources: the original X post, the company's own blog announcement.*

— not inline per-claim citation next to every number and quote. A
proximity-only detector cannot see a source that isn't proximate, so it
read every well-sourced document as riddled with gaps.

`sourcing.py` names that convention explicitly (`Sources:` lines,
`Source:` lines, and "applies the framework from" citations), and
`VerificationLintResult.severe_gap_count` uses it: when a document has
end-of-document sourcing, its per-item quote/statistic gaps are real
leads (verify against the sources list) but not severe. Only a missing
disclaimer section stays severe in that case. `gap_count` (the raw
heuristic total) is still reported — useful as a checklist — but
`severe_gap_count` is what `.ok` and the CLI's exit code are based on.

After this fix, the same 14 files: **67 total gaps, 5 files with a
severe gap** — `2026-07-27_ssi_nvidia_partnership.md`,
`2026-07-28_grok_x_instant_sycophancy.md`,
`2026-07-28_minimal_input_elaboration_drift.md`,
`2026-07-28_nfl_misapplication_grok_x.md`, and `case_studies/README.md`
(an index page, correctly flagged — it has neither a disclaimer nor
end-sourcing, because it isn't a specimen analysis). The first four are
not a bug either: they independently corroborate what
[`case_scaffold`](../case_scaffold/)'s separately-derived
`PRE_CONVENTION_FILES` list found by checking document *structure* —
the house format (title prefix, Does-Not-Claim section) stabilized
2026-08-04, and these four predate it. Two tools, built independently,
tuned against different signals, converged on the same historical fact
about the same four files. The Marcus case study scans at 0 gaps; the
OpenAI/Hugging Face breach case study scans at 1 gap, 0 severe.

## A real bug this tool's own tuning surfaced

The `dollar_amount` pattern originally ended in a bare `\b`
word-boundary assertion. Testing it against this repo's own real
numbers ("$3.9T", the SSI valuation figure) found it silently
truncated the match to `"$3"`. The cause: both the digit before `T` and
`T` itself are `\w` characters, so `\b` cannot sit between them — the
regex engine backtracked off the entire decimal-and-suffix portion
looking for *some* boundary to satisfy the assertion, and found one
right after the first digit. Fixed by replacing the trailing `\b` with
a lookahead, `(?=[\s,.:;!?)]|$)`, which asserts what comes *after* the
match without requiring a word/non-word transition at that exact point.
Pinned as `test_dollar_amount_with_trillion_suffix_regression` in
`tests/test_statistics.py`.

## What this tool does NOT do

- **It does not fact-check anything.** A perfectly cited quote can
  still misrepresent its source; a well-formatted disclaimer can still
  be dishonest. This tool checks for the *presence of a citation
  signal near a claim*, never whether the citation is accurate, or
  whether the claim itself is true. That verification step is BIFP's
  job, or a human's.
- **It does not understand sentences.** Every check here is a regex and
  a character-distance window, not a parse. `"according to nobody in
  particular"` will satisfy the `according to` citation signal exactly
  as if a real source followed it — a documented, deliberate tradeoff
  (fewer false positives on real prose) rather than an oversight; see
  `test_large_comma_count_with_no_citation_is_flagged`'s docstring in
  `tests/test_statistics.py` for the concrete case that surfaced it.
- **It does not know your project's citation convention unless you
  tell it.** `sourcing.py` currently recognizes exactly two shapes:
  a `Sources:`/`Source:` line and an "applies the framework from"
  citation — the two this repo actually uses. A different project's
  convention (inline footnotes only, a bibliography file, DOI links)
  would need its own signal added to `sourcing.py` or it will read as
  unsourced.
- **"reads" counts as an attribution verb** ("the document reads:
  ..."), even with no named speaker — a deliberately loose signal,
  tuned against this repo's real files, that trades a few missed real
  gaps for far fewer false positives on prose that merely quotes
  something in full. See `test_quote_attributed_by_verb_reads_not_flagged`
  in `tests/test_quotes.py`.
- **The 40-character quote floor and 400-word disclaimer floor are
  judgment calls**, not values taken from any project document. Tune
  `find_unattributed_quotes(text, window=...)` and
  `check_disclaimer(text, min_word_count=...)` per corpus if your
  documents run shorter or longer than this repo's case studies.

## Usage

```python
from verification_lint import scan_document, scan_file

result = scan_document('The report found "definitely true, no exceptions" and moved on.')
print(result.gap_count, result.severe_gap_count, result.ok)

result = scan_file("case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md")
```

```bash
verification-lint scan case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md
verification-lint scan-dir case_studies/ --only-gaps
```

`scan-dir` exits 0 only if every scanned file has zero severe gaps —
suitable as a CI gate without failing the build on well-sourced files
that merely use blanket end-sourcing.

## Development

```bash
python3 -m pytest tests/ -v
```

50 tests. Every quote/statistic/disclaimer/sourcing check is validated
both against constructed examples and against this repo's own real
`case_studies/` files (`tests/test_scan.py`), pinning the exact
gap/severe-gap counts reported above so a future change to the
heuristics has to consciously re-justify any shift in those numbers.
`tests/test_agent_tools.py` covers the `agent_tools.py` surface below.

## Agent tool-calling surface

`agent_tools.py` exposes `verification_lint_scan_text(text, *,
min_word_count=400) -> dict`, the same JSON-in/JSON-out contract as
`basin_depth`, `bifp`, `attractor_scan`, `debasinizer`, and
`paper_rigor`'s own `agent_tools.py` modules. Not wired into
`tools/research_mcp/` — that server's own README scopes this package
as a repository-maintenance tool (linting this repo's own
`case_studies/` house format) rather than an agent-callable research
tool, a distinction specific to research_mcp's own scope question. It
is used directly by the in-browser paper-rigor scanner at
[`docs/scan.html`](../../docs/scan.html), where unattributed-quote and
uncited-statistic detection is directly relevant to an arbitrary
uploaded paper regardless of source repository.

## License

MIT.
