import json, math
from math import isqrt, log2

EPS = 1/(128*1024)

def lse(*xs):
    m = max(xs)
    return m + log2(sum(2**(x-m) for x in xs))

def simulate(lam, C):
    """log2-domain worst-case recursion, every quantity normalized by s (so 'logp' = log2(p/s), 'logM' = log2(M/s)).
    h = ceil(3M/u) ~ 3M/u (M is astronomically large, the ceiling is negligible)."""
    sqrt_lam = math.sqrt(lam)
    logH = -log2(math.floor(sqrt_lam))                    # H/s
    recs = []
    a_prev = 0
    u_sum = 0
    logp = log2(C)                                        # P0 <= C s
    d = 0
    while True:
        logM = log2(C) - 3*d                              # M_d <= C s 8^{-d}
        if logM <= logH: break                            # leaf level
        u = math.floor(EPS*lam/2**d)
        if u < 1:
            return recs, 'u<1 at depth %d' % d
        u_sum += u
        a = 2*u_sum
        logh = logM + log2(3/u)                           # h/s
        c_d = (logp - a_prev)/log2(lam)                   # claim 1 exponent: p/s = lam^c 2^{a_{d-1}}
        log_Dmin = a - u + 1                              # smallest D_t with q_t > 0 (i = u-1)
        rho = logp + log2(u) - (logH + log_Dmin)          # log2 of p u/(H D_tmin) (worst M just above H)
        # child precision at the worst node (i = u-1, M = H): p_t = p + 8 h D_t + 8 M (a+1)
        logh_min = logH + log2(3/u)
        p_t_min = lse(logp, 3 + logh_min + log_Dmin, 3 + logH + log2(a+1))
        # child precision at the largest node (i = 0, M = M_d): feeds depth d+1
        child_max = lse(logp, 3 + logh + a, 3 + logM + log2(a+1))
        recs.append(dict(d=d, u=u, a=a, logM=logM, c_exponent=c_d, log2_rho=rho, bits_log2=logp,
                         log2_pt_over_MDu=p_t_min - (logH + log_Dmin - log2(u))))
        logp = child_max
        a_prev = a
        d += 1
        if d > 200: break
    return recs, 'ok'

def summarize(lam, C):
    recs, status = simulate(lam, C)
    if status != 'ok' or not recs: return dict(lam=lam, C=C, status=status)
    return dict(lam=lam, C=C, status=status, depths=len(recs),
                max_c_exponent=max(r['c_exponent'] for r in recs),
                max_log2_rho=max(r['log2_rho'] for r in recs),
                max_pt_over_MDu=2**max(r['log2_pt_over_MDu'] for r in recs),
                max_bits_over_lam=1+max(r['bits_log2'] for r in recs)/lam, final_bits_log2_rel_s=recs[-1]['bits_log2'])

def threshold_rho(C, lo=1e6, hi=1e16):
    # first lam where rho <= 1 (p u/(H D_tmin) <= 1) at every depth, found on a grid then verified above
    x = lo; grid = []
    while x < hi: grid.append(int(x)); x *= 1.05
    ok = lambda L: (lambda s: s.get('status') == 'ok' and s['max_log2_rho'] <= 0)(summarize(L, C))
    fails = [g for g in grid if not ok(g)]
    last_fail = max(fails) if fails else lo
    a_, b_ = last_fail, min(g for g in grid if g > last_fail)
    while b_ - a_ > 1:
        m = (a_+b_)//2
        if ok(m): b_ = m
        else: a_ = m
    bad = sum(1 for k in range(5000) if not ok(int(b_*(1+0.01*k))))
    return b_, bad

if __name__ == "__main__":
    out = {}
    for C in (12, 144):
        rows = []
        for e in (7, 8, 9, 10, 11, 12, 14, 18, 30, 60, 150, 300):
            s = summarize(int(10**e), C); rows.append(s)
        out[f"C{C}"] = dict(rows=rows)
        for s in rows:
            if s.get('status') == 'ok' and 'depths' in s:
                print(f"C={C} lam=1e{round(math.log10(s['lam']))}: depths {s['depths']}, max c-exponent {s['max_c_exponent']:.3f}, max log2(rho) {s['max_log2_rho']:.1f}, max p_t/(M D_t/u) {s['max_pt_over_MDu']:.2f}, bits/lam {s['max_bits_over_lam']:.4f}")
            else: print(f"C={C} lam=1e{round(math.log10(s['lam']))}: {s['status']}")
        t, bad = threshold_rho(C)
        out[f"C{C}"]['lambda1_rho<=1'] = t; out[f"C{C}"]['failures_above'] = bad
        print(f"C={C}: lambda_1 (p u/(H D_tmin) <= 1 at every depth) = {t:,}; failures above (5000 samples): {bad}")
    # literal (D.5) condition u >= lam^(4/5) at last depth: needs lam >= (C^(1/3)/eps)^30
    for C in (12, 144):
        print(f"literal u>=lam^(4/5) at last level: lam >= 2^{30*math.log2(C**(1/3)/EPS):.0f} (C={C})")
    json.dump(out, open("d11_results.json", "w"), indent=1, default=str)
