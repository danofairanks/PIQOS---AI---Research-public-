# mem_proposal_reading_v1: supporting files

Reading: [`../mem_proposal_reading_v1.md`](../mem_proposal_reading_v1.md). Nothing here runs the authors' code (none is linked); every script is the reader's own implementation from the papers' text. Same-source caveat: written by the same AI-assisted reader as the reading.

- `counter_models/PREREG_DEFEAT_CONDITIONS.md`: defeat conditions and predictions written before any toy existed (published copy; three wording substitutions disclosed in its first lines; the original's sha256 is recorded there). `AMENDMENTS.md`: flaws found after run 1, written before run 2. `toys_formal.py` (T1, T2; numpy), `toys_rl.py` (T3-T5; standard library; run 2), `toys_rl_run1.py` (run 1, kept), `out_*.txt` (outputs; `out_t5_run1_INVALID.txt` is the invalid run). Run: `python3 -I toys_formal.py`; `python3 -I toys_rl.py t3|t4|t5` (t4 and t5 take a few minutes).
- `rating_check/chk_gnwt.py`: recomputes the evidence row and the K comparison of arXiv 2609.38495 from its Table 5. Needs the PDF's text layer: `pdftotext -layout 2609.38495.pdf 2609.38495.txt`. `out_chk_gnwt.txt` is the output.
- `quote_checks.py`, `quote_check_results.txt`: lexical check of the reading's quoted strings against the four PDFs' text layers. The PDFs are not stored here.
- `tool_scan_*.json`: this repository's scanners run on the reading. Read in context: the attractor scan's "goal-post" match is the reader's own heading ("cannot yet support") and its "equivocation" match is a journal title containing the word "Intelligence"; both are false positives.
- `SHA256SUMS`: hashes of the files in this folder.
