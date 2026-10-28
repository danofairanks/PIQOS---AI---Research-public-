import itertools, json, math, random
from fractions import Fraction
from math import lgamma, log, log2, comb, ceil, floor, exp

def H2(x): return 0.0 if x <= 0 or x >= 1 else -x*log2(x)-(1-x)*log2(1-x)
def log2binom(n, k): return (lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1))/log(2)

# ---------- Part A: Lemma 6.1 parameter arithmetic ----------
def part_A():
    rows = []; fails = []
    for B in (1, 2, 5, 20, 100):
        for mu in list(range(1, 61)) + [80, 120, 200, 400]:
            for m in {2**(mu-1), 2**mu-1}:
                if m < 1: continue
                mu_ = m.bit_length()          # floor(log2 m)+1
                assert mu_ == mu
                P = 20000*B*B*mu*mu; D0 = 320000*B*B*mu**3
                dG = min(m, D0)
                qG = 1
                while qG*dG < m: qG *= 2
                eps = Fraction(1, 200*B*mu); delta = Fraction(1, 100*B*mu)
                chk = dict(B=B, mu=mu, m=m, dG=dG, qG=qG)
                chk['delta*(delta-eps)==1/P'] = (delta*(delta-eps) == Fraction(1, P))
                # (i) union bound for eps-biased shifts (only if qG>1 -> dG = D0)
                if qG > 1:
                    lhs = log(2*qG) - float(eps*eps)*dG/2
                    chk['i_union_log'] = lhs; chk['i_ok'] = lhs < 0
                    chk['i_closed_form'] = (float(eps*eps)*dG/2 == 4*mu)
                else:
                    chk['i_ok'] = True
                # (ii) local code
                cG = dG//(8*B)
                h = ceil(delta*dG) - 1
                if h <= 0:
                    chk['ii_ok'] = True; chk['ii_slack_bits'] = None
                else:
                    if dG <= 300000:
                        terms = [log2binom(dG, j) for j in range(1, h+1)]
                        mx = max(terms); lg = mx + log2(sum(2**(t-mx) for t in terms))
                    else:
                        lg = dG*H2(h/dG) if h <= dG/2 else dG
                    chk['ii_slack_bits'] = cG - lg                  # need > 0
                    chk['ii_ok'] = cG - lg > 0
                    # paper's intermediate bound (2 dG)^(2h) < 2^(dG/(25B))
                    chk['ii_paper_bound_ok'] = 2*h*log2(2*dG) < dG/(25*B)
                # (iii) rows: 2 qG cG <= 3n with n >= ceil(m/B)
                n_min = -(-m//B)
                chk['iii_ok'] = 2*qG*cG <= 3*n_min
                # additionally: paper's claimed intermediate: qG=1 -> 2cG <= m/(4B)+2 ; qG>1 -> 2 qG cG < n
                chk['iii_strict_n_ok'] = (2*qG*cG <= n_min) if qG > 1 else True
                rows.append(chk)
                if not (chk['i_ok'] and chk['ii_ok'] and chk['iii_ok'] and chk['delta*(delta-eps)==1/P'] and chk.get('ii_paper_bound_ok', True) and chk['iii_strict_n_ok']):
                    fails.append(chk)
    return rows, fails

# ---------- Part B: Lemma 6.2's rejection probability ----------
def part_B():
    worst = 1.0; arg = None
    for P in [1, 2, 3, 5, 10, 50, 1000, 20000, 10**7]:
        for m in [1, 2, 5, 10, 100, 10**4, 10**8]:
            smin = max(1, -(-m//P))                  # support size >= m/P (integer)
            for s in {smin, min(m, smin+1), m}:
                if s > m or s < 1: continue
                pr = 0.5*(1-(1-s/m)**P)
                if pr < worst: worst, arg = pr, (P, m, s)
    return dict(min_prob=worst, at_P_m_s=arg, threshold=0.25, ok=worst >= 0.25)

# ---------- Part C: exact greedy on tiny formulas ----------
def part_C(trials=300, seed=3):
    rng = random.Random(seed); worst_ratio = 0; max_rounds = 0; worst_avg_ratio = 0; fails = 0
    for _ in range(trials):
        n = rng.randint(4, 6); m = 4; P = 4; k = 3
        clauses = []
        for _ in range(m):
            vs = rng.sample(range(n), k); clauses.append([(v, rng.random() < 0.5) for v in vs])
        # violation vectors v(x) in F2^m
        viol = []
        for x in range(1 << n):
            vec = 0
            for e, cl in enumerate(clauses):
                if all(((x >> v) & 1) == (1 if neg else 0) for v, neg in cl): vec |= (1 << e)
            viol.append(vec)
        nonsat = [x for x in range(1 << n) if viol[x] != 0]
        passing = list(nonsat)                        # A empty: all pass
        # distribution over rows h from lists gamma in ([m] x {0,1})^P
        rowcount = {}
        for gamma in itertools.product(range(m*2), repeat=P):
            h = 0
            for g in gamma:
                e, c = g // 2, g % 2
                if c: h ^= (1 << e)
            rowcount[h] = rowcount.get(h, 0) + 1
        total = sum(rowcount.values())
        rounds = 0
        while passing and rounds < 3*n + 5:
            D = len(passing)
            # expected D after appending a random-list row
            avg = sum(cnt*sum(1 for x in passing if bin(viol[x] & h).count('1') % 2 == 0) for h, cnt in rowcount.items())/total
            worst_avg_ratio = max(worst_avg_ratio, avg/D)
            best = min(rowcount, key=lambda h: sum(1 for x in passing if bin(viol[x] & h).count('1') % 2 == 0))
            newp = [x for x in passing if bin(viol[x] & best).count('1') % 2 == 0]
            worst_ratio = max(worst_ratio, len(newp)/D)
            passing = newp; rounds += 1
        max_rounds = max(max_rounds, rounds)
        if passing: fails += 1
    return dict(trials=trials, max_avg_over_D=round(worst_avg_ratio, 4), max_min_over_D=round(worst_ratio, 4), max_rounds=max_rounds,
                bound_rounds_3n_max=18, not_cleared=fails, avg_le_3_4=worst_avg_ratio <= 0.75+1e-12)

# ---------- Part D: mixing inequality (6.3) with the measured bias ----------
def part_D(trials=2000, seed=5):
    rng = random.Random(seed)
    l = 6; q = 1 << l; d = 40
    shifts = [rng.randrange(q) for _ in range(d)]
    eps = 0.0
    for b in range(1, q):
        s = sum(1 if bin(b & s_).count('1') % 2 == 0 else -1 for s_ in shifts)
        eps = max(eps, abs(s)/d)
    bad = 0
    for _ in range(trials):
        U = rng.sample(range(q), rng.randint(1, q)); V = set(rng.sample(range(q), rng.randint(1, q)))
        e = sum(1 for u in U for s_ in shifts if (u ^ s_) in V)
        bound = d*len(U)*len(V)/q + eps*d*math.sqrt(len(U)*len(V))
        if e > bound + 1e-9: bad += 1
    return dict(q=q, d=d, measured_eps=round(eps, 3), trials=trials, violations=bad)

if __name__ == "__main__":
    A, fails = part_A()
    print("Part A: cases", len(A), "failures", len(fails))
    if fails: print(fails[:3])
    ii = [r['ii_slack_bits'] for r in A if r.get('ii_slack_bits') is not None]
    print("  min slack bits (c_G - log2 #light words):", round(min(ii), 1))
    i_ = [r['i_union_log'] for r in A if 'i_union_log' in r]
    print("  union bound (i): max ln(2 qG) - eps^2 dG/2 over qG>1 cases:", round(max(i_), 2) if i_ else None, "(need < 0), cases qG>1:", len(i_))
    qs = [r for r in A if r['qG'] > 1]; print("  cases with qG>1:", len(qs), " qG=1:", len(A)-len(qs))
    B_ = part_B(); print("Part B:", B_)
    C_ = part_C(); print("Part C:", C_)
    D_ = part_D(); print("Part D:", D_)
    json.dump(dict(A_failures=fails, A_cases=len(A), B=B_, C=C_, D=D_), open("section6_results.json", "w"), indent=1, default=str)
