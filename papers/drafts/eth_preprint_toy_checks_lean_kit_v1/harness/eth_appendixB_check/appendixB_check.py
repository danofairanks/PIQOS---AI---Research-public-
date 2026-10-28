import itertools, json, math, random, sys
from fractions import Fraction
from math import comb, factorial, log2

# ---------- T1: Lemma 5.1 / B.1 ----------
def pmul(a, b):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i+j] += x*y
    return out

def p_ell(l):
    one_minus_Y_l = [comb(l, i)*(-1)**i for i in range(l+1)]
    series = [comb(l+j-1, j) for j in range(l)]
    return pmul(one_minus_Y_l, series)

def divmod_h(poly):
    """divide poly(Y) by h = Y^2 - Y (monic): return quotient, remainder (a + bY). counts eliminations."""
    p = list(poly); q = [0]*max(1, len(p)-2); elim = 0
    for m in range(len(p)-1, 1, -1):
        c = p[m]
        if c:
            q[m-2] += c; p[m] -= c; p[m-1] += c; elim += 1
    rem = p[:2] + [0]*(2-len(p[:2]))
    return q, rem, elim

def decompose(l):
    p = p_ell(l); es = []; tot_elim = 0; maxnorm = 0
    cur = p
    for j in range(l):
        cur, rem, el = divmod_h(cur); tot_elim += el
        es.append(rem)
        maxnorm = max(maxnorm, sum(abs(x) for x in cur) + sum(abs(x) for x in rem))
    return p, es, tot_elim, maxnorm

def evalpoly(p, y):
    v = 0
    for c in reversed(p): v = v*y + c
    return v

def T1(lmax=40):
    rows = []
    for l in range(1, lmax+1):
        p, es, el, mx = decompose(l)
        # identity p = sum e_j h^j
        ok_id = True; ok_cong = True
        for y in range(-12, 13):
            h = y*(y-1)
            s = sum((es[j][0] + es[j][1]*y) * h**j for j in range(l))
            if s != evalpoly(p, y): ok_id = False
            if evalpoly(p, y) % 2**l != (1 if y % 2 == 0 else 0): ok_cong = False
        maxbits = max(max(abs(a), abs(b)).bit_length() for a, b in es)
        norm_p = sum(abs(c) for c in p)
        rows.append(dict(l=l, identity=ok_id, congruence=ok_cong, max_coef_bits=maxbits, log2_norm_p=round(log2(norm_p), 1),
                         bound_3l=3*l, eliminations=el, log2_maxnorm=round(log2(max(mx, 1)), 1)))
    return rows

# ---------- T2: Lemma 5.2 truncated product ----------
def T2(trials=300, seed=1):
    rng = random.Random(seed); bad = 0; n = 0
    for _ in range(trials):
        l = rng.randint(1, 9); mt = rng.randint(1, 5)
        p, es, _, _ = decompose(l)
        ys = [rng.randint(-15, 15) for _ in range(mt)]
        # product in Z[V]/(V^l) of B_i(V) = sum_j e_j(y_i) h(y_i)^j V^j
        prod = [1] + [0]*(l-1)
        for y in ys:
            h = y*(y-1)
            Bv = [(es[j][0] + es[j][1]*y) * h**j for j in range(l)]
            new = [0]*l
            for i in range(l):
                for j in range(l-i):
                    new[i+j] += prod[i]*Bv[j]
            prod = new
        S = sum(prod)
        want = 1 if all(y % 2 == 0 for y in ys) else 0
        if (S - want) % 2**l != 0: bad += 1
        n += 1
    return dict(trials=n, failures=bad)

# ---------- T3: denominators of the Section 2.7 rows (exact rationals) ----------
def construction_exact(r, Q, R):
    base = r*r; D = r**(2*Q)
    pairs = [[(idx // base**s) % base for s in range(Q)] for idx in range(D)]
    enc = lambda ps: sum(p*base**s for s, p in enumerate(ps))
    swap = lambda pa: (pa % r)*r + pa//r
    perm_s = [[enc([swap(p) if q == s else p for q, p in enumerate(pairs[idx])]) for idx in range(D)] for s in range(Q)]
    perm_V = [enc([swap(p) for p in pairs[idx]]) for idx in range(D)]
    p = (r-1)/(2*r)
    a0 = max(0, min(int(round(Q*p-(R-1)/2)), Q+1-R)); I = list(range(a0, a0+R))
    # Lagrange f on I
    coeffs = [Fraction(0)]
    for i, xi in enumerate(I):
        num = [Fraction(1)]; den = Fraction(1)
        for k, xk in enumerate(I):
            if k == i: continue
            nn = [Fraction(0)]*(len(num)+1)
            for a, c in enumerate(num):
                nn[a] += -xk*c; nn[a+1] += c
            num = nn; den *= (xi-xk)
        yi = (-1)**xi
        for a, c in enumerate(num):
            if a >= len(coeffs): coeffs.append(Fraction(0))
            coeffs[a] += c*Fraction(yi)/den
    f = coeffs
    def apply_W0(Mat):
        out = []
        for u in range(D):
            row = [Fraction(Q)*x for x in Mat[u]]
            for s in range(Q):
                pr = Mat[perm_s[s][u]]
                row = [a-b for a, b in zip(row, pr)]
            out.append([x/2 for x in row])
        return out
    F = [[f[-1]*(1 if i == j else 0) for j in range(D)] for i in range(D)]
    for c in reversed(f[:-1]):
        F = apply_W0(F)
        for u in range(D): F[u][u] += c
    M0 = [F[perm_V[u]] for u in range(D)]
    return dict(D=D, pairs=pairs, M0=M0, I=I, f=f)

def T3(r, Q, R):
    c = construction_exact(r, Q, R); D = c['D']; pairs = c['pairs']; M0 = c['M0']
    dden = factorial(R-1)*factorial(Q)
    maxcoef = 0; nonint = 0; maxden_M0 = 1
    for u in range(D):
        du = [p % r for p in pairs[u]]
        for w in range(D):
            m = M0[u][w]
            if m == 0: continue
            maxden_M0 = max(maxden_M0, m.denominator)
            aw = [p//r for p in pairs[w]]
            E = [s+1 for s in range(Q) if aw[s] != du[s]]
            phi = [Fraction(1)]
            for s in E:
                new = [Fraction(0)]*(len(phi)+1)
                for a, cc in enumerate(phi):
                    new[a] += cc; new[a+1] -= cc/s
                phi = new
            poly = [m*(x - (1 if a == 0 else 0)) for a, x in enumerate(phi)]
            poly[0] += (1 if u == w else 0)
            for x in poly:
                v = x*dden
                if v.denominator != 1: nonint += 1
                maxcoef = max(maxcoef, abs(v.numerator))
    BP_formula = Q*log2(Q) + log2(D)
    return dict(r=r, Q=Q, R=R, D=D, dden=dden, nonintegral_coefficients=nonint, max_den_M0=maxden_M0,
                max_abs_dden_P=int(maxcoef), log2_max_abs=round(log2(maxcoef), 2) if maxcoef else 0,
                Q_log2Q_plus_log2D=round(BP_formula, 2))

if __name__ == "__main__":
    out = {}
    t1 = T1(40); out['T1'] = t1
    print("T1 identity all:", all(r['identity'] for r in t1), "congruence all:", all(r['congruence'] for r in t1))
    for r in t1[::6]: print("  ", r)
    # growth fit of max_coef_bits vs l
    import numpy as np
    ls = np.array([r['l'] for r in t1]); bits = np.array([r['max_coef_bits'] for r in t1])
    print("  max_coef_bits / l at l=40:", bits[-1]/ls[-1], " / l^2:", bits[-1]/ls[-1]**2)
    out['T2'] = T2(); print("T2", out['T2'])
    out['T3'] = []
    for (r, Q, R) in [(2, 3, 2), (2, 3, 3), (3, 2, 2), (2, 4, 3)]:
        t = T3(r, Q, R); out['T3'].append(t); print("T3", t)
    json.dump(out, open("appendixB_results.json", "w"), indent=1)
