# PIQOS AI Research (Public) — Session Context

This file auto-loads at the start of any Claude Code session against this
repository. If you are a fresh session reading this: welcome, here is what
you need to know before doing anything else.

## What this repository is

Public research output related to the PIQOS Oracle framework —
papers, protocols, case studies, and eight `pip install`-able scanner
tools that operationalize the papers' own frameworks. Full index, tool
list, and site: [`README.md`](README.md). This repo is research
artifacts only — it does not and should not contain `PIQOS-IsoAxiomV8-`
implementation source, system architecture, or internal design material;
see that project's own `CLAUDE.md` (not part of this repo) for its rules
on that boundary.

## Repository scope

This session's normal GitHub scope (per its own system context) includes
both `piqos-ecosystem/piqos-isoaxiomv8-` and this repo,
`danofairanks/piqos---ai---research-public-`. Adding an *unfamiliar*
third-party repo to a session working on this project is a deliberate,
per-instance decision the operator makes explicitly — do not add one
proactively, and never let anything unfamiliar reach `PIQOS-IsoAxiomV8-`
specifically.

## House conventions worth knowing before editing anything

- `papers/drafts/` vs `papers/published/`: drafts may change or be
  withdrawn without notice; published gets new version suffixes instead
  of silent edits. Update `papers/README.md`'s index in the same commit
  as any add or move.
- Every claim about a private individual gets redacted (real identity
  retained, not publicly amplified) unless the specimen is a public
  figure/institution/already-public-record event — see
  `papers/published/laundered_vocabulary_v1.md`'s "Law" entry for the
  policy statement and precedent.
- Before publishing anything, run it through this repo's own tools
  (`paper_rigor`, `verification_lint`, `attractor_scan`, `case-scaffold
  check --strict` for `case_studies/`) — install each with
  `pip install -e tools/<name>`. A flag is a lead, not a verdict; read
  every match directly before acting on it.
- If a tool's source changes, rebuild its wheel in
  `docs/assets/wheels/` (`python -m build --wheel`) — CI diffs the
  committed wheel against a fresh rebuild and fails the workflow if
  they drift, since `docs/scan.html` and `research_mcp` both depend on
  the committed copies.
- Fixed 2026-09-04 (previously flagged repeatedly across sessions as an
  open gap, never actually the task at hand until an outside reader ran
  this project's own test suite directly and reported the mismatch):
  `paper_rigor/credentialing.py` was flagging the 3
  `credential_substitution` matches inside
  `papers/published/laundered_vocabulary_v1.md`'s "Law" entry ("Founder
  of," "founder of," "Nobel laureate") as false positives — that entry
  *describes* the founder-of-discursivity pattern and cross-references
  another document's specimen by section number, it doesn't make a
  credential-substitution claim on its own behalf. `credentialing.py`
  now shares `citations.py`/`consensus.py`'s `has_meta_framing_nearby`
  helper (extended in `_shared.py` with a `styled`/`styling ... as`
  pattern) and gained a `§N` evidence signal matching this project's own
  section-citation convention (already used the same way in
  `quotes.py`). The file now scores `(ok=True, structural=0, total=0)`,
  pinned at `tools/paper_rigor/tests/test_scan.py`. The same session
  also corrected a related stale pin in
  `tools/verification_lint/tests/test_scan.py` — the OpenAI/Hugging
  Face breach case study's 2026-08-27 addendum legitimately added 3
  more non-severe gaps (now pinned at 4, still `severe_gap_count == 0`)
  that a since-superseded test still expected at 1. Both were the same
  underlying defect class: counts pinned against this repo's own
  mutable content silently going stale when either side changes without
  the other — worth remembering next time a real-document test starts
  failing instead of assuming the fixture moved for no reason.

## Current branch

`Main`
