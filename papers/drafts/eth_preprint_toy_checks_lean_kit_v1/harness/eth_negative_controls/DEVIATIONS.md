# Deviations: negative controls
1. Smoke run before scoring: `run_controls.py 2` (2 seeds per config, same seeds as the first two of the scored 12) to check the code executes. Output not scored: all classes correct; D1 flagged, D1b not.
2. D1c added after the first scoring pass to test whether the Z-call profile could be spoofed. It is labeled post hoc and is not a prereg prediction.
3. D4 flag rule fixed as: `brute_H` or `count_sat` called from `taylor_decoupled` or `design_at`. The prereg described D4 as "counts calls to the primitives and reports them"; the explicit rule and the Z-call-count column were fixed in code before scoring, and both are reported.
4. Sections 3-5 decoy replaces the decoupled-evaluation loop of `run_system` by textual substitution of its source (`negative_controls/sections_decoy.py`); everything downstream is the real code.
5. The Lean witness for `contract_correct` needed one fix (`show N - 1 < N` before `omega`) after the first compile; statement unchanged.
6. Lean builds ran concurrently and took ~8 minutes (memory contention from four Mathlib imports); no result affected. Package directory ownership was reset to the unprivileged user before the Comparator runs, as for the main kit.
