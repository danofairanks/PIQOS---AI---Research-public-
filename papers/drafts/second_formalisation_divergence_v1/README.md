# Companion folder: second formalisation, divergence and flagged alternatives (draft v1)
Files for `../second_formalisation_divergence_v1.md`. One sub-folder per experiment, exactly as run (relative paths between them are preserved).
- `evidence_2026-10-08_cross_family_formalisation/`: six-statement first test, checker (`check.py`), preregistration, replies.
- `evidence_2026-10-08_boundary_divergence_rate/`: batch 1 (24 items), briefs, raw replies of three arms, scorer.
- `evidence_2026-10-08_batch2/`: batch 2 (external sentences plus the six-wording cap ladder), four arms, scorers, the post-hoc domain normalisation.
- `evidence_2026-10-08_flagged_alternatives/`: re-analysis of the ambiguity notes (script and outputs).
- `evidence_2026-10-08_batch3_oracle/`: nine library-documentation sentences scored against observed library behaviour (`oracle.py`, `oracle_truth.json`).
Reproduce: `pip install z3-solver`; `python check.py A.json B.json` in a folder compares two sets of formalisations; `score*.py` and `flagged_alt.py` regenerate the tables. `oracle.py` additionally needs the libraries it probes (aiolimiter, limits, pyrate-limiter, token-bucket, ratelimit) and a local Redis is NOT needed.
Provenance notes: the model replies are as pasted by the operator (several were invalid JSON because of unescaped quotes; the SMT fields are unchanged). Two phrases in the copied preregistration files that named a project-specific instruction file were reworded to "a project instruction file" when copying; no other edit. Result summaries (RESULTS files) are not copied: the paper carries them.
