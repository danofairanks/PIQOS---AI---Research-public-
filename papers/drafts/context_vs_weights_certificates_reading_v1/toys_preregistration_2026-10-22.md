# Preregistration: counter-model toys (2026-10-22)
Written 2026-10-22 before any toy was built or run (the evaluator's own record, not independently timestamped). Context: the draft's section 4 (paper read; certificates need the true answer law and designed data; the betting test needs held-out queries drawn independently from the task and an exchangeable order). All toys are numpy only (the race toys reuse the repo's `bitsy.core.race` unchanged at commit cf81a50 (set BITSY_PATH to a checkout) so that the paper's test, not my reimplementation, is what is stressed). Same-source caveat: the toys are written by the evaluator; each tests whether a stated precondition is load-bearing, not whether the paper is wrong where its preconditions hold. E1 executed.

## CM1: certificates with an estimated, not true, answer law
Setup: outcome alphabet V = 16, a random fixed true law P* (Dirichlet(1)), capacity C = 0 (the window/capacity distinction does not matter for this precondition), a prompt memory whose per-episode code length has mean H(P*) - C + delta and sd 0.3 bits, 64 episodes, certificate issued when the lower end of the 95% interval of the mean margin (prior code length minus C minus prompt code length) is above zero. "Prior code length" uses -log2 q(Q_ep) with q = P* (exact) or q = an add-one-smoothed empirical law from n_est independent samples. A false certificate is one issued while the true margin H - C - L_prompt = -delta <= 0.
- CM1a: with the exact law and delta = 0.05, the false-issue rate over 5,000 trials is at most 2.5%.
- CM1b: with n_est = 50, the false-issue rate at delta = 0.05 is at least 20%.
- CM1c: with n_est = 5,000, the false-issue rate at delta = 0.05 is at most 5%.
- CM1d: at n_est = 50 certificates are still issued at delta = 0.10 in at least 10% of trials.
Reading if all hold: the exactness of the information terms is load-bearing; the "correct" count on designed data does not extend to estimated laws. If CM1b fails, the bias of the estimated law is smaller than I expect in this setting and the precondition is less fragile than claimed.

## CM2: the betting test under an ordered, non-exchangeable stream (uses `bitsy.core.race`)
Setup: score differences bounded in [-c, c] with c = 4 bits; total length T = 2,000; no true winner on the stream as a whole (overall mean exactly 0): the first 300 queries have mean +0.5 and the remaining 1,700 have mean -0.0882 (so the overall mean is 0), independent noise of sd 1; alpha = 0.05; 5,000 streams.
- CM2a: false-call rate on the ordered stream is at least 15% (the paper's guarantee is for independently drawn held-out queries).
- CM2b: the same streams randomly reordered give a false-call rate of at most 5%.
- CM2c: a stream that drifts to the opposite sign after the test window (stream mean +0.1, deployment mean -0.1) is called for the stream's winner in at least 95% of 2,000 streams; the call is wrong for deployment. (Included to quantify scope, not to find a flaw.)

## CM3: held-out queries leaking into one channel's context (uses `bitsy.core.race`)
Setup: channel A reads a context that, for a fraction f of the held-out queries, contains the answer (code length 0.05 bits; otherwise 2.0 bits); channel B is better than A by 0.1 bits on every clean query. Score difference = loss_B - loss_A, clipped to a bound c = 4. 2,000 streams of 2,000 queries, alpha = 0.05.
- CM3a: the call flips to channel A (the false call for the clean task) at a leakage fraction between 3% and 8%.
- CM3b: at f = 10%, A is called in at least 95% of streams; at f = 0, B is called in at least 95% (power) and A in at most 2.5%.
Reading: the test's error control is conditional on independence between context and queries, which the test cannot check.

## Not built here (stated)
Real-model contamination, adjudicator robustness to manipulated evidence, and the continual-learning per-sequence error question (needs a model of rounds; noted for the entry as E3).
Misses are recorded as missed, not edited.
