# Does a Second Formalisation Catch the Silent Reading? A Small Measurement of Translator Divergence on Boundary Statements

**Draft v1 for review. Not peer reviewed; may be revised or withdrawn.**

**Scope of naming.** Two model families are named as products (OpenAI's ChatGPT, Anthropic's Claude) because the comparison is between them; no individual is named. Short sentences are quoted from the public documentation of open-source projects (the `CAGE` repository documentation and the docstrings of five rate-limiting libraries) only as test inputs; no vulnerability or defect in any of those projects is claimed here.

**Disclosure.** Drafted with AI assistance. One of the four "arms" below is the drafting model itself, working in a session with a project instruction file and operator preferences loaded; it also wrote most of the test items, so it is the least independent arm. The other arms were run by the operator in fresh chats and pasted back. Everything reported is a count over small item sets; no confidence intervals are claimed.

## 1. The question

A model that translates a plain-language statement into a formal one makes small choices (is "between 5 and 20" inclusive, is "up to 10" a bound with no lower limit) and a checker then verifies only the formal statement. A recent paper on autoformalisation of mathematics (arXiv 2610.08144, read in part for this note) argues that a formal proof that compiles does not show the plain-language claim was translated faithfully. This note asks a narrow, measurable version of that worry: if a second, independent translation is produced and the two are compared by an exact entailment check, how often do they differ, what kinds of difference does the comparison find, and what does it miss?

## 2. Method

**Items.** Short statements, each with a fixed argument list and a one-line context defining the variables (disclosed: this context can cue a reading). First test: 6 statements. Batch 1: 24 (18 boundary or scope items, 6 explicit controls). Batch 2: 18 (10 sentences taken verbatim from third-party documentation, 2 controls, and a six-wording "ladder" for one cap rule). Batch 3: 9 sentences from library docstrings with an executable oracle (below).

**Formalisation schema.** Each translator returns one SMT-LIB `define-fun spec ... Bool` over integer arguments, plus a free-text ambiguity note ("no", or an alternative reading it did not choose). Nothing a translator returns is executed; the checker parses exactly one `define-fun`.

**Checker.** For two formalisations the checker asks the SMT solver (Z3) whether one entails the other in each direction. `unsat` is a proof of entailment, `sat` is a concrete counterexample; both directions give: equivalent, one stronger, incomparable. Items where a formalisation was malformed are recorded as invalid and are not counted as divergences. Self-tests on constructed pairs pass; one expected result in the self-test was wrong on my side and the checker was right (recorded in the companion files).

**Arms.** A: the drafting model (non-blind). B: a fresh ChatGPT session. C: a fresh Claude chat (account preferences or memory possibly active; not verified). D: an incognito Claude chat. Not every arm ran every test.

**Preregistration.** Predictions with probabilities were committed before each batch's outside replies existed. Misses are reported. Two post-hoc steps are labelled where used: a domain normalisation (section 3.3) and a script fix for classification (section 3.4).

## 3. Results

### 3.1 First test (6 statements, arms A and B)
Five of six pairs were equivalent. The sixth, "between 1 and 10", differed (A exclusive, B inclusive); B reported no ambiguity on it. I had predicted two or more divergences; there was one.

### 3.2 Batch 1 (24 items; arms A, B, C, D)
Divergent items among valid ambiguous items (controls: 0 of 6 in every pair):

| pair | divergent / valid ambiguous items | items |
|---|---|---|
| A-B | 5 / 17 (B02 invalid) | between, and/or precedence, "at most two positive", "consecutive", "greater by no more than 3" |
| A-C | 2 / 18 | between; "greater by no more than 3" |
| A-D | 2 / 18 | same two |
| B-C | 3 / 17 | and/or precedence; "at most two positive"; "consecutive" |
| B-D | 3 / 17 | same three |
| C-D | 0 / 18 | none |

Of the five divergent items, four are reading choices and one is a translation error: arm B rendered the statement that at most two of a, b and c are positive as at least two being non-positive, which means at most one positive, and reported no ambiguity. The author arm (A) was an outlier on two items, partly through its own inconsistency: it made the word between exclusive in two items and inclusive in the negated third. All four arms read a cap rule with negative amounts as the plain signed sum.
Self-reports (the ambiguity notes) as a divergence detector over the five divergent items: C flagged 13 of 18 items and covered 4 of 5; D flagged 8 and covered 4 of 5; B flagged 6 and covered 2 of 5. No arm flagged the one error.

### 3.3 Batch 2 (18 items; arms A, B, C, D)
Counted as pasted, ChatGPT's replies diverge from the Claude arms on most items because it adds domain guards (counts and durations at least zero, flags in {0,1}); four of its forms lacked one closing parenthesis and are excluded. After a **post-hoc** shared domain assumption (counts and durations non-negative, flags zero or one), the remaining reading divergences are: "pool 2, reserve 1" (exact in B and C, upper bound in A and D) and "not acknowledged within 4h" (strictly greater than 4 in A and B, at least 4 in C and D). The two blind Claude chats differ on one item (the first). Controls: 0 divergences after normalisation.

**Cap ladder.** One rule written six ways (K0 baseline; K1 "capacity consumed ... never exceeds"; K2 plus "Consumed capacity is never given back"; K3 plus "A negative amount restores no capacity"; K4 explicit net sum; K5 explicit sum of positive amounts). Intended readings were declared before the replies: gross consumption for K1, K2, K3, K5.

| item | A | B | C | D |
|---|---|---|---|---|
| K0 | net total | net total | net total | net total |
| K1 | net total | net total | prefix sums | prefix sums |
| K2 | gross | prefix sums | gross | gross |
| K3 | gross | gross | gross | gross |
| K4 | net total | net total | net total | net total |
| K5 | gross | gross | gross | gross |

No arm read K1 as gross, the declared intent; four of four arms read it as a net reading (two different ones). Gross appeared at K2 in three arms and at K3 in all four.

### 3.4 Flagged alternatives (re-analysis; no new runs)
Question: do the ambiguity notes name the readings other arms chose? A fixed keyword rule (committed before running) maps each note to named readings. Recall, counted as "another arm chose reading X; did this arm's note name X":

| arm | batch 1 (held out from the observation that prompted the test) | batch 2, domain-normalised |
|---|---|---|
| ChatGPT | 0 / 8 | 0 / 9 |
| fresh Claude | 4 / 4 | 6 / 7 |
| incognito Claude | 4 / 4 | 7 / 7 |

On K1 both Claude arms named *negatives restoring nothing* (the intended gross reading) as the alternative they did not choose. No note covered the translation error. The classification step was changed once after the first output (a domain-normalised mode for two items); both outputs are in the companion folder. The *precision* metric preregistered for this test did not work: the reading space contained almost only readings some arm chose, so every named reading counted as chosen, except the intended K1 reading, which the metric penalised.

### 3.5 Batch 3 (9 sentences, executable oracle)
To avoid choosing an intended reading after seeing answers, nine sentences were taken from library docstrings (for example "Raises ValueError if amount is not a number between zero and max_rate, inclusive", "Acquire an entry if the weighted count of the current and previous windows is less than or equal to the limit"), and the intended reading was defined as the libraries' observed behaviour on small integer domains (every item's table matched a simple rule). Arms B, C and D all matched the oracle on 9 of 9; arms C and D produced identical formalisations. With explicit variable roles the batch did not discriminate. No claim is made about bare text.

## 4. What this does and does not establish

This note does not claim a divergence rate for translators in general, does not establish which reading of any statement is correct, and does not claim that agreement between two families is verification.

- A second independent formalisation plus an exact entailment check finds both reading choices and outright translation errors, with no false divergence on the explicit controls once domain guards are handled. It cannot tell the two kinds apart on its own.
- Whether a second family finds more than a second same-family pass is not settled. Batch 1 gave 3 of 17 (cross-family) against 0 of 18 (blind same-family); after normalising, batch 2 gave 1 to 2 of 10 against 1 of 10.
- A reading every arm shares is invisible to divergence: the cap rule's signed-sum reading, and K1.
- Self-reported ambiguity is an incomplete detector. In the two Claude arms it covered most reading divergences while flagging many items that never diverged; in the other arm it flagged almost everything, or the wrong things.
- Where an arm's notes named the alternative reading, formalising each named alternative and checking what the chosen reading implies is a candidate route to surface shared under-reads. This was not run as a pipeline.
- The drafting model, which wrote the items, was the outlier on several divergences and inconsistent on one phrase: an author-written baseline is not a safe reference.

## 5. What would count against this

(1) A batch with a human-declared or executable intended reading in which the entailment check against a second family shows no divergence and the flagged alternatives also fail to contain the intended reading while all arms mistranslate: the method would then be shown blind to exactly the failures it is meant to catch. (2) A third model family that collapses the cross-family divergence to the same-family level on a fresh item set written by someone else. (3) A reanalysis of the flagged-alternatives recall with a reading space not derived from the arms' own choices that falls well below the figures above. None of these has been run.

Predictions that missed: more divergences than occurred in the first test; ChatGPT's reading of one cap wording; the divergence rate difference after normalisation; a prediction that library-documentation sentences would produce some non-oracle readings (they did not); the preregistered precision metric.

## 6. Limitations

Small item sets mostly written by the drafting model; one sample per arm; two model families sharing much training data; chat-level state (preferences, memory) for one arm unverified; the item contexts may cue readings (batch 3's did, apparently); equivalence is over the SMT encodings and a small integer domain for the oracle; the domain normalisation and one classification fix are post hoc; arm A was not blind; the second arm family was run by hand in a chat interface, so format failures (invalid JSON, one missing parenthesis) are part of the data. External sentences' true authorial intent is unknown (one reads as probably inverted).

## 7. Reproduction

All inputs, raw replies, scripts and outputs are in the companion folder `second_formalisation_divergence_v1/` (see its README). The checker needs `z3-solver`; the oracle script additionally needs the five probed libraries.

## References

Sources: [1] A. Bastounis, F. Circelli, A. C. Hansen, "Navier-Stokes lost in translation", arXiv 2610.08144v1 (October 2026); sections 1 to 4 and the start of the appendix read, the rest not read. [2] The companion folder's files (prereg, stimuli, replies, scorers), as listed in its README. [3] L. de Moura and N. Bjorner, Z3: An efficient SMT solver, TACAS 2008; known, not re-read. [4] C. Barrett, P. Fontaine and C. Tinelli, The SMT-LIB Standard: Version 2.6; known, not re-read. [5] The public documentation and docstrings quoted as test inputs: the `CAGE` repository documentation and the aiolimiter, limits, pyrate-limiter, token-bucket and ratelimit libraries as installed in October 2026.

## Revision log

- *2026-10-08, v1.* First version.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
