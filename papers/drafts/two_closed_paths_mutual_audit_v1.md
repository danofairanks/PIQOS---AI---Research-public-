# Two Closed Paths Auditing Each Other: When a Joint Verdict Adds Independence and When It Does Not

*Status: DRAFT OUTLINE. Filed 2026-10-16. Authors: operator + Claude (Sonnet 5.5). Sections 1-3 and the toy
are written; sections 4-6 are scaffolds with evidence still to be pinned and verified. All cases are
anonymized (Cases A-H); no person, company or repository is named, and no identifying pin is published in
this draft. Numbers in §3 come from `two_closed_paths_mutual_audit_v1/toy_mutual_audit.py` (seeded,
stdlib only, output in `output.txt`, predictions in `PREREG.md` written before the first run).
Same-source caveat: one model-assisted reader and author. Tool run 2026-10-17 (after Cases G and H were added): `paper_rigor` ok (0 gaps); `verification_lint` ok (0 gaps); `attractor_scan` one weak `goal_post_movement` flag on "not yet" in plain-English uses, read in context and benign.*

---

## Abstract (provisional)

Two verification procedures that are each closed (each checks only against artifacts it, its counterpart, or
their shared specification supplied) are increasingly paired so that their joint verdict is offered as
evidence. This note asks when that pairing adds independence. We state four conditions, show with a small
runnable toy that a pair built from one flawed specification agrees on everything the specification talks
about and is jointly wrong exactly where it does not, and outline eight anonymized public-record cases
(three largely positive, two mixed) against the conditions. The contribution is a way to ask the question, not a measured
rate in the wild.

## 1. Definitions

- **Closed path.** A verification procedure whose inputs, expected outputs and pass criteria all derive from
  the same source as the artifact under test (same author, same specification, same model, or same data).
- **Mutual audit.** Two closed paths, each treating the other's output as evidence. Includes a gate and an
  auditor, two vendors' conformance suites, and a generator and a checker from one system.
- **Joint verdict.** A conjunction (both ALLOW) or agreement (verdicts equal) presented as the result.
- **Referent.** Something outside both paths that can disagree with them: real outcomes, third-party replay,
  physical or financial effects, held-out data.

## 2. Four conditions for a mutual audit to add independence

1. **Different failure modes.** The paths must differ in the space where errors live, not only in
   implementation. Two expressions of one specification differ on edge inputs but share every flaw of the
   specification.
2. **A referent outside both.** At least one check whose expected values do not come from either path's source.
3. **A stated claim boundary.** What the joint record covers and what it does not, in words a reader can test.
4. **A check that can fail.** The suite must be able to return FAIL on a defect, and failures are preserved.

## 3. Toy (runnable): what agreement can and cannot show

Setup (fixed in `PREREG.md`): a permission rule with limit 100. Truth allows only finite values in (0, 100].
The shared specification says "allow if value <= limit", which omits zero, negatives and non-finite values.
Verifier A implements it one way; verifier B implements it another way (differs on NaN); verifier B2 is
written from a second specification flawed differently. The operational input mix is stated in advance.

| Result (seed 20261016; referent-draw and repetition counts are the script's constants) | Value |
|---|---|
| Spec-derived conformance suite: pass rate for A and for B | 1.000 and 1.000 |
| Pair (A, B): joint false-allow on referent distribution | 0.1365 |
| Pair (A, B): disagreement rate; classes of disagreement | 0.0602; NaN only |
| Pair (A, B2): joint false-allow; disagreement | 0.0209; 0.1156 (negative, -inf) |
| Detecting the common-mode class with 20 referent draws / 20 spec-derived draws | 0.936 / 0.000 |
| Mutant M1 (A also allows huge values): spec suite detects; joint false-allow before and after; disagreement audit detects | 0.000; 0.1318 and 0.1318; 1.000 |
| Mutant M2 (A wrongly denies small positives): spec suite detects | 0.820 |

Reading (all six preregistered checks pass on the first run; the predictions are close to analytic, so
this demonstrates a mechanism, it is not a discovery):
- A spec-derived suite passes both verifiers by construction, so it cannot reveal a flaw in the
  specification (condition 4 for that suite).
- Agreement between A and B reveals only where their expressions differ (NaN). The class both share, 13% of
  the operational mix, is invisible to disagreement (condition 1).
- Swapping in B2, written from a differently flawed specification, cuts the joint false-allow from 13% to 2%,
  because failures no longer coincide. Diversity must be in the failure space.
- A bug in one verifier can be masked by a conjunction (M1: joint verdict unchanged) yet surfaced by the
  disagreement rate on referent-distributed draws.
- Only a sampler that draws from the operational distribution (a referent) finds the common-mode class
  (condition 2).

## 4. Cases (anonymized; evidence to pin and verify before any claim is made)

| Case | Shape | Evidence tier | Conditions it illustrates |
|---|---|---|---|
| A | Two public codebases (a governance framework and a partner's reference harness) with a documented bilateral integration and a joint conformance record | public repositories; pins held privately | 3 and 4 largely met (explicit claim boundary, preserved FAIL records, dated staging); 2 partly (referent is a wire contract and staging, not outcomes). The paper's most positive example. |
| B | A vendor demonstration where the verifier is authored by the same system that produced the artifact | public blog post and prompts; pins held privately | 1 and 2 unmet |
| C | A self-published validation script presented as the authority for a threshold claim | public repositories and papers; pins held privately | 2 and 4 unmet: no null, no pass/fail rule |
| D | A practitioner recommendation to use an AI system to find and troubleshoot problems with AI systems, with trust in the orchestrating model | public post; screenshot held privately | 1 and 2 untested |
| E | A public technical report documenting a multi-stage model post-training recipe, with stated limits and disclosed discrepancies between its own tables | public report; pin held privately | 3 largely met; 1, 2 and 4 met in some stages and only partly in others (one stage trains and evaluates with different judges and external benchmarks; another uses a reward model that is also used to monitor the benchmark it is reported on). The paper's second largely positive example. |
| F | A public paper and code repository describing a self-improving agent harness in which a language model edits the harness and selects among candidate outputs, with no verifier inside the improvement loop | public paper and repository; pins held privately | 2 and 3 largely met (grading rubric and scores isolated from the improver by a guard; limits stated; a best-of-k control using the same selector); 1 only partly met (the grader is the improver's model or family) and unmeasured. Mixed example. |
| G | A public paper describing a self-improving agent harness for streams of tasks, in which several language-model roles rewrite the harness each cycle and a language-model verifier gates changes before they go live; outcome labels reach the improver only after each task resolves, and the scored outcomes come from external resolutions and benchmark criteria | public paper; pin held privately | 2 and 3 largely met (external, delayed outcome labels; limitations stated, including that its loss terms are not estimated); 1 only partly met (improver, solver, router and in-loop verifier are one model family) and unmeasured; 4 met for the negative results it reports, while the headline comparisons rest on one run per cell, so the check's resolving power against run-to-run spread is unmeasured. Mixed example. |
| H | A public paper describing an evolutionary search in which a language model proposes programs and a separate programmatic evaluator verifies and scores each candidate; the evaluator checks the complete final state exactly on sampled inputs, states a confidence bound on residual failure, separates exact rewrites from changes that spend a stated failure budget, and states its task boundary and the designs it excludes | public paper; pin held privately | 2, 3 and 4 largely met (the evaluator is independent of the proposer and can reject a candidate; claim boundary and statistical bound stated); 1 met in kind (proposer and evaluator fail in different spaces), with a residual common-mode risk in the task specification, input distribution and failure budget, which are author-chosen and shared by both; verification is by sampling with a stated bound, not exhaustive. Positive example. |

Editorial rules for this section: (i) no adverse empirical claim about the counterpart or maker in any
case is published unless it has been verified, pinned and the operator has decided on contact; (ii) the
paper's evidence for what mutual audits cannot show rests on the toy, not on the cases; (iii) credit what
each case does well (Cases A, E and H are chosen because they are good examples; Cases F and G are chosen for their isolation controls and stated limitations).

## 5. Counter-models: when a closed-path pair is fine

- Fully specified, finite domains where the specification is the referent (e.g., an interface contract the
  parties intend to enforce).
- Low-stakes, reversible actions where a shared flaw has bounded cost.
- Pairs whose claim boundary says exactly this and no more.
(OPEN, not yet written: state the cost-of-common-mode argument as an inequality, not an assertion.)

## 6. Positive patterns (what good looks like)

Explicit claim boundary; dated FAIL records kept next to RESULT records; a referent-derived check alongside
a spec-derived one; disagreement rate reported, not only the joint verdict; the check can return FAIL.
(OPEN, not yet written: one worked repair of a mutual-audit design from these patterns.)

## 7. Preregistered claims and status

The toy's six predictions (PREREG.md) all held. No claim about prevalence is made. Open: pin and verify the
cases; literature search on common-mode failure in redundant design and on AI systems judging AI systems,
to be read at primary level before citing.

## Limitations

- The toy is constructed; the numbers describe its stated mix and rules.
- A framework paper: it offers conditions and a demonstration, not a measured effect in deployed systems.
- Eight cases, anonymized, unverified at the claim level.
- This note does not claim any prevalence of the pattern in deployed systems, and does not establish that any specific author, company or repository is affected.
