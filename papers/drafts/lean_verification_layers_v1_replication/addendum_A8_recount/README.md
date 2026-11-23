# Recount for Addendum A.8 (draft; reader-run, single reader)
`audit_repo.py` recounts the lab's public Lean repository described in A.8: manifest status counts, source-hash and receipt checks, per-declaration support by a passing receipt, and a text scan of the sources. Standard library only; it reads files and runs no Lean. `audit_output.txt` is its output on a copy fetched on 2026-11-23.

To rerun: fetch `MANIFEST.tsv`, `ISSUES.md` and the files listed in it (sources and receipts) from the lab's public repository into one directory, write the list of receipt paths to `receipts.txt` in that directory, retry any file that returns a rate-limit page, then run `python3 -I audit_repo.py <that directory>`.

Limits: the fetched copy and the repository can change; the four-source rebuild reported in A.8 used Lean 4.27.0-rc1 and Mathlib at commit `fdddb3ea` and is not reproduced by this script; the script does not judge whether the formal statements match the manuscript.
