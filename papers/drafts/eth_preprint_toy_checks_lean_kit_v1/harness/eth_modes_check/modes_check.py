import itertools, json, math, random, sys
from fractions import Fraction
from math import log, exp, pi, comb

def v2(n):
    n = abs(int(n)); assert n != 0
    return (n & -n).bit_length() - 1
def v2f(x):
    x = Fraction(x)
    return 10**9 if x == 0 else v2(x.numerator) - v2(x.denominator)

def Cfun(S, T):
    r = Fraction(1)
    for q in S: r *= (T - q)
    return r

def Cprime0(S):
    r = 1
    for q in S:
        if q != 0: r *= (0 - q)
    return r

def W(S, x, y, T, Cp0):
    s = y - x; num = Fraction(1)
    for q in S:
        if q != s: num *= (T - q)
    return num / Cp0

# ---------- A: valuation claim and B: geometric expansion ----------
def test_AB(amax=5, seed=3, nz=3, pmax=14):
    rng = random.Random(seed); rows = []
    viol_val = 0; viol_exp = 0; term_val_viol = 0; cnt = 0; crossing = 0
    for a in range(1, amax+1):
        L = 2**a; S = list(range(-L, L)); alpha = 2**(a+1); Cp0 = Cprime0(S)
        for t in S:
            if t == 0: continue
            i = v2(t)
            if i >= a: continue
            for x in range(L):
                for y in range(L):
                    if ((x >> i) & 1) != ((y >> i) & 1): continue     # crossing: equal i-th bits
                    crossing += 1
                    y0 = y % 2**(i+1); j = (y - y0)//2**(i+1)
                    if v2(t - y0 + x) > i: viol_val += 1
                    for _ in range(nz):
                        zeta = rng.randint(-40, 40)
                        T = t + alpha*zeta
                        den = T - y0 + x
                        if v2(den) > i: viol_val += 1; continue
                        exact = W(S, x, y, T, Cp0)
                        first = Cfun(S, T) / (Cp0*den)
                        ratio = Fraction(2**(i+1), den)
                        for p in (1, 2, 5, 9, pmax):
                            trunc = sum(first*ratio**b*(j**b if (b > 0 or j != 0 or True) else 1) for b in range(p-1))
                            # j^0 = 1 including j = 0
                            trunc = sum(first*ratio**b*(1 if b == 0 else j**b) for b in range(p-1))
                            if v2f(exact - trunc) < p: viol_exp += 1
                        for b in range(0, 6):
                            term = first*ratio**b*(1 if b == 0 else j**b)
                            if term != 0 and v2f(term) < b+1: term_val_viol += 1
                        cnt += 1
    return dict(crossing_pairs=crossing, evaluations=cnt, valuation_violations=viol_val, expansion_violations=viol_exp, term_valuation_violations=term_val_viol)

# ---------- C: counting bound ----------
def count_tuples(N, p):
    ser = [1] + [0]*(p-1)
    for w in range(1, p):
        for _ in range(N):
            for k in range(w, p):
                ser[k] += ser[k-w]
    return sum(ser)         # sum of coefficients of x^0..x^{p-1}

def test_C():
    bad = []; rows = []
    for N in (1, 2, 6, 12, 60, 600):
        for p in (2, 5, 10, 20, 50, 100, 300):
            cnt = count_tuples(N, p) if p <= 300 else None
            theta = math.sqrt(N/(6*p))
            s = sum(-log(1 - exp(-theta*j)) for j in range(1, 200000))
            bound_ln = theta*p + N*s
            simple_ln = (1+pi**2)*math.sqrt(N*p/6)
            lc = math.log(cnt)
            ok = lc <= bound_ln + 1e-9 and bound_ln <= simple_ln + 1e-9
            rows.append(dict(N=N, p=p, ln_count=round(lc, 2), ln_bound=round(bound_ln, 2), ln_simple=round(simple_ln, 2), ok=ok))
            if not ok: bad.append(rows[-1])
    return dict(cases=len(rows), failures=bad, sample=rows[::7])

# ---------- D: tiny packet network, identity (D.16) ----------
def poly_add(P, Q_):
    R = dict(P)
    for k, v in Q_.items(): R[k] = R.get(k, 0) + v
    return R

def test_D(a=2, p=5, seed=1, trials=8):
    rng = random.Random(seed)
    L = 2**a; S = list(range(-L, L)); alpha = 2**(a+1); Cp0 = Cprime0(S)
    res = []; bad = 0; total = 0
    for t in S:
        if t == 0: continue
        i = v2(t)
        if i >= a: continue
        for _ in range(trials):
            zeta = rng.randint(-20, 20); T = Fraction(t + alpha*zeta)
            Rt = [[rng.randint(0, 3) for _ in (0, 1)] for _ in range(L)]      # row vertex tensors R_s(Y)
            Ct = [[rng.randint(0, 3) for _ in (0, 1)] for _ in range(L)]      # column vertex tensors C_s(X)
            Wm = [[W(S, x, y, T, Cp0) for y in range(L)] for x in range(L)]
            # direct F
            F = Fraction(0)
            for Ybits in itertools.product((0, 1), repeat=L):
                for Xbits in itertools.product((0, 1), repeat=L):
                    term = Fraction(1)
                    for s in range(L): term *= Rt[s][Ybits[s]]*Ct[s][Xbits[s]]
                    if term == 0: continue
                    for x in range(L):
                        form = sum(Wm[x][y]*Xbits[y] for y in range(L))
                        term *= (1 - form) if Ybits[x] == 0 else form
                    F += term
            # modes
            ntile = 2**(i+1)
            bit = lambda s: (s >> i) & 1
            modes = [(y0, b) for y0 in range(ntile) for b in range(p-1)]
            wt = {m: m[1]+1 for m in modes}
            def coef(x, y0, b):
                den = T - y0 + x
                return Cfun(S, T)/(Cp0*den) * (Fraction(2**(i+1))/den)**b
            def Lz(m, Xbits):
                y0, b = m
                return sum((1 if b == 0 else j**b)*Xbits[y0 + ntile*j] for j in range(L//ntile) if y0 + ntile*j < L)
            # enumerate beta tuples with total weight < p
            def gen(idx, remaining):
                if idx == len(modes): yield (); return
                w = wt[modes[idx]]
                for k in range(0, (remaining//w)+1 if remaining >= 0 else 0):
                    if k*w >= p: break
                    for rest in gen(idx+1, remaining - k*w): yield (k,)+rest
            tuples = [b_ for b_ in gen(0, p-1) if sum(k*wt[m] for k, m in zip(b_, modes)) < p]
            total_modesum = Fraction(0)
            for beta in tuples:
                prod_g = Fraction(1)
                for g in (0, 1):
                    Rg = [x for x in range(L) if bit(x) == g]; Cg = [y for y in range(L) if 1-bit(y) == g]
                    targ = [k for k, m in enumerate(modes) if bit(m[0]) == g]       # modes targeted at g
                    srcs = [k for k, m in enumerate(modes) if bit(m[0]) == 1-g]     # modes sourced at g
                    Zg = Fraction(0)
                    for Y in itertools.product((0, 1), repeat=len(Rg)):
                        for X in itertools.product((0, 1), repeat=len(Cg)):
                            Xfull = [0]*L
                            for y, xv in zip(Cg, X): Xfull[y] = xv
                            wgt = Fraction(1)
                            for x, yv in zip(Rg, Y): wgt *= Rt[x][yv]
                            for y, xv in zip(Cg, X): wgt *= Ct[y][xv]
                            if wgt == 0: continue
                            # polynomial in targeted modes
                            poly = {tuple([0]*len(modes)): Fraction(1)}
                            for x, yv in zip(Rg, Y):
                                loc = sum(Wm[x][y]*Xfull[y] for y in range(L) if bit(y) != bit(x))
                                lin = {tuple([0]*len(modes)): loc}
                                for k in targ:
                                    y0, b = modes[k]
                                    if bit(x) == bit(y0):
                                        e = [0]*len(modes); e[k] = 1; lin[tuple(e)] = coef(x, y0, b)
                                lf = {}
                                if yv == 0:
                                    lf[tuple([0]*len(modes))] = 1 - lin[tuple([0]*len(modes))]
                                    for kk, vv in lin.items():
                                        if sum(kk) > 0: lf[kk] = -vv
                                else: lf = lin
                                new = {}
                                for k1, v1 in poly.items():
                                    for k2, v2_ in lf.items():
                                        kk = tuple(u+v for u, v in zip(k1, k2))
                                        if sum(kk[m]*wt[modes[m]] for m in range(len(modes))) >= p: continue
                                        new[kk] = new.get(kk, 0) + v1*v2_
                                poly = new
                            # extract coefficient at beta restricted to targeted modes
                            key = tuple(beta[m] if m in targ else 0 for m in range(len(modes)))
                            ext = poly.get(key, Fraction(0))
                            pw = Fraction(1)
                            for k in srcs:
                                if beta[k]: pw *= Lz(modes[k], Xfull)**beta[k]
                            Zg += wgt*ext*pw
                    prod_g *= Zg
                total_modesum += prod_g
            diff = F - total_modesum
            total += 1
            ok = (v2f(diff) >= p) if diff != 0 else True
            if not ok: bad += 1
            res.append((t, ok))
    return dict(a=a, p=p, node_trials=total, failures=bad, tuples_example=len(tuples))

if __name__ == "__main__":
    which = sys.argv[1]
    out = {}
    if which == "AB":
        out = test_AB(); print("AB", out)
    elif which == "C":
        out = test_C(); print("C", {k: v for k, v in out.items() if k != 'sample'}); print(out['sample'])
    elif which == "D":
        out = [test_D(2, p, seed=p) for p in (3, 5)]
        for o in out: print("D", o, flush=True)
    json.dump(out, open(f"modes_{which}.json", "w"), indent=1, default=str)
