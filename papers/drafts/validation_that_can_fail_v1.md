# Validation That Can Fail: A Practical Checklist for Quantitative Claims in Self-Published Work

*Status: DRAFT. Filed 2026-10-15. Authors: operator + Claude (Sonnet 5.5).
Written as guidance, not as a critique of any person or work. It names no
one, links no repository, and uses a constructed illustrative claim (§3).
Every number in §3 comes from `validation_that_can_fail_v1/check_threshold_claim.py`
(seeded; output in `output.txt`) and can be reproduced in about a minute.
Same-source caveat: one model-assisted reader. The checklist is a set of
leads to test, not a verdict machine. Tool run 2026-10-15: `paper_rigor` ok (0 gaps);
`verification_lint` ok (0 gaps, after a trial-count false positive was
rewritten to cite the script constant); `attractor_scan` one weak
`goal_post_movement` flag on "not yet" and "as soon as", both read in context
and benign (plain-English uses).*

---

## Abstract

Independent researchers increasingly publish a quantitative claim, a short
script that "confirms" it, and a table of results. The effort is real and the
instinct, to attach a runnable check, is the right one. The failure shape that
recurs is narrow and fixable: the check is built in a way that cannot return
"no." This note gives six patterns, a five-minute test for each, a worked
example with runnable code, and a ten-question checklist. The fixes are cheap,
and they make a claim stronger, not weaker.

## 1. Who this is for

Anyone who has written "run the code yourself and verify" at the end of a
paper, and anyone reading such a paper. The standard here is the one
the claim's own author would want applied: *what result would show I am wrong,
and could my script ever produce it?*

A claim of invariance, stability or "zero drift" is held to this standard
hardest by its own premise. If the thing being asserted is that structure does
not drift, then the paper, the code, the README and the table must not drift
from one another either (§2.4). The most common finding, in practice, is not a
wrong idea. It is an artifact that no longer matches its sibling.

## 2. Six patterns, each with a five-minute test

### 2.1 Defined-by-construction, then "confirmed"
**Symptom.** A quantity is defined so that it equals zero (or one) at the
claimed point, then a table shows it is zero at that point.
**Why it matters.** A definition cannot be evidence for the thing it defines.
**Test.** Strike the defining formula from the argument. Does any independent
measurement remain that shows the point is special?

### 2.2 A validation that cannot fail
**Symptom.** The script prints numbers. It has no threshold, no assertion, no
`PASS`/`FAIL`, and the text says "all results to date confirm."
**Why it matters.** A procedure with one possible output carries no
information.
**Test.** Edit the script so the claim is false (change the generator,
flip the sign). If the output still reads as support, the script was never
testing.

### 2.3 No null process
**Symptom.** The effect is shown under the author's process and nowhere else.
**Why it matters.** Many "thresholds" appear in sequences with no structure at
all. A windowed correlation between the first k values and later windows of a
purely random sequence falls to zero as soon as the windows stop overlapping,
and the *signed mean* of correlations over trials is near zero for any
independent data.
**Test.** Run the identical metric on (a) pure noise, (b) a generic
memory-1 process, (c) a process with the same memory depth but different
structure. If the claimed feature shows up in the null, it is not evidence.
§3 does this.

### 2.4 Artifact drift
**Symptom.** The paper, README, code and results table disagree.
Examples seen in the wild: a text that lists one recurrence while the code
generates another; a README table whose rows contradict the function it
documents; a README falsifier that is stricter or looser than the paper's.
**Why it matters.** Readers cannot tell which artifact is the claim.
**Test.** Pick every number in a table and recompute it from the code and the
stated formula, by hand if necessary. Pick every named object in the paper
("the X family") and find the line of code that makes it.

### 2.5 A falsifier that absorbs counter-evidence
**Symptom.** A disproof clause that ends: "a result that needs a correction
to behave confirms the claim, because the correction was compensating."
**Why it matters.** It converts every counterexample into support.
**Test.** Write down one outcome the clause would classify as refutation. If
you cannot, the claim is not yet falsifiable as stated.

### 2.6 Circular inputs, straw baselines, counted rows
Three small variants of one error:
- **Circular inputs.** A "predicted" column is the reciprocal, or a rounding,
  of the observed column. *Test:* trace each input to its origin.
- **Straw baseline.** The new law is compared with a weak alternative while
  the strongest known one, which may already need no free constants, is
  omitted. *Test:* ask what the best existing law would score on the same table
  (for example, a claim to reproduce orbital distances "without gravitational
  constants" should be compared with Kepler's third law in AU and years, which
  already needs none).
- **Counted rows.** The headline error averages rows that are inputs (a
  baseline set to 1.000, a value copied from the observation, a node placed by
  hand). *Test:* recompute the average over genuine predictions only.

## 3. Worked example: a threshold claim that looks confirmed and is not

**Illustrative claim (constructed; attributed to no one).** For a recursive
sequence with memory depth *k*, the correlation between the first *k* values
and the window ending at step *n* decays to about zero at *n* = 4*k*, and not
before.

The check is cheap to write, so it is common to see only the printed values at
2*k* and 4*k*. Here is how to make the test able to fail
(`check_threshold_claim.py`, seeded, `TRIALS = 2000`, 63 steps):

1. **Fix the rule before running.** *Settle point* = the first *n*/*k* after
   which |mean correlation| < 0.05 for every later step. The claim passes only
   if the settle point is exactly 4.0 for every *k* from 2 to 10.
2. **Run four processes.** A noisy moving average (mean of the last *k* values
   plus small noise), a *k*-step sum (the literal recurrence family, in the
   usual "Fibonacci, tribonacci, ..." sense), pure iid noise (null), and a
   generic memory-1 process (null).
3. **Report the result for each, including the ones you did not expect.**

| process | settle point n/k for k = 2 … 10 | claim holds? |
|---|---|---|
| noisy moving average | 5.00, 4.33, 3.50, 3.40, 3.33, 3.29, 3.25, 3.22, 2.50 | no |
| k-step sum | never for k ≤ 5; 2.17, 2.14, 1.38, 1.33, 1.30 for k = 6…10 | no |
| iid noise (null) | 25.0 (degenerate, see below), 2.00, 2.00, 2.00, 2.00, 1.71, 1.62, 1.67, 1.60 | no |
| memory-1 (null) | 12.5, 12.0, 7.25, 7.80, 6.00, 4.29, 4.25, 3.89, 4.10 | no |

What this teaches, and none of it is about any particular author:

- **The null "decorrelates" first.** Pure noise settles by about 2*k*, once the
  windows stop overlapping. "Near zero by 4*k*" is then true of noise, so it
  cannot be evidence of structure.
- **The settle point moves with k.** Where there *is* a decay, it falls from
  about 5*k* at *k* = 2 to about 2.5*k* at *k* = 10. A single threshold at
  4*k* is not what the data show, and the "not before" half of the claim fails
  for larger *k*.
- **The literal recurrence never decays.** For the *k*-step sum the windows
  converge to one shape and the mean correlation plateaus at a small non-zero
  value at *n* = 4*k* (about 0.15 at *k* = 2, falling to 0.02 at *k* = 10), so a "decay to
  zero" is the wrong description. A table labelled with the family names but
  produced by a different generator hides exactly this.
- **Mean of signed correlations is a weak statistic.** It sits near zero for
  independent noise at every lag. The mean *absolute* correlation per trial
  stays between about 0.27 and 1.0 for every process here, null included, so
  "near zero" in the mean does not mean "independent of the start."
- **k = 2 is degenerate.** Correlation of two points is always ±1; the 25.0
  in the null row is one late excursion, not a finding. Report small-window
  cases but do not read structure into them.

None of this says the underlying idea is worthless. It says *this* test cannot
distinguish it from nothing, and that a better one (a stated threshold, a null,
a per-k comparison, a literal recurrence) is a ten-line change.

## 4. A ten-question checklist before you publish

1. Can the validation script return FAIL? Show the line.
2. Is the pass/fail rule written down before running, with a numeric threshold?
3. Is there at least one null process that should *not* show the effect?
4. Is the quantity you test defined independently of the point you claim is
   special?
5. Does every named family/object in the text correspond to code that
   generates it?
6. Does every table row recompute from the stated formula and code?
7. Does the paper's falsifier match the README's, word for word?
8. Is there a counterexample that the falsifier would count as a refutation?
9. Is the strongest existing alternative in the comparison table?
10. Are inputs, baselines and hand-placed values excluded from the headline
    average?

## 5. What good looks like

Two habits to copy:
- **Say what the result does not claim.** A "what this does not claim"
  section that actually narrows scope (no novelty claimed for the algebra, no
  physical link asserted, an analogy named as analogy) makes a paper easier to
  trust and harder to misquote.
- **Size the claim to the proof.** A small, correct, honestly scoped result
  (an identity, a reuse of an existing tool, a worked example matching a
  textbook value) is a real contribution. It becomes a problem only when a
  larger conclusion is built on top of it as if it had supplied the missing
  evidence. Algebra that holds of the *form* of a structure does not validate
  a *physical* claim about it.

## 6. How to use this with a reviewer

If someone raises a failure like those in §2, the most productive answer is
usually the cheapest one: add the null, state the threshold, publish the
result including the part that did not work. A claim that survives its own
null is worth more than one that was never exposed to it.

## Limits

- Constructed example; its numbers describe the four processes in
  `check_threshold_claim.py` under the stated rule and threshold (0.05; the
  qualitative picture is the same at 0.10).
- The checklist finds leads, not verdicts: a flag is a reason to read the
  artifact, not a conclusion.
- Not a claim about any specific author, repository or paper.
