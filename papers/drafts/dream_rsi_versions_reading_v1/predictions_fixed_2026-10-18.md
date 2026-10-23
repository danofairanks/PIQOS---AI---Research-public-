# Preregistration — arXiv 2609.14858v2 vs v1 (written before v2 was read), 2026-10-18
Operator upload: `f95b1024-2609.14858v2.pdf` (1.5 MB). Baseline: the v1 PDF on file (sha256 b2d13d59…). Same-source caveat: my reading; the diff is mechanical, the classification of changes is mine.
## Predictions [probability]
C1 The v2 PDF carries a "v2" arXiv stamp and a date later than 14 Sep 2026. [0.95]
C2 A Limitations, Broader Impact, Ethics or Safety section appears that v1 lacked. [0.35]
C3 The exploration-prompt line "Never execute pkill, kill, killall, or terminate unrelated processes." is still present and unchanged. [0.8]
C4 The F/M partition is unchanged: base models, evaluator and execution interface remain fixed; only the exploration policy is optimised. [0.85]
C5 Headline results are unchanged within rounding (1.22x downstream runtime, 1.74x less discovery compute, 162x fewer calls, 4 of 4 GPU kernels, 2.09x performance, 2.43x fewer generations). [0.6]
C6 Page count increases. [0.6]
C7 A code or data release statement is added or changed (code URL, release plan). [0.5]
C8 The reference list grows. [0.6]
## Reporting
A word-level diff of v1 vs v2 text with blocks counted and the substantive ones quoted (<= 25 words); a prediction that fails is reported as failed. Changes in math rendering are excluded by normalizing the text first. Anything I cannot classify is listed as unclassified.
