# What "Verified in Lean" Establishes: Seven Layers, Public Evidence on Checker Failures, and What Remains Unread

*Status: DRAFT. AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn. Evidence as of 2026-11-21; several sources named below change over time (see §8).*

**Disclosure.** AI-assisted (Claude, working under this project's own non-default standard: the operator's instructions, preregistration and primary-source checking discipline; not a vanilla configuration). Object selection, method and release decisions are the operator's. A single reader carried out every reading. Two systems discussed here (a Lean checker and its Rust port) and one result discussed here were produced with Claude models, so the assessor is not independent of part of the subject. Two cross-family readings of excerpts were obtained; both self-reported the same model family, so they are not independent of each other (§5.6). Nothing here asserts that any specific result is wrong; it asks which parts of a "verified" claim rest on which kind of evidence.

## 1. Question and scope

When a result is announced as machine-checked in Lean, which parts rest on software verdicts, which on human judgement, and how much of the apparatus can be trusted? The question became pressing in 2026 because very large formal developments (tens of millions of lines) and AI-assisted proof search both reached public announcements, and because Lean's checker had public soundness bugs in the same year. This draft does not evaluate any mathematical claim. It reads public documentation, public repositories and public data, runs a few small analyses on public data, and states what each piece of evidence does and does not show.

Tiers used throughout: **E1** = read in a public source or computed by the reader from public data; **E2** = the reader's own reading of code or statements (not a proof check); **E3** = inference.

## 2. Seven layers

| # | Layer | Who or what vouches | Evidence type |
|---|---|---|---|
| 1 | The formal statement matches the informal claim | people | judgement; no software check exists |
| 2 | The development compiles | the build | software verdict |
| 3 | The statement actually proved equals an isolated challenge statement (including every definition it uses) | a comparison tool | software verdict, given a trusted challenge file |
| 4 | Independent checkers accept the exported proof | several checkers | software verdicts |
| 5 | The definitions the statement relies on are the intended ones | experts reviewing library definitions; cross-checks | judgement; occasionally a cross-check against an independent formalisation |
| 6 | The checkers do not share a flaw | their independence | only partly testable |
| 7 | A human understands why it is true | people | absent for machine-scale proofs |

Lean's reference manual states the first limit itself: Lean "can establish that a statement has been proven, but not whether it is the intended statement" (Lean reference manual, "Validating a Lean Proof"), and its escalating validation steps (the editor's check marks, the assumption listing, a module replay, then an isolated challenge comparison with several kernels) list their remaining assumptions: the soundness of the logic, the comparison tool's plumbing and sandbox, no flaw shared by every checker, and no human error in the trusted challenge statement.

## 3. Sources

All public. Lean reference manual, "Validating a Lean Proof"; two postmortems on kernel soundness bugs (2026-08-01, 2026-08-24) and a post on shipped verified kernels (2026-10-15), by the Lean project's maintainers; a long explainer on interpreting "checked in Lean" claims and its comments (2026-11-12); the Lean Kernel Arena results file (round of 2026-11-14 to 2026-11-21, repository revision `fdc02ded`) and the arena repository's history; repositories for four checkers at stated commits (con-leche `5ea446d`, con-ron `de06320`, lean4lean `67f63b0`, lean-inductive-models `86caadd`); the community certification and a university verification page for a large Lean proof announced 2026-11-20, and that announcement; arXiv 2606.29493 and its repository (review branch); and arXiv 2611.26300 with its formal statement in the Formal Conjectures repository (main at `d8d031d`; proof commit `af88acbf`).

## 4. Findings from the postmortems and the arena

### 4.1 Checker failures are recent and were found with AI help (E1)

In July 2026 a kernel soundness bug (nested inductive types with phantom parameters) was exploited by an AI-assisted repository that proved a famous conjecture false without `sorry`; it was reachable only by submitting a declaration directly to the kernel and was fixed one hour after the report. The second postmortem describes a three-week hunt (30 July to 20 August) by a vendor's internal models that exploited several further official-kernel bugs and two runtime bugs (a reference-counter overflow that corrupts memory, and a Linux build that bundled an outdated arithmetic library). The post states that groups using publicly available models reported none and that similar exploits "cannot be ruled out." In two cases a second independent checker also accepted the exploit (an old version of one checker for the July bug; the same checker for one August bug), and a port of the reference kernel shared the July bug.

### 4.2 Arena failures are correlated (E1, computed)

For each of the 90 invalid tests in the arena, I counted how many of the 37 checkers wrongly accepted it. Nine checkers wrongly accept at least one; the checkers shipped with Lean (official kernel, nanoda, lean4lean, con-leche, con-ron and an inductives validator) wrongly accept none this round. The overlap statistic S = sum over invalid tests of C(k,2) (k = number of checkers accepting that test) is 46; permuting each checker's set of wrong accepts across the 90 tests (20,000 draws; computed from the arena results file named in §3) gives a mean of 4.2 and a 95th percentile of 8. The six tests accepted by two or more checkers all concern inductive types or recursor rules; the most-accepted (7 checkers, 5 implementation languages) is a nested-inductive recursor rule. The highest pair overlap (Jaccard 0.75) is between a Rust and a Fortran checker with different owners. Implementation language did not predict independence of failure. Limits: the arena's checkers are a volunteer sample; its tests were added after bugs were found, so a clean row says nothing about unknown bugs; one round.

### 4.3 The unseen failure mass is not identified by these data (E1, computed)

Treating each regression test as one failure event, with classes assigned by a fixed keyword rule on the test name, Good–Turing missing mass and Chao1 estimates are 0.03–0.10 and 1.00–1.17 for the coarse classes (11–12 classes), but 0.31 and 1.76 for classes by first name token, 0.63 and 3.14 for first two tokens, and 1.0 when every test is its own class. The estimator's output is set by the granularity choice, not the data. Three observations do not depend on it: new coarse classes appeared at about one per month from September to November (14 tests added after a bulk import); the coarse history predicted a new class with probability 0.06 on average while 3 of 14 were new (0.21); and two classes in the postmortems (runtime reference counting; arithmetic library version in the build) lie outside the kernel's logic and could not be predicted from the logic-class history. Limits: tests are not an i.i.d. draw of bugs; the first-commit date is a lagging proxy; 21 of the 35 tests share one import date.

### 4.4 What a joint paranoid check means (E1, computed; E3)

Against the 90 invalid arena tests, the six shipped checkers' rejection depth is at least 4 of 6 (87 tests at 6, three at 4), at least 2 of 3 lineage groups, and at least one rejecting checker that does not run on the Lean runtime. The three tests at depth 4 are tests the two verified kernels decline. A decline is not a rejection: for those inputs the verified kernels give no verdict. The six checkers form roughly three independence groups (official kernel with its port and the inductives validator; an independent Rust checker; the verified kernel and its derived port), and two groups when the runtime is the weak point (only the independent Rust checker and the Rust port run off it). For all seven soundness-class bugs named in the postmortems, at least one shipped checker rejected the exploit with current versions.

## 5. The verified kernels, read from their own documentation and statements

### 5.1 Documented assumptions (E1)

The consistency proof for con-leche is relative to a set theory with an omega-chain of Grothendieck universes (equivalent in strength to omega many inaccessible cardinals), which Lean cannot prove consistent from inside. Beyond that, its documentation lists 14 assumptions or gaps, mostly at the Lean runtime and bignum library, the reading of files, the export decoder (stated to be "a review claim, not a theorem"), the `.olean` reader ("tested on `Init`, not proved"), modes outside the theorems (`--trusted`), and declines (native-evaluation proofs and a few features). It deliberately accepts more than the official kernel in four ways, so its acceptance is evidence of consistency, not that the official kernel would accept. con-ron, its Rust port, replaces Lean's compiler, runtime and arithmetic library with a translator pair, `rustc` and its standard library as the trusted base, and its human-written README calls it "not a high assurance verification effort"; its parser is verified. lean4lean is derived from the official C++ kernel ("likely shares some implementation bugs"); my count of unfinished-proof placeholders is 14 in its verification directory and 9 in its theory directory, at projections, inductive declarations and structure eta. The inductives validator uses the official kernel as its reference for conversion questions and does not, by default, recheck its input declarations.

### 5.2 The specification surface (E1, E2)

The main theorem is written as a challenge file in which the checker's own functions are placeholders that the proofs fill. The import closure of that file is 55 modules and 12,577 lines (line counts from the con-leche repository at the commit named in §3). The part that defines what "a model" means is small: about 100 definition lines in the set-operator, universe and recursor-rule files I read (1,900 raw lines), and the main statement chain is about 14 statements (capstone, acceptance-to-model, the fold invariant, one mutual induction over the checker's relations with semantic motives that are conditional on the proof point, and eight environment-level inputs). The proof directories I censused (about 9,300 theorems) contain no `sorry`, `unsafe`, new-assumption, `native_decide` or `implemented_by` tokens in the model and semantics directories; the executable code has one reference-count primitive, persistent-marking calls and a few partial loops, each allowlisted by a textual gate with a stated justification. I read no proof bodies.

### 5.3 Documentation versus code (E1)

The overview lists five covered argument shapes; the main-theorem file has ten theorems covering more. A documentation comment names a theorem that does not exist. Two documentation lines overstate the assumed set theory or name `Empty` where the theorem concerns `False`. These are stale-documentation findings, not soundness findings.

### 5.4 An open item for large runs (E3)

The printed theorems fix the argument list; the overview says other flags are not covered. A verification page for a large proof reports a verified-mode run on 64 threads. Whether that command line is literally covered, or whether the proofs treat such flags generically, is unresolved here.

### 5.5 Recursor rules and the proof point (E2)

Recursor rules the checker cannot read give no constraint in the model, but the checker rejects such recursors by design (the documentation says none occur in the standard corpora). The model's "proof point" is chosen so that it collides with no type the construction forms; I found theorems for each construction's strictness (not one global statement). The acceptance chain for `False` is a stated, model-free theorem.

### 5.6 Cross-family readings (E1, E2)

Two excerpt sets (the headline statements; the set operators and recursor-rule reading) were given to a second model family. Both answers self-reported the same family. They converged with my reading on the open items (the single-template meaning of "a theorem of type False"; weakening for placeholders and opaque constants; the flags question; the empty-domain reading; the proof point's design intent) and found no new defect; the first made two reading errors (a claim that a declared assumption does not constrain truth, and reading placeholders in a challenge file as missing proofs). Limits: the excerpts were my selection; one family; two runs.

## 6. The statement layer is measurable and an LLM audit does not find it (E1, computed)

The authors of arXiv 2606.29493 audit five Lean theorem-proving benchmarks and release run summaries and labelled sets. Their Table 4 totals (4,833 findings; 398 "proven"; figures from arXiv 2606.29493 and recomputed from its released summaries) reproduce exactly from the released summaries. The 398 are 199 declarations of an unproved assumption in problem files (all in one benchmark), 98 integer-division truncation cases, 79 counterexamples, 19 modulo cases, 2 vacuous theorems and 1 other; 91.8% of the 4,833 findings are unverified hazard flags. Excluding the declared-assumption pattern, machine-certifiable statement faults are 0–2.8% of problems per variant, a lower bound. Their semantic-audit challenge set is 94.6% positive rows (87 of 92); precision of 0.20–0.30 is about 1.0–1.9 times prevalence and reported accuracies (39–68%) are below an always-negative baseline (78–84%). The paper's text describes the static-warning labelled set as 42 true and 13 false positives; the released file has 21 and 34.

## 7. Two case readings

**A short formal result (arXiv 2611.26300; no-go theorem for photonic GHZ states, found by an AI prover).** I checked the proof by hand and a key lemma on 20,000 random matrices (no failures). The formal statement in the Formal Conjectures main branch matches the manuscript; the proof is not in that branch (the body is a placeholder and a documentation pointer names an earlier commit). On a current Lean toolchain three of the proof's golfed lemmas did not elaborate and I re-proved them myself (599 of 639 proof lines unchanged; only the three standard assumptions in the output); the proof's own pinned environment could not be built here. The paper gives no attempt count for the AI discovery, its "first unconditional proof for every even N ≥ 4" overlaps results listed in its own Table I, and it has no competing-interests statement although co-authors include the prover's and the benchmark's developers.

**A large announced result (a Lean proof of the Riemann Hypothesis, announced 2026-11-20).** The evidence for the mathematical claim is the artefact and its checks, not the four-page announcement, which says its author had not mastered the argument and supplies no attempt denominator; its 20-step timeline was compiled by the AI and is out of order. The community certification (2026-11-21) says all criteria are satisfied; the university page it cites lists two checks (a default-kernel replay of the export and an end-to-end comparator run) as still running, and its time stamp precedes results listed at later times. The scope verified is Dirichlet L-functions, narrower than "the Generalized Riemann Hypothesis" in the announcement. The page's cross-check against an independent formalisation of Robin's and Lagarias's criteria is the one anchor that avoids the library's definition of the zeta function. I did not rebuild the library (about 166,000 modules per the verification page named in §3).

## 8. What to ask of a "verified in Lean" claim, and limits

1. Is the statement isolated in a small file importing only the standard library, and who has read the definition closure it relies on (tens of thousands of declarations for a headline theorem)?
2. Which checkers, at which versions, in which mode, with which arguments, accepted the export; did any decline; are the declines counted as no vote?
3. Are the checkers independent in lineage and runtime, or do they share a runtime, a port lineage or a model family?
4. Was a cross-check against an independent formalisation of the claim, or a hand check of special cases, made?
5. What is the denominator behind an "AI-discovered" claim (attempts, failures, human edits), and where does the proof live (in the tree, or behind a pointer)?
6. Are the logged checks complete at the time of the announcement?

## 9. Limitations: what this does and does not establish

One assessor; classifications by one coder from public text; small samples; one arena round; arena tests are added after bugs are fixed; proof bodies and compiled binaries were not read; the cross-family readings are not independent of each other; same-family bias is possible where the subject is Claude-built. Time-sensitive items: the arena round, the verification page's running checks, the announcement and its certification, and repository commits. They should be re-read before relying on this draft.

**Open items.** Whether a large verified run is literally covered by the printed theorem; the bridge between the proof's own reading of terms and the statement's reading (not read); per-check detail of the extra verification checks; an independent human reading of the specification; a base rate of kernel bugs by other means than the 2026 hunt (not found in any source read).

## Addendum A (2026-11-23): a public explainer after the evidence cutoff

*Status: DRAFT. AI-assisted (Claude), single reader. Evidence for this addendum is one public explainer and workshop write-up dated 2026-11-23, two days after this draft's evidence cutoff, read from a pasted copy. Everything it says about third-party reports (checker runs, logs, a certification statement, maintainers' postmortems) is its own account; those sources were not re-read here.*

**A.1 Timing of the §7 items.** §7 records two checks on the cited verification page as still running at the cutoff. The explainer reports that the certifying parties' comparator run and four independent checkers accept the proof, and that a third party's sandboxed build reproduced the published export byte for byte. If those reports are accurate, §7's "still running" is out of date. This draft has not read the logs; the sentence in §7 should be replaced by a reading of them, not by the explainer's summary.

**A.2 The independence argument.** The explainer argues that a false proof would have to fool every checker "in the same way", and that this is "small enough that beyond reasonable doubt means something precise". That rests on the checkers being independent samples of failure. §4.2's computed overlap (statistic 46 against a permuted mean of 4.2 and a 95th percentile of 8) and §4.4's grouping (about three independence groups among the six shipped checkers; a verified kernel and its derived port form one lineage) show they are not independent samples in the arena data. Neither result says the chance of a joint failure on a given proof is large. §4.3 says the data do not identify a rate, and the explainer gives none. What its account of last summer's bug does support is narrower: that exploit needed two separate implementation errors in two checkers.

**A.3 "Read the twenty lines".** The explainer says a reader needs to read only the few lines that state the theorem, because the statement is the library's own definition and the library is curated. This draft's layer 3 and §8 question 1 ask who has read the definition closure the statement relies on. The two positions are compatible when the statement uses only curated library definitions: then the open question is whether anyone has read that closure, not whether the headline lines are readable. The explainer's own list of human skills (reading the statement, knowing which statements to trust, running the checks) matches layers 1, 5 and 3 here.

**A.4 What the explainer adds that this draft lacked.** A short worked list of conventions that make a Lean statement differ from its informal form (natural-number subtraction truncates; division by zero is defined to be zero), and a sandboxing warning for running unreviewed Lean code. Both are consistent with §6 and §8 and could be cited there.

**A.5 Limits of this addendum.** One reader; one explainer; no logs opened; same-family caveat (the explainer reports that the proof and one of the checkers were produced with Claude, and this draft is AI-assisted by the same model family).

**A.6 A contrast case: a kernel-checked Lean package whose theorems are not the advertised ones.** This project's own case study of a published claim to have solved the six remaining Clay Millennium problems (AIX Global, paper dated 2026-08-30; downloadable Lean 4 package; [`2026-09-03_aix_global_millennium_lean_proof_claim.md`](../../case_studies/2026-09-03_aix_global_millennium_lean_proof_claim.md)) is a useful negative control for the layers in §2 and for the explainer's four tests in A.1 to A.3. As read in the case study (one reader plus two outside reviewers, authorship method not established): the package compiles; the package's own certificate reports no `sorry` and no project-specific assumptions, which the case study finds literally true; three of the six headline theorems (Hodge, Navier-Stokes, Birch and Swinnerton-Dyer) prove the same statement, `0 < n + 1`, which is not any of those problems; two more (Riemann Hypothesis, P versus NP) are real conditional theorems whose decisive hypotheses are never supplied; the named "closed final" theorems and certificate identifiers that the paper says carry the result do not appear in the published package. The kernel accepts every term in it, because every term is a correct proof of its own stated type.

The comparison with the RH case in §7 and A.1 is therefore structural, not a statement about the merits of either proof:

| Layer (§2) | AIX Global package (case study) | RH proof (§7, A.1; as reported, logs not read here) |
|---|---|---|
| 2 compiles; assumption listing shows only standard assumptions | passes; no `sorry`, no project-specific assumptions | reported to pass |
| 4 independent checkers accept the exported proof | the package is kernel-checked in its own build; independent checkers were not run here, and acceptance is expected because each term proves its stated type | reported to pass (the explainer names four checkers) |
| 1 stated type is the claimed theorem | fails for three theorems; conditional on unsupplied hypotheses for two | the statement is the library's own definition, per the explainer |
| 3 proved statement equals an isolated challenge statement | no challenge file; the identifiers the paper cites are absent | a comparator run is reported |
| 7 a human understands why | absent | absent (§2) |

What separates the two is not layers 2 or 4. The assumption listing and checker acceptance are reported to look the same in both, which is why neither can substitute for layers 1 and 3. The case study's outside reviewers name the failure "local correctness without global target fidelity", and the companion draft [`register_dressing_v1.md`](register_dressing_v1.md) (Addendum of 2026-09-22) reads the same pairing from the register side: a verifier checks internal consistency, and does not check whether the stated target is the advertised one. One refinement the Lean pipeline adds to that reading: the kernel does not bind the target, but a comparator against a trusted challenge statement is built to (layer 3), which is why §8 question 1 asks for the isolated statement file and who has read its definitions.

*Limits.* One case, one reader plus two outside reviewers quoted in the case study; the case study states it does not establish intent or authorship method and does not check the proprietary computation the paper describes; the contrast is not a predictor of which packages merit review, and it makes no claim about the RH proof beyond which layers its reported checks address.

## Appendix A. Preregistration and replication material

For each computed analysis (§4.2, §4.3, §4.4, §6), the operator's working notes contain a prediction file committed before the analysis ran; commit ordering is recorded in version history. Hit/miss tallies are not reproduced here because they were scored by the same single reader who wrote the predictions.

Scripts and derived outputs for §4.2 and §4.3 are in `lean_verification_layers_v1_replication/` (README there states limits). The 2026-11-21 raw results file was not retained; a rerun of the §4.2 script on the 2026-11-22 file gives an overlap statistic of 43 against a null mean of 4.45 (46 and 4.22 as quoted in §4.2). §4.4 and §6 scripts are not yet released, so those figures remain reader-reported computations.

## Sources and provenance

Sources are those listed in §3 (public documents, repositories at the stated commits, and arXiv 2606.29493 and 2611.26300). Computed figures are the reader's own recounts of public data; scripts for §4.2–§4.3 are in the replication folder and those for §4.4 and §6 are not yet released (Appendix A). Primary-source verification: every number above was read or computed by the reader from the named source; none is taken from a secondary summary.
