# Reading a Persuasion Study Against Its Own Numbers: "AI Can Persuade People to Take Political Actions", Its Preprint, and Its Public Data

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** The object examined is one published article, "AI can persuade people to take political actions" (PNAS 123:e2611368123, 2026, as printed on the copy read), its arXiv preprint (arXiv:2604.09200v1, "Artificial intelligence can persuade people to take political actions", 10 April 2026), and the public data release that accompanies it, named by its repository path, `kobihackenburg/AI-action-persuasion`, at commit `d7025d1`. The authors are called "the authors". No intent is attributed to anyone.

**Disclosure.** Drafted with AI assistance; one reader, an AI system. The predictions in section 4 were fixed after the title, metadata, Significance statement and first three abstract sentences were seen, so P1 to P3 were partly informed by that opening. The published article is a later version than the preprint, and the publisher refuses automated fetches, so most of this draft rests on a copy supplied to the reader on 2026-10-22 that is not stored here; section 2 states exactly what could and could not be re-checked.

## 1. The question

Two preregistered experiments on an online panel (UK adults; 8,000 and 9,950 analysed) had chatbots try to persuade people to sign a real petition and give money to its sponsoring charity, against a control chat about a neutral topic. The paper reports that petition signing rose by 12.8 and 19.7 percentage points, and that the conditions that moved attitudes were not the ones that moved behaviour. This note asks what the printed numbers support, and, using the public data, how much of the headline is carried by who the participant already was and by whether the chatbot asked.

## 2. What was read, and how verified

- **The published article** (main text, 9 pages), supplied by an operator on 2026-10-22; sha256 begins `fbcb1aae409d4700`. The Supporting Information was not read. **This copy could not be re-fetched** (the publisher returns an access-denied page to automated requests), so findings that depend on its wording alone are marked *unresolved* in section 6.
- **The preprint** (arXiv:2604.09200v1, sha256 `4d97c742…b17d`) was fetched on 2026-10-26 and its text layer searched (`paper_checks.py`). Everything the preprint shares with the article is E1 today: sample flows (8,412 - 339 - 73 = 8,000; 10,317 - 301 - 66 = 9,950), the two headline effects, the printed condition-level correlations and their p-values, the Wald test, the preregistration statement, and the quoted wording of the abstract and the Figure 3 title. Strings the draft attributes to the published article that do **not** occur in the preprint are listed in `paper_checks_output.txt` (for example the 25.2% and 21.1% control rates, the information-prompt standardised effects of +0.19 and -0.04, and the phrase "the act of being asked").
- **The public data** were read earlier (2026-10-22) from a read-only clone made with the operator's approval; summary statistics only, no participant-level data stored. `repo_check/analysis.py` was **not re-run** in this pass, because a fresh clone of a third-party repository needs a fresh approval.
- **Unresolved without the published article** (these strings are not in the preprint and could not be re-checked): the control signing rates of 25.2% and 21.1% and the treated rates of 37.8% and 40.4% as printed in the article (the public data give the same figures, section 6); the information strategy's standardised effects of +0.19 SD on attitudes and -0.04 SD on behaviour; the article's sentences that the act of being asked drives behaviour more than message framing and that the information strategy asked least; the sentence on limited scalability outside a paid survey; and the article's "62 to 94%" range for ask rates (the data give 61.5% to 92.7%). Findings 3 and 5, and the information-strategy part of finding 1, depend on them.
- Evidence classes: **E1** executed (`checks.py` on numbers printed in the main text; `repo_check/analysis.py`); **E2** read; **E3** interpretation.

## 3. What the paper reports

Real UK petitions (eight in the preprint), a control chat on a neutral topic (fluoride, recycling, antibiotics or artificial sweeteners), several frontier models told to persuade, behavioural outcomes (signing, switching or keeping a donation, a clicking task) and attitude outcomes. Signing: +12.8 pp (Study 1), +19.7 pp (Study 2). Condition-level effects on attitudes and on signing are reported as uncorrelated (r = 0.05, n = 15; r = 0.18, n = 8). An information-heavy strategy moved attitudes (+0.19 SD) but not behaviour (-0.04 SD). Eight strategies moved signing within +16.2 to +23.7 pp; a combined "Mega" prompt was highest.

## 4. Predictions scored

| P | Prediction | Result |
|---|---|---|
| P1 | Behavioural effects at most 5 pp | **Missed.** +12.8 and +19.7 pp (observed 12.6 and 19.3). |
| P2 | The information result is a non-significant contrast | **Missed.** The pooled individual-level estimate is significantly negative on behaviour with a confidence interval excluding positive values. The weakness is elsewhere (finding 3). |
| P3 | Significant-versus-nonsignificant reasoning across outcomes | **Partial.** The attitude/behaviour contrast is made by correlating condition effects (n = 15, 8) and by comparing r = 0.87 with r = -0.15; no direct test of the difference is shown in the main text. An individual-level and a mediation analysis (SI) are also reported. |
| P4 | Neutral-chat control; no static or human comparator at the behavioural stage | **Held.** Comparison with other modalities is a literature review in the SI. |
| P5 | Low-cost actions, stated in limitations rather than the title | **Held.** Paid-survey attention, "relatively low" cost behaviours, money from an endowed bonus. |
| P6 | Repeat participation handled | **Not scored.** 17,950 responses from 14,779 people (3,171 implied repeats); the main text does not say how the two studies were de-duplicated or clustered. |
| P7 | Opt-in panel, in-session behaviour | **Held.** Panel pay about £12 an hour, behaviour at the end of the session, no follow-up. |
| P8 | Intervals, multiple-comparison correction, model-adjusted headline | **Held.** 95% intervals; Benjamini-Hochberg in Study 2; adjusted 12.8 and 19.7 against observed 12.6 and 19.3. |
| P9 | At least one abstract or conclusion statement the paper's own numbers cannot support | **Held.** Finding 1. |
| P10 | Preregistration and data linked | **Held.** AsPredicted (Study 1) and the Open Science Framework (Study 2); code and anonymised data on GitHub. |

Tally: 6 held, 1 partial, 2 missed, 1 not scored.

## 5. Findings

Each carries its verification status: **V** = the numbers or wording occur in the preprint and were re-checked on 2026-10-26; **U** = rests on the published-article copy or on the earlier data check and could not be re-checked today.

1. **"Uncorrelated" is not supported by n = 15 and n = 8 (E1; V for the numbers, U for the heading).** The abstract says "no evidence of a correlation", which is accurate; the preprint's Figure 3 title and the article's heading and Discussion say the effects "are uncorrelated". The 95% intervals for r = 0.05 (n = 15) and r = 0.18 (n = 8) are [-0.47, 0.55] and [-0.60, 0.79]; the smallest |r| detectable at 80% power is 0.67 and 0.85. Condition effects are also noisy (per-strategy standard error of the signing effect about 1.8 pp against an observed spread of 7.5 pp; implied reliability about 0.5), which pulls an observed r toward zero by a factor of about 0.65 even if the true correlation were high (rough, E3). The individual-level analysis answers a different question: whether one prompt helped attitudes and not behaviour, not whether effects co-vary across conditions.
2. **The Figure 3 panel shows r = 0.44 and 0.63 for another behaviour (E1; V).** Learning against organisation-directed behaviour is r = 0.44 (n = 15, p = 0.10) and r = 0.63 (n = 8, p = 0.10), recomputed. The text reports only the petition-signing correlation (-0.15, -0.16) as "behaviour".
3. **The control never asks; the treatment almost always does (U).** In the public data (section 6, R2) the control conversations contain an explicit request to sign in 0.1% of cases and treated conversations in 84.4%, from 61.5% to 92.7% by strategy. The article is read as saying that "the act of being asked" drives behaviour more than message framing, and that the information strategy asked least; those sentences are not in the preprint and could not be re-checked. If so, the headline contrast cannot separate "AI persuades" from "a chat agent asked", and the information-versus-behaviour dissociation is confounded with ask frequency. No non-AI "ask" arm exists in the experiments.
4. **"Narrow band" for behaviour against "order of magnitude" for attitudes (E1, with a flagged assumption; V).** The ratio of extremes is 12.5 for attitudes (0.25 / 0.02, a near-zero denominator) and 1.46 for signing (23.7 / 16.2). In a common unit (binary SD about 0.48 at p about 0.36, an assumption), the signing spread of 7.5 pp is about 0.16 SD and the attitude spread about 0.23 SD, a ratio of 1.5, not ten. The test of differences across strategies on signing is significant (Wald chi-square(7) = 22.42, p = .002) while the preprint's text says all eight strategies produced effects "within a relatively narrow range".
5. **The baseline is high and the setting is a paid survey (E1 from the data; U for the paper's wording).** Control signing is 25.2% and 21.1% (public data, R1), inside a paid study. The article is read as noting limited scalability outside a paid survey and as comparing with canvassing and other field effects through an SI review with "considerable" heterogeneity; the preprint mentions canvassing but not the scalability sentence.
6. **The abstract picks the larger of two studies (V).** "+19.7 percentage points" is Study 2; Study 1 is +12.8. Both are stated in the body. Disclosed; not counted as a mismatch.
7. **Arithmetic that holds (E1; V).** Sample flows reconcile (attrition 4.03% and 2.92%); the printed p-values for the correlations recompute (for example r = 0.05, n = 15, p = 0.86 against 0.85; r = 0.18, n = 8, p = 0.67 against 0.68); observed and adjusted effects agree within 0.4 pp; the clicking-task result is driven by one petition and disappears when it is excluded.

Counted for the mismatch rate defined in `scientisttwo_release_reading_v1.md` section 4: one, finding 1 (type b, cannot support). Not pooled with the generated-paper rates there: a different genre (a published, human-written article).

## 6. The public-data check

Preregistered before any outcome statistic was computed (`repo_check/predictions_fixed_2026-10-22.md`); R9 to R11 were added afterwards and are post hoc. Transcripts in the release are redacted, so turn-level behaviour cannot be coded, only proxies. Splits by ask, rating or length are observational because those variables are measured after assignment.

- **Scope.** These participants were paid, task-intent respondents asked to chat and optionally sign. Their declining is ordinary non-compliance, and the model was instructed to persuade. Nothing here bears on other populations or intents.
- **R1 to R8: 7 held, 1 partial, 0 missed.** Replication (S1 25.2% against 37.8%, diff 12.6; S2 21.1% against 40.4%, diff 19.3). Control ask rate 0.1%, treated 84.4%, 61.5% (information-issue, lowest) to 92.7% (Mega, implementation intentions); the article says 62 to 94%. Among treated in Study 2, ask against no ask: 43.6% against 22.9%, but the no-ask treated were **not** above control (22.9% [20.7, 25.3] against 21.1% [19.3, 22.9]), the one preregistered miss inside R3. By number of asks: 0: 21.2%, 1: 35.5%, 2: 46.1%, 3: 49.0%, 4 or more: 39.1%. Effect among prior supporters against others: 15.2 against 6.6 pp (S1), 22.9 against 10.8 (S2); strong opponents 2.5 and 5.1. Signed given wants-to-sign is similar in control and treated (73.5/69.9 against 78.7/75.2); the effect sits in "wants to sign". Perceived bias is higher among non-signers and opponents.
- **Post hoc (R9 to R11).** Prior supporters are 72.4% and 73.3% of the sample and contribute 11.0 of 12.8 pp (86%) and 16.8 of 19.7 pp (85%). Without an ask the uplift over control is about zero for opponents and 6 to 7 pp for neutral and supporters. The model asked opponents less (no-ask share 24.7% against 13.4% for supporters), so whether an ask occurs is partly a function of the user's stance, not randomised.

**Reading (E3).** About 85% of the headline comes from prior supporters, and treated opponents sign at 5 to 8%. The treatment lifts "wants to sign" far more than it changes follow-through. The ask is the second large factor: treated participants who were never asked sign at about the control rate. Because asks are not randomised and are made less often to opponents, "the ask causes signing" and "receptive users get asked" cannot be separated with this release. The data are what a user-side pathway would also produce; they do not show one. The drop in signing at four or more asks is suggestive and untested.

## 7. What this does and does not establish

- It shows where the printed numbers carry the paper's wording and where they do not (findings 1, 2 and 4), and what the public data say about who drives the headline.
- It does not show that the paper's conclusions are wrong. The Supporting Information, the unredacted transcripts and the published article's exact wording could not be checked, and the article may answer some of these points in places not read.
- Limits: one reader; the binary-SD assumption (finding 4) and the noise model (finding 1) are rough; the data check was not re-run; the article's wording rests on a copy not stored here.

## 8. What would change this

The published article's text and Supporting Information (to settle findings 1, 3 and 5); a non-AI "ask" arm; unredacted transcripts coded for turn-level pushback; a re-run of `repo_check/analysis.py` on a fresh approved clone; and a direct test of the difference between the attitude and behaviour correlations.

## 9. Reproduction

Everything is in `pnas_ai_persuasion_political_actions_reading_v1/`: `predictions_fixed_2026-10-22.md`; `checks.py` and its output (standard library; uses numbers printed in the main text); `paper_checks.py` and its output (needs the preprint PDF and `pdftotext`; the PDF is not stored here); `repo_check/` with its predictions, `analysis.py` (run as `python3 -I analysis.py /path/to/AI-action-persuasion`) and output; `tool_scan_*.json`. `checks.py` re-ran on 2026-10-26 and reproduced its committed output.

## References

Sources: the published article (PNAS 123:e2611368123, 2026, copy not stored); arXiv:2604.09200v1 (10 April 2026); the public repository `kobihackenburg/AI-action-persuasion` at commit `d7025d1`.

## Revision log

- *2026-10-26, v1.* First public version, from private notes of 2026-10-22. New in this version: the preprint re-check (section 2, `paper_checks.py`), verification status on each finding, and neutral wording of the data check's scope.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
