# Live-probe runner mutation checks, 2026-10-03
Each mutation applied to a copy of `live_probe.mjs`; the selftest (15 checks, loopback stubs only) re-run. Each was caught by exactly the check intended, and by no other.
| # | Mutation | Check that failed |
|---|---|---|
| m1 | controls gate disabled | non-discriminating controls stop the run after four calls |
| m2 | host allow-list disabled | a host off the allow-list is refused |
| m3 | the key added to the transcript | the key appears nowhere |
| m4 | abort on non-2xx disabled | the first non-2xx aborts the run, with no retry |
| m5 | spacing floor disabled | spacing under 5 s on the real host is refused |
| m6 | authorization reference not required | live without an authorization reference is refused |
Harness note: the selftest's own key-leak assertion was first written so that it could not fail (an `||` made it vacuous); it was rewritten before these mutations to test the transcript file, stdout and stderr directly.
