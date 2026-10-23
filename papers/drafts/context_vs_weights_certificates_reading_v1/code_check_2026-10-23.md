# Second search for the supplementary package, 2026-10-23

Question: has the supplementary material that Appendix F of arXiv:2610.29419 describes (a package, scripts under `scripts/`, saved results) become obtainable? A plan was written before any fetch: expected the repository HEAD unchanged at cf81a50, the arXiv source package to hold TeX and figures but no scripts, no new paper version, and no other public code. Result: **not obtainable; all four expectations held.** Nothing was run, because there was nothing to run.

| Source | What was found |
|---|---|
| Repository `github.com/leochlon/bitsy` | `git ls-remote`: one ref, `main`, at `cf81a50f3040380d9e957532841f8e270261c8d5`. Not cloned (HEAD unchanged). |
| arXiv abstract page | `[v1]` only (21 October 2026); no ancillary-files section; no comments field; no code link. |
| arXiv source package (`/e-print/2610.29419`, sha256 `655b7b1a2bf726bc4f7c40059d3263c6450ff3adde6fceb89055ee5e73311462`) | `main.tex`, `main.bbl`, `fig_budget.tex`, `icmlfallback.sty`, `00README.json`, 11 figure PDFs. No scripts, data or results files. |
| Appendix F (Reproducibility), in `main.tex` | No URL, DOI or repository name. States that "the supplementary material holds the code and saved results" and names a package `shippable`, `scripts/closed_forms.py`, `scripts/simulate_and_plot.py`, `scripts/domains/`, `scripts/counts/`, `scripts/decision/` and `scripts/gpt2/` with their `results/` directories (23 names, in `promised_supplement_list_from_appendix_F.txt`). States that "repeating the model executions requires the original datasets and pretrained weights". |
| Comments in the TeX | None mentioning code, scripts, release, supplement or a repository. |
| Package registries and guessed names | PyPI `bitsy` is an unrelated package by another author; PyPI `shippable` returns 404. `git ls-remote` for three guessed repository names under the authors' account returned a credentials prompt, which GitHub gives for both missing and private repositories, so the two cases are not distinguished. |

Observation: the paper's package is named `shippable`; the public repository's package is `bitsy` (`pyproject.toml`, `packages = ["bitsy"]` at cf81a50).

Not tried: the authors' other repositories; Zenodo, Hugging Face and OSF listings (the paper points to none); asking the authors, which is an outward step and was not taken.
