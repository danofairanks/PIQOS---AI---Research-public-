# Replication material for `lean_verification_layers_v1.md`

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

What is here, and what is not.

| File | What | Status |
|---|---|---|
| `probe1_correlated_failure.py` | Overlap of wrong accepts among checkers (§4.2) | runs as shipped; takes the arena results file path as argument |
| `probe1_results.json` | Its output on the 2026-11-21 results (arena revision `fdc02ded`) | the numbers quoted in §4.2 |
| `probe1_results_rerun_2026-11-22.json` | Same script, run on the live results file on 2026-11-22 (revision `abd3dd4f`, 270 tests, SHA-256 `654117417a57e44c0d3b2345fdc51c6927f4410e62eb49e673a06c6332b72aa1`) | replication on later data |
| `probe4_unseen_mass.py` | Unseen-failure-mass estimators (§4.3) | script only; see below |
| `probe4_results.json` | Its output on the 2026-11-21 inputs | the numbers quoted in §4.3 |
| `arena_summary_2026-11-21.json` | Derived summary of the 2026-11-21 results file | summary, not the raw file |

## What this does and does not establish

- **The 2026-11-21 raw results file was not retained.** Only the derived summaries above were kept. The quoted §4.2 and §4.3 numbers therefore cannot be re-derived byte for byte from a pinned input.
- **Rerun on later data.** The arena's results file is overwritten each round. On 2026-11-22 (two more invalid tests, two more valid) the same script gives overlap statistic 43 against a permutation-null mean of 4.45 (95th percentile 8), against 46 and 4.22 on 2026-11-21. The direction and size of the effect hold; the exact values moved with the data. The six tests accepted by two or more checkers were unchanged in kind (inductive types and recursor rules). This is a rerun of one analysis by the same reader, not an independent replication.
- **`probe4_unseen_mass.py` is not rerun.** It needs a second input, `/tmp/arena_test_dates.json`: a JSON list of `[test_name, "YYYY-MM-DD"]` pairs giving the date of the first commit that added each test file in the arena repository. That file was not retained; regenerate it from a clone of the arena repository's history and the results file for the round you want, and expect different values on later data.
- Paths in the scripts (`/tmp/...`) are the reader's scratch locations; pass or edit them.
- Scripts were written and run by one AI-assisted reader. They have not been reviewed by a second person.
