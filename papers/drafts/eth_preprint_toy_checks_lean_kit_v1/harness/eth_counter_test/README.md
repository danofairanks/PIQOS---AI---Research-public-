Code and logs for the small-parameter test of Section 2 of "The Exponential Time Hypothesis is False" (OpenAI, 25 Oct 2026; paper.pdf sha256 5b1612dc2eebb2cad5b4cbe62d1fed2982f01ab1908c26f70010a651487e8123).
- eth_counter.py: construction (Sec 2.7), forms, decoupled evaluation (Sec 2.4), Taylor recovery (2.5, eq 2.9), Hermite solve.
- run_tests.py: `L1` construction checks; `<tag> r Q R n m seeds [nodec] [mutation]` end-to-end cases.
- sweep.sh / sweep2.sh: the runs reported in ../../results/RESULTS_eth_counter.md. results_*.json, log_*.txt, L1_results.json: raw outputs.
- PREREG.md (committed before implementing), DEVIATIONS.md.
Run: `python3 run_tests.py L1`; e.g. `python3 run_tests.py x 2 3 3 6 9 6`.
