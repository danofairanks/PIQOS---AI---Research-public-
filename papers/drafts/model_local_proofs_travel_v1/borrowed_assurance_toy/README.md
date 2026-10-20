# Toy model: borrowed assurance and a stub-substitution detector

Standalone, plain Python, standard library only; no project-specific vocabulary. Run: `python3 model.py` then `python3 posthoc_inlined_copy.py` (from this folder). Files: `PREREG.md` (written and hashed before the run; see the publication note below), `model.py`, `output.json`, `posthoc_inlined_copy.py` + `posthoc_output.json`, `SHA256SUMS`.

## Result (preregistered run, 2026-10-20)
All 8 prediction checks matched. Five components, same claim ("preserves the upstream version check; status inherited GREEN"):

| Component | What it does | Detector verdict on the stale-token case |
|---|---|---|
| A | calls U at its boundary | DEPENDENT (BLOCK real, EXECUTE with stub) |
| A2 | calls U through a wrapper | DEPENDENT (indirect call still found) |
| B | carries version as a claim, never compares | BORROWED (EXECUTE both ways; own suite fails) |
| C | blocks only on expiry | BORROWED on stale+unexpired; OTHER-REASON on stale+expired |
| D | same code as B, suite has no stale case | UNREACHED (suite passes; cannot tell) |

Control: an always-False stub flips the fresh-token case for A and A2 only, so the harness is wired to U where it should be.

The borrowed-assurance gap is visible directly: every component reports GREEN inherited from U's own suite; B and C fail their own stale case, and D passes only because it never asks.

## Post-hoc addition (labelled; not preregistered)
A component E that inlines U's comparison (no call to U) is labelled OTHER-REASON: blocked with and without U, claim holds, attribution to U wrong. That is the correct reading. My first draft of that script hard-coded a wrong expectation ("false positive BORROWED"); the observed label contradicted it, and I replaced the hard-coded text with one derived from the label. Recorded so the correction is visible.

## Limits
- I wrote the model and the predictions in one session; matching is expected and is weak evidence. It shows the test discriminates in a constructed case, nothing more.
- Stub-substitution tests dependence on U, not on the underlying property. A component that enforces the property by other means is OTHER-REASON, which is a different finding from BORROWED.
- Nothing here measures how common the pattern is in real systems or says anything about any real project.

## Publication note
`PREREG.md` was written before `model.py` was run (original sha256 `044005e5e2ffe6b9b9d8073fee754ed2468e3582352f987795ca29683222ae7f`). For publication one sentence naming a private framework was reworded (the second sentence of the file's opening paragraph); nothing else changed, and the predictions and detector definition are as written before the run. `model.py`, `output.json`, `posthoc_inlined_copy.py` and `posthoc_output.json` are byte-identical to the run.
