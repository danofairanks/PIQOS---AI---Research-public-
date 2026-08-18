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
- Known pre-existing gap, not yet fixed, out of scope in every session so
  far: `tools/paper_rigor/tests/test_scan.py::test_real_document_gap_counts`
  pins `papers/published/laundered_vocabulary_v1.md` at
  `(ok=False, structural=1, total=1)`; the file as it stands now actually
  scores `(ok=True, structural=0, total=3)`. The 3 flagged items are all
  `credential_substitution` matches ("Founder of," "founder of," "Nobel
  laureate") sitting inside the "Law" and "Coherence" entries' own
  discussion *of* credential substitution as a topic — plausibly false
  positives from the document using the phrases as examples, not making
  credential-substitution claims itself, but not yet checked closely
  enough to say for certain. Flagged repeatedly across sessions, never
  actually the task at hand — worth investigating and fixing properly
  rather than re-flagging it a fifth time.

## Current branch

`Main`
