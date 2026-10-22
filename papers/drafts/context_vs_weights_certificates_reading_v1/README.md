Scripts and outputs for `context_vs_weights_certificates_reading_v1.md`. Nothing here downloads data or models; every script runs on numpy and the paper's printed numbers.
- `predictions_fixed_2026-10-20.md`: the predictions and checks fixed before the paper was read.
- `checks_paper.py` / `_output.txt`: the "exact law" tested on 2,000 random discrete distributions; the paper's printed counts, means and Wilson bounds recomputed.
- `closed_forms_check.py` / `_output.txt`: an independent check of the paper's linear-Gaussian closed forms (Appendix A.10), written from the printed model; the formula reading is stated in the script header.
- `toys_preregistration_2026-10-22.md`, `toys.py` / `toys_output.txt`: the three counter-model toys. `toys.py` calls `bitsy.core.race` from a checkout of the repository at commit cf81a50 (`BITSY_PATH=/path/to/bitsy python3 -I toys.py`; about 10 seconds).
