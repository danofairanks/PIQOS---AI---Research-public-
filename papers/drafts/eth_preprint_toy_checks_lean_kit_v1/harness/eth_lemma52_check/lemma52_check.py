import itertools, json, random, sys
from math import comb
sys.path.insert(0, '../eth_appendixB_check')
from appendixB_check import decompose          # e_j(Y) = a_j + b_j Y from Lemma 5.1 (exact integers)

# multivariate polynomials: dict {exponent tuple: int coeff}
def padd(P, Q):
    R = dict(P)
    for k, v in Q.items():
        R[k] = R.get(k, 0) + v
        if R[k] == 0: del R[k]
    return R
def pmul(P, Q):
    R = {}
    for k1, v1 in P.items():
        for k2, v2 in Q.items():
            k = tuple(a+b for a, b in zip(k1, k2)); R[k] = R.get(k, 0) + v1*v2
    return {k: v for k, v in R.items() if v != 0}
def pscal(P, c): return {k: v*c for k, v in P.items() if v*c != 0}
def deg(P): return max((sum(k) for k in P), default=-1)
def const(c, nv): return {tuple([0]*nv): c} if c else {}
def ppow(P, n, nv):
    R = const(1, nv)
    for _ in range(n): R = pmul(R, P)
    return R

def rand_poly(nv, dstar, rng, full=True):
    P = {}
    for e in itertools.product(range(dstar+1), repeat=nv):
        if sum(e) <= dstar and (full or rng.random() < 0.5):
            c = rng.randint(-3, 3)
            if c: P[e] = c
    # ensure degree exactly dstar when possible
    top = tuple([dstar]+[0]*(nv-1))
    P[top] = P.get(top, 0) or 1
    return P

def Bi(y, es, l, nv):
    h = padd(pmul(y, y), pscal(y, -1))
    out = []; hp = const(1, nv)
    for j in range(l):
        a_, b_ = es[j]
        ej = padd(const(a_, nv), pscal(y, b_))
        out.append(pmul(ej, hp)); hp = pmul(hp, h)
    return out                                     # list over j of polynomials (coefficient of V^j)

def vmul(A, B, l, truncate=True):
    n = l if truncate else len(A)+len(B)-1
    C = [dict() for _ in range(n)]
    for i, P in enumerate(A):
        for j, Q in enumerate(B):
            if i+j < n: C[i+j] = padd(C[i+j], pmul(P, Q))
    return C

def run(nv=3, trials=60, seed=0):
    rng = random.Random(seed); fails = 0; tight = 0; total = 0
    maxrat = 0; untr_exceeds = 0; untr_cases = 0; recs = []
    for _ in range(trials):
        l = rng.randint(1, 5); m = rng.randint(1, 4); dstar = rng.randint(1, 2)
        p, es, _, _ = decompose(l)
        ys = [rand_poly(nv, dstar, rng) for _ in range(m)]
        prod = [const(1, nv)] + [dict() for _ in range(l-1)]
        full = [const(1, nv)]
        for y in ys:
            B = Bi(y, es, l, nv)
            prod = vmul(prod, B, l)
            if l <= 3 and m <= 3:                          # untruncated product for comparison (expensive)
                full = vmul(full, B, l, truncate=False)
        for s in range(l):
            d = deg(prod[s]); total += 1
            if d > dstar*(m + 2*s): fails += 1
            if d == dstar*(m + 2*s): tight += 1
        tot = {}
        for s in range(l): tot = padd(tot, prod[s])
        if deg(tot) > dstar*(m + 2*(l-1)): fails += 1
        if l <= 3 and m <= 3:
            untr_cases += 1
            fd = max(deg(P) for P in full)
            bound = dstar*(m + 2*(l-1))
            if fd > bound: untr_exceeds += 1
        recs.append((l, m, dstar, deg(tot), dstar*(m + 2*(l-1))))
    return dict(coefficient_checks=total, bound_violations=fails, coefficients_attaining_bound=tight, untruncated_cases=untr_cases,
                untruncated_exceeding_bound=untr_exceeds, sample=recs[:6])

def example_l2():
    # p_2(Y) = 1 - 3Y^2 + 2Y^3 = (1-Y) + (2Y-1) h(Y)
    ok = all(1 - 3*Y*Y + 2*Y**3 == (1-Y) + (2*Y-1)*(Y*(Y-1)) for Y in range(-20, 21))
    # two equations, d*=1: retained terms degree <= 4; omitted term degree 6
    y1 = {(1, 0): 1}; y2 = {(0, 1): 1}       # y1 = x, y2 = y (degree 1)
    p, es, _, _ = decompose(2)
    B1 = Bi(y1, es, 2, 2); B2 = Bi(y2, es, 2, 2)
    prod = vmul(B1, B2, 2)
    degs = [deg(P) for P in prod]
    full = vmul(B1, B2, 2, truncate=False); fdegs = [deg(P) for P in full]
    return dict(identity_ok=ok, retained_degrees=degs, bound=1*(2+2*1), untruncated_degrees=fdegs)

def substitution_T(trials=40, seed=5, nv=3):
    """LD-5: substitute degree <= R-1 polynomials in T for the input variables."""
    rng = random.Random(seed); bad = 0; maxd = []
    for _ in range(trials):
        l = rng.randint(1, 4); m = rng.randint(1, 3); dstar = rng.randint(1, 2); R = rng.randint(2, 4)
        p, es, _, _ = decompose(l)
        ys = [rand_poly(nv, dstar, rng) for _ in range(m)]
        prod = [const(1, nv)] + [dict() for _ in range(l-1)]
        for y in ys: prod = vmul(prod, Bi(y, es, l, nv), l)
        tot = {}
        for s in range(l): tot = padd(tot, prod[s])
        # variable X_v -> random polynomial in T of degree <= R-1: represent polynomials in T as dict {(e,):c}
        subs = [{(e,): rng.randint(-2, 2) for e in range(R)} for _ in range(nv)]
        subs = [{k: v for k, v in S.items() if v} or {(0,): 1} for S in subs]
        res = {}
        for mon, c in tot.items():
            term = {(0,): c}
            for v, e in enumerate(mon):
                for _ in range(e): term = pmul(term, subs[v])
            res = padd(res, term)
        d = deg(res)
        maxd.append((d, dstar*(R-1)*(m + 2*(l-1))))
        if d > dstar*(R-1)*(m + 2*(l-1)): bad += 1
    return dict(trials=trials, violations=bad, sample=maxd[:8])

if __name__ == "__main__":
    out = dict(deg=run(trials=120), example=example_l2(), subst=substitution_T())
    print(json.dumps(out, indent=1))
    json.dump(out, open("lemma52_results.json", "w"), indent=1)
