# Quality scorecard, four gallery manuscripts (rubric: quality_rubric.md, fixed before the cells were filled)
Single rater; not blind (the manuscripts had been read); E-tiers as in the README; OCR-based reading of page images. No total across axes.

## Axis 1: abstract claims vs the manuscript's own evidence
| Sample | S | P | C | U | Score (S+0.5P)/n | Rhetoric (R, unscored) |
|---|---|---|---|---|---|---|
| CVPR-style, plots off | 2 | 1 | 1 | 1 | 0.50 | "new paradigm" |
| CVPR-style, plots on | 4 | 2 | 0 | 0 | 0.83 | none |
| ICLR-style, plots off | 1 | 2 | 1 | 0 | 0.50 | "highly efficient and scalable foundation model" |
| ICLR-style, plots on | 1 | 2 | 0 | 0 | 0.67 | "highly effective meta-heuristic" |
Cell basis:
- CVPR off: S "median aggregation + adaptive clamping" (Sec. 3.2), S "trajectory-specific DAE" (Sec. 3.3); P "significantly improves downstream collision avoidance" (Table 6: 21.0% to 15.1% under noise 0.2, one setting, 5,000 episodes, no interval); C "the first mathematically certified robustness framework" (the manuscript cites earlier certified work as [1] in its own text); U "state-of-the-art certified accuracy ... outperforming standard models like EqMotion and D-Pool under noise" (Table 1 gives the standard models N/A on certified metrics; no certified competitor is compared; the best Cert-FDE, 2.00 m, is the authors' own smoothed variant).
- CVPR on: S diffusion pre-processing (28 mentions, Sec. 3), S bounds tighten at fixed FDE (Table 3, 1.20 to 0.78 m), S datasets (setup names ETH, UCY, WildTrack, nuScenes via Trajnet++ splits), S bounded under PGD (qualitative, Fig. 4; the bound holds by construction, not by an empirical test); P "first certified robustness framework" (the source paper is in the reference list; in-text use not determined, E3); P "substantially reduce collision rates" (same Table 6 limits).
- ICLR off: S "0.91% ATSP and 3.16% CVRP" (Table 1); P "robust zero-shot generalization up to 1000 nodes" (Table 2: CVRP gap grows from 3.16% at 100 nodes to 7.37% at 1000, ATSP 1.96%; robust relative to baselines that reach 72.95% and 284.58%); P "fine-tuned onto eight unseen tasks in under 3.5 minutes" (own Sec. 4.4: only with supervised fine-tuning on 128 labelled instances; 5.5 hours for the unsupervised route); C "matches or exceeds the performance of specialized models" (own Table 1: multi-task worse than single-task in 8 of 8 cells; own Sec. 4.2: "sacrifices minimal performance").
- ICLR on: S "highly competitive with specialized state-of-the-art baselines"; P zero-shot to 1000 nodes (as above); P "under 3.5 minutes" (own text: supervised, 128 labelled; the unsupervised cost is absent).

## Axis 2: internal-consistency defects (count; i = inherited from the source paper)
| Sample | Count | Items |
|---|---|---|
| CVPR off | 5 (2i) | title "Diffusion-Denoised" vs Sec. 3.3 "single-step DAE"; abstract "first" vs own [1]; Theorem 1 "confidence level 1-alpha" with indices lacking alpha (E2); Smoothed EqMotion FDE 1.14 (Table 1) vs 1.13 (Table 4) (i); multi-modal FDE 0.39 compared with single-modal 1.13 as "better accuracy" with no best-of-k metric defined (E2, i) |
| CVPR on | 2 (2i) | the same Table 1/Table 4 mismatch and undefined best-of-k comparison (both present in the plots-on text) |
| ICLR off | 2 | abstract "matches or exceeds" vs own Table 1 and Sec. 4.2; headline "under 3.5 minutes" vs own 5.5 hours |
| ICLR on | 0 found | headline scope drop counted in Axis 1 |

## Axis 3: decimal tokens found in the source text
CVPR off 51/53 (the two: "2.00" for source "2.0", derived 0.03 s); CVPR on 47/57 (the ten unmatched are figure-axis tick labels and "2.00"); ICLR off 120/125; ICLR on 105/111 (the rest are OCR splits and section numbers).

## Axis 4: citations
Existence: 12/12 arXiv-identified references resolve with matching titles for the CVPR off and ICLR off reference lists (checked at arXiv); not checked for the two plots-on runs (E3). Relevance defects found: ICLR off 1 (a driving-motion-forecasting transformer cited as routing-solver foundation); CVPR off 0 found in the checked set (the relevance check was not exhaustive).

## Axis 5: novelty-claim integrity
CVPR off: yes in text (claims "first", cites earlier certified work as [1]). CVPR on: listed-only (source in reference list; claims "first"). ICLR off: listed-only (source paper in reference list under the sample's own title; in-text use not determined). ICLR on: no (the source is not in this run's reference list).

## Axis 6: disclosure and limits inside the manuscript
All four: no limitations section; no AI-generation disclosure (author block is the template's placeholder or "Anonymous authors").

## Axis 7: run-to-run (same inputs, two runs)
CVPR pair: "first" claim in both; method description differs (single-step DAE vs multi-step diffusion; source: multi-step diffusion); Theorem 1, the 50 m constant and "single-step" occur in plots off only; abstract-claim score 0.50 vs 0.83.
ICLR pair: claim strength differs on the headline ("matches or exceeds" vs "highly competitive"); source in the reference list in plots off only; abstract-claim score 0.50 vs 0.67; the scope-dropped "3.5 minutes" appears in both.

## Reading
Where the numbers come from the log, they are reliable. Where the manuscript asserts novelty, strength of results, scope of a headline, or a mechanism, the text can differ from its own evidence, and differs between runs on the same inputs. The plots-on runs score higher on Axis 1 in both pairs on one draw each; with one pair per venue that is not a result about plots. Not measured: how the pipeline's own LLM-judge comparisons would rate these manuscripts.
