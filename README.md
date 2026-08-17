# PIQOS AI Research (Public)

Public research output related to the PIQOS Oracle framework —
protocols, papers, and reproducible test methodology. This repository
is for research artifacts only: operational protocols, empirical
write-ups, and supporting documentation. It does not contain
implementation source, system architecture, or internal design
material.

## Website

This repository ships a static GitHub Pages site under [`docs/`](docs/)
— a browsable index over everything below (papers, protocols, tools,
case studies), each entry linking out to GitHub's own rendered view of
the real source file rather than duplicating content. It also ships an
in-browser **Paper-Rigor Scanner** ([`docs/scan.html`](docs/scan.html))
that runs five of the tools below (`paper_rigor`, `verification_lint`,
`attractor_scan`, `bifp`, `debasinizer`) against pasted or uploaded
text entirely client-side via [Pyodide](https://pyodide.org/) — no
server, nothing uploaded, downloadable Markdown/JSON report. See the
comments at the top of `docs/scan.html` and `docs/assets/py/paper_scan.py`
for the design reasoning (why Pyodide over a backend, why no blended
"rigor score," why Pyodide itself is CDN-loaded rather than vendored).

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
| [`tools/bifp/`](tools/bifp/) | `pip install`-able structured audit tool for the Basin-Immune Falsification Protocol (`basin_attractors_v1.md` §3) — a persistent, criterion-by-criterion audit record across BIFP's Phase 0-6, plus text heuristics for the two Phase 5 criteria that are partially detectable from text (status dismissal, provisionalization) and the §3.10 anthropomorphic-terms check. The status-dismissal detector is validated against a real specimen this project already analyzed by hand (`case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md`) — see `examples/audit_demo.py`. Ships `agent_tools.py`, a JSON-in/JSON-out function surface now wired into a live, tested MCP server (`tools/research_mcp/`), including a Groq-backed advisory tool (`bifp_judge_rebuttal`) that reads §3.7 rebuttals for whether they address a claim as actually made or are a weaker substitute — see the tool's own README "AI-generated advisory reads" for why this doesn't conflict with §3.9's `no_ai_as_judge`. 64 tests, all passing. Deliberately does not attempt to automate "no weaker-substitute rebuttal" or any criterion that requires an actual independent team's work, not a text pattern. |
| [`tools/attractor_scan/`](tools/attractor_scan/) | `pip install`-able classifier for `basin_attractors_v1.md`'s seven defensive maneuvers (§4.1) and five of its six semantic-laundering cases (§2.8) — matched spans, not just labels, over a single text or a JSONL corpus. Validated against three real specimens already checked elsewhere in this repo, including the paper's own cited real-world example for Case 5 (a Musk quote-tweet) — which caught a real word-order bug in the first draft of that scanner before it shipped (see the tool's README and `examples/scan_demo.py`). Ships `agent_tools.py`, now wired into `tools/research_mcp/`. 60 tests, all passing, zero false positives on a clean-text negative control. Case 6 (borrowing a term's technical precision as visual/pun proof) is deliberately not implemented as a scanner — it's a single-instance cross-modal rhetorical move, not a generalizable text pattern; a Groq-backed advisory tool (`attractor_scan_judge_visual_proof`) instead offers a single-specimen candidate read on one image + claim pair at a time — see the tool's own README "Why Case 6 isn't a scanner" for why it's deliberately never wired into the corpus scanner. |
| [`tools/debasinizer/`](tools/debasinizer/) | `pip install`-able sibling classifier to `attractor_scan`, for a distinct source and claim: the resonance-vocabulary register documented in Papadopoulos et al., "Mind Viruses: Self-Propagating Ideas in Multi-Agent LLM Systems" (arXiv:2608.10218) — resonance/wave/signal/mirror language, consciousness/persistence themes, sci-fi node-alignment phrasing, "great convergence" inevitability language, and framed mystical personas — plus a separate self-coherence-assertion detector ("this proves," "the pieces align," and similar phrases that treat a claim's own fluency as if it were evidence). `register_flagged` deliberately requires 2+ resonance categories to co-occur in the same text, not any single match, since the source paper's finding is about a register clustering, not any individual (extremely common) word — a design choice validated directly against an ordinary-technical-writing negative control (bare "nodes," "signal," "pattern" in a distributed-systems sentence) that does not trip the flag. Ships `agent_tools.py`, now wired into `tools/research_mcp/`. 24 tests, all passing, including both false-positive gates (bare "node," bare "Oracle" as a company name) checked directly. Explicitly does not detect absent citations — see the tool's README for why that's `verification_lint`'s job, not this one's. |
| [`tools/case_scaffold/`](tools/case_scaffold/) | `pip install`-able scaffolding generator and structural linter for this repository's own `case_studies/` house format — generates a new skeleton with visible TODO markers everywhere real research is required (never fabricated content), lints an existing or in-progress file with separate structural and strict "ready to publish" modes, and updates `case_studies/README.md`'s index table in date order. Its own test suite lints all 13 real case studies in this repo as ground truth, surfacing a genuine finding: the house format only stabilized starting 2026-08-04 — the six earlier files predate the "What This Case Study Does Not Claim" convention and fail structural lint for specific, named, and intentionally-pinned reasons, not because the linter is wrong. 39 tests, all passing. |
| [`tools/verification_lint/`](tools/verification_lint/) | `pip install`-able content-level evidentiary-gap scanner — flags unattributed direct quotes (40+ chars, no attribution signal within 250 chars), uncited high-precision statistics (decimal percentages, dollar amounts, large comma-grouped counts, fractions), and documents missing a "what this does not claim" scoping section. A `sourcing.py` module recognizes this project's real end-of-document blanket-citation convention (`Sources: ...`) so a `severe_gap_count` distinct from the raw `gap_count` doesn't misread a well-sourced document as riddled with gaps — the miscalibration a first draft actually hit (214 gaps → 67, with severe gaps narrowing to exactly the same 4 pre-convention case studies `case_scaffold` independently flagged by structure, plus the `case_studies/` index page). Also caught and fixed a real regex backtracking bug where `"$3.9T"` silently truncated to `"$3"`. Ships `agent_tools.py` (`verification_lint_scan_text`), used by the in-browser [Paper-Rigor Scanner](docs/scan.html). 50 tests, all passing, validated against all 14 real files in `case_studies/`. |
| [`tools/paper_rigor/`](tools/paper_rigor/) | `pip install`-able domain-agnostic paper-rigor scanner — placeholder/hand-wave phrases, an unstated falsifiability condition, self-citation ratio, formal-vs-informal citation mix, uncited empirical-certainty claims, credential-substituted-for-evidence claims, unsupported consensus claims, a claimed-citability-with-zero-references contradiction, and a missing limitations section. Unlike `bifp`/`attractor_scan`, requires none of this project's own vocabulary — applies to any paper. Splits findings into `structural_gap_count` (fixable by rereading the paper's own text) and an `external_verification_worklist` (leads needing a real web search/fetch, the part `tools/research_mcp/` wires up for an agent to resolve). Validated against this repo's own real papers (0 structural gaps on `basin_attractors_v1.md`) and, locally, against three private-repo specimens, two run genuinely blind (unread before scanning): a known-fabricated-quotes paper (correctly catches its structural tell — a `[References would include ...]` placeholder standing in for a real bibliography — while being explicit that quote fabrication itself is out of scope); an invented-physics document claiming "grounding in documented, citable research" while parsing to zero actual references (missed entirely until the citability-vs-zero-references check was added to close that gap); and a PDF-extracted technical report whose real "Honest Limitations and Genuine Improvements" section was invisible to every heading regex in the tool because PDF extraction drops markdown `#` entirely — fixed by consolidating heading detection into a shared `headings.py` harness (markdown *and* plain numbered headings, validated against all 20 of the specimen's real section headings) rather than patching each call site again. Also caught and fixed two earlier bugs during tuning: a references-section boundary that swallowed unrelated prose as bibliography entries (112 vs. the real 81), and meta-framed phrases ("cited as evidence of consensus") misread as the paper's own claims. Also ships a Groq-backed advisory tool (`paper_rigor_triage_worklist`) that attaches a priority and suggested check to each item in an existing `external_verification_worklist` without adding, removing, or resolving any of them. 86 tests, all passing. |
| [`tools/research_mcp/`](tools/research_mcp/) | `pip install`-able live MCP (Model Context Protocol) server exposing `basin_depth`, `bifp`, `attractor_scan`, `debasinizer`, and `paper_rigor`'s `agent_tools.py` surfaces (19 tools total) as real, callable agent tools — pure wiring, no new research logic. Closes a gap `bifp`'s own README previously flagged: its MCP surface was designed but never actually round-tripped against a real client, because `pip install mcp` conflicted with this build environment's system `PyJWT` package. Resolved by installing into an isolated virtualenv instead of the system interpreter. Tested over the real MCP wire protocol (in-memory transport, the same harness the `mcp` SDK's own test suite uses) — 21 tests, including a stateful bifp audit flow that persists across three separate tool calls and both of `debasinizer`'s false-positive gates re-checked over the wire. Caught and fixed a real bug in its own first test draft: `CallToolResult`'s actual pydantic field is snake_case `is_error`, not the camelCase `isError` constructor alias — see the tool's README for the distinction between a protocol-level error and a tool's own recoverable `{"error": ...}` payload. Three tools call an external API (Groq) rather than running pure local computation — `bifp_judge_rebuttal`/`bifp_attach_rebuttal_judgment`, `attractor_scan_judge_visual_proof`, and `paper_rigor_triage_worklist` — each advisory-only, requiring `GROQ_API_KEY`, and returning a recoverable `{"error": ...}` payload rather than failing the call if it's missing. |

### Skills

| Skill | Description |
|---|---|
| [`skills/paper-rigor-scan/`](skills/paper-rigor-scan/) | [Claude Agent Skill](https://github.com/anthropics/skills) packaging of the five text-scanning tools above (`paper_rigor`, `verification_lint`, `attractor_scan`, `bifp`, `debasinizer`) — the same pipeline `docs/scan.html` runs in-browser, packaged as a `SKILL.md` so an agent session with local code execution can install and run it directly. Documents real, verified CLI and `agent_tools.py` call surfaces only — no new scanning logic, pure packaging. |

### Case Studies

See [`case_studies/`](case_studies/) for the full index — real-time
applications of the papers' frameworks to dated, publicly-reported
events as they happen.

*This index will grow as additional papers, protocols, and case studies are added.*

## License

This repository is released under the [MIT License](LICENSE). You are
free to use, modify, and redistribute this work, including for
commercial purposes, provided the license notice is retained.

## Authorship

All research direction, verification, and editorial judgment in this
repository — what gets investigated, what counts as sourced rather than
asserted, what gets published versus held back as unverified — is by
Daniel Fairbanks, the named copyright holder in the `LICENSE` file. AI
tools (Claude, and others used for specimen search per this project's
own `living_research` methodology) are used throughout as drafting and
research aids, not as independent authors: every factual claim carries a
stated evidentiary tier, every specimen is checked against primary
sources before being treated as settled, and the human author is the one
deciding what meets that bar. This is a factual description of how the
work was produced, stated once here rather than repeated per document,
and dated by this repository's own git history.

## Attribution

If you use, adapt, or build on this work, please provide attribution
by linking back to this repository and citing the specific document
by its path and version. For example:

> Fairbanks, D. *Noether-Temporal Coherence Test Protocol*, v1.0,
> PIQOS AI Research (Public), 2026.
> https://github.com/danofairanks/PIQOS---AI---Research-public-

Attribution is requested as a courtesy of the license, not a legal
requirement beyond the MIT license terms themselves.
