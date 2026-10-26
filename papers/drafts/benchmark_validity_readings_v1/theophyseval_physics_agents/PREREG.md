# Preregistration — checks on TheoPhysEval's reported per-problem table (2026-10-17)
Written before the script. Source: arXiv 2610.16733v1 (Chandra et al., 9 Oct 2026), Table IV (per-problem pass/fail, 5 agents x 2 tracks, 50 problems), Tables III/V-X (tokens, costs). Same-source caveat: single Anthropic-model reader/coder; Table IV was parsed by me from PDF text (parse is verified against the paper's own printed "Solved" row).
Only the paper's reported table is used. No agent was run. Everything below is secondary analysis of one single-run table; post-hoc status is stated for anything not listed here.

## Checks and predictions [probability]
C1 Parse: per-column pass counts equal the printed totals (49,46 | 46,46 | 34,31 | 27,25 | 21,26) and the text's 98/92/68/54/42 and 92/92/62/50/52 percentages. [0.95]
C2 Wilson 95% CIs on each agent's pass rate (n=50). Prediction: Astra-realistic lower bound < 0.90 and the Astra-vs-Opus realistic CIs overlap. [0.95]
C3 Paired realistic-vs-isolated differences per agent, exact McNemar. Prediction: no agent's difference is significant at 0.05 (so the paper's "well within uncertainty" statement holds), BUT the discordant-pair counts are large relative to the net differences, i.e. run-to-run/condition noise is of order several problems per agent. [0.85 / 0.8]
C4 Pooled over agents, treating the 5 agents as given: net R minus I = +3 problem-passes of 250. Prediction: not distinguishable from 0 (exact binomial on discordant pairs, p>0.05). [0.9]
C5 Subset claim: "the sets solved by other models, and by Astra isolated, are each a strict subset of those solved by Astra realistic." Prediction: true, and true trivially (Astra-R fails only §1b, which no agent solved; any set omitting §1b is a subset). Report the number of problems that could falsify it (=1). [0.97]
C6 Saturation/discrimination: number of problems solved by all 5 agents (R track) and by both Astra and Opus. Prediction: >= 15 solved by all five; >= 40 solved by both Astra and Opus (so the top two are separated by <= 6 informative items). [0.8 / 0.85]
C7 Nestedness: fraction of Opus-R passes that are also Astra-R passes; fraction of Gemini-R passes that are also Opus-R passes. Prediction: >= 0.95 and >= 0.85. [0.8]
C8 Dependent (linked) problems: §6a-6d (and §5c-5e) are described as linked. Prediction: within linked sets, agent outcomes are more correlated than across the rest (all-agree rate higher). Report per-agent same-outcome rate on linked sets vs the rest; this affects the effective n. [0.7]
C9 Cost arithmetic: per-problem cost columns (Table X) sum to the printed totals within rounding; Astra realistic mean cost per problem < USD 3 as claimed. [0.9]
C10 §1b: Astra's realistic and isolated token spend on §1b (the only item it failed on the realistic track) is the smallest among agents that did not time out; consistent with an early "0 = no equation exists" answer. [0.75]

## Reporting
Counts and exact p-values; predictions that fail are reported as failed. The C8 clustering is exploratory (the linked-set list is read from the Appendix A headings; if a list cannot be read unambiguously it is reported as not checked).
