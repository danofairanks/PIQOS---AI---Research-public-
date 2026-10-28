"""Implementation of the Section 2 counter of 'The Exponential Time Hypothesis is False'
(OpenAI, 25 Oct 2026; sha256 of paper.pdf recorded in RESULTS).  Small-parameter, exact
arithmetic (mod the prime PR; every true quantity is a small integer so results are exact
when they land in [0, 2^n]).  Section references are to the paper.

Stages (see PREREG.md):
  L1  construction properties of M0, C and the rows P_u(T)       (Sec 2.7, eqs 2.13-2.16)
  L2  generic algebra: H(0)=#F, deg H, Taylor/Hermite recovery   (Sec 2.2-2.3, 2.5)
  L3  decoupled evaluation == brute force H(t+z) mod z^J         (Sec 2.4-2.5, eq 2.9)
  L4  end-to-end count == brute force #F
"""
import itertools, random, time, json, sys
from math import comb

PR = (1 << 61) - 1


def inv(a):
    return pow(a % PR, PR - 2, PR)


# ---------- polynomial helpers: lists of ints mod PR, low -> high ----------
def padd(a, b):
    n = max(len(a), len(b))
    return [((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % PR for i in range(n)]


def psub(a, b):
    n = max(len(a), len(b))
    return [((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % PR for i in range(n)]


def pmul(a, b, J=None):
    if not a or not b:
        return []
    n = len(a) + len(b) - 1
    if J is not None:
        n = min(n, J)
    out = [0] * n
    for i, x in enumerate(a):
        if x == 0 or i >= n:
            continue
        for j, y in enumerate(b):
            if i + j >= n:
                break
            out[i + j] = (out[i + j] + x * y) % PR
    return out


def pscale(a, c):
    return [(x * c) % PR for x in a]


def pshift(a, t, J):
    """coefficients of a(t+z) mod z^J."""
    out = [0] * J
    for i, c in enumerate(a):
        if c == 0:
            continue
        tp = 1
        for k in range(i, -1, -1):  # coefficient of z^j is c*C(i,j)*t^(i-j)
            pass
        for j in range(min(i, J - 1) + 1):
            out[j] = (out[j] + c * comb(i, j) % PR * pow(t, i - j, PR)) % PR
    return out


def trim(a, J):
    a = (a + [0] * J)[:J]
    return a


# ---------- formulas ----------
def random_formula(n, m, rng, width=3, max_occ=3):
    """k-CNF clauses as lists of (var, neg); each var in <= max_occ clauses. Dummy clauses added."""
    occ = [0] * n
    clauses = []
    tries = 0
    while len(clauses) < m and tries < 1000:
        tries += 1
        avail = [v for v in range(n) if occ[v] < max_occ]
        if not avail:
            break
        w = rng.randint(1, min(width, len(avail)))
        vs = rng.sample(avail, w)
        clauses.append([(v, rng.random() < 0.5) for v in vs])
        for v in vs:
            occ[v] += 1
    return clauses


def count_sat(n, clauses):
    cnt = 0
    for bits in range(1 << n):
        ok = True
        for cl in clauses:
            if not any(((bits >> v) & 1) != (1 if neg else 0) for v, neg in cl):
                ok = False
                break
        cnt += ok
    return cnt


# ---------- Section 2.7 construction ----------
class Construction:
    MUT = None  # 'no_phi' | 'drop_row'
    def __init__(self, r, Q, R, mut=None):
        self.mut = mut
        assert 1 <= R <= Q + 1
        self.r, self.Q, self.R = r, Q, R
        self.D = r ** (2 * Q)
        D = self.D
        base = r * r
        self.base = base
        # index <-> tuple of pair indices pa=a*r+d, position s=0..Q-1
        self.pairs = [[(idx // base ** s) % base for s in range(Q)] for idx in range(D)]

        def enc(ps):
            return sum(p * base ** s for s, p in enumerate(ps))
        self.enc = enc
        swap = lambda pa: (pa % r) * r + pa // r  # (a,d)->(d,a)
        self.perm_s = []
        for s in range(Q):
            self.perm_s.append([enc([swap(p) if q == s else p for q, p in enumerate(self.pairs[idx])])
                                for idx in range(D)])
        self.perm_V = [enc([swap(p) for p in self.pairs[idx]]) for idx in range(D)]
        # interval I of R consecutive integers near Q*p, p=(r-1)/(2r)
        p = (r - 1) / (2 * r)
        a0 = int(round(Q * p - (R - 1) / 2))
        a0 = max(0, min(a0, Q + 1 - R))
        self.I = list(range(a0, a0 + R))
        # f: Lagrange interpolation of (-1)^j on I, degree <= R-1
        self.f = self._lagrange([(j, (-1) ** j) for j in self.I])
        self.M0 = self._build_M0()
        self._build_C()

    def _lagrange(self, pts):
        poly = [0]
        for i, (xi, yi) in enumerate(pts):
            num = [1]
            den = 1
            for k, (xk, _) in enumerate(pts):
                if k == i:
                    continue
                num = pmul(num, [(-xk) % PR, 1])
                den = den * (xi - xk) % PR
            poly = padd(poly, pscale(num, yi * inv(den) % PR))
        return poly

    def _build_M0(self):
        D, Q = self.D, self.Q
        f = self.f
        i2 = inv(2)
        # F = f(W0), W0 = (Q I - sum Pi_s)/2 acting as (Pi x)[u] = x[pi(u)]
        def apply_W0(Mat):  # rows indexed by u
            out = []
            for u in range(D):
                row = [(Q * x) % PR for x in Mat[u]]
                for s in range(Q):
                    pr = Mat[self.perm_s[s][u]]
                    row = [(a - b) % PR for a, b in zip(row, pr)]
                out.append([(x * i2) % PR for x in row])
            return out
        ident = [[1 if i == j else 0 for j in range(D)] for i in range(D)]
        F = [[(f[-1] * x) % PR for x in row] for row in ident]
        for c in reversed(f[:-1]):
            F = apply_W0(F)
            for u in range(D):
                F[u][u] = (F[u][u] + c) % PR
        # M0 = V0 F ; (V0 x)[u] = x[perm_V(u)]
        return [F[self.perm_V[u]] for u in range(D)]

    def _build_C(self):
        r, Q, D = self.r, self.Q, self.D
        # per-position eigen-vectors as dict pair_idx -> val, with eigenvalue sign
        vecs = []
        for a in range(r):
            vecs.append(({a * r + a: 1}, +1))
        for a in range(r):
            for b in range(a + 1, r):
                vecs.append(({a * r + b: 1, b * r + a: 1}, +1))
        for a in range(r):
            for b in range(a + 1, r):
                vecs.append(({a * r + b: 1, b * r + a: -1}, -1))
        assert len(vecs) == r * r
        self.basis = []  # (j, dense vector as dict idx->val)
        for combo in itertools.product(range(r * r), repeat=Q):
            j = sum(1 for k in combo if vecs[k][1] == -1)
            vec = {}
            for idx in range(D):
                v = 1
                for s in range(Q):
                    v *= vecs[combo[s]][0].get(self.pairs[idx][s], 0)
                    if v == 0:
                        break
                if v:
                    vec[idx] = v
            self.basis.append((j, vec))
        self.C_rows = [vec for (j, vec) in self.basis if j not in self.I]
        self.fixed_vecs = [vec for (j, vec) in self.basis if j in self.I]
        if self.mut == 'drop_row' and self.C_rows:
            self.C_rows = self.C_rows[:-1]
        if self.mut == 'no_C':
            self.C_rows = []

    # ---- L1 checks ----
    def check_L1(self):
        D, R = self.D, self.R
        out = {}
        # basis orthogonality and eigen action
        # W0 psi = j psi, M0 psi = (-1)^j f(j) psi
        fixed_ok = True
        for (j, vec) in self.basis[:: max(1, len(self.basis) // 40)]:
            x = [vec.get(i, 0) % PR for i in range(D)]
            Mx = [sum(self.M0[u][w] * x[w] for w in range(D)) % PR for u in range(D)]
            fj = 0
            for k, c in enumerate(self.f):
                fj = (fj + c * pow(j, k, PR)) % PR
            lam = ((-1) ** j) * fj % PR
            if Mx != [(lam * xi) % PR for xi in x]:
                fixed_ok = False
        out["M0_eigen_action_on_basis_sample"] = fixed_ok
        # (2.14) first: M0 xi = xi for xi in ker C (span of fixed_vecs)
        ok = True
        for vec in self.fixed_vecs:
            x = [vec.get(i, 0) % PR for i in range(D)]
            Mx = [sum(self.M0[u][w] * x[w] for w in range(D)) % PR for u in range(D)]
            if Mx != x:
                ok = False
        out["M0_fixes_kerC"] = ok
        # (2.14) second: |E_{u,w}| <= R-1 whenever M0[u,w] != 0 ; E = {t: a_w(t) != d_u(t)}
        r, Q = self.r, self.Q
        maxE, nz = 0, 0
        for u in range(D):
            du = [p % r for p in self.pairs[u]]
            for w in range(D):
                if self.M0[u][w]:
                    nz += 1
                    aw = [p // r for p in self.pairs[w]]
                    E = sum(1 for s in range(Q) if aw[s] != du[s])
                    maxE = max(maxE, E)
        out["max_|E_uw|_over_nonzero_M0"] = maxE
        out["sparsity_ok(<=R-1)"] = maxE <= R - 1
        out["nonzero_M0_entries"] = nz
        out["c_rows"] = len(self.C_rows)
        out["D"] = D
        out["I"] = self.I
        return out

    def row_poly(self, u):
        """P_u(T): dict w -> poly in T (only entries that differ from delta_uw)."""
        r, Q = self.r, self.Q
        du = [p % r for p in self.pairs[u]]
        row = {}
        for w in range(self.D):
            m = self.M0[u][w]
            aw = [p // r for p in self.pairs[w]]
            E = [s + 1 for s in range(Q) if aw[s] != du[s]]  # points t=s+1
            phi = [1]
            if self.mut != 'no_phi':
                for s in E:
                    phi = pmul(phi, [1, (-inv(s)) % PR])
            poly = [1 if u == w else 0]
            if m:
                poly = padd(poly, pscale(psub(phi, [1]), m))
            if any(poly):
                row[w] = poly
        return row


# ---------- the counter ----------
def solve_lambda(rows, target):
    """find lam with sum_k lam_k * rows[k][i] = target[i] for all i (mod PR); rows: list of lists.
    returns list lam or None."""
    k = len(rows)
    cols = len(target)
    if cols == 0:
        return [0] * k
    # system A lam = target, A[i][k] = rows[k][i]
    A = [[rows[kk][i] % PR for kk in range(k)] + [target[i] % PR] for i in range(cols)]
    piv = []
    ri = 0
    for c in range(k):
        pr_ = None
        for i in range(ri, cols):
            if A[i][c]:
                pr_ = i
                break
        if pr_ is None:
            continue
        A[ri], A[pr_] = A[pr_], A[ri]
        iv = inv(A[ri][c])
        A[ri] = [(x * iv) % PR for x in A[ri]]
        for i in range(cols):
            if i != ri and A[i][c]:
                fac = A[i][c]
                A[i] = [(x - fac * y) % PR for x, y in zip(A[i], A[ri])]
        piv.append(c)
        ri += 1
        if ri == cols:
            break
    for i in range(ri, cols):
        if A[i][k]:
            return None
    lam = [0] * k
    for i, c in enumerate(piv):
        lam[c] = A[i][k]
    return lam


class Counter:
    def __init__(self, n, clauses, cons: Construction, seed):
        self.n, self.cons = n, cons
        self.rng = random.Random(seed)
        r, Q, R = cons.r, cons.Q, cons.R
        # clauses incl. dummy clauses for variables occurring in no clause
        used = {v for cl in clauses for v, _ in cl}
        self.clauses = [list(cl) for cl in clauses]
        self.dummy = [False] * len(self.clauses)
        for v in range(n):
            if v not in used:
                self.clauses.append([(v, False)])
                self.dummy.append(True)
        self.ne = len(self.clauses)
        # schedules (deviation D-1: random, not Lemma 4.5)
        self.a = [tuple(self.rng.randrange(r) for _ in range(Q)) for _ in range(n)]
        self.d = [tuple(self.rng.randrange(r) for _ in range(Q)) for _ in range(self.ne)]
        # labels and copies
        self.occ = []  # (e, v, label_idx, copy)
        seen = {}
        for e, cl in enumerate(self.clauses):
            for v, _ in cl:
                lab = cons.enc([self.a[v][s] * r + self.d[e][s] for s in range(Q)])
                k = seen.get(lab, 0)
                seen[lab] = k + 1
                self.occ.append((e, v, lab, k))
        self.h = max(seen.values())
        # per-copy map w -> variable
        self.zeta = [dict() for _ in range(self.h)]
        for (e, v, lab, k) in self.occ:
            assert lab not in self.zeta[k]
            self.zeta[k][lab] = v
        # replacement forms P_{e,v}[i](T), polynomials in T, for every non-dummy occurrence
        self.rowcache = {}
        self.form = {}
        for (e, v, lab, k) in self.occ:
            if lab not in self.rowcache:
                self.rowcache[lab] = cons.row_poly(lab)
            row = self.rowcache[lab]
            vec = [[0] for _ in range(n)]
            for w, poly in row.items():
                i = self.zeta[k].get(w)
                if i is not None:
                    vec[i] = padd(vec[i], poly)
            self.form[(e, v)] = vec
        # measurement rows: (copy, c-row) -> integer vector over variables
        self.meas = []
        for k in range(self.h):
            for crow in cons.C_rows:
                m = [0] * n
                for w, i in self.zeta[k].items():
                    m[i] += crow.get(w, 0)
                self.meas.append(m)
        self.stats = {"h": self.h, "meas_rows": len(self.meas)}

    # ---- evaluation of a form at T=t as vector ----
    def form_at(self, e, v, t):
        out = []
        for poly in self.form[(e, v)]:
            val = 0
            for c in reversed(poly):
                val = (val * t + c) % PR
            out.append(val)
        return out

    # ---- brute force H(T) ----
    def brute_H(self):
        n = self.n
        # degree bound
        tot = [0]
        for bits in range(1 << n):
            x = [(bits >> i) & 1 for i in range(n)]
            prod = [1]
            for e, cl in enumerate(self.clauses):
                if self.dummy[e]:
                    continue
                inner = [1]
                for v, neg in cl:
                    w = [0]
                    for i in range(n):
                        if x[i]:
                            w = padd(w, self.form[(e, v)][i])
                    # literal L = w (pos) or 1-w (neg); factor (1 - L)
                    fac = psub([1], w) if not neg else w
                    inner = pmul(inner, fac)
                phi = psub([1], inner)
                prod = pmul(prod, phi)
            tot = padd(tot, prod)
        return tot

    # ---- decoupled evaluation, eq (2.6)/(2.8) ----
    def design_at(self, t):
        n, cons = self.n, self.cons
        r = cons.r
        S = [[i for i in range(n) if self.a[i][t - 1] == g] for g in range(r)]
        # per group measurement restrictions
        Cg = [[[m[i] for i in S[g]] for m in self.meas] for g in range(r)]
        # lambda coefficients
        lam = {}
        bad = 0
        for e, cl in enumerate(self.clauses):
            if self.dummy[e]:
                continue
            g = self.d[e][t - 1]
            for v, _ in cl:
                p = self.form_at(e, v, t)
                for hgrp in range(r):
                    if hgrp == g:
                        continue
                    target = [p[i] for i in S[hgrp]]
                    # rows of C_{t,h}: one per measurement
                    rows = [[Cg[hgrp][k][ci] for ci in range(len(S[hgrp]))] for k in range(len(self.meas))]
                    sol = solve_lambda(rows, target)
                    if sol is None:
                        bad += 1
                        sol = [0] * len(self.meas)
                    lam[(e, v, hgrp)] = sol
        return {"S": S, "Cg": Cg, "lam": lam, "bad": bad}

    def Z(self, t, design, E, U, J, counters):
        """Z_{t,E,U}(z) in Q[z]/(z^J) via measurement-tuple enumeration."""
        n, cons = self.n, self.cons
        r = cons.r
        S, Cg, lam = design["S"], design["Cg"], design["lam"]
        # per group: allowed assignments, with measurement vector
        group_assign = []
        for g in range(r):
            lst = []
            for bits in range(1 << len(S[g])):
                u = {S[g][k]: (bits >> k) & 1 for k in range(len(S[g]))}
                if any(u.get(i, 1) == 0 for i in E):
                    continue
                y = tuple(sum(Cg[g][k][ci] * u[S[g][ci]] for ci in range(len(S[g]))) for k in range(len(self.meas)))
                lst.append((u, y))
            group_assign.append(lst)
        ach = [sorted({y for _, y in group_assign[g]}) for g in range(r)]
        by_y = []
        for g in range(r):
            dct = {}
            for (u, y) in group_assign[g]:
                dct.setdefault(y, []).append(u)
            by_y.append(dct)
        # shifted Delta polys: Delta_{e,v}^U(z) = sum_{i in U} (P[i](t+z) - P[i](t))
        delta = {}
        for e, cl in enumerate(self.clauses):
            if self.dummy[e]:
                continue
            for v, _ in cl:
                tot = [0] * J
                for i in U:
                    sh = pshift(self.form[(e, v)][i], t, J)
                    sh[0] = (sh[0] - sh[0]) % PR  # remove constant (value at t): DeltaP has zero constant term
                    tot = padd(tot, sh)
                delta[(e, v)] = trim(tot, J)
        # NOTE: the zeroth coefficient of P(t+z)-P(t) is zero; we subtracted it by zeroing sh[0] above.
        clause_by_group = [[e for e in range(self.ne) if not self.dummy[e] and self.d[e][t - 1] == g] for g in range(r)]
        total = [0] * J
        for ytuple in itertools.product(*ach):
            prod = [1] + [0] * (J - 1)
            for g in range(r):
                Bg = [0] * J
                for u in by_y[g][ytuple[g]]:
                    counters["assign_evals"] += 1
                    A = [1] + [0] * (J - 1)
                    for e in clause_by_group[g]:
                        inner = [1] + [0] * (J - 1)
                        for v, neg in self.clauses[e]:
                            p = self.form_at(e, v, t)
                            val = sum(p[i] * u[i] for i in S[g]) % PR
                            for hgrp in range(r):
                                if hgrp == g:
                                    continue
                                val = (val + sum(lc * yy for lc, yy in zip(lam[(e, v, hgrp)], ytuple[hgrp]))) % PR
                            w = padd([val], delta[(e, v)])
                            fac = psub([1], w) if not neg else w
                            inner = pmul(inner, trim(fac, J), J)
                            counters["poly_mults"] += 1
                        phi = trim(psub([1], inner), J)
                        A = pmul(A, phi, J)
                        counters["poly_mults"] += 1
                    Bg = padd(Bg, trim(A, J))
                prod = pmul(prod, trim(Bg, J), J)
                counters["poly_mults"] += 1
            total = padd(total, trim(prod, J))
        return trim(total, J)

    def taylor_decoupled(self, t, design, J, q, counters):
        n = self.n
        res = [0] * J
        for size in range(0, min(q, n) + 1):
            for E in itertools.combinations(range(n), size):
                for usz in range(size + 1):
                    for U in itertools.combinations(E, usz):
                        zz = self.Z(t, design, set(E), set(U), J, counters)
                        counters["triples"] += 1
                        sgn = -1 if (size - usz) % 2 else 1
                        res = padd(res, pscale(zz, sgn % PR))
        return trim(res, J)


def hermite_recover(taylor, Q, J, deg):
    """solve for h_0..h_deg from Taylor data taylor[t][j] (t=1..Q, j<J). return (h0, rank_ok)."""
    N = deg + 1
    rows = []
    for t in range(1, Q + 1):
        for j in range(J):
            row = [(comb(i, j) * pow(t, i - j, PR)) % PR if i >= j else 0 for i in range(N)]
            row.append(taylor[t - 1][j] % PR)
            rows.append(row)
    ri = 0
    piv = []
    for c in range(N):
        pr_ = None
        for i in range(ri, len(rows)):
            if rows[i][c]:
                pr_ = i
                break
        if pr_ is None:
            continue
        rows[ri], rows[pr_] = rows[pr_], rows[ri]
        iv = inv(rows[ri][c])
        rows[ri] = [(x * iv) % PR for x in rows[ri]]
        for i in range(len(rows)):
            if i != ri and rows[i][c]:
                fac = rows[i][c]
                rows[i] = [(x - fac * y) % PR for x, y in zip(rows[i], rows[ri])]
        piv.append(c)
        ri += 1
    consistent = all(not rows[i][N] for i in range(ri, len(rows)))
    full = len(piv) == N
    h0 = None
    if full and piv[0] == 0:
        h0 = rows[0][N]
    return h0, full, consistent
