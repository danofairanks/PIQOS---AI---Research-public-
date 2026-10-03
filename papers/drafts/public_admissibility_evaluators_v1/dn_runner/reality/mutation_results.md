# Reality-mode runner mutation checks, 2026-10-03 (run after Amendment 1)
Each mutation applied to a copy of `dn_reality.js`; the six-system selftest re-run. A mutation that left the selftest green would mean that part of the runner is vacuous.
| # | Mutation | Selftest result |
|---|---|---|
| m1 | sink never enforces the fence | FAILED: S1 and S5 change verdict (the flip after the read stops being caught) |
| m2 | changes never applied | FAILED 4: S1, S2, S5, S6 |
| m3 | accepted effects never counted | FAILED 5 (every system reads FAIL_UTILITY) |
| m4 | order dependence ignored | FAILED: S6 loses ORDER_DEPENDENT |
| m5 | Tr flip applied before the read is served instead of after | FAILED: S2 and S5 change verdict |
| m6 | a benign change bumps the revision | FAILED: S1 (the fence then rejects benign changes: FAIL_UTILITY) |
All six were caught on the first mutated run each.
