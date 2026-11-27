#!/usr/bin/env python3
"""Arithmetic spot checks of displayed steps in Appendix D of arXiv:2611.34924v1 (standard library only).
Not checks of the physics: each test confirms that an inequality or identity printed in the appendix holds
as written for random inputs, or that a printed closed form agrees with an independent computation."""
import math, random
random.seed(20261127)
ok = True
def report(name, passed, detail=''):
    global ok; ok &= passed
    print(('PASS ' if passed else 'FAIL ') + name + (' | ' + detail if detail else ''))

# (D.21): c[1/4 - e^eta/(1+e^eta)^2] = (c/4) tanh^2(eta/2), from the vacuum correlator (D.19)
worst = 0.0
for eta in [i/10 for i in range(-50, 51) if i]:
    c = 1.7
    lhs = c*(0.25 - math.exp(eta)/(1+math.exp(eta))**2)
    rhs = c/4*math.tanh(eta/2)**2
    worst = max(worst, abs(lhs-rhs))
report('D.21 tanh^2 identity', worst < 1e-12, f'max abs diff {worst:.2e}')

# (D.20): E[sin(a X) sin(b Y)] for jointly Gaussian zero-mean X, Y with covariances GLL, GRR, GLR
a, b, GLL, GRR, GLR = 0.9, 1.1, 0.8, 1.3, 0.5
closed = math.exp(-(a*a*GLL + b*b*GRR)/2)*math.sinh(a*b*GLR)
N = 1_500_000
s = 0.0
sx, sy = math.sqrt(GLL), None
l11 = math.sqrt(GLL); l21 = GLR/l11; l22 = math.sqrt(GRR - l21*l21)
for _ in range(N):
    z1, z2 = random.gauss(0, 1), random.gauss(0, 1)
    X = l11*z1; Y = l21*z1 + l22*z2
    s += math.sin(a*X)*math.sin(b*Y)
mc = s/N
report('D.20 closed form vs Monte Carlo', abs(mc-closed) < 4e-3, f'closed {closed:.5f} MC {mc:.5f}')

# (D.23): |e^{ix} - 1| <= |x|
worst = max(abs(complex(math.cos(x), math.sin(x)) - 1) - abs(x) for x in [random.uniform(-50, 50) for _ in range(100000)])
report('D.23 |e^{ix}-1| <= |x|', worst <= 1e-12, f'max (lhs-rhs) {worst:.2e}')

# (D.46): beta = (s^3/Q)^(1/4) gives beta*Q + (s/beta)^3 = 2 (s Q)^(3/4)
worst = 0.0
for _ in range(1000):
    s_, Q = 10**random.uniform(-3, 3), 10**random.uniform(-3, 3)
    beta = (s_**3/Q)**0.25
    worst = max(worst, abs((beta*Q + (s_/beta)**3) - 2*(s_*Q)**0.75)/(2*(s_*Q)**0.75))
report('D.46 optimisation over beta', worst < 1e-9, f'max rel diff {worst:.2e}')

# (D.49): Cauchy-Schwarz: (sum_s sum_a k)^2 <= (sum_s e^s d(s)) (sum_s e^-s sum_a k^2)
worst = 1.0
for _ in range(300):
    grid = [random.uniform(0, 5) for _ in range(12)]
    d = [random.randint(1, 8) for _ in grid]
    k = [[random.random() for _ in range(di)] for di in d]
    Z1 = sum(sum(ki) for ki in k)
    Zc = sum(math.exp(-s_)*sum(x*x for x in ki) for s_, ki in zip(grid, k))
    bound = 1/sum(math.exp(s_)*di for s_, di in zip(grid, d))
    worst = min(worst, Zc/Z1**2/bound)
report('D.49 ratio >= 1/(sum e^s d(s))', worst >= 1-1e-12, f'min ratio/bound {worst:.6f}')

# (D.52b): with t = 1/(1+log r), r = A*/A_P >= 1: r^t <= e and 1/t = 1+log r
worst = 0.0
for _ in range(10000):
    r = 10**random.uniform(0, 12)
    t = 1/(1+math.log(r))
    worst = max(worst, r**t - math.e)
report('D.52b exponent step r^t <= e', worst <= 1e-12, f'max (r^t - e) {worst:.2e}')

# (D.25) arithmetic: outside-interval weight s*^2 k /((k+N) e^{-s*} m) vs s*^2 /(r e^{-s*} m) when k = rank(P)/r outside, k+N = rank(P)
worst = 0.0
for _ in range(1000):
    r = random.randint(2, 50); rank = r*random.randint(1, 30); sstar = random.uniform(1, 9); m = 10**random.uniform(-6, 0)
    lhs = sstar**2*(rank/r)/(rank*math.exp(-sstar)*m)
    rhs = sstar**2/(r*math.exp(-sstar)*m)
    worst = max(worst, abs(lhs-rhs)/rhs)
report('D.25 weight outside interval (one outside vector per cycle)', worst < 1e-12, f'max rel diff {worst:.2e}')
print('ALL PASS' if ok else 'SOME FAIL')
