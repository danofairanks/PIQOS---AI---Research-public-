#!/usr/bin/env python3
"""Arithmetic check of the paper's equations (4.33) and (4.34) as written (standard library only).
Not a check of the physics: it only confirms that the displayed sum equals the displayed closed form
and that the order-G_N^3 term grows like log N."""
import cmath, math
s = 10.0; N = 3_000_000
tot = sum(2 * (1 / (2 * s * k)) ** 2 * cmath.exp(-2j * k / s) for k in range(1, N + 1))
z = cmath.exp(-2j / s); li = sum(z ** k / k ** 2 for k in range(1, N + 1)); cf = li / (2 * s * s)
print("sum of 2*(dq_k)^4 e^{-2ik/s}:", tot); print("Li2(e^{-2i/s})/(2 s^2):      ", cf); print("abs difference:", abs(tot - cf))
for n in (10**3, 10**4, 10**5, 10**6):
    print(n, "sum 1/k =", round(sum(1 / k for k in range(1, n + 1)), 5), " ln N + gamma =", round(math.log(n) + 0.5772156649, 5))
# the entropy bookkeeping of (5.68)-(5.69)
from fractions import Fraction as F
q = F(257, 302); print("q/(1-q) =", q / (1 - q), "; q/(2(1-q)) - 1/2 =", q / (2 * (1 - q)) - F(1, 2), "= 106/45?", q / (2 * (1 - q)) - F(1, 2) == F(106, 45))
