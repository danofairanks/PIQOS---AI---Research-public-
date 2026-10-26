Scripts and outputs for `agent4sci_hill_climbing_reading_v1.md`.
- `recompute_table2.py` / `out_recompute.txt`: Table 2 aggregates (means, medians, sign tests, leave-out means) recomputed from the 20 benchmark rows transcribed from the paper. Standard library only.
- `paper_checks.py` / `paper_checks_output.txt`: (A) the 20 x 4 delta values of Table 2, as transcribed in `recompute_table2.py`, against the printed table; (B) 25 quoted strings and printed counts found verbatim; (C) two derived counts; (D) keyword searches for terms the draft says are absent. Needs the arXiv v1 PDF (sha256 in the script; not stored here) and `pdftotext`.
- `tool_scan_*.json`: output of `paper_rigor`, `verification_lint` and `attractor_scan` on the draft.
There is no `predictions_fixed` file: this reading was post hoc.
