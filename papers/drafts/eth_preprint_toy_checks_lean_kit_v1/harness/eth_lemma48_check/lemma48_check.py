import json, math
from math import isqrt, log2, log, exp
from fractions import Fraction

def params(lam, beta):
    nu = (lam-1).bit_length()                        # ceil(log2 lam)
    r = isqrt(lam)//(nu*nu)
    Q = lam//(128*nu)
    R = (beta+3)*(isqrt(lam-1)+1)
    return nu, r, Q, R

def checks(lam, beta):
    """all numerical hypotheses of Lemma 4.8 / 4.7 at lambda (n = 2^(lam-1)+1, the smallest n with ceil(log2 n) = lam)."""
    nu, r, Q, R = params(lam, beta)
    out = dict(lam=lam, beta=beta, nu=nu, r=r, Q=Q, R=R)
    out['r>=2'] = r >= 2
    out['R>=32'] = R >= 32
    out['6R<=Q'] = 6*R <= Q
    out['Q>R'] = Q > R
    if r < 2 or Q <= R:
        out['ok_all'] = False; return out
    # D <= 2^(lam/128): log2 D = 2 Q log2 r
    out['D<=2^(lam/128)'] = 2*Q*log2(r) <= lam/128
    # balance: 2(b+w) D^2 <= n with b = w = lam^beta ; 2 Q r^2 <= n ; n >= 2^(lam-1)
    lg_n = lam-1
    lhs = log2(4) + beta*log2(lam) + 4*Q*log2(r)
    out['2(b+w)D^2<=n'] = lhs <= lg_n
    out['2Qr^2<=n'] = log2(2*Q*r*r) <= lg_n
    # interval
    mu = Fraction(Q*(r-1), 2*r)
    A0 = math.floor(mu - Fraction(R-1, 2))
    out['I_in_[0,Q]'] = (A0 >= 0) and (A0+R-1 <= Q)
    # contains every integer within R/4 of mu
    lo = math.ceil(mu - Fraction(R, 4)); hi = math.floor(mu + Fraction(R, 4))
    out['I_contains_mu+-R/4'] = (A0 <= lo) and (A0+R-1 >= hi)
    out['Q/4<=mu<=Q/2'] = (Fraction(Q, 4) <= mu <= Fraction(Q, 2))
    # tail chain (in log2 units)
    exponent = R*R/(8*Q)                                  # ln of Hoeffding
    c1 = 2*exp(-exponent) if exponent < 700 else 0.0
    out['R^2/(8Q)>=16(beta+3)^2 nu'] = (R*R)/(8*Q) >= 16*(beta+3)**2*nu
    out['2e^{-16(b+3)^2 nu}<=2^{-(b+2)nu}'] = (log(2) - 16*(beta+3)**2*nu) <= -(beta+2)*nu*log(2)
    out['2^{-(b+2)nu}<=lam^{-(b+2)}'] = (2**nu >= lam)
    out['lam^{-(b+2)}<=1/(b r^2 lam)'] = (beta+2)*log2(lam) >= beta*log2(lam) + log2(r*r) + log2(lam) - 1e-12   # b <= lam^beta, r^2 <= lam
    out['tau<=1/2'] = (1/(r*lam) <= 0.5)
    ok = all(v for k, v in out.items() if isinstance(v, bool))
    out['ok_all'] = ok
    return out

def lhs418(lam, beta):
    nu, r, Q, R = params(lam, beta)
    if r < 2 or Q <= R: return None
    t1 = (R/Q)*log2(2*Q/R)
    t2 = (1/(r*lam))*(1 + 2*Q*log2(r))
    t3 = 1/r
    tot = t1+t2+t3
    return tot, tot/(nu*nu/math.sqrt(lam)), nu

def threshold(beta, lo=10, hi=10**16):
    """least lam0 such that checks hold at all sampled lam >= lam0 (monotone-ish; verified by dense sampling above)."""
    # find via scanning on a geometric grid then bisect the last failing->passing transition
    grid = []; x = float(lo)
    while x < hi: grid.append(int(x)); x *= 1.02
    fails = [g for g in grid if not checks(g, beta)['ok_all']]
    last_fail = max(fails) if fails else lo
    # refine between last_fail and next grid point
    nxt = min(g for g in grid if g > last_fail)
    a, b = last_fail, nxt
    while b - a > 1:
        m = (a+b)//2
        if checks(m, beta)['ok_all']: b = m
        else: a = m
    # verify no failure at denser sampling above
    bad = 0
    for k in range(20000):
        L = int(b*(1+0.01*k))
        if not checks(L, beta)['ok_all']: bad += 1
    return b, bad

if __name__ == "__main__":
    out = {}
    out['thresholds'] = {}
    for beta in (1, 2, 3, 4, 5, 6, 8, 10):
        lam0, bad = threshold(beta)
        c = checks(lam0, beta)
        out['thresholds'][beta] = dict(lam0=lam0, failures_above_sampled=bad, nu=c['nu'], r=c['r'], Q=c['Q'], R=c['R'])
        print(f"beta={beta}: lambda_0 = {lam0:,} (n >= 2^{lam0-1:,} -> checks hold above), nu={c['nu']}, r={c['r']}, Q={c['Q']:,}, R={c['R']:,}; failures above (20000 samples): {bad}", flush=True)
    # individual thresholds for beta = 6
    ind = {}
    for key in ['r>=2', 'R>=32', '6R<=Q', '2(b+w)D^2<=n', '2Qr^2<=n', 'I_in_[0,Q]', 'I_contains_mu+-R/4']:
        lam = 10; ok_from = None
        grid = [int(1.05**k) for k in range(100, 1000) if int(1.05**k) < 10**17]
        fails = [g for g in grid if not checks(g, 6).get(key, False)]
        ind[key] = max(fails) if fails else None
    out['last_failing_lambda_beta6'] = ind
    print("last failing lambda (beta=6, grid) by individual check:", ind)
    # (4.18) ratio
    out['ratio418'] = {}
    for beta in (1, 3, 6):
        rows = []
        for e in (10, 12, 14, 18, 24, 40, 70, 100):
            lam = 10**e
            v = lhs418(lam, beta)
            if v: rows.append((e, round(v[1], 2), v[2]))
        out['ratio418'][beta] = rows
        print(f"(4.18) ratio LHS/(nu^2/sqrt(lam)) for beta={beta}: {rows}")
        print("   hand asymptote 64(beta+3)+1 =", 64*(beta+3)+1)
    json.dump(out, open("lemma48_results.json", "w"), indent=1, default=str)
