#!/usr/bin/env python3
"""Runnable check: does the exponential-tilt family, restricted to
lambda >= 0 (the paper's own stated domain), admit an agent with
ordinary risk-averse preferences over continuity variance?
Deterministic, no dependencies. Independently re-run to confirm.

Referenced from continuity_weighted_caring_risk_aversion_exclusion_v1.md
as "this repository, run alongside this paper, no dependencies."
"""
import math

def V(lam, mu, S):
    return sum(m * math.exp(lam * s) for m, s in zip(mu, S))

def mu_star(lam, mu, S):
    v = V(lam, mu, S)
    return [m * math.exp(lam * s) / v for m, s in zip(mu, S)]

mu = [0.5, 0.5]
S_A = [0.0, 1.0]   # spread, mean 0.5
S_B = [0.5, 0.5]   # concentrated, mean 0.5

# --- Lemma 1: V > 0, mu* is a probability ---
for lam in [0.0, 0.5, 1.0, 5.0, 50.0]:
    v = V(lam, mu, S_A)
    ms = mu_star(lam, mu, S_A)
    assert v > 0
    assert abs(sum(ms) - 1.0) < 1e-9
    assert all(m >= 0 for m in ms)

# --- Lemma 2: lambda=0 identity; lambda->inf concentration ---
assert abs(V(0.0, mu, S_A) - 1.0) < 1e-12
assert all(abs(a - b) < 1e-12 for a, b in zip(mu_star(0.0, mu, S_A), mu))

# --- The defeat-relevant construction: mean-matched, variance-differing ---
print("lambda   V_A         V_B         A strictly preferred")
for lam in [0.0, 0.1, 0.5, 1.0, 3.0, 10.0]:
    va, vb = V(lam, mu, S_A), V(lam, mu, S_B)
    print(f"{lam:6.1f}  {va:10.6f}  {vb:10.6f}  {va > vb}")
