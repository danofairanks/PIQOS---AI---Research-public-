# Idea leads and rebuilds for A.2 and A.15

The two addenda cite earlier work only as leads and carry their own derivations from the definitions. `rebuild_check.py` (standard library, fixed seed) checks the identities numerically; `rebuild_check_output.txt` is its output. It guards against a transcription error and is not a proof; the identities are elementary.

## What was checked about each lead (25 November 2026)
| Lead | Used in | Checked | Not checked |
|---|---|---|---|
| Popper, falsifiability, the asymmetry between verifying a universal claim and refuting it, ad hoc rescue | A.15 | Passages read in the Stanford Encyclopedia of Philosophy entry "Karl Popper" (section 3: a universal proposition cannot be verified by experience but one counter-instance falsifies it; section 2: demarcation by falsifiability; ad hoc hypotheses) | Popper's own text |
| Mayo, severity of a test (*Statistical Inference as Severe Testing*, Cambridge University Press, 2018) | A.15 | Bibliographic record (Open Library) | The text; a publisher or author page quoting the definition could not be fetched |
| Eckhardt and Lee, *IEEE Trans. Software Eng.* SE-11(12), 1985, 1511-1517; Knight and Leveson, SE-12(1), 1986, 96-109; Littlewood and Miller, 15(12), 1989, 1596-1614 | A.2 | Bibliographic records (Crossref) | The papers and their abstracts (the publisher's pages returned no text) |
| Campbell, "Assessing the impact of planned social change", *Evaluation and Program Planning* 2(1), 1979, 67-90 | not used in the paper | Bibliographic record (Crossref) | The text; the "corruption pressures" sentence was not retrieved |
| Kuhn, anomalies and crisis; paradigm choice not purely social | not used in the paper | Passages read in the Stanford Encyclopedia entry "Thomas Kuhn" | Kuhn's own text |

Nothing in A.2 or A.15 relies on a claim about what the unread sources say. Each lead is named as a lead; each derivation stands on its definitions.

## What the script checks
1. For a failure-probability profile theta over inputs, E[theta^2] = (E theta)^2 + Var(theta), and E[theta^n] >= (E theta)^n for n = 2 to 5 (Jensen).
2. For two development processes, E[theta_A theta_B] = E theta_A E theta_B + Cov, with a small example above and below the product.
3. A shared flaw of probability s forces P(all fail) >= s, whatever the number of validators.
4. For a claim H with pass probability 1 if true and q if false, a pass multiplies the odds by 1/q; for tests that share a pass-through path, P(all pass | H false) exceeds the product of the marginals, and the odds multiplier falls (example: 3125 independent versus 16.6 and 6.2).

## Limits
The models are the simplest that carry the point (conditional independence given the input; a single shared path). They say nothing about how large any quantity is for any real validator or test.
