# Corrections on the Card, Claims on the Page: Reading a Weight-Engineering Vendor's Model Releases

*AI-assisted. Living research: staged, not peer reviewed, may be revised or withdrawn.*

**Scope of naming.** One small independent publisher of weight-editing model releases on a public model hub (71 models listed, created 2026-07-14 to 2026-10-06), its two pitch pages (a technical brief and a release note), and a page comparing itself with published editing methods. The publisher is a private party and is called "the vendor"; its product, handle and locators are not named here and are held privately. Dual-use handling: some releases are models with refusals removed; this reading reproduces no method details and tested no model. No intent is attributed.

**Disclosure.** Drafted with AI assistance; one reader, an AI system (an Anthropic model). Read 2026-11-08: the README of 70 of the 71 releases (one image-style model has none), the three pages, the hub's public commit histories for the six cards that carry correction notices, and the shipped manifest and data files of the rebuilt 6.9B knowledge-writing card. Nothing was run; no weights downloaded.

## Flags (ranked; post hoc)
1. **Corrections live in the card and not in the pitch.** Six of the 70 cards (8.6%) carry a correction or retirement notice; all three knowledge-writing cards among them. They were written in one sprint, 2 Nov 21:39 to 4 Nov 04:45 UTC (about 30 commits, several correcting earlier corrections: one reads "still said 'no training' under its own correction"). What was withdrawn: recall headlines of 489/500 (1.4B model) and 486/500 (6.9B; its artifact measured +323.87% wikitext perplexity and -41.35 points on a language benchmark, per the card), a reasoning gain of 7% to 56% (the evaluation could not distinguish reasoning from letter preference), no-gradient wording on four cards, and a same-pipeline claim. The pitch pages' Last-Modified headers are 2026-10-01 (brief) and 2026-11-01 (release and comparison pages), before every correction, and the text of the brief and the release page was identical across two reads on 2026-11-08. As read, the brief still carries 489/500 (three times), 486/500 (three times), the 7% to 56% gain, "zero degradation" and "fully preserved", each withdrawn or contradicted on a card; the release page still reads "No training loop. No training data. No optimization.", which the cards say does not hold for knowledge writing. The lag was four to five days at the read and whether the pages are updated later is unknown. (E1; archive history not reachable)
2. **"No training" names the edit step.** The rebuilt 6.9B card's manifest records 10,000 plain-SGD updates over 738,197,504 parameters (11 layers x 16,384 x 4,096; about 10.7% of the model) in 1,029 seconds: a restricted fine-tune, which the card now states. (E1, arithmetic in `checks_arithmetic.py`)
3. **Rigor differs across one publisher's cards.** The 1.4B card has a deranged-answer control (0/500), a reworded-prompt probe (220/500 against 500/500 on the training prompt), a base-knowledge control, a perplexity cost (+18.5%) and a blind third-party diff check. The 6.9B card has paired intervals and a base-knew control but recall is measured on the training prompts only (its prompts file and facts file are byte-identical). A release whose edit removes a model's compliance with system-prompt restrictions reports 16 single-response scenarios scored by keyword lists, a five-case helpfulness check and the note "None measured" on capability, with no public contrast set, and it is the later of the two. Only 28 of the 70 cards mention any evaluation term. (E1)
4. **Adverse literature is used about competitors and not about the vendor's own class.** The comparison page surveys the failures of rank-one editing methods, a batched variant and low-rank fine-tuning (ceilings on sequential edits, no generalization across paraphrase, forgetting) and says the vendor's method has no forgetting curve, with the update rule withheld: "This is a claim about geometry, not a disclosure of the geometry." Nothing on the page tests the vendor's method against the failures it lists (no sequential-edit curve; the 1.4B card later reports 44% retention under rewording); the page says refusal-direction removal damages capability, while the vendor's own release for a compliance-removal edit reports no measured helpfulness impact. (E1)
5. **A priority claim without a survey.** The release page: "After extensive searching, we have not found another working weight-engineering system anywhere on the planet", with a hedge for an unseen internal lab. Directional ablation of a refusal direction in open models is documented in earlier public work (see `literature_context/`). (E1)
6. **Distribution.** Nine releases are named for refusal removal; the release card says the same machinery "can strip safety from any open-weight model at scale", while the tool is described as withheld. (E1 count from the hub listing)

## What holds
The correction habit is real and public: replacement notices, a retirement of a headline "rather than carrying both", a paired-statistics rebuild of the 6.9B model (recall 499/500 by prefix and anywhere against 1/500 and 9/500 for the base; perplexity 8.7188 to 9.0508, +3.81%, paired delta-NLL +0.03737 with interval [+0.03533, +0.03941], recomputed consistent; LAMBADA +1.65 points on 5,153 items). The 1.4B card's controls are the right kind. The cards' own cost statements are plain.

## Depth ratings (rubric in the series overview; one rater, not blind)
1.4B knowledge-writing card 7.0 (D4, narrow reach); 6.9B card 5.5 (D3, narrow, recall measured on training prompts); the compliance-removal card 1.5 (D1, wide reach); the pitch pages 0.5 (D0, wide reach).

## Predictions, and what changed
Fixed before reading: that corrections exist on the cards (yes, six of 70); that none reach the pitch (as read, yes); that no card carries an uncorrected contradiction between no-training wording and a gradient-method description (none found among eight read by hand). I did not predict that the publisher would correct its own no-gradient claim; the correction habit exceeded expectation.

## Limitations: what this does and does not establish
It establishes a dated lag between card corrections and pitch pages, and the contrast in rigor across releases. It does not establish intent, that the pages will remain unchanged, or any property of the models. One publisher, one snapshot.

**Tier:** E1 executed (term scan of 70 cards and hand reading of every match; commit histories; arithmetic; byte comparison of two shipped files); E2 read (pages in full; the rest of the 70 cards by term only); E3 interpretation (flags 4 and 5 as selective use).
**Deeper pass:** recommended: date the pages by archive copies; read the other 52 tool-tagged cards' methods against their negation wording. Not done (archive host unreachable from the session).

## Reproduction
`checks_card_count.py` and `checks_citation_scan.py` (term lists fixed before running) with outputs; `checks_arithmetic.py`; snapshots held privately; `quote_checks_output.txt`; `tool_scan_*.json`.

## References
Sources: the vendor's public model listing and READMEs, three public pages and the hub's public commit histories, read on 2026-11-08 (locators held privately); the numbers recomputed in `checks_arithmetic.py` are typed from the 6.9B card.

## Revision log
- *2026-11-09, v1 (pre-draft).* Private pre-build.
- *2026-11-09, v1 (pre-draft), edit.* Removed the download counts (total and refusal-removal releases) at the operator's decision; no other change.

---

*Living research. This draft is part of ongoing work and may be updated, corrected or withdrawn at any time; the repository history holds the current version and the earlier ones.*
