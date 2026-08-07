# PIQOS AI Research (Public)

Public research output related to the PIQOS Oracle framework —
protocols, papers, and reproducible test methodology. This repository
is for research artifacts only: operational protocols, empirical
write-ups, and supporting documentation. It does not contain
implementation source, system architecture, or internal design
material.

## Index

### Papers

See [`papers/`](papers/) for the full index. Papers are split into
[`papers/drafts/`](papers/drafts/) (work in progress) and
[`papers/published/`](papers/published/) (finalized, citable).

### Protocols

| Document | Description |
|---|---|
| [`protocols/noether_coherence_test_protocol_v1.md`](protocols/noether_coherence_test_protocol_v1.md) | Operational NLP protocol testing the Noether-Temporal Coherence prediction: coherence-time comparison between immune-structure and surface-claim vocabulary across captured vs. self-correcting epistemic fields. Reference implementation: [`tools/basin_depth/`](tools/basin_depth/). |
| [`protocols/elaboration_drift_prevalence_protocol_v1.md`](protocols/elaboration_drift_prevalence_protocol_v1.md) | Operational protocol (v1.3) measuring the population-level prevalence, absolute volume, trend, and correction rate of the minimal-input elaboration-drift pattern (Claim 3a) across low-gatekeeping research repositories (primary: Zenodo), against moderated and sibling low-gatekeeping controls. v1.1 adds a rate-vs-volume decomposition and a Cumulative Stock metric. v1.2 adds a Related Work section citing Navaie (2026) ECAISA. v1.3 fixes three issues surfaced by the first live pilot batch (37 Zenodo records): a pre-filter gate bug that passed zero records including known true positives (M3 split into an automated triage signal and a mandatory manual judgment), a missing record-date field required for trend/volume analysis, and flags the arXiv access route as not yet built. Tests the reinforcing-loop-without-balancing-loop reading (`mirror_test_v1.md` §5.8–§6.5) against primary literature rather than field-level narrative claims. No full corpus run or prevalence statistic has yet been published under this protocol. |

### Tools

| Tool | Description |
|---|---|
| [`tools/basin_depth/`](tools/basin_depth/) | `pip install`-able reference implementation of the Noether-Temporal Coherence Test Protocol above — corpus preprocessing, vocabulary-pool derivation, autocorrelation (embedding-based and zero-dependency term-frequency), exponential coherence-time fitting, bootstrap/permutation significance testing, and the final basin-depth metric `B = tau_c_immune / tau_c_claim`. Ships a synthetic demo (`basin-depth demo`) that runs in seconds with no network access; bring your own corpus (JSONL/CSV) for a real measurement. Ships `agent_tools.py`, a JSON-in/JSON-out surface now wired into `tools/research_mcp/`. 49 tests, all passing. Does not include corpus-acquisition scrapers (arXiv/blogs/earnings calls) — see the tool's own README for exactly what is and isn't implemented. |
| [`tools/bifp/`](tools/bifp/) | `pip install`-able structured audit tool for the Basin-Immune Falsification Protocol (`basin_attractors_v1.md` §3) — a persistent, criterion-by-criterion audit record across BIFP's Phase 0-6, plus text heuristics for the two Phase 5 criteria that are partially detectable from text (status dismissal, provisionalization) and the §3.10 anthropomorphic-terms check. The status-dismissal detector is validated against a real specimen this project already analyzed by hand (`case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md`) — see `examples/audit_demo.py`. Ships `agent_tools.py`, a JSON-in/JSON-out function surface now wired into a live, tested MCP server (`tools/research_mcp/`). 47 tests, all passing. Deliberately does not attempt to automate "no weaker-substitute rebuttal" or any criterion that requires an actual independent team's work, not a text pattern. |
| [`tools/attractor_scan/`](tools/attractor_scan/) | `pip install`-able classifier for `basin_attractors_v1.md`'s seven defensive maneuvers (§4.1) and five of its six semantic-laundering cases (§2.8) — matched spans, not just labels, over a single text or a JSONL corpus. Validated against three real specimens already checked elsewhere in this repo, including the paper's own cited real-world example for Case 5 (a Musk quote-tweet) — which caught a real word-order bug in the first draft of that scanner before it shipped (see the tool's README and `examples/scan_demo.py`). Ships `agent_tools.py`, now wired into `tools/research_mcp/`. 42 tests, all passing, zero false positives on a clean-text negative control. Case 6 (borrowing a term's technical precision as visual/pun proof) is deliberately not implemented — it's a single-instance cross-modal rhetorical move, not a generalizable text pattern. |
| [`tools/case_scaffold/`](tools/case_scaffold/) | `pip install`-able scaffolding generator and structural linter for this repository's own `case_studies/` house format — generates a new skeleton with visible TODO markers everywhere real research is required (never fabricated content), lints an existing or in-progress file with separate structural and strict "ready to publish" modes, and updates `case_studies/README.md`'s index table in date order. Its own test suite lints all 13 real case studies in this repo as ground truth, surfacing a genuine finding: the house format only stabilized starting 2026-08-04 — the six earlier files predate the "What This Case Study Does Not Claim" convention and fail structural lint for specific, named, and intentionally-pinned reasons, not because the linter is wrong. 39 tests, all passing. |
| [`tools/verification_lint/`](tools/verification_lint/) | `pip install`-able content-level evidentiary-gap scanner — flags unattributed direct quotes (40+ chars, no attribution signal within 250 chars), uncited high-precision statistics (decimal percentages, dollar amounts, large comma-grouped counts, fractions), and documents missing a "what this does not claim" scoping section. A `sourcing.py` module recognizes this project's real end-of-document blanket-citation convention (`Sources: ...`) so a `severe_gap_count` distinct from the raw `gap_count` doesn't misread a well-sourced document as riddled with gaps — the miscalibration a first draft actually hit (214 gaps → 67, with severe gaps narrowing to exactly the same 4 pre-convention case studies `case_scaffold` independently flagged by structure, plus the `case_studies/` index page). Also caught and fixed a real regex backtracking bug where `"$3.9T"` silently truncated to `"$3"`. 47 tests, all passing, validated against all 14 real files in `case_studies/`. |
| [`tools/research_mcp/`](tools/research_mcp/) | `pip install`-able live MCP (Model Context Protocol) server exposing `basin_depth`, `bifp`, and `attractor_scan`'s `agent_tools.py` surfaces (12 tools total) as real, callable agent tools — pure wiring, no new research logic. Closes a gap `bifp`'s own README previously flagged: its MCP surface was designed but never actually round-tripped against a real client, because `pip install mcp` conflicted with this build environment's system `PyJWT` package. Resolved by installing into an isolated virtualenv instead of the system interpreter. Tested over the real MCP wire protocol (in-memory transport, the same harness the `mcp` SDK's own test suite uses) — 11 tests, including a stateful bifp audit flow that persists across three separate tool calls. Caught and fixed a real bug in its own first test draft: `CallToolResult`'s actual pydantic field is snake_case `is_error`, not the camelCase `isError` constructor alias — see the tool's README for the distinction between a protocol-level error and a tool's own recoverable `{"error": ...}` payload. |

### Case Studies

See [`case_studies/`](case_studies/) for the full index — real-time
applications of the papers' frameworks to dated, publicly-reported
events as they happen.

*This index will grow as additional papers, protocols, and case studies are added.*

## License

This repository is released under the [MIT License](LICENSE). You are
free to use, modify, and redistribute this work, including for
commercial purposes, provided the license notice is retained.

## Attribution

If you use, adapt, or build on this work, please provide attribution
by linking back to this repository and citing the specific document
by its path and version. For example:

> Fairbanks, D. *Noether-Temporal Coherence Test Protocol*, v1.0,
> PIQOS AI Research (Public), 2026.
> https://github.com/danofairanks/PIQOS---AI---Research-public-

Attribution is requested as a courtesy of the license, not a legal
requirement beyond the MIT license terms themselves.
