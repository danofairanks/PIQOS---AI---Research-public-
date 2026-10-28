import math, json
from math import isqrt, log2

def H2(x):
    return 0.0 if x <= 0 or x >= 1 else -x*log2(x) - (1-x)*log2(1-x)

def params(lam):
    nu = (lam-1).bit_length()          # ceil(log2 lam)
    r = isqrt(lam)//(nu*nu)
    Q = lam//(128*nu)
    R = 4*(isqrt(lam-1)+1)             # 4*ceil(sqrt(lam))
    return nu, r, Q, R

def model(lam):
    nu, r, Q, R = params(lam)
    if r < 2 or Q < 1:
        return None
    delta = 3*R/Q
    e1 = (H2(delta)+delta) if delta <= 2/3 else log2(3)
    tau = 1/(r*lam)
    log2D = 2*Q*log2(r)
    e2 = 2*tau*(1+log2D)               # log2(2D+1) ~ 1+log2 D
    e3 = 2/r
    return dict(lam=lam, nu=nu, r=r, Q=Q, R=R, delta=delta, e1=e1, e2=e2, e3=e3, total=e1+e2+e3,
                six_R_le_Q=(6*R <= Q), step5_tail=(R*R/(8*Q) >= 256*nu))

if __name__ == "__main__":
    out = {}
    # first valid lambda
    lam = 2
    while model(lam) is None: lam += 1
    out["first_valid_lambda"] = lam
    # scan: log grid
    rows = []
    x = lam
    while x < 10**15:
        m = model(int(x))
        if m: rows.append(m)
        x = x*1.15 if x < 10**6 else x*1.25
    out["scan"] = rows
    # smallest lambda where total < 1, found by bracketing then local scan, then check stays < 1 after
    prev = None
    cross = None
    for m in rows:
        if m["total"] < 1:
            cross = m; break
    out["first_scan_point_below_1"] = cross
    # refine by bisection on the grid interval (non-monotone possible; verify)
    if cross:
        i = rows.index(cross)
        lo = rows[i-1]["lam"]; hi = cross["lam"]
        while hi - lo > 1:
            mid = (lo+hi)//2
            m = model(mid)
            if m and m["total"] < 1: hi = mid
            else: lo = mid
        out["refined_crossover_lambda"] = hi
        out["refined_model_at_crossover"] = model(hi)
        # check no re-crossing above: sample 20000 points above
        bad = 0
        for k in range(20000):
            L = int(hi*(1+k*0.001))
            m = model(L)
            if m and m["total"] >= 1: bad += 1
        out["recross_samples_above_1"] = bad
    # delta thresholds
    for tag, cond in [("6R<=Q first", lambda m: m["six_R_le_Q"]), ("step5 tail ok first", lambda m: m["step5_tail"])]:
        for m in rows:
            if cond(m): out[tag] = m; break
    # rate check: total / ((log2 lam)^2/sqrt(lam))  at large lam
    rate = []
    for m in rows:
        L = m["lam"]
        if L > 10**4:
            rate.append((L, m["total"]/ (math.log2(L)**2/ math.sqrt(L))))
    out["rate_ratio_samples"] = rate[::4]
    # dominant term near crossover
    json.dump(out, open("cost_model_results.json","w"), indent=1, default=str)
    print("first valid lambda", out["first_valid_lambda"], model(out["first_valid_lambda"]))
    if cross:
        print("crossover lambda", out["refined_crossover_lambda"], "n ~ 2^%d" % out["refined_crossover_lambda"], out["refined_model_at_crossover"])
        print("recross samples", out["recross_samples_above_1"])
    for k in ["6R<=Q first","step5 tail ok first"]:
        print(k, out.get(k))
    print("rate ratio samples", [(l, round(v,2)) for l,v in out["rate_ratio_samples"]])
    for m in rows[::6]:
        print(m["lam"], "nu",m["nu"],"r",m["r"],"Q",m["Q"],"R",m["R"],"delta %.4g e1 %.4g e2 %.3g e3 %.3g total %.4g"%(m["delta"],m["e1"],m["e2"],m["e3"],m["total"]))
