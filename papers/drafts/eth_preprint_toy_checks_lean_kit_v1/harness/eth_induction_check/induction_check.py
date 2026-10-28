import json, math
from math import log2, floor, ceil, sqrt
EPS = 1/(128*1024); R_SYM = 64

def invariants(lam, C):
    """returns (ok, details) at every active depth; all in log2 domain, normalized where needed."""
    logs = float(lam)                                      # log2 s  (s = 2^lam) -- used only in comparisons with small numbers
    logH = logs - log2(floor(sqrt(lam)))
    logDelta = 0.9*lam + 0.0                               # ceil(s^{9/10})
    d = 0; u_sum = 0; recs = []
    while True:
        logM = log2(C) + logs - 3*d
        if logM <= logH: break
        u = floor(EPS*lam/2**d)
        if u < 1: return False, dict(reason='u<1 at depth %d' % d, recs=recs)
        u_sum += u; a = 2*u_sum
        logL = a; logDarr = 2*a*log2(R_SYM)                # D_arr = r^{2a}
        # use M_min = H (worst case) for the (D.6) tests
        c = {}
        c['D6a: H >= 2 Darr^2 Delta'] = logH >= 1 + 2*logDarr + logDelta
        c['D6b: H >= L Darr'] = logH >= logL + logDarr
        c['D6c: 2L <= Delta'] = 1 + logL <= logDelta
        c['L,Darr <= s^(1/1000)'] = max(logL, logDarr) <= lam/1000
        c['a <= 4 eps lam'] = a <= 4*EPS*lam + 1e-9
        c['1<=u, 2u<=a'] = (u >= 1) and (2*u <= a)
        c['M >= u (M>H>=u)'] = logH >= log2(u)
        # interpolation points M(2L-1)+1 < 2^(4 lam) (residue field F_{2^e}, e = 4 lam)
        c['points<2^(4 lam)'] = log2(C) + logs + a + 1 < 4*lam
        c['u<=lam^(4/5) literal ok'] = u >= lam**0.8
        recs.append(dict(d=d, u=u, a=a, **c))
        d += 1
        if d > 200: break
    keys = [k for k in recs[0] if k not in ('d', 'u', 'a')] if recs else []
    # the literal condition is reported separately (not required)
    required = [k for k in keys if k != 'u<=lam^(4/5) literal ok']
    ok = all(r[k] for r in recs for k in required)
    return ok, dict(depths=len(recs), recs=recs, failing=sorted({k for r in recs for k in required if not r[k]}),
                    literal_ok=all(r['u<=lam^(4/5) literal ok'] for r in recs))

def bisect_threshold(C, lo=1e4, hi=1e12):
    ok = lambda L: invariants(L, C)[0]
    x = lo; grid = []
    while x < hi: grid.append(int(x)); x *= 1.03
    fails = [g for g in grid if not ok(g)]
    last = max(fails) if fails else grid[0]
    a, b = last, min(g for g in grid if g > last)
    while b - a > 1:
        m = (a+b)//2
        if ok(m): b = m
        else: a = m
    bad = sum(1 for k in range(3000) if not ok(int(b*(1+0.01*k))))
    return b, bad

def toy_tuple_count(M=8, a=2, u=1, p=4, nmodes_per_weight=None):
    L = 2**a; i = 0                                        # worst node: odd t
    D = L // 2**i
    h = -(-3*M//u)
    pt = p + 8*h*D + 8*M*(a+1)
    N = 6*M//D                                              # variables per weight (D.13), D = L/2^i
    # number of tuples with sum w beta < pt over N variables of each weight w = 1..pt-1: coefficient sums of prod (1-x^w)^(-N)
    ser = [0]*(pt); ser[0] = 1
    for w in range(1, pt):
        for _ in range(N):
            for k in range(w, pt): ser[k] += ser[k-w]
    return dict(M=M, L=L, u=u, p=p, h=h, p_t=pt, vars_per_weight=N, log10_tuples=round(math.log10(sum(ser)), 1))

if __name__ == "__main__":
    out = {}
    for C in (12, 144):
        t, bad = bisect_threshold(C)
        ok, det = invariants(t, C)
        print(f"C={C}: lambda_2 (all numerical invariants hold at every active depth) = {t:,}; failures above (3000 samples) = {bad}; depths {det['depths']}; literal u>=lam^(4/5) also satisfied: {det['literal_ok']}")
        # which invariant binds: examine just below threshold
        ok2, det2 = invariants(int(t*0.9), C)
        print("   just below (0.9 lambda_2): failing =", det2.get('failing') or det2.get('reason'))
        out[f"C{C}"] = dict(lambda_2=t, failures_above=bad, failing_below=det2.get('failing') or det2.get('reason'))
    out['toy'] = toy_tuple_count()
    print("toy tuple count:", out['toy'])
    # also with a more generous toy (M = 64, a = 3, u = 1)
    out['toy2'] = toy_tuple_count(M=64, a=3, u=1, p=4)
    print("toy2 tuple count:", out['toy2'])
    json.dump(out, open("induction_results.json", "w"), indent=1, default=str)
