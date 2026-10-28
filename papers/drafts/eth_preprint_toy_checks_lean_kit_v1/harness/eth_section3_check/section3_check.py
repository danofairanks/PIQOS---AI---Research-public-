import itertools, json, math, random, sys
from fractions import Fraction
from math import comb, log2, log
sys.path.insert(0, '../eth_counter_test')
import eth_counter as ec

# ---------- ring wrappers: A = Z/12, Q[V]/(V^2), or Q ----------
class Zmod:
    def __init__(self, m): self.m = m
    def zero(self): return 0
    def one(self): return 1 % self.m
    def add(self, a, b): return (a+b) % self.m
    def mul(self, a, b): return (a*b) % self.m
    def rnd(self, rng): return rng.randrange(self.m)
class QV2:                                   # Q[V]/(V^2): pairs (a,b) = a + bV
    def zero(self): return (Fraction(0), Fraction(0))
    def one(self): return (Fraction(1), Fraction(0))
    def add(self, x, y): return (x[0]+y[0], x[1]+y[1])
    def mul(self, x, y): return (x[0]*y[0], x[0]*y[1]+x[1]*y[0])
    def rnd(self, rng): return (Fraction(rng.randint(-5, 5)), Fraction(rng.randint(-5, 5)))

# ---------- Lemma 3.2 ----------
def lemma32(n, parts, Cs, D, Afun, ring, E):
    """Afun[g](x) with x a tuple in Q^n (ints); returns (Z_E via the paper's routine, examined vectors)."""
    r = len(parts); c = sum(len(C) for C in Cs)
    # measurement of u on group g
    def meas(g, u):                          # u: dict var->0/1 on parts[g]
        return tuple(sum(row[k]*u[parts[g][k]] for k in range(len(parts[g]))) for row in Cs[g])
    assigns = []
    for g in range(r):
        lst = []
        for bits in range(1 << len(parts[g])):
            u = {parts[g][k]: (bits >> k) & 1 for k in range(len(parts[g]))}
            lst.append((u, meas(g, u)))
        assigns.append(lst)
    examined = 0
    # tuples y in prod {-D..D}^{c_g}: iterate only over those realized by SOME assignment in every group (others skipped by the paper's first scan)
    ys_per_g = [sorted({y for (_, y) in assigns[g]}) for g in range(r)]
    Z = ring.zero()
    # the paper loops over all of Y = prod_g {-D..D}^{c_g}; tuples with an empty X_g are skipped after the first scan of that group.
    # account for the first scan cost over realized tuples only (upper bound is by (2D+1)^c anyway).
    for yt in itertools.product(*ys_per_g):
        reps = []
        for g in range(r):
            examined += len(assigns[g])           # first scan (representative)
            reps.append(next(u for (u, y) in assigns[g] if y == yt[g]))
        p = ring.one()
        for g in range(r):
            s = ring.zero()
            for (u, y) in assigns[g]:
                examined += 1                      # second scan
                if y != yt[g]: continue
                if any(u.get(i, 1) == 0 for i in E if i in parts[g]): continue
                x = [0]*n
                for i, v in u.items(): x[i] = v
                for h in range(r):
                    if h == g: continue
                    for i, v in reps[h].items(): x[i] += v
                s = ring.add(s, Afun[g](tuple(x)))
            p = ring.mul(p, s)
        Z = ring.add(Z, p)
    bound = 2*(2*D+1)**c*sum(2**len(P) for P in parts)
    return Z, examined, bound

def test_lemma32(trials=60, seed=2):
    rng = random.Random(seed); fails = 0; over = 0; tot = 0
    for ring in (Zmod(12), QV2()):
        for _ in range(trials):
            n = rng.randint(3, 6); r = rng.randint(2, 3)
            perm = list(range(n)); rng.shuffle(perm)
            cuts = sorted(rng.sample(range(1, n), r-1)) if n > r else list(range(1, r))
            parts = [perm[i:j] for i, j in zip([0]+cuts, cuts+[n])]
            parts = [p for p in parts]
            r = len(parts)
            D = rng.randint(1, 3)
            Cs = []
            for P in parts:
                rows = []
                for _ in range(rng.randint(0, 2)):
                    row = [rng.randint(-D, D) for _ in P]
                    s_ = sum(abs(v) for v in row)
                    if s_ > D or s_ == 0:
                        row = [0]*len(P); 
                        if P: row[rng.randrange(len(P))] = rng.choice([-1, 1])
                    rows.append(row)
                Cs.append(rows)
            # invariant A_g: depends on x only through x_g and the measurements C_h x_h (h != g): random lookup table
            tables = []
            def make(g):
                cache = {}
                def A(x):
                    xg = tuple(x[i] for i in parts[g])
                    ms = tuple(tuple(sum(row[k]*x[parts[h][k]] for k in range(len(parts[h]))) for row in Cs[h]) for h in range(r) if h != g)
                    key = (xg, ms)
                    if key not in cache: cache[key] = ring.rnd(rng)
                    return cache[key]
                return A
            Afun = [make(g) for g in range(r)]
            E = set(rng.sample(range(n), rng.randint(0, min(2, n))))
            # brute force Z_E = sum_x prod_g A_g(x)
            brute = ring.zero()
            for bits in range(1 << n):
                x = tuple((bits >> i) & 1 for i in range(n))
                if any(x[i] == 0 for i in E): continue
                prod = ring.one()
                for g in range(r): prod = ring.mul(prod, Afun[g](x))
                brute = ring.add(brute, prod)
            Z, ex, bd = lemma32(n, parts, Cs, D, Afun, ring, E)
            tot += 1
            if Z != brute: fails += 1
            if ex > bd: over += 1
    return dict(trials=tot, value_mismatches=fails, examined_over_bound=over)

# ---------- Lemma 3.3 ----------
def test_lemma33(trials=60, seed=4):
    rng = random.Random(seed); bad = 0
    for ring_name in ("Q", "Z12"):
        for _ in range(trials):
            n = rng.randint(2, 5); q = rng.randint(0, 3)
            # p_x(X) = sum over monomials (multi-degree <= q) with random coefficient depending on x
            monos = [m for m in itertools.product(range(q+1), repeat=n) if sum(m) <= q]
            coef = {x: {m: (Fraction(rng.randint(-3, 3)) if ring_name == "Q" else rng.randrange(12)) for m in monos} for x in itertools.product((0, 1), repeat=n)}
            def evalp(x, Xv):
                tot = 0
                for m, c in coef[x].items():
                    t = c
                    for i, e in enumerate(m):
                        t = t*(Xv[i]**e)
                    tot += t
                return tot
            lhs = sum(evalp(x, x) for x in coef)
            rhs = 0
            for size in range(0, min(q, n)+1):
                for E in itertools.combinations(range(n), size):
                    for k in range(size+1):
                        for U in itertools.combinations(E, k):
                            ind = tuple(1 if i in U else 0 for i in range(n))
                            s_ = sum(evalp(x, ind) for x in coef if all(x[i] == 1 for i in E))
                            rhs += (-1)**(size-k)*s_
            if ring_name == "Z12": lhs, rhs = lhs % 12, rhs % 12
            if lhs != rhs: bad += 1
    return dict(trials=2*trials, failures=bad)

# ---------- (3.15), (3.16) ----------
def test_315():
    bad = []; cnt = 0
    for n in (1, 2, 3, 5, 10, 20, 50, 100, 200):
        for q in sorted({0, 1, 2, n//4, n//2, n, n+3}):
            Cq = sum(2**s*comb(n, s) for s in range(0, min(q, n)+1))
            for eta in (Fraction(1, 100), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2), Fraction(9, 10), Fraction(1)):
                cnt += 1
                if eta**q*Cq > (1+2*eta)**n: bad.append((n, q, str(eta)))
                # (3.16) with eta = R/Q:  log Cq <= q log(1/eta) + n log(1 + 2 eta)
                if log(Cq) > q*log(1/float(eta)) + n*log(1+2*float(eta)) + 1e-9: bad.append(('3.16', n, q, str(eta)))
    return dict(cases=cnt, failures=bad[:5], n_fail=len(bad))

# ---------- Prop 3.4 on the real design with representative-based Z ----------
def Z_rep(ctr, t, design, E, U, J, counters):
    n, cons = ctr.n, ctr.cons; r = cons.r
    S, Cg = design["S"], design["Cg"]
    # per-group assignments (all of X_g, unfiltered) with measurements
    ga = []
    for g in range(r):
        lst = []
        for bits in range(1 << len(S[g])):
            u = {S[g][k]: (bits >> k) & 1 for k in range(len(S[g]))}
            y = tuple(sum(Cg[g][k][ci]*u[S[g][ci]] for ci in range(len(S[g]))) for k in range(len(ctr.meas)))
            lst.append((u, y))
        ga.append(lst)
    ys = [sorted({y for _, y in ga[g]}) for g in range(r)]
    delta = {}
    for e, cl in enumerate(ctr.clauses):
        if ctr.dummy[e]: continue
        for v, _ in cl:
            tot = [0]*J
            for i in U:
                sh = ec.pshift(ctr.form[(e, v)][i], t, J); sh[0] = 0
                tot = ec.padd(tot, sh)
            delta[(e, v)] = ec.trim(tot, J)
    by_g = [[e for e in range(ctr.ne) if not ctr.dummy[e] and ctr.d[e][t-1] == g] for g in range(r)]
    total = [0]*J; examined = 0
    pcache = {}
    def pvec(e, v):
        if (e, v) not in pcache: pcache[(e, v)] = ctr.form_at(e, v, t)
        return pcache[(e, v)]
    for yt in itertools.product(*ys):
        reps = [next(u for (u, y) in ga[g] if y == yt[g]) for g in range(r)]
        examined += sum(len(x) for x in ga)
        prod = [1]+[0]*(J-1)
        for g in range(r):
            Bg = [0]*J
            for (u, y) in ga[g]:
                examined += 1
                if y != yt[g]: continue
                if any(u.get(i, 1) == 0 for i in E if i in S[g]): continue
                x = [0]*n
                for i, v in u.items(): x[i] = v
                for h in range(r):
                    if h != g:
                        for i, v in reps[h].items(): x[i] += v
                A = [1]+[0]*(J-1)
                for e in by_g[g]:
                    inner = [1]+[0]*(J-1)
                    for v, neg in ctr.clauses[e]:
                        p = pvec(e, v)
                        val = sum(p[i]*x[i] for i in range(n)) % ec.PR
                        w = ec.padd([val], delta[(e, v)])
                        fac = ec.psub([1], w) if not neg else w
                        inner = ec.pmul(inner, ec.trim(fac, J), J)
                    A = ec.pmul(A, ec.trim(ec.psub([1], inner), J), J)
                Bg = ec.padd(Bg, ec.trim(A, J))
            prod = ec.pmul(prod, ec.trim(Bg, J), J)
        total = ec.padd(total, ec.trim(prod, J))
    return ec.trim(total, J), examined

def test_prop34(seed=7):
    rng = random.Random(seed); res = []; mism = 0; cnt_bad = 0; vec_over = 0; tested = 0
    for (r, Q, R) in [(2, 3, 2), (2, 3, 3)]:
        cons = ec.Construction(r, Q, R)
        for n, m in ((4, 5), (5, 6)):
            for s in range(3):
                clauses = ec.random_formula(n, m, random.Random(100+s))
                truth = ec.count_sat(n, clauses)
                ctr = ec.Counter(n, clauses, cons, 100+s)
                q = (3*n*R)//Q; J = q+1
                taylor = []
                for t in range(1, Q+1):
                    design = ctr.design_at(t)
                    # compare Z_rep with lambda-based Z on a sample of (E,U)
                    for _ in range(4):
                        size = rng.randint(0, min(q, n)); E = set(rng.sample(range(n), size)); U = set(rng.sample(sorted(E), rng.randint(0, len(E)))) if E else set()
                        z1 = ctr.Z(t, design, E, U, J, {"assign_evals": 0, "poly_mults": 0, "triples": 0})
                        z2, ex = Z_rep(ctr, t, design, E, U, J, {})
                        tested += 1
                        if ec.trim(z1, J) != ec.trim(z2, J): mism += 1
                        # Prop 3.4 per-pair vector bound 2 r (2D+1)^{2 tau n} 2^{2n/r}: use the actual (2D+1)^c with c measurement rows
                        c = sum(len(Cg_) for Cg_ in design['Cg'])
                    # full Taylor coefficients via representative-based Z
                    res_t = [0]*J
                    for size in range(0, min(q, n)+1):
                        for E in itertools.combinations(range(n), size):
                            for usz in range(size+1):
                                for U in itertools.combinations(E, usz):
                                    zz, ex = Z_rep(ctr, t, design, set(E), set(U), J, {})
                                    sgn = -1 if (size-usz) % 2 else 1
                                    res_t = ec.padd(res_t, ec.pscale(zz, sgn % ec.PR))
                    taylor.append(ec.trim(res_t, J))
                h0, full, cons_ok = ec.hermite_recover(taylor, Q, J, 3*n*R)
                brute = ctr.brute_H(); 
                bt = [ec.pshift(brute, t, J) for t in range(1, Q+1)]
                if any(ec.trim(taylor[t], J) != ec.trim(bt[t], J) for t in range(Q)): cnt_bad += 1
                res.append(dict(r=r, Q=Q, R=R, n=n, truth=truth, recovered=h0, correct=(h0 == truth % ec.PR) and full and cons_ok))
    return dict(Z_rep_vs_lambda_mismatches=mism, Z_rep_vs_lambda_tested=tested, taylor_vs_brute_failures=cnt_bad, end_to_end=res)

if __name__ == "__main__":
    out = {}
    out['lemma32'] = test_lemma32(); print("Lemma 3.2:", out['lemma32'], flush=True)
    out['lemma33'] = test_lemma33(); print("Lemma 3.3:", out['lemma33'], flush=True)
    out['eq315'] = test_315(); print("(3.15)/(3.16):", out['eq315'], flush=True)
    out['prop34'] = test_prop34()
    p = out['prop34']
    print("Prop 3.4 (representative routine on the real design): Z_rep vs lambda-based mismatches", p['Z_rep_vs_lambda_mismatches'], "of", p['Z_rep_vs_lambda_tested'], "; Taylor vs brute failures", p['taylor_vs_brute_failures'], "; end-to-end", sum(1 for x in p['end_to_end'] if x['correct']), "/", len(p['end_to_end']))
    json.dump(out, open("section3_results.json", "w"), indent=1, default=str)
