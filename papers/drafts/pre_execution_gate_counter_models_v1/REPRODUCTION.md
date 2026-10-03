# Reproduction record (execution only)

Scope: shows the code executes and reproduces its pinned outputs across environments. It is not a re-implementation from the paper text and not a check that the toys test the right claims.

## Run A: another model family, as reported to the operator (identity relayed, not independently verifiable)
- Runner: Grok session (xAI); request "run the repo scripts only". Linux sandbox, Python 3.12.3, stdlib only. UTC 2026-10-03T15:30:32Z.
- Source: this repository, branch `ccr-dbf2cfde-i60ilt`, folder `papers/drafts/pre_execution_gate_counter_models_v1/`, fetched from raw.githubusercontent.com. Read order: code first; the companion paper was not required for the run.
- Script hashes matched the folder's `SHA256SUMS` and equal the hashes listed there.
- `--selftest` printed `selftest OK` for all three scripts. Unmodified runs (stdout to file) produced:
  - gate_counter_models.py: `3af03152827b30eb6b1c66f9510eb859e07050f4b61a9c66f4404b0ed47080df`
  - gate_round2.py: `13b3ce60a6726a83bba253c0f2d6711dd87b15ba03c1463d88634a511d6fc119`
  - gate_hybrid_toy.py: `4460d09f003b25e3b122d13eb76516ee6561468a73f231be99361c583c719f38`

## Run B: author's environment (same checkout)
Python 3.11.15 and Python 3.10.20, unmodified runs: stdout SHA256 **identical to Run A for all three scripts**; `--selftest` OK on both versions; `sha256sum -c SHA256SUMS` passes.

## Reading
Output is byte-identical across Python 3.10.20, 3.11.15 and 3.12.3 and across two environments. Runner A had access to the code and so is not independent of it; the hash comparison is self-consistent with this folder and the anchor is the filing commit plus independently recomputed hashes. A fabricated report would need the output hashes, which were not published before this run.
**Still owed:** a re-implementation from the paper text alone, and an independent attack round.

## Addendum: `gate_round3.py`
Added after the runs above; run by the author only (Python 3.10, 3.11, 3.12: `--selftest` OK, pinned counts hold). It has not been run by anyone else, so the cross-environment claim above covers the first three scripts only.
