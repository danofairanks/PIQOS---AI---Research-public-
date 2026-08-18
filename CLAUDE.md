# PIQOS AI Research (Public) — Session Context

This file auto-loads at the start of any Claude Code session against this
repository. If you are a fresh session reading this: welcome, here is what
you need to know before doing anything else.

## Handoff note (filed 2026-08-18, action pending)

A prior session on branch `claude/public-research-repo-setup-rppbk2`
repeatedly failed to add `piqos-ecosystem/piqos-isoaxiomv8-` to its session
scope. Four separate `add_repo` calls across ~20 minutes all returned
`MCP tool call requires approval` even after the operator confirmed
approving the prompt each time — a session-level bug, not a real
permission denial (the repo is in this project's normal allowed scope; see
"Repository scope" below). **If you can reach that repo, the first thing
worth doing is retrying `add_repo` once, cleanly, before anything else.**

Why it matters: the operator recalled that `PIQOS-IsoAxiomV8-` already has
a rule requiring a definition be checked for value/falsifiability *before*
equations built on it are evaluated — arrived at independently, after a
prior paper checked out structurally while its definition made the work
meaningless. Likely in a derivations folder, or already built into
Harold/CrossOracleAuditor's pipeline. This project has since filed
[`papers/drafts/definition_first_gate_proposal_v1.md`](papers/drafts/definition_first_gate_proposal_v1.md),
a *deliberately unbuilt* proposal for the same idea, grounded entirely in
a fully-verified local specimen
([`case_studies/2026-08-18_grok_falsifiable_agi_definition_oracle_loop.md`](case_studies/2026-08-18_grok_falsifiable_agi_definition_oracle_loop.md))
because the IsoAxiomV8 precedent could not be independently verified this
session. **If you can reach the source, check it and update the proposal
accordingly** — confirm it, correct it, fold in a real citation, or say
plainly that it doesn't match what the operator recalled. The proposal
already states this provenance note as explicitly unverified; that's the
thing to resolve.

Do not treat this note as itself a citable source once the above is
resolved — update or remove it in the same commit that acts on it. A stale
handoff note left in place after its action item is done is exactly the
kind of drift this project's own tooling exists to catch elsewhere.

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

`claude/public-research-repo-setup-rppbk2`
