# Replication material for Addendum A.14 of `lean_verification_layers_v1.md`

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

Addendum A.14 reads a public reconstruction-and-audit repository for the Lean proof of A.9 against the layers of section 2. This folder holds what a reader needs to check the counts and to find each quoted line. The repository is third-party; no individual is named here.

## Source (pinned)
- Repository state read: commit `aa9c86bf2a7d29b08575641fecea19a2a603e87c` (24 November 2026). 33 commits, all dated that day; 222 files. Read from a blobless clone; nothing was built or run, and no Lean was run.
- Table recounted: `audit/final_certification/Global_Ownership.tsv.gz` at that commit, SHA-256 `7aff62b3f6b077a54415f351492c27b00b98138610ccab49d6c1efc3fd698753` (15.6 MB; not stored here).
- Script SHA-256 prefixes at that commit (`audit/final_certification/scripts/`): `index_decls.py` `27af0476a9dd386a`, `build_graph.py` `0c644fc424b8c02e`, `gc_live.py` `657875a52dd78b6b`, `gc_named.py` `b34e80fdb96e7182`, `gc_classify.py` `1a5bb34d22a5d417`, `gc_final.py` `7aab13e22b78bcfa`, `gc_layer3.py` `f10541826b9dffe8`.

## What is here
| File | What |
|---|---|
| `recount_ownership.py` | Standard-library recount of the ownership table (status counts; the evidence kinds inside "closed via prior package") |
| `recount_output.txt` | Its output on the table above; matches the repository's own status table exactly |

To reproduce: obtain the repository at the commit above and run `python3 -I recount_ownership.py audit/final_certification/Global_Ownership.tsv.gz`.

## Where each reading in A.14 can be checked (paths are inside the repository at the pinned commit)
| Reading | Where |
|---|---|
| The dependency graph is built by approximate name resolution over text | `scripts/build_graph.py`, module docstring ("Lean 4 rules, approximated"; "dot" edges kept when at most 40 declarations share the last name component); `scripts/index_decls.py` (line-oriented parser; records identifier tokens) |
| A report mention is read as a citation, without checking what the sentence says | `scripts/gc_named.py` (tokens from `\lean{}` and backtick spans and the first column of TSVs; suffix resolution) |
| Status by position in the dominator tree | `scripts/gc_classify.py`, the step commented "nearest cited THEOREM dominator at depth >= 4" |
| Leftover live theorems are reassigned unconditionally | `scripts/gc_final.py`, the loop over the leftover live theorems (around lines 54-62) and the later fold of definitions into the same status (line 65) |
| The Lean kernel was not run; the archive was not built or replayed | `docs/STATUS.md` ("The certification did not run the Lean kernel", section 3; "This repository did not build or replay the archive", section 6); `docs/SOURCE_MANIFEST.md` section 2 |
| Agents read the proofs as text; no report built or ran the archive | `audit/README.md`, the paragraph after the first heading |
| 1,696 declarations in nontrivial strongly connected components; dot edges over-approximate | `audit/final_certification/Final_Global_Internal_Certification.tex`, paragraph "Live subgraph" |
| Five of 26 closure verdicts rest on reports not in the workspace | `audit/final_certification/Global_Residual_Reconciliation.tsv`, the notes column (PC-1, PC-2, PC-3, PC-5, PC4.13 R4-D) |
| Title and abstract versus the conditional final implication | `manuscript/abstract.tex`; `manuscript/sec18_assembly.tex`, "remains conditional on the hypotheses above" |
| The scripts read prebuilt indices that are not in the repository | about 235 references to paths under `/home/claude/` and 44 distinct `.pkl`/`.npy` input names across the 78 scripts; none of those files is in the repository |

## What this does and does not establish
- It establishes what the code and the status files say and what the table contains. It does not establish anything about the mathematics, the archive, or whether a gap exists.
- Which Lean features create dependencies that no token names (tactics, simp sets, instance resolution, notation) is the reader's inference (E3); it was not tested here because no Lean was run.
- One AI-assisted reader, static read of a minimum set of files plus the classification scripts, the external-theorem ledger and one manuscript argument. The repository changes; re-read before relying on this.
