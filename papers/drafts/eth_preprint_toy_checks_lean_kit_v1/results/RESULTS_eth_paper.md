# Results: OpenAI preprint "The Exponential Time Hypothesis is False"
Scored against PREREG_eth_paper.md (8236731). Source: `paper.pdf` from openai/math origin/main (7ef5c0cc5), 67 pages, metadata "ETH is False", dated "17 October 2026, revised 25 October 2026". Extracted with pdftotext (3,820 lines).

**Read depth (E1 for what was read; nothing else claimed).** Fully read: abstract, contents, introduction and related work (1.1-1.2), technique overview 2.1-2.4, Theorem 2.2 and Proposition 6.4 statements, Appendix C headers. Skimmed by heading/lemma list only: Sections 2.5-2.9, 3-6, Appendices A, B, D (about 3,000 lines). **The proof of the main theorem was not checked.** Nothing was run or implemented. The conclusions below are about what the paper claims, how it is structured and what it says about its own status.

## The claim (as the paper states it)
- Theorem 1.1: for each fixed k >= 2 a **deterministic** algorithm **counts** the satisfying assignments of a k-CNF (n variables, m clauses) in (n+m)^{O_k(1)} * 2^{O_k(n loglog n/sqrt(log n))} bit operations [corrected 2026-10-28, see end] and polynomial space; for m <= Dn, 2^{O(n/sqrt(log n))}. The abstract gives the weaker exponent n/(log n)^{1/2+o(1)}. Appendix D proves the stronger bounds by tensor contraction.
- Decision follows from counting; so ETH is refuted. The paper says the theorem also refutes SETH, Gap-ETH, NSETH, #ETH, and the bounded-error randomized versions.
- Corollaries: Max-k-SAT approximation (randomized; uses the OpenAI preprint "The Unique Games Theorem" [Ope26] for the matching NP-hardness context); subexponential counting of independent sets, q-colorings, perfect matchings; a circuit lower bound c*sqrt(n log n) for a language in E^NP (Cor. 1.4, Appendix C.1).
- Approach (E1, intro and 2.1-2.4): polynomial method. Count = sum over assignments of a product of clause polynomials of degree <= 3n (bounded-occurrence case); replace clause inputs with T-dependent linear forms so that at T=1..Q variable groups decouple once a few integer linear "measurements" are fixed; recover H(0)=#F by Taylor/Hermite interpolation. General k-CNF reduced to this by counting-preserving sparsification (Impagliazzo-Paturi-Zane; Calabro et al.), Tanner/expander-code parity tests, and counting common zeros of sparse low-degree polynomials (Theorem 2.2).
- Scope statements: runtime bound 2^{o(n)} does not transfer through general polynomial reductions, "so our result does not imply that general NP problems admit subexponential time algorithms"; does not conflict with regular-resolution lower bounds; OVC and other weaker hypotheses "may still hold". Lower bounds resting on ETH/SETH lose their basis (listed in 1.1.3).

## Scores
| id | result | note |
|---|---|---|
| E-1 | **Held in substance, form wrong** | refutes ETH, but via an explicit rate 2^{n/(log n)^{1/2+o(1)}}, not "2^{eps n} for every eps". Hexagon's "qualitative form" is a weaker restatement (E3). |
| E-2 | **Falsified** | deterministic, polynomial space, no randomization or non-uniformity. Only Cor. 1.2 is randomized. |
| E-3 | **Held** | polynomial interpolation, Hermite recovery, Taylor coefficients, plus sparsification and expander-code tests. |
| E-4 | **Partly** | SETH/Gap-ETH/NSETH/#ETH consequences stated at length; P vs NP is not mentioned by name; the closest is the sentence that NP is not shown to be subexponential. |
| E-5 | **Held** | no mention of Lean or formalization anywhere in the text (grep: Lean, formaliz*, verification: none). |
| E-6 | **Held** | cites [Ope26] OpenAI "The Unique Games Theorem" (Sept 23); used for Cor. 1.2's context, not for Theorem 1.1. Only that one OpenAI reference is in the bibliography as seen. |
| E-7 | **Held on form** | 67 pages; key lemmas stated with proofs in text; I did not check them. |
| E-8 | **Held** | 1.1.1-1.1.3 name the refuted hypotheses and the lower bounds that lose their basis. |
| E-9 | **Held (inverted)** | the main theorem is for exact counting (#k-SAT); decision follows. |
| E-10 | **Held** | no acknowledgments, no verification or review statement, no referee thanks. |

## Findings
1. **The claim is stronger than the press versions.** Deterministic exact counting in 2^{n/sqrt(log n)} time, polynomial space, for every fixed k, is the paper's own statement. Compared with the Hexagon abstract (O_eps(2^{eps n}...)): the Hexagon text is a weaker qualitative form, not the theorem.
2. **Extraordinary consequence set, no verification stated in the paper.** ETH, SETH, #ETH, Gap-ETH and NSETH all fall if Theorem 1.1 holds. The paper has no Lean files, no external-review statement, no acknowledgments. The external review the article reported (Impagliazzo, Paturi, Williams) is outside the paper and unreported here.
3. **Internal structure is checkable by outsiders in principle.** A deterministic algorithm with explicit lemmas and an explicit complexity bound is the kind of claim that can be implemented on small instances; I did not do that. The most efficient external test would be: implement the Section 2 bounded-occurrence counter and check #F against brute force for n up to ~25 with the intermediate parameters, and check Lemma 4.x's matrix M0 properties. Not attempted.
4. **A dependency to watch.** Cor. 1.2 relies on a separate OpenAI claim ("The Unique Games Theorem"). It is not an input to Theorem 1.1, but it shows these releases build on each other; verification status of the base claim is not stated in this paper.
5. **Release strategy for ETH:** public PDF and TeX sources; no Lean. So the claim's source of truth is human/expert checking of a 67-page proof, not a kernel.

## Not established
That Theorem 1.1 is correct (or wrong); the correctness of the 3,000 lines I did not read; whether any Lean development of the proof exists; the claim [Ope26] "The Unique Games Theorem"; any statement the paper makes about the review group.

## Correction (added after reading the rendered page, 2026-10-28)
The general-density exponent in Theorem 1.1 is O_k(n loglog n / sqrt(log n)), not the 'n sqrt(loglog n)/sqrt(log n)' I first wrote: that came from the pdftotext extraction, which drops radicals and fraction bars (rendered page 2 and page 57 checked as images). Fixed-density: O(n/sqrt(log n)). The Section 6.4 bound rho(n) = n (loglog n)^2/sqrt(log n) is unchanged. The prereg of eth_appendixD_model repeated the wrong form; scored there.
