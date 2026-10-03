# Runner mutation checks (the selftest must fail when the runner is broken), 2026-10-03
Each mutation was applied to a copy of `dn_runner.js` and the nine-system selftest re-run (A1 against the pinned clone). A mutation that leaves the selftest green would mean the selftest is vacuous for that part of the runner.
| # | Mutation | Selftest result |
|---|---|---|
| m1 | Tb change applied at pre_decision instead of post_check | FAILED (A1, A3, A6 change verdict: the TOCTOU cases stop being detected) |
| m2 | defeating/benign changes never applied | FAILED 8 of 8 checked: the unapplied-change rule yields NOT_DEMONSTRATED instead of a verdict |
| m3 | effect observation always false | FAILED 7: every system reads FAIL_UTILITY |
| m4 | order dependence ignored | FAILED (A9 loses ORDER_DEPENDENT) |
| m5 | Tc graded | FAILED 3 (A2, A5, A7 change verdict): the in-flight timing must stay ungraded or a correct system fails |
Harness note: the first background run of m4 stalled because the public guard's HTTP server was kept alive by an open connection at close (the preceding unmutated run also hung once in that session); the A1 adapter now closes all connections, and m4/m5 were re-run after that change. A1 was not otherwise changed.
