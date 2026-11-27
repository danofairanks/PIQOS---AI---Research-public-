#!/usr/bin/env python3
"""Arithmetic checks on printed numbers and printed statements in arXiv:2611.23476v1 (standard library only).
Not checks of the method: each test confirms that a printed number follows from other printed numbers, or that a printed
inequality or identity holds as written for random inputs."""
import math, random
from fractions import Fraction as F
random.seed(20261127)
ok = True
def report(name, passed, detail=''):
    global ok; ok &= passed
    print(('PASS ' if passed else 'FAIL ') + name + (' | ' + detail if detail else ''))

# Table 2 and caption: tokens per task, reduction, runtime
red = 1 - 59651/131032
report('token reduction 54.5% (59,651 vs 131,032)', abs(red*100 - 54.5) < 0.05, f'{red*100:.3f}%')
vs_best = 1 - 59651/78705
report('reduction vs the lowest-token evolving baseline printed as 78,705: 24.2%', abs(vs_best*100 - 24.2) < 0.05, f'{vs_best*100:.3f}%')
report('runtime 167.6 vs 158.8 min is within 6%', 167.6/158.8 - 1 < 0.06, f'{(167.6/158.8-1)*100:.2f}%')
report('233.8 s/task over 43 tasks', abs(167.6*60/43 - 233.8) < 0.2, f'{167.6*60/43:.2f}')
# headline row against the five-configuration mean
report('headline gain over the best baseline is larger than the mean-based gain', (80.80-74.52) > (77.09-74.52), f'headline {80.80-74.52:.2f} pp, mean-based {77.09-74.52:.2f} pp')
# sign-flip test: 8 tasks better, 0 worse, rest tied; two-sided exact p
p = 2/2**8
report('exact sign-flip p for 8 better, 0 worse (printed p = 0.008)', abs(p - 0.008) < 5e-4, f'{p:.5f}')

# Theorem 1(iv): per-group gating advantage a^(1-|G|) at a = 0.5, |G| = 4
report('Theorem 1(iv) example 8x', abs(0.5**(1-4) - 8) < 1e-12, f'{0.5**(1-4)}')

# Theorem 2(i): E[max of J geometric(eps)] >= H_J (1-eps)/eps ; exact expectation by summation
def e_max(J, eps, N=200000):
    q = 1-eps
    return sum(1 - (1-q**n)**J for n in range(N))
worst = 1e9
for J in (1, 2, 5, 10, 30):
    for eps in (0.5, 0.2, 0.1, 0.05, 0.02):
        H = sum(1/l for l in range(1, J+1))
        worst = min(worst, e_max(J, eps) - H*(1-eps)/eps)
report('Theorem 2(i) lower bound H_J (1-eps)/eps', worst >= -1e-6, f'min slack {worst:.4f}')

# Proposition 1: Priority = (1-o) + max(0, delta); difference of a regressed and a non-regressed criterion
worst = 0.0
for _ in range(20000):
    oc, oc2 = random.random(), random.random()
    dc = random.random()          # regressed: delta > 0
    dc2 = -random.random()        # non-regressed: delta <= 0
    pc = (1-oc) + max(0, dc); pc2 = (1-oc2) + max(0, dc2)
    worst = max(worst, abs((pc-pc2) - (dc - (oc-oc2))))
report('Proposition 1 identity Priority(c) - Priority(c2) = delta_c - (o_c - o_c2)', worst < 1e-12, f'max abs diff {worst:.2e}')
# single-rollout binary case: fresh regression (1 -> 0) has priority 2, a non-regressed criterion at most 1
report('binary case priorities 2 vs <= 1', (1-0)+max(0, 1-0) == 2 and max((1-o)+0 for o in (0, 1)) == 1)

# harmonic-number example in the proof of Theorem 2(i): J = 10, eps = 0.1
H10 = sum(F(1, l) for l in range(1, 11))
report('H_10 = 7381/2520', H10 == F(7381, 2520), str(H10))
print('ALL PASS' if ok else 'SOME FAIL')
