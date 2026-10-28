import sys, itertools, random, json, time
sys.path.insert(0, '../eth_counter_test'); sys.path.insert(0, '../eth_appendixB_check')
import eth_counter as ec
PRIME = 2**127 - 1
ec.PR = PRIME                                           # set BEFORE building Construction/Counter (all helpers read the global)
from appendixB_check import decompose

# ---------- systems ----------
def reduce_system(eqs):
    out = []
    for monos in eqs:
        cnt = {}
        for m in monos:
            m = tuple(sorted(set(m)))                  # x^j -> x on Boolean inputs
            cnt[m] = cnt.get(m, 0) ^ 1
        out.append([m for m, c in cnt.items() if c])
    return out

def count_N(n, eqs):
    N = 0
    for bits in range(1 << n):
        x = [(bits >> i) & 1 for i in range(n)]
        if all(sum(all(x[v] for v in m) for m in monos) % 2 == 0 for monos in eqs): N += 1
    return N

def Lval(monos, x): return sum(all(x[v] for v in m) for m in monos)

def exact_S_bruteforce(n, eqs, es, l):
    """S_l(H(0)) as an exact integer: sum_x [sum of coefficients of prod_i B_i(V) mod V^l] with B_i(V) = sum_j e_j(L_i)h(L_i)^j V^j."""
    tot = 0; vco = [0]*l
    for bits in range(1 << n):
        x = [(bits >> i) & 1 for i in range(n)]
        prod = [1] + [0]*(l-1)
        for monos in eqs:
            Lv = Lval(monos, x); h = Lv*(Lv-1)
            B = [(es[j][0] + es[j][1]*Lv)*h**j for j in range(l)]
            new = [0]*l
            for a in range(l):
                for b in range(l-a): new[a+b] += prod[a]*B[b]
            prod = new
        for s in range(l): vco[s] += prod[s]
    return sum(vco), vco

def S_bound(n, eqs, es, l):
    b = 2**n
    for monos in eqs:
        mu = len(monos); tot = 0
        for j in range(l):
            tot += max(abs(es[j][0] + es[j][1]*Lv)*abs(Lv*(Lv-1))**j for Lv in range(mu+1))
        b *= tot
    return b

# ---------- ring A[z]/(z^J)[V]/(V^l) helpers (elements: list over V of z-polys) ----------
def rzero(l, J): return [[0]*J for _ in range(l)]
def rone(l, J): r = rzero(l, J); r[0][0] = 1 % ec.PR; return r
def radd(A, B): return [ec.padd(a, b) for a, b in zip(A, B)]
def rmul(A, B, l, J):
    C = rzero(l, J)
    for i in range(l):
        if not any(A[i]): continue
        for j in range(l - i):
            if not any(B[j]): continue
            C[i+j] = ec.padd(C[i+j], ec.trim(ec.pmul(A[i], B[j], J), J))
    return [ec.trim(c, J) for c in C]

def factor_ring(Lz, es, l, J):
    h = ec.trim(ec.psub(ec.pmul(Lz, Lz, J), Lz), J)
    hp = [1] + [0]*(J-1); out = []
    for j in range(l):
        a_, b_ = es[j]
        ej = ec.trim(ec.padd([a_ % ec.PR], ec.pscale(Lz, b_ % ec.PR)), J)
        out.append(ec.trim(ec.pmul(ej, hp, J), J))
        hp = ec.trim(ec.pmul(hp, h, J), J)
    return out

def L_of_inputs(monos, wv, J):
    """L(Y) with inputs wv[v] (z-polys, length J)."""
    tot = [0]*J
    for m in monos:
        t = [1] + [0]*(J-1)
        for v in m: t = ec.trim(ec.pmul(t, wv[v], J), J)
        tot = ec.padd(tot, t)
    return ec.trim(tot, J)

# ---------- decoupled sum (Lemma 3.2 representative routine) in the ring ----------
def Z_rep_ring(ctr, eqs, es, l, t, design, E, U, J):
    n, cons = ctr.n, ctr.cons; r = cons.r
    S, Cg = design['S'], design['Cg']
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
    for e in range(len(eqs)):
        for v, _ in ctr.clauses[e]:
            tot = [0]*J
            for i in U:
                sh = ec.pshift(ctr.form[(e, v)][i], t, J); sh[0] = 0
                tot = ec.padd(tot, sh)
            delta[(e, v)] = ec.trim(tot, J)
    by_g = [[e for e in range(len(eqs)) if ctr.d[e][t-1] == g] for g in range(r)]
    pcache = {}
    def pvec(e, v):
        if (e, v) not in pcache: pcache[(e, v)] = ctr.form_at(e, v, t)
        return pcache[(e, v)]
    total = rzero(l, J); nvec = 0
    for yt in itertools.product(*ys):
        reps = [next(u for (u, y) in ga[g] if y == yt[g]) for g in range(r)]
        prod = rone(l, J)
        for g in range(r):
            Bg = rzero(l, J)
            for (u, y) in ga[g]:
                nvec += 1
                if y != yt[g]: continue
                if any(u.get(i, 1) == 0 for i in E if i in S[g]): continue
                x = [0]*n
                for i, v in u.items(): x[i] = v
                for h in range(r):
                    if h != g:
                        for i, v in reps[h].items(): x[i] += v
                A = rone(l, J)
                for e in by_g[g]:
                    wv = {}
                    for v, _ in ctr.clauses[e]:
                        p = pvec(e, v)
                        val = sum(p[i]*x[i] for i in range(n)) % ec.PR
                        wv[v] = ec.trim(ec.padd([val], delta[(e, v)]), J)
                    Lz = L_of_inputs(eqs[e], wv, J)
                    A = rmul(A, factor_ring(Lz, es, l, J), l, J)
                Bg = radd(Bg, A)
            prod = rmul(prod, Bg, l, J)
        total = radd(total, prod)
    return total, nvec

# ---------- brute-force H(T) in A[T] ----------
def brute_H_ring(ctr, eqs, es, l):
    n = ctr.n; H = [[0] for _ in range(l)]
    for bits in range(1 << n):
        x = [(bits >> i) & 1 for i in range(n)]
        prod = [[1]] + [[0] for _ in range(l-1)]
        for e, monos in enumerate(eqs):
            wv = {}
            for v, _ in ctr.clauses[e]:
                w = [0]
                for i in range(n):
                    if x[i]: w = ec.padd(w, ctr.form[(e, v)][i])
                wv[v] = w
            Lp = [0]
            for m in monos:
                t_ = [1]
                for v in m: t_ = ec.pmul(t_, wv[v])
                Lp = ec.padd(Lp, t_)
            h = ec.psub(ec.pmul(Lp, Lp), Lp); hp = [1]; B = []
            for j in range(l):
                ej = ec.padd([es[j][0] % ec.PR], ec.pscale(Lp, es[j][1] % ec.PR))
                B.append(ec.pmul(ej, hp)); hp = ec.pmul(hp, h)
            new = [[0] for _ in range(l)]
            for a in range(l):
                for b in range(l-a): new[a+b] = ec.padd(new[a+b], ec.pmul(prod[a], B[b]))
            prod = new
        H = [ec.padd(H[s], prod[s]) for s in range(l)]
    return H

def run_system(name, n, eqs, seed, do_brute_H=True, r=2, Q=3, R=2):
    eqs = reduce_system(eqs)
    eqs = [m for m in eqs if m]                          # discard identically-zero equations (paper: 0 = 0 dropped)
    l = n + 1; m_test = len(eqs); k = max((len(mm) for monos in eqs for mm in monos), default=1)
    p_, es, _, _ = decompose(l)
    N = count_N(n, eqs); Sx, vco = exact_S_bruteforce(n, eqs, es, l)
    bound = S_bound(n, eqs, es, l)
    assert Sx % 2**l == N
    d = k*(m_test + 2*(l-1)); dH = k*R*(m_test + 2*(l-1)); q = dH//Q; J = q+1
    cons = ec.Construction(r, Q, R)
    clauses = [[(v, False) for v in sorted({v for m in monos for v in m})] for monos in eqs]
    ctr = ec.Counter(n, clauses, cons, seed)
    t0 = time.time()
    Hb = brute_H_ring(ctr, eqs, es, l) if do_brute_H else None
    degH = max((len(P)-1 for P in Hb), default=0) if Hb else None
    brute_taylor = None
    if Hb: brute_taylor = [[ec.pshift(Hb[s], t, J) for t in range(1, Q+1)] for s in range(l)]
    taylor = [[None]*Q for _ in range(l)]; nvec_tot = 0
    for t in range(1, Q+1):
        design = ctr.design_at(t)
        res = rzero(l, J)
        for size in range(0, min(q, n)+1):
            for E in itertools.combinations(range(n), size):
                for usz in range(size+1):
                    for U in itertools.combinations(E, usz):
                        Z, nv = Z_rep_ring(ctr, eqs, es, l, t, design, set(E), set(U), J); nvec_tot += nv
                        sgn = -1 if (size-usz) % 2 else 1
                        res = radd(res, [ec.pscale(z_, sgn % ec.PR) for z_ in Z])
        for s in range(l): taylor[s][t-1] = ec.trim(res[s], J)
    taylor_ok = None
    if brute_taylor is not None:
        taylor_ok = all(ec.trim(taylor[s][t], J) == ec.trim(brute_taylor[s][t], J) for s in range(l) for t in range(Q))
    h0s = []; herm_ok = True
    for s in range(l):
        h0, full, cons_ok = ec.hermite_recover(taylor[s], Q, J, dH)
        herm_ok = herm_ok and full and cons_ok; h0s.append(h0)
    S_mod = sum(h0s) % ec.PR
    S_signed = S_mod - ec.PR if S_mod > ec.PR//2 else S_mod
    per_s_ok = all((h0s[s] - vco[s]) % ec.PR == 0 for s in range(l))
    rec = dict(name=name, n=n, m_test=m_test, k=k, l=l, N=N, d=d, d_H=dH, q=q, J=J, degT_H=degH, deg_ok=(degH is None) or degH <= d*(R-1),
               S_bruteforce=Sx, S_bound_bits=bound.bit_length(), prime_bits=ec.PR.bit_length(), bound_ok=bound < ec.PR//2,
               S_pipeline=S_signed, S_equal=(S_signed == Sx), per_V_coef_equal=per_s_ok, N_pipeline=S_signed % 2**l, N_correct=(S_signed % 2**l == N),
               taylor_equals_bruteforce=taylor_ok, hermite_ok=herm_ok, vectors_examined=nvec_tot, seconds=round(time.time()-t0, 1))
    return rec

if __name__ == "__main__":
    which = sys.argv[1]
    n = 4
    systems = {
        "unsat": [[(0,), ()], [(0,)]],                                  # x0 + 1 = 0 and x0 = 0
        "A": [[(0, 1), (2,)], [(1, 3), (0,), ()]],
        "B": [[(0, 1, 2), (3,)], [(0, 3), (1,)]],
        "C": [[(0, 1), (2, 3)], [(0, 2), (1, 3), ()]],
        "D": [[(0, 1), (1, 2), (3,)], [(0, 3)], [(2, 3), (0,)]],
        "E": [[(0,), (1,), (2,)], [(0, 1), (2, 3), (1, 3)]],
    }
    out = []
    if which == "sweep":
        import zlib
        cfgs = [(4, 40, (2, 3, 2)), (5, 12, (2, 3, 2)), (4, 12, (2, 3, 3)), (4, 12, (3, 2, 2)), (6, 3, (2, 3, 2))]
        for (nn, count, (r_, Q_, R_)) in cfgs:
            for sd in range(count):
                rng = random.Random(10000*nn + 100*r_ + sd)
                m_test = rng.randint(2, 3); eqs = []
                for _ in range(m_test):
                    monos = []
                    for _ in range(rng.randint(1, 3)):
                        if rng.random() < 0.15: monos.append(())
                        else: monos.append(tuple(rng.sample(range(nn), rng.randint(1, min(3, nn)))))
                    eqs.append(monos)
                try:
                    rec = run_system(f"sw_n{nn}_r{r_}Q{Q_}R{R_}_{sd}", nn, eqs, seed=sd, do_brute_H=(nn <= 5), r=r_, Q=Q_, R=R_)
                except AssertionError as ex:
                    rec = dict(name=f"sw_n{nn}_{sd}", error="assert " + str(ex)[:80])
                except Exception as ex:
                    rec = dict(name=f"sw_n{nn}_{sd}", error=type(ex).__name__ + " " + str(ex)[:120])
                out.append(rec); print(json.dumps(rec), flush=True)
        json.dump(out, open("run_sweep.json", "w"), indent=1, default=str)
        raise SystemExit
    names = [which] if which != "all" else list(systems)
    for nm in names:
        rec = run_system(nm, n, systems[nm], seed=sum(map(ord, nm)) % 1000)
        out.append(rec); print(json.dumps(rec), flush=True)
    json.dump(out, open(f"run_{which}.json", "w"), indent=1, default=str)
