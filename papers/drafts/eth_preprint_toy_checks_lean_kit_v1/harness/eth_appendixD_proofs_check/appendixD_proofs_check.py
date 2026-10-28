import itertools, json, math, random, sys
from fractions import Fraction
from math import comb, ceil, log2
import numpy as np

def v2(n):
    n = abs(int(n)); assert n != 0
    return (n & -n).bit_length() - 1

def v2f(x):
    x = Fraction(x)
    if x == 0: return 10**9
    return v2(x.numerator) - v2(x.denominator)

# ================= Lemma D.4 =================
def pmul(a, b):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i+j] += x*y
    return out

def test_D4(amax=4):
    res = []
    for a in range(1, amax+1):
        L = 2**a; S = list(range(-L, L)); alpha = 2**(a+1)
        Cp0 = 1
        for q in S:
            if q != 0: Cp0 *= (0-q)
        v0 = v2(Cp0)
        eq_val = all(v2(math.prod(t-q for q in S if q != t)) == v0 for t in S)
        cache = {}
        def prodpoly(t, s):                     # prod_{q != s} (t - q + alpha z), integer coeffs low->high in z
            if (t, s) not in cache:
                P = [1]
                for q in S:
                    if q != s: P = pmul(P, [t-q, alpha])
                cache[(t, s)] = P
            return cache[(t, s)]
        nonint = 0; notdiv2 = 0; checked = 0; w0_ok = True
        for t in S:
            for x in range(L):
                for y in range(L):
                    s = y - x
                    P = prodpoly(t, s)          # = C(t+alpha z)/(t+alpha z - s) numerator; W = P / C'(0)
                    for c in P:
                        checked += 1
                        if c == 0: continue
                        # 2-adic integrality of c/C'(0) (ring O = Z_(2)[U]/(f): odd denominators allowed)
                        if v2(c) < v0: nonint += 1
                        elif s != t and v2(c) < v0 + 1: notdiv2 += 1
        # W(0) = I and degree 2L-1
        for x in range(L):
            for y in range(L):
                s = y-x
                val0 = 1
                for q in S:
                    if q != s: val0 *= (0-q)
                want = Cp0 if s == 0 else 0
                if val0 != want: w0_ok = False
        deg_ok = all(len(prodpoly(0, y-x)) - 1 == 2*L-1 for x in range(L) for y in range(L))
        res.append(dict(a=a, L=L, v2_Cprime_const=eq_val, W0_is_I=w0_ok, deg_2L_1=deg_ok, coeffs_checked=checked, nonintegral=nonint, not_div_by_2_when_y_minus_x_ne_t=notdiv2))
    return res

# ================= Lemma D.5 =================
def test_valuations():
    bad = []; cnt = 0; worst = 0
    for a in range(1, 8):
        L = 2**a; S = list(range(-L, L))
        for u in range(1, a+1):
            for h in (1, 2, 5, 11):
                qf = lambda i: h*max(0, u-i)
                for t in S:
                    if t == 0: continue
                    i = v2(t)
                    if i >= u: continue
                    D = L // 2**i
                    exact = sum(qf(v2(q))*(v2(q) - v2(t-q)) for q in S if q != 0 and q != t)
                    closed = D*sum(Fraction(j, 2**j)*(qf(i+j)-qf(i)) for j in range(1, a-i+1))
                    cnt += 1
                    if Fraction(exact) != closed: bad.append(('closed_form', a, u, h, t, exact, float(closed)))
                    if exact < -6*D*h: bad.append(('bound', a, u, h, t, exact, -6*D*h))
                    worst = max(worst, -exact/(D*h))
    return dict(cases=cnt, failures=bad[:5], n_fail=len(bad), worst_ratio_neg_v2_over_Dh=round(worst, 3))

def series_recip_E(t, S, mult, alpha, qt):
    """series of 1/E_t(t+alpha z) up to z^(qt-1), Fractions."""
    ser = [Fraction(1)] + [Fraction(0)]*(qt-1)
    for q in S:
        if q == 0 or q == t or mult(q) == 0: continue
        c = Fraction(alpha, t-q)
        m = mult(q)
        # (1 + c z)^(-m) = sum_k binom(-m,k) c^k z^k
        fac = [Fraction(1)]
        coef = Fraction(1)
        for k in range(1, qt):
            coef = coef*(-m-k+1)/k
            fac.append(coef*c**k)
        new = [Fraction(0)]*qt
        for i, x in enumerate(ser):
            if x == 0: continue
            for j, y in enumerate(fac):
                if i+j >= qt: break
                new[i+j] += x*y
        ser = new
    return ser

def recover(Fcoef, a, u, M, p, margin_h=8, margin_M=8, rng=None):
    L = 2**a; S = list(range(-L, L)); alpha = 2**(a+1)
    h = -(-3*M//u)
    mult = lambda q: h*max(0, u - v2(q)) if q != 0 else 0
    total = Fraction(0)
    for t in S:
        if t == 0: continue
        i = v2(t); qt = h*max(0, u-i)
        if qt <= 0: continue
        D_t = L // 2**i
        pt = p + margin_h*h*D_t + margin_M*M*(a+1)
        mod = 2**pt
        # Taylor coefficients of F(t+alpha z) through z^(qt-1), reduced mod 2^pt
        deg = len(Fcoef)-1
        c = []
        for j in range(qt):
            s = 0
            for ii in range(j, deg+1):
                s += Fcoef[ii]*comb(ii, j)*t**(ii-j)
            c.append((s*alpha**j) % mod)
        recip = series_recip_E(t, S, mult, alpha, qt)
        g = [sum(Fraction(c[k])*recip[j-k] for k in range(j+1)) for j in range(qt)]
        # residues of g mod 2^pt (odd denominators), random lifts
        lifts = []
        for x in g:
            assert x.denominator % 2 == 1
            r = (x.numerator * pow(x.denominator, -1, mod)) % mod
            if rng is not None: r += mod*rng.randint(-3, 3)
            lifts.append(r)
        ev = sum(Fraction(lifts[j])*Fraction(-t, alpha)**j for j in range(qt))
        Et0 = Fraction(1)
        for q in S:
            if q == 0 or q == t or mult(q) == 0: continue
            Et0 *= (Fraction(0-q, t-q))**mult(q)
        total += Et0*ev
    return total, h

def test_D5(trials_per=6, seed=11):
    rng = random.Random(seed); rows = []; fails = {}; sumq_ok = True
    for a in (1, 2, 3):
        L = 2**a
        for u in range(1, a+1):
            for M in sorted({u, u+1, 2*u+1, 5}):
                if M < u: continue
                h = -(-3*M//u)
                sq = sum(h*max(0, u-v2(t)) for t in range(-L, L) if t != 0)
                if not sq > M*(2*L-1): sumq_ok = False
                for p in (1, 3, 8):
                    for _ in range(trials_per):
                        deg = M*(2*L-1)
                        F = [rng.randint(-50, 50) for _ in range(deg+1)]
                        for (mh, mM) in ((8, 8), (6, 4), (0, 0)):
                            tot, _ = recover(F, a, u, M, p, mh, mM, rng)
                            diff = tot - F[0]
                            ok = (v2f(diff) >= p) if diff != 0 else True
                            ok = ok and (tot.denominator % 2 == 1)
                            key = (mh, mM)
                            fails.setdefault(key, [0, 0])
                            fails[key][1] += 1
                            if not ok: fails[key][0] += 1
    return dict(sum_q_gt_M_2L_minus_1=sumq_ok, margins={f"{k[0]}hD+{k[1]}M(a+1)": f"fail {v[0]}/{v[1]}" for k, v in fails.items()})

# ================= Lemma D.3 =================
def rand_bipartite(V, M, Delta, rng):
    rows = []; cols = []
    deg_r = [0]*V; deg_c = [0]*V
    while len(rows) < M:
        u = rng.randrange(V); v = rng.randrange(V)
        if deg_r[u] < Delta and deg_c[v] < Delta:
            deg_r[u] += 1; deg_c[v] += 1; rows.append(u); cols.append(v)
    return np.array(rows), np.array(cols)

def test_D3(r, a, V, seed=0):
    rng = random.Random(seed)
    L = 2**a; K = r**a; Darr = K*K; Delta = 2*L
    M = 2*Darr*Darr*Delta
    conds = (M >= 2*Darr*Darr*Delta, M >= L*Darr, 2*L <= Delta)
    er, ec = rand_bipartite(V, M, Delta, rng)
    # label arrays; -1 = unfixed
    lr = -np.ones(V, dtype=np.int64); lc = -np.ones(V, dtype=np.int64)
    inc_r = [[] for _ in range(V)]; inc_c = [[] for _ in range(V)]
    for e in range(M): inc_r[er[e]].append(e); inc_c[ec[e]].append(e)
    def fac_row(v, cand):                        # row-side agreement prob of each edge e' with an edge on vertex v labelled cand
        lab = lr[er]
        return np.where(er == v, 1.0, np.where(lab >= 0, (lab == cand).astype(float), 1.0/K))
    def fac_col(v, cand):
        lab = lc[ec]
        return np.where(ec == v, 1.0, np.where(lab >= 0, (lab == cand).astype(float), 1.0/K))
    order = [("r", v) for v in range(V)] + [("c", v) for v in range(V)]
    # initial exact expectation (all unfixed)
    nsr = sum(len(x)**2 for x in inc_r); nsc = sum(len(x)**2 for x in inc_c)
    nboth = M   # diagonal
    # pairs sharing a row vertex (and maybe also col vertex): count exactly by brute force on pair structure
    same_r = nsr; same_c = nsc
    both = sum(1 for e in range(M) for e2 in set(inc_r[er[e]]) if ec[e2] == ec[e])    # ordered pairs sharing both endpoints (incl. diagonal)
    only_r = same_r - both; only_c = same_c - both; none = M*M - same_r - same_c + both
    EPhi0 = both + (only_r + only_c)/K + none/Darr - M*M/Darr
    for side, v in order:
        I = inc_r[v] if side == "r" else inc_c[v]
        if not I: continue
        best = None
        for cand in range(K):
            tot = 0.0
            for e in I:
                if side == "r":
                    fr = fac_row(v, cand); fc = np.where(ec == ec[e], 1.0, np.where(lc[ec] >= 0, (lc[ec] == lc[ec[e]]).astype(float) if lc[ec[e]] >= 0 else 1.0/K, 1.0/K))
                else:
                    fc = fac_col(v, cand); fr = np.where(er == er[e], 1.0, np.where(lr[er] >= 0, (lr[er] == lr[er[e]]).astype(float) if lr[er[e]] >= 0 else 1.0/K, 1.0/K))
                p_ = fr*fc
                inI = (er == v) if side == "r" else (ec == v)
                tot += 2*p_[~inI].sum() + p_[inI].sum()
            if best is None or tot < best[0] - 1e-9: best = (tot, cand)
        (lr if side == "r" else lc)[v] = best[1]
    # realized
    digits = lambda x, i: (x // r**i) % r
    pairlab = lr[er]*K + lc[ec]
    X = np.bincount(pairlab, minlength=Darr)
    Phi = float(((X - M/Darr)**2).sum())
    maxload = int(X.max()); Hpad = -(-maxload//L)*L
    # packets
    packets = 0; slot_ok = True; orient_ok = True; edges_placed = 0
    edge_slot = {}
    labels_by_class = {}
    for gam in range(Darr):
        rl, cl = gam//K, gam % K
        cls = tuple(sorted((digits(rl, i), digits(cl, i))) for i in range(a))
        cls = tuple(tuple(x) for x in cls)
        labels_by_class.setdefault(cls, []).append(gam)
    edges_of = {gam: list(np.nonzero(pairlab == gam)[0]) for gam in range(Darr)}
    pack_list = []
    for cls, gams in labels_by_class.items():
        uneq = [i for i in range(a) if cls[i][0] != cls[i][1]]; eq = [i for i in range(a) if i not in uneq]
        ap = len(uneq); ncopy = 2**(a-ap)
        npk = Hpad // ncopy
        for pk in range(npk):
            slots = [None]*L
            for gam in gams:
                rl, cl = gam//K, gam % K
                o = [1 if digits(rl, i) > digits(cl, i) else 0 for i in uneq]
                for c in range(ncopy):
                    s = sum(o[j]*2**uneq[j] for j in range(ap)) + sum(((c >> k) & 1)*2**eq[k] for k in range(len(eq)))
                    idx = pk*ncopy + c
                    lst = edges_of[gam]
                    slots[s] = lst[idx] if idx < len(lst) else None
            pack_list.append((cls, uneq, slots))
    packets = len(pack_list)
    placed = set()
    for cls, uneq, slots in pack_list:
        # property (2): orientation bits match edges
        for s, e in enumerate(slots):
            if e is None: continue
            if e in placed: slot_ok = False
            placed.add(e)
            for i in uneq:
                orient_bit = (s >> i) & 1
                real = 1 if digits(lr[er[e]], i) > digits(lc[ec[e]], i) else 0
                if orient_bit != real: orient_ok = False
    all_edges_once = (len(placed) == M)
    # property (3): real ports per coordinate/symbol
    max_sym = 0
    for i in range(a):
        for g in range(r):
            nr = int(((lr[er] // r**i) % r == g).sum()); nc = int(((lc[ec] // r**i) % r == g).sum())
            max_sym = max(max_sym, nr, nc)
    return dict(r=r, a=a, L=L, Darr=Darr, Delta=Delta, M=M, V=V, conds=conds, EPhi0=round(EPhi0, 1), bound_2MDelta=2*M*Delta,
                Phi_realized=round(Phi, 2), maxload=maxload, M_over_Darr=round(M/Darr, 2), Hpad=Hpad, Hpad_le_3M_over_Darr=Hpad <= 3*M/Darr,
                packets=packets, packets_bound_3M_over_L=3*M/L, packets_ok=packets <= 3*M/L, all_edges_placed_once=all_edges_once and slot_ok,
                orientation_ok=orient_ok, max_real_ports_per_symbol=max_sym, bound_3M_over_r=3*M/r, ports_ok=max_sym <= 3*M/r,
                EPhi0_le_2MDelta=EPhi0 <= 2*M*Delta)

if __name__ == "__main__":
    which = sys.argv[1]
    out = {}
    if which == "D4":
        out['D4'] = test_D4(4)
        for x in out['D4']: print("D4", x)
    elif which == "val":
        out['val'] = test_valuations(); print("D10 valuations", out['val'])
    elif which == "D5":
        out['D5'] = test_D5(); print("D5", out['D5'])
    elif which == "D3":
        out['D3'] = []
        for (r, a, V, seed) in [(2, 1, 60, 0), (3, 1, 220, 1), (2, 2, 1200, 2)]:
            d3 = test_D3(r, a, V, seed); out['D3'].append(d3); print("D3", d3, flush=True)
    json.dump(out, open(f"appendixD_proofs_{which}.json", "w"), indent=1, default=str)
