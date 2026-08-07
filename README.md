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
| [`tools/basin_depth/`](tools/basin_depth/) | `pip install`-able reference implementation of the Noether-Temporal Coherence Test Protocol above — corpus preprocessing, vocabulary-pool derivation, autocorrelation (embedding-based and zero-dependency term-frequency), exponential coherence-time fitting, bootstrap/permutation significance testing, and the final basin-depth metric `B = tau_c_immune / tau_c_claim`. Ships a synthetic demo (`basin-depth demo`) that runs in seconds with no network access; bring your own corpus (JSONL/CSV) for a real measurement. 43 tests, all passing. Does not include corpus-acquisition scrapers (arXiv/blogs/earnings calls) — see the tool's own README for exactly what is and isn't implemented. |
| [`tools/bifp/`](tools/bifp/) | `pip install`-able structured audit tool for the Basin-Immune Falsification Protocol (`basin_attractors_v1.md` §3) — a persistent, criterion-by-criterion audit record across BIFP's Phase 0-6, plus text heuristics for the two Phase 5 criteria that are partially detectable from text (status dismissal, provisionalization) and the §3.10 anthropomorphic-terms check. The status-dismissal detector is validated against a real specimen this project already analyzed by hand (`case_studies/2026-08-06_marcus_karapetyan_status_dismissal.md`) — see `examples/audit_demo.py`. Ships `agent_tools.py`, a JSON-in/JSON-out function surface designed for MCP/agent tool-calling (not shipped as a live MCP server — see the tool's README for why). 47 tests, all passing. Deliberately does not attempt to automate "no weaker-substitute rebuttal" or any criterion that requires an actual independent team's work, not a text pattern. |

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
