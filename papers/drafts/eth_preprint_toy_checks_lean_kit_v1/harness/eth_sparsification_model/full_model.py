"""Per-n log2-cost model of the full #k-SAT algorithm (Prop 6.4), from Sections 5, 6, Lemma 4.8, Appendix A.
All terms depend on n only through lambda = ceil(log2 n) (n ~ 2^lambda). See DEVIATIONS.md."""
import math, json, sys
from math import isqrt, log2, log

def H2(x):
    return 0.0 if x <= 0 or x >= 1 else -x*log2(x) - (1-x)*log2(1-x)

def tree_params(lam, k):
    nu = (lam-1).bit_length()
    s = isqrt(lam)//(nu*nu)
    if s < 2: return None
    Gam = 2*(3**(k-1)-1)
    M = 1
    while M < Gam: M *= 2
    while True:
        C = 4*sum((3*M)**j for j in range(0, k-1))
        h = (4*C*M-1).bit_length()          # ceil(log2(4CM))
        if Gam*h*s <= M: break              # Gam*h <= sigma*M with sigma=1/s
        M *= 2
    B = 2*sum(M**j for j in range(0, k))
    return nu, s, M, B

def full_model(lam, k):
    t = tree_params(lam, k)
    if t is None: return None
    nu, s, M, B = t
    sigma = 1/s
    mu = lam + (B.bit_length()) + 1                 # floor(log2 m)+1 with m <= B n
    D0 = 320000*B*B*mu**3
    P = 20000*B*B*mu*mu
    w = k*max(D0, P)                                # scope: union of <= max(D0,P) clauses' variables
    b0 = -(-(6*w+1)*isqrt(lam-1)+1)//1 if False else (6*w+1)*(isqrt(lam-1)+1)   # ceil((M_inc/n) sqrt(lam)), M_inc/n <= 6w+1
    beta = max(1, math.ceil(log(b0)/log(lam)))
    r = isqrt(lam)//(nu*nu)
    Q = lam//(128*nu)
    R = (beta+3)*(isqrt(lam-1)+1)
    if r < 2 or Q <= R: return dict(lam=lam, k=k, valid=False, nu=nu, s=s, M=M, B=B, beta=beta, r=r, Q=Q, R=R)
    tau = 1/(r*lam)
    nfrac = 1 - 1/math.sqrt(lam)                    # n'/n for branching over |S| <= n/sqrt(lam) variables
    dH_over_n = k*R*(6 + 2)                         # k R (mtest + 2(l-1)) / n with mtest <= 6n, l = n+1
    delta = dH_over_n/(Q*nfrac)
    e1 = (H2(delta)+delta) if delta <= 2/3 else log2(3)
    e2 = 2*tau*(1 + 2*Q*log2(r))
    e3 = 2/r
    branch = 1/math.sqrt(lam)
    inner = e1+e2+e3
    total = sigma + branch + nfrac*inner
    return dict(lam=lam, k=k, valid=True, nu=nu, s=s, M=M, B=B, beta=beta, r=r, Q=Q, R=R, delta=delta,
                sigma=sigma, branch=branch, e1=e1, e2=e2, e3=e3, total=total,
                six_R_le_Q=(6*R <= Q), log2_D0=log2(D0), log2_w=log2(w), log2_b0=log2(b0))

def crossover(k):
    lam = 2; x = 10.0
    prev = None
    # log grid from 1e3 up
    pts = []
    x = 1e3
    while x < 1e20:
        m = full_model(int(x), k)
        if m and m.get('valid'): pts.append(m)
        x *= 1.2
    first = next((m for m in pts if m['total'] < 1), None)
    if not first: return None, pts
    i = pts.index(first)
    lo, hi = pts[i-1]['lam'] if i > 0 else 1000, first['lam']
    while hi - lo > 1:
        mid = (lo+hi)//2
        m = full_model(mid, k)
        if m and m.get('valid') and m['total'] < 1: hi = mid
        else: lo = mid
    # recross check
    bad = 0
    for j in range(5000):
        m = full_model(int(hi*(1+0.002*j)), k)
        if m and m.get('valid') and m['total'] >= 1: bad += 1
    return (hi, full_model(hi, k), bad), pts

if __name__ == "__main__":
    out = {}
    for k in (2, 3, 4):
        res, pts = crossover(k)
        if res is None:
            print("k", k, "no crossover found"); continue
        hi, m, bad = res
        out[f"k{k}"] = dict(crossover_lambda=hi, model=m, recross_samples=bad,
                            first_valid=pts[0], scan=[{kk: v for kk, v in p.items()} for p in pts[::5]])
        print(f"k={k}: crossover lambda* = {hi:,}  (n ~ 2^{hi:,}); recross samples {bad}")
        print("  ", {kk: (round(v, 5) if isinstance(v, float) else v) for kk, v in m.items()})
        print("   first valid scan point:", {kk: (round(v, 4) if isinstance(v, float) else v) for kk, v in pts[0].items() if kk in ('lam','beta','r','Q','R','delta','total','sigma')})
    json.dump(out, open("full_model_results.json", "w"), indent=1, default=str)
