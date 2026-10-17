# Theorem 1 mechanical check — results (2026-10-17)
Script `theorem1_check.py`, preregistration `PREREG.md` (sha256 b0ea0b83acbe72b6db64b66d98dc08fcc483511eac445ed1bfddbf94b0d201d7, written before the script), raw output `theorem1_check_output.txt` (preregistered reading C) and `theorem1_check_output_readingB_posthoc.txt` (post-hoc variant). Seed 20261017, N = 400,000 random finite worlds per reading (22 and 24 skipped for the derivation cap). The script was edited once after the first run, only to add the reading flag; reading-C numbers are identical before and after.
Same-source caveat: single Anthropic-model reader/coder; the formalization of Defs 3-13 is mine. Small random structures (at most 12 nodes) are a test, not a proof.

## Scorecard against the preregistered predictions
| Prediction | Result (reading C) | Held? |
|---|---|---|
| P1 all five premises hold => no counterexample | 204,984 worlds, 0 counterexamples to PASS => SemInd=1 and FAIL => SemInd=0 | yes |
| P2 non-vacuous | PASS 9.9%, FAIL 29.7%, UNRESOLVED 60.5%; under UNRESOLVED SemInd=1 in 69,879 and SemInd=0 in 54,094 (so "no semantic conclusion follows from UNRESOLVED" is non-vacuous) | yes |
| P3 only (iii) violated => PASS counterexamples | 613 of 10,590 | yes |
| P4 only (iv-NO) violated => PASS counterexamples | 2,077 of 17,529 | yes |
| P5 only (iv-YES) violated => FAIL counterexamples | 4,748 of 30,063 | yes |
| P6 only (v-wit) violated => FAIL counterexamples | 3,094 of 4,710 (every FAIL in that class is a counterexample) | yes |
| P7 only (v-route) violated => none | 0 of 13,375 | yes (by construction under reading C; see below) |
| P8 only (ii) violated => none | 0 of 44,025 | yes |
| P9 only (i) violated => none or n/a | 0 of 19,954 | yes |
Nine of nine held. No prediction failed.

## What this shows
1. **Theorem 1 holds as stated** on 205k random worlds satisfying its premises: no counterexample in either direction. The proof's structure is sound for the implications it claims.
2. **Four of the listed premises do the work; the rest are idle for these two implications.**
   - Load-bearing (removing each alone produces counterexamples): rule soundness (iii) [or, see 3, route completeness], NO-label correctness (PASS direction), YES-label correctness (FAIL direction), and witness-closure soundness WClosed => WComp (FAIL direction).
   - Idle for the stated conclusion: (i) normal form, (ii) current-support audit soundness, and one of {(iii), RouteClosed => RouteComp}. (ii) is used by Corollary 1 in the paper (not tested here).
3. **Redundancy between (iii) and route completeness depends on how RouteComp is read.** Reading C (preregistered; RouteComp is an ontic attribute not tied to truth values, as the text's "distinct premises" suggests): the route half of (v) is idle and (iii) carries PASS => SemInd. Reading B (post hoc; RouteComp means the route carries q): the isolated (iii) class has 0 counterexamples (10,883 worlds) and (iii) becomes idle, while violating the route half is no longer separable from (iii) (class n = 0). Either way, for this conclusion, one of the two is redundant; the paper says the proof uses both.
4. **The load-bearing premises are the audit facts.** Label correctness (both directions) and witness-closure soundness are the epistemic inputs the paper elsewhere calls regime-supplied ("externally supplied"; no universal procedure for WComp). The theorem is a soundness lemma: audits correct => conclusions correct. In worlds where those fail, the mechanical consequences are concrete: a wrong NO label gives a false PASS, and a wrong YES label or an unsound witness certificate gives a false FAIL (the smallest counterexamples found have 4 nodes each; they are printed in the raw output). That is the failure mode the paper's Limitations 2-3 already name.
5. **FAIL needs the coverage certificate.** In the class where only the witness certificate is unsound (WComp = 0, WClosed = 1), 3,094 of the 4,710 worlds are false FAILs and the other 1,616 stay UNRESOLVED; with a sound certificate, a world with WComp = 0 cannot be certified FAIL at all (that is premise (v)). Worlds whose root survives only through an omitted route are where WComp = 0, so the negative-closure burden is not decoration.

## Limits
Finite, small, randomly generated; one formalization of the definitions (mine) with the RouteComp ambiguity above; the generator's violation knobs were chosen by me and may under-sample the cases an adversary would build; derivations capped at 300 records per world; Corollary 1/2 and Proposition 1 not tested; the check says nothing about whether the premises can be established for any real lineage (the substantive gap).
