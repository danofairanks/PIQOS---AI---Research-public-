import numpy as np, json, math, random, sys, itertools
from math import log2

def make_instance(kind, n, b=3, w=3, seed=0):
    rng = random.Random(seed)
    occ = [0]*n; scopes = []
    if kind == "random":
        tries = 0
        while tries < 20*n:
            tries += 1
            avail = [v for v in range(n) if occ[v] < b]
            if len(avail) < 1: break
            k = min(w, len(avail)); sz = rng.randint(1, k)
            vs = rng.sample(avail, sz); scopes.append(vs)
            for v in vs: occ[v] += 1
    elif kind == "clustered":      # identical scopes repeated b times: maximal dependence
        for base in range(0, n - n % w, w):
            vs = list(range(base, base+w))
            for _ in range(b): scopes.append(vs)
            for v in vs: occ[v] += b
    elif kind == "star":           # many variables share a few factors of full width (w) -- each var in b scopes
        for rep in range(b):
            perm = list(range(n)); rng.shuffle(perm)
            for i in range(0, n - n % w, w): scopes.append(perm[i:i+w])
            for v in perm[:n - n % w]: occ[v] += 1
    # neutral factors for variables in no scope (as in the paper)
    for v in range(n):
        if occ[v] == 0: scopes.append([v]); occ[v] = 1
    return scopes

def run(r, Q, scopes, n, b, w, seed=0):
    K = r**Q; D = K*K
    inc_f = []; inc_v = []
    for f, vs in enumerate(scopes):
        for v in vs: inc_f.append(f); inc_v.append(v)
    inc_f = np.array(inc_f); inc_v = np.array(inc_v); M = len(inc_f); F = len(scopes)
    cond1 = 2*(b+w)*D*D <= M; cond2 = 2*Q*r*r <= n
    # variables: a_v (n of them), d_f (F of them); each in [K] (encode as base-r digits when counting groups)
    a = -np.ones(n, dtype=np.int64); d = -np.ones(F, dtype=np.int64)
    # incidence lists
    inc_of_v = [[] for _ in range(n)]; inc_of_f = [[] for _ in range(F)]
    for i in range(M): inc_of_v[inc_v[i]].append(i); inc_of_f[inc_f[i]].append(i)
    # fixed-count tables for Xi: cnt[t][g] = number of fixed v with a_v(t)=g
    digits = lambda x: [(x // r**t) % r for t in range(Q)]
    cnt = np.zeros((Q, r)); nfixed = 0
    def pair_factor(fixedvals, idx_i, idxs_j, var_i, vars_j, cand=None):
        pass
    # A_ij(c): a-equality probability between incidence i (variable x) and every incidence j
    def Aeq(x, cand):
        av = a[inc_v]                     # array over incidences j: value or -1
        res = np.where(inc_v == x, 1.0, np.where(av >= 0, (av == cand).astype(float), 1.0/K))
        return res
    def Deq(y, cand):
        dv = d[inc_f]
        res = np.where(inc_f == y, 1.0, np.where(dv >= 0, (dv == cand).astype(float), 1.0/K))
        return res
    def Aeq_fixedvar(x):                  # a-equality of x (unfixed, symmetric) vs all j, used when d changes
        av = a[inc_v]
        return np.where(inc_v == x, 1.0, 1.0/K)
    # current p_ij factors for pairs needed when choosing d_f: need A_ij with a states (all a fixed by then if we fix a first)
    # order: fix all a_v first, then all d_f
    # --- initial potentials (exact)
    # E Phi = sum_{ordered pairs} p_ij - M^2/D ; E Xi = Q n (1-1/r)
    # compute exactly by counting: p_ij = Aeq*Deq with both unfixed
    # pairs (i,j): A=1 if same var else 1/K ; Dd=1 if same factor else 1/K
    same_v = {}; same_f = {}
    # count ordered pairs by (same_v, same_f)
    nsv = sum(len(l)**2 for l in inc_of_v); nsf = sum(len(l)**2 for l in inc_of_f)
    # pairs with both same var and same factor are the diagonal (f,v) distinct incidences -> M ordered pairs
    nboth = M
    nA_only = nsv - nboth; nD_only = nsf - nboth; nnone = M*M - nsv - nsf + nboth
    EPhi0 = nboth*1.0 + (nA_only + nD_only)/K + nnone/D - M*M/D
    EXi0 = Q*n*(1-1/r)
    psi0 = EPhi0/(M*(b+w)) + EXi0/(Q*n)
    # --- fix a_v one at a time, minimizing Phi/(M(b+w)) + Xi/(Qn) conditional expectation
    order_a = list(range(n)); 
    def phi_contrib_a(x, cand):
        I = inc_of_v[x]
        if not I: return 0.0
        A = Aeq(x, cand)             # over j
        Dd = np.ones(M)              # d all unfixed at this stage: D-factor = 1 if same factor else 1/K
        total = 0.0
        for i in I:
            Dd = np.where(inc_f == inc_f[i], 1.0, 1.0/K)
            pij = A*Dd
            in_I = (inc_v == x)
            total += 2*pij[~in_I].sum() + pij[in_I].sum()   # i with j outside (x2) and j inside (once per ordered pair counted when loop over i)
        return total
    for x in order_a:
        best = None
        for c in range(K):
            ph = phi_contrib_a(x, c) / (M*(b+w))
            dg = digits(c)
            # Xi: choosing a_x = c changes sum_{v,v'} [eq] : pairs with already-fixed v' contribute [eq]; unfixed contribute 1/r ; self 1
            xi = 0.0
            for t in range(Q):
                xi += 2*cnt[t][dg[t]]    # ordered pairs (x, fixed v') and (v', x)
            xi = xi/(Q*n)
            val = ph + xi
            if best is None or val < best[0] - 1e-15: best = (val, c)
        c = best[1]; a[x] = c
        for t, g in enumerate(digits(c)): cnt[t][g] += 1
    # --- fix d_f
    def phi_contrib_d(y, cand):
        I = inc_of_f[y]
        if not I: return 0.0
        D_ = Deq(y, cand)
        av = a[inc_v]                # all fixed now
        total = 0.0
        for i in I:
            A = np.where(inc_v == inc_v[i], 1.0, (av == av[i]).astype(float))
            pij = A*D_
            in_I = (inc_f == y)
            total += 2*pij[~in_I].sum() + pij[in_I].sum()
        return total
    for y in range(F):
        if not inc_of_f[y]:
            d[y] = 0; continue
        best = None
        for c in range(K):
            val = phi_contrib_d(y, c)
            if best is None or val < best[0] - 1e-9: best = (val, c)
        d[y] = best[1]
    # --- final realized values
    lab = a[inc_v]*K + d[inc_f]
    counts = np.bincount(lab, minlength=D)
    Phi = float(((counts - M/D)**2).sum())
    Xi = 0.0; maxgroup = 0
    for t in range(Q):
        g = (a // r**t) % r
        cc = np.bincount(g, minlength=r)
        Xi += float(((cc - n/r)**2).sum()); maxgroup = max(maxgroup, int(cc.max()))
    psi = Phi/(M*(b+w)) + Xi/(Q*n)
    return dict(r=r, Q=Q, D=D, n=n, M=M, b=b, w=w, cond_4_13=(cond1, cond2), psi0_exact=round(psi0, 4), psi_final=round(psi, 4),
                psi_final_le_2=psi <= 2+1e-9, max_label=int(counts.max()), bound_label=2*M/D, label_ok=int(counts.max()) <= 2*M/D,
                max_group=maxgroup, bound_group=2*n/r, group_ok=maxgroup <= 2*n/r,
                label_dev_over_MD=round((counts.max()-M/D)/(M/D), 3), group_dev_over_nr=round((maxgroup-n/r)/(n/r), 3),
                Phi_over_bound=round(Phi/(2*M*(b+w)), 4), Xi_over_bound=round(Xi/(2*Q*n), 4))

if __name__ == "__main__":
    out = []
    specs = [(2, 2, "random", 1200), (2, 2, "clustered", 1200), (2, 2, "star", 1200), (3, 1, "random", 400),
             (3, 1, "clustered", 400), (2, 1, "random", 200), (2, 2, "random", 1500)]
    for (r, Q, kind, n) in specs:
        sc = make_instance(kind, n, 3, 3, seed=1)
        res = run(r, Q, sc, n, 3, 3); res['kind'] = kind
        out.append(res)
        print(json.dumps(res), flush=True)
    json.dump(out, open("lemma45_results.json", "w"), indent=1)
    print("all psi_final<=2:", all(o['psi_final_le_2'] for o in out), "all label_ok:", all(o['label_ok'] for o in out), "all group_ok:", all(o['group_ok'] for o in out))
