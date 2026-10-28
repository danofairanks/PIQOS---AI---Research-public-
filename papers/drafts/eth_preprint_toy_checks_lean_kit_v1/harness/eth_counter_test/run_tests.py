import sys, json, time, random
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from eth_counter import *


def run_case(cons, n, m, seed, do_decoupled=True, verbose=True):
    rng = random.Random(seed)
    clauses = random_formula(n, m, rng)
    truth = count_sat(n, clauses)
    ctr = Counter(n, clauses, cons, seed)
    R, Q = cons.R, cons.Q
    q = (3 * n * R) // Q
    J = q + 1
    degbound = 3 * n * R
    res = {"n": n, "m": len(clauses), "seed": seed, "truth": truth, "q": q, "J": J, **ctr.stats}
    # L2: brute force H(T)
    H = ctr.brute_H()
    while H and H[-1] == 0:
        H.pop()
    res["H(0)==#F"] = (H[0] % PR if H else 0) == truth % PR
    res["deg_H"] = len(H) - 1
    nreal = sum(len(cl) for e, cl in enumerate(ctr.clauses) if not ctr.dummy[e])
    res["deg_H<=occ*(R-1)"] = (len(H) - 1) <= nreal * (R - 1)
    brute_taylor = [pshift(H, t, J) for t in range(1, Q + 1)]
    h0, full, cons_ok = hermite_recover(brute_taylor, Q, J, degbound)
    res["L2_hermite_from_brute_ok"] = (h0 == truth % PR) and full and cons_ok
    res["Q*J>3nR"] = Q * J > degbound
    if do_decoupled:
        counters = {"assign_evals": 0, "poly_mults": 0, "triples": 0}
        t0 = time.time()
        dec_taylor = []
        bad = 0
        for t in range(1, Q + 1):
            des = ctr.design_at(t)
            bad += des["bad"]
            dec_taylor.append(ctr.taylor_decoupled(t, des, J, q, counters))
        res["design_violations(2.5)"] = bad
        res["L3_decoupled_matches_brute_taylor"] = all(
            trim(dec_taylor[t], J) == trim(brute_taylor[t], J) for t in range(Q))
        h0d, fulld, consd = hermite_recover(dec_taylor, Q, J, degbound)
        res["L4_count"] = h0d
        res["L4_count_correct"] = (h0d == truth % PR) and fulld and consd
        res["counters"] = counters
        res["2^n"] = 1 << n
        res["assign_evals_over_2^n"] = round(counters["assign_evals"] / (1 << n), 1)
        res["seconds"] = round(time.time() - t0, 1)
    if verbose:
        print(json.dumps(res, default=str), flush=True)
    return res


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "L1":
        out = {}
        for (r, Q, R) in [(2, 3, 2), (2, 3, 3), (3, 2, 2), (2, 4, 3), (2, 4, 2)]:
            t0 = time.time()
            c = Construction(r, Q, R)
            o = c.check_L1()
            o["seconds"] = round(time.time() - t0, 1)
            out[f"r{r}_Q{Q}_R{R}"] = o
            print(r, Q, R, json.dumps(o), flush=True)
        json.dump(out, open("L1_results.json", "w"), indent=1, default=str)
    else:
        r, Q, R = map(int, sys.argv[2:5])
        n = int(sys.argv[5]); m = int(sys.argv[6]); seeds = int(sys.argv[7])
        dec = (len(sys.argv) <= 8) or sys.argv[8] != "nodec"
        mut = sys.argv[9] if len(sys.argv) > 9 else None
        cons = Construction(r, Q, R, mut=mut)
        rs = [run_case(cons, n, m, 1000 + s, do_decoupled=dec) for s in range(seeds)]
        json.dump(rs, open(f"results_{which}_r{r}Q{Q}R{R}_n{n}{'_'+mut if mut else ''}.json", "w"), indent=1, default=str)
