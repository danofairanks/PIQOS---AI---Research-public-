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
| [`protocols/noether_coherence_test_protocol_v1.md`](protocols/noether_coherence_test_protocol_v1.md) | Operational NLP protocol testing the Noether-Temporal Coherence prediction: coherence-time comparison between immune-structure and surface-claim vocabulary across captured vs. self-correcting epistemic fields. |
| [`protocols/elaboration_drift_prevalence_protocol_v1.md`](protocols/elaboration_drift_prevalence_protocol_v1.md) | Operational protocol (v1.3) measuring the population-level prevalence, absolute volume, trend, and correction rate of the minimal-input elaboration-drift pattern (Claim 3a) across low-gatekeeping research repositories (primary: Zenodo), against moderated and sibling low-gatekeeping controls. v1.1 adds a rate-vs-volume decomposition and a Cumulative Stock metric. v1.2 adds a Related Work section citing Navaie (2026) ECAISA. v1.3 fixes three issues surfaced by the first live pilot batch (37 Zenodo records): a pre-filter gate bug that passed zero records including known true positives (M3 split into an automated triage signal and a mandatory manual judgment), a missing record-date field required for trend/volume analysis, and flags the arXiv access route as not yet built. Tests the reinforcing-loop-without-balancing-loop reading (`mirror_test_v1.md` §5.8–§6.5) against primary literature rather than field-level narrative claims. No full corpus run or prevalence statistic has yet been published under this protocol. |

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
