#!/usr/bin/env python3
"""Numeric check of the identities used in the idea-lead rebuilds of A.2 and A.15.
Standard library only; fixed seed. Not a proof: the identities are elementary and are
stated in the paper; this only guards against a transcription error."""
import random, itertools
random.seed(20261125)

def rand_dist(m):
    w = [random.random() for _ in range(m)]
    s = sum(w)
    p = [x / s for x in w]
    th = [random.random() for _ in range(m)]
    return p, th

def E(p, f):
    return sum(pi * fi for pi, fi in zip(p, f))

worst_identity = 0.0
jensen_ok = True
for _ in range(2000):
    p, th = rand_dist(random.randint(2, 8))
    m1 = E(p, th); m2 = E(p, [t * t for t in th])
    var = m2 - m1 * m1
    worst_identity = max(worst_identity, abs(m2 - (m1 * m1 + var)))
    for n in range(2, 6):
        if E(p, [t ** n for t in th]) < m1 ** n - 1e-12:
            jensen_ok = False
print("E[th^2] = (E th)^2 + Var: max abs error", f"{worst_identity:.2e}")
print("Jensen E[th^n] >= (E th)^n for n=2..5 on 2000 random cases:", jensen_ok)

# Two development processes A and B: E[thA*thB] = E thA * E thB + Cov
p = [0.5, 0.5]
thA = [0.9, 0.1]; thB = [0.1, 0.9]       # negatively correlated difficulty
e = E(p, [a * b for a, b in zip(thA, thB)])
prod = E(p, thA) * E(p, thB)
print(f"negatively correlated difficulty: joint {e:.3f} < product {prod:.3f}")
thB2 = [0.9, 0.1]                          # same difficulty profile
e2 = E(p, [a * b for a, b in zip(thA, thB2)])
print(f"same difficulty profile: joint {e2:.3f} > product {prod:.3f}")

# Shared flaw: probability s wrong for all validators forces P(all fail) >= s
s = 0.01; per = 0.05; n = 4
indep = per ** n
total = s + (1 - s) * indep
print(f"shared flaw s={s}: P(all {n} fail) = {total:.4f} vs independent-only {indep:.2e}")

# Contact: pass prob 1 if H true, q if H false. Odds multiplier of a pass = 1/q.
# k tests sharing a pass-through path with weight r: P(all pass | H false) = r*q + (1-r)*q^k
q, k = 0.2, 5
for r in (0.0, 0.3, 0.8):
    allpass = r * q + (1 - r) * q ** k
    print(f"r={r}: P(all {k} pass | H false) = {allpass:.5f}  (product of marginals {q**k:.5f}); odds multiplier {1/allpass:.1f}")
