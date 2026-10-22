# Predictions and checks fixed before the paper was read
Written 2026-10-20 from the abstract (a screenshot) and the public repository at commit cf81a50; the arXiv paper (2610.29419v1, 21 Oct 2026) did not yet exist. The text below is copied unchanged apart from two private pointers removed. The date is the evaluator's own record (a private repository commit); it is not independently timestamped. Scores and results are in the draft, section 4.

## 4. Predictions about the paper (fixed 2026-10-20, before reading it)
- **P1.** The "exact law" is an expectation identity: a decomposition of the code-length difference into information, prior-repair and decoding-loss terms, proved in a few lines.
- **P2.** The capacity certificate's proof reduces to a data-processing or Fano-type inequality (H(Q) minus stored bits); no new inequality.
- **P3.** The body (not only an appendix) states that certificates need the true answer law and run on designed data.
- **P4a.** The related work cites prequential coding or MDL (for example Blier and Ollivier, 2018). **P4b.** It cites betting or e-process literature for forecast comparison (for example Choe and Ramdas, 2024) or an equivalent. I have no strong prior on either.
- **P5.** "First" is scoped in the body to a narrower claim than the abstract's sentence.
- **P6.** The 3.3% null-error figure is an observed rate over a stated number of null streams, below the 5% target, with "null stream" defined in the body.
- **P7.** All experiments are by the authors; no external replication.
- **P8.** The certificates table in the paper matches the README's (36 of 96 issued; 86 checks all agree).
- **P9.** The AUROC 0.91 comes from a model valuing evidence by its own probability change; the 0.95 threshold is described as a default and not tuned on that data.

## 5. Checks on release, with defeat conditions for my evaluation
- **C1 theorems.** Read the statements and proofs. *If either the law or the certificate contains a non-textbook result, "textbook inequalities" is withdrawn.* Numerically test the identity on my own simulated distributions once the three terms are defined.
- **C2 abstract vs body.** Does the body qualify "every certificate is correct" as same-episodes and built-memories-only? *If it also reports an out-of-sample check, scrutiny item 4 is corrected; if it only qualifies it, the item becomes "abstract compresses".*
- **C3 priority.** Does related work cite and distinguish the neighbours (prequential description length, betting forecast comparison, demonstration valuation)? *If yes and the distinction is substantive, the priority claim moves from unverified to supported at scope; if the neighbours are absent, the claim stays unverified and the omission is recorded.*
- **C4 real-model numbers.** Locate 61,948 of 64,000, the 32 comparisons, the 3.3%, the kriging ranking and the AUROC; record definitions, denominators and whether anything is recomputable from the repo's data. Label each recomputable or blocked.
- **C5 repo vs paper.** Do the repo's functions implement the paper's definitions (`gate.capacity`, `gate.window`, `bakeoff.race`, `guard`)? Any mismatch is a finding either way.
- **C6 null error.** Compare the paper's null-error design with my T4 results (2 to 3% under three cost distributions).
- **C7 licence and release.** Whether a licence, tests, versioned release or data statement accompanies the paper.
- **C8 anything that cites or contradicts our own record** (guarantees borrowed from another setting, anchoring on the authors' own earlier work, vacuity).

