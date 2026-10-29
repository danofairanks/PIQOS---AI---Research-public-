"""O10 counter-model search (see PREREG.md). Two independent ring implementations; abstract
bookkeeping model of canonical lifts and precision chains. Run: python3 -I o10_check.py [N] [seed0]"""
import sys, json, random, itertools
import numpy as np

RINGS = {"e3": ([1, 1, 0], 3), "e4": ([1, 1, 0, 0], 4)}   # f = U^e + sum f_i U^i ; f_0..f_{e-1}
# f = U^3+U+1 -> low coeffs [1,1,0]; f = U^4+U+1 -> [1,1,0,0]; both irreducible mod 2

class Ring:
    def __init__(self, low, e, ell):
        self.low, self.e, self.ell = low, e, ell
        self.n = e * ell
        # companion matrix of U acting on basis U^0..U^{e-1}: column i = U*U^i
        CU = [[0] * e for _ in range(e)]
        for i in range(e - 1):
            CU[i + 1][i] = 1
        for i in range(e):
            CU[i][e - 1] = -low[i]
        CU = np.array(CU, dtype=object)
        NV = np.zeros((ell, ell), dtype=object)
        for j in range(ell - 1):
            NV[j + 1][j] = 1
        I_e = np.identity(e, dtype=object); I_l = np.identity(ell, dtype=object)
        self.basis = {}
        pw = I_e
        for i in range(e):
            vw = I_l
            for j in range(ell):
                # coordinate index (j, i) -> position j*e + i
                self.basis[(j, i)] = np.kron(vw, pw)
                vw = vw @ NV
            pw = pw @ CU
    # implementation (i): explicit coefficient arithmetic
    def mul_i(self, x, y):
        e, ell, low = self.e, self.ell, self.low
        out = [[0] * e for _ in range(ell)]
        for j1 in range(ell):
            for j2 in range(ell - j1):
                a, b = x[j1], y[j2]
                prod = [0] * (2 * e - 1)
                for i1 in range(e):
                    if a[i1]:
                        for i2 in range(e):
                            prod[i1 + i2] += a[i1] * b[i2]
                for k in range(2 * e - 2, e - 1, -1):
                    c = prod[k]
                    if c:
                        prod[k] = 0
                        for i in range(e):
                            prod[k - e + i] -= c * low[i]
                for i in range(e):
                    out[j1 + j2][i] += prod[i]
        return out
    # implementation (ii): left-multiplication matrices
    def mat(self, x):
        M = np.zeros((self.n, self.n), dtype=object)
        for j in range(self.ell):
            for i in range(self.e):
                c = x[j][i]
                if c:
                    M = M + c * self.basis[(j, i)]
        return M
    def vec(self, x):
        return np.array([x[j][i] for j in range(self.ell) for i in range(self.e)], dtype=object)

def rand_elem(rng, ell, e, bound):
    return [[rng.randrange(bound) for _ in range(e)] for _ in range(ell)]

def reduce_mod(x, m):
    return [[c % m for c in row] for row in x]

def centered(x, kappa):
    h = 1 << (kappa - 1); m = 1 << kappa
    return [[(c % m) - m if (c % m) >= h else (c % m) for c in row] for row in x]

class Net:
    """Bipartite multigraph; tables[v] maps bit-tuple on ports -> ring element (list of ell lists of e ints)."""
    def __init__(self, nv, edges, tables, kappa):
        self.nv, self.edges, self.tables, self.kappa = nv, edges, tables, kappa
        self.ports = [[] for _ in range(nv)]
        for ei, (a, b) in enumerate(edges):
            self.ports[a].append(ei); self.ports[b].append(ei)
    def copy(self):
        return Net(self.nv, self.edges, [dict(t) for t in self.tables], list(self.kappa))

def rand_net(rng, R, bound):
    nl = rng.randint(2, 3); nr = rng.randint(2, 3)
    nv = nl + nr
    ne = rng.randint(4, 6)
    edges = [(rng.randrange(nl), nl + rng.randrange(nr)) for _ in range(ne)]
    # make sure every vertex has at least one port
    for v in range(nv):
        if not any(v in ed for ed in edges):
            edges[rng.randrange(ne)] = (v, nl + rng.randrange(nr)) if v < nl else (rng.randrange(nl), v)
    net = Net(nv, edges, [None] * nv, [1] * nv)
    tables = []
    for v in range(nv):
        d = len(net.ports[v])
        tables.append({b: rand_elem(rng, R.ell, R.e, bound) for b in itertools.product((0, 1), repeat=d)})
    net.tables = tables
    return net

def Z_i(R, net):
    ne = len(net.edges)
    tot = [[0] * R.e for _ in range(R.ell)]
    for b in itertools.product((0, 1), repeat=ne):
        acc = None
        for v in range(net.nv):
            key = tuple(b[ei] for ei in net.ports[v])
            ent = net.tables[v][key]
            acc = ent if acc is None else R.mul_i(acc, ent)
        for j in range(R.ell):
            for i in range(R.e):
                tot[j][i] += acc[j][i]
    return tot

def Z_ii(R, net):
    ne = len(net.edges)
    mats = [{k: R.mat(x) for k, x in net.tables[v].items()} for v in range(net.nv)]
    vecs = [{k: R.vec(x) for k, x in net.tables[v].items()} for v in range(net.nv)]
    tot = np.zeros(R.n, dtype=object)
    for b in itertools.product((0, 1), repeat=ne):
        cur = None
        for v in range(net.nv):
            key = tuple(b[ei] for ei in net.ports[v])
            cur = vecs[v][key] if cur is None else mats[v][key].dot(cur)
        tot = tot + cur
    return [[int(tot[j * R.e + i]) for i in range(R.e)] for j in range(R.ell)]

def eqmod(a, b, p):
    m = 1 << p
    return all((a[j][i] - b[j][i]) % m == 0 for j in range(len(a)) for i in range(len(a[0])))

def Z(R, net, stats):
    a, b = Z_i(R, net), Z_ii(R, net)
    stats["impl_disagree"] += (a != b)
    return a

def replace_with_lift(net, S, q):
    n2 = net.copy()
    for v in S:
        n2.tables[v] = {k: reduce_mod(x, 1 << q) for k, x in n2.tables[v].items()}
        n2.kappa[v] = q
    return n2

def run(N, seed0):
    out = {}
    rng0 = random.Random(seed0)
    conds = ["O10a", "O10b", "M1", "M2", "M3"]
    stats = {c: {"trials": 0, "applicable": 0, "fail": 0, "kappa_viol": 0} for c in conds}
    stats["impl_disagree"] = 0
    for t in range(N):
        seed = seed0 * 1000003 + t
        rng = random.Random(seed)
        rname = rng.choice(list(RINGS)); low, e = RINGS[rname]; ell = rng.choice([2, 3])
        R = Ring(low, e, ell)
        p0 = rng.randint(1, 6); p1 = p0 + rng.randint(0, 4); p2 = p1 + rng.randint(0, 4)
        net0 = rand_net(rng, R, 1 << (p2 + 4))   # "true" entries, coordinates beyond every precision
        # O10a
        q = p0 + rng.randint(0, 4)
        S = [v for v in range(net0.nv) if rng.random() < 0.6]
        st = stats["O10a"]; st["trials"] += 1; st["applicable"] += 1
        z0 = Z(R, net0, stats); za = Z(R, replace_with_lift(net0, S, q), stats)
        st["fail"] += (not eqmod(z0, za, p0))
        # O10b
        S1 = [v for v in range(net0.nv) if rng.random() < 0.6]; S2 = [v for v in range(net0.nv) if rng.random() < 0.6]
        n1 = replace_with_lift(net0, S1, p1); n2 = replace_with_lift(n1, S2, p2)
        z1, z2 = Z(R, n1, stats), Z(R, n2, stats)
        st = stats["O10b"]; st["trials"] += 1; st["applicable"] += 1
        ok = eqmod(z0, z1, p0) and eqmod(z1, z2, p1) and eqmod(z0, z2, p0)
        st["fail"] += (not ok)
        st["kappa_viol"] += (any(n2.kappa[v] > p2 for v in range(n2.nv)) or any(n1.kappa[v] > p1 for v in range(n1.nv)))
        # M1: non-monotone: reduce mod 2^q with q < p0 then evaluate at p0
        if p0 >= 2:
            qm = rng.randint(1, p0 - 1)
            Sm = [v for v in range(net0.nv) if rng.random() < 0.6] or [0]
            nm = replace_with_lift(net0, Sm, qm)
            changed = any(eqmod([r for r in (a,)][0], b, p0) is False
                          for v in Sm for k in net0.tables[v]
                          for a, b in [(net0.tables[v][k], nm.tables[v][k])])
            st = stats["M1"]; st["trials"] += 1
            if changed:
                st["applicable"] += 1
                st["fail"] += (not eqmod(z0, Z(R, nm, stats), p0))
        # M2: mismatched convention (centered lift in child for retained vertices), kappa < p0
        kap = rng.randint(1, p0 - 1) if p0 >= 2 else None
        if kap:
            nparent = replace_with_lift(net0, list(range(net0.nv)), kap)        # canonical lift at kappa
            Sc = [v for v in range(net0.nv) if rng.random() < 0.6] or [0]
            nchild = nparent.copy()
            for v in Sc:
                nchild.tables[v] = {k: centered(x, kap) for k, x in nparent.tables[v].items()}
            changed = any(not eqmod(nparent.tables[v][k], nchild.tables[v][k], p0) for v in Sc for k in nparent.tables[v])
            st = stats["M2"]; st["trials"] += 1
            if changed:
                st["applicable"] += 1
                st["fail"] += (not eqmod(Z(R, nparent, stats), Z(R, nchild, stats), p0))
        # M3: packet created at kappa1 > later call precision, truncated, then evaluated at higher precision
        if p1 >= 2:
            kap1 = p1; pcall = rng.randint(1, kap1 - 1); phigh = rng.randint(pcall + 1, kap1)
            Sp = [v for v in range(net0.nv) if rng.random() < 0.6] or [0]
            npk = replace_with_lift(net0, Sp, kap1)
            ntr = replace_with_lift(npk, Sp, pcall)
            changed = any(not eqmod(npk.tables[v][k], ntr.tables[v][k], phigh) for v in Sp for k in npk.tables[v])
            st = stats["M3"]; st["trials"] += 1
            if changed:
                st["applicable"] += 1
                st["fail"] += (not eqmod(Z(R, npk, stats), Z(R, ntr, stats), phigh))
    return stats

def schedule_check():
    """P4: pi_{d+1}>=pi_d and p_t<=pi_{d+1}-style bound, integer grid. Preconditions are from the reconstruction
    (INDUCTION_LEMMA.md step 5): h=ceil(3M/u), D_t=L/2^i<=2^a, M<=M_d, p<=pi_d."""
    import math
    bad = 0; n = 0
    for Cs in (10**3, 10**4, 10**6):
        for d in range(0, 6):
            Md = Cs / 8 ** d
            for u in (1, 2, 3, 5, 8):
                for a in (2 * u, 2 * u + 1, 2 * u + 4):
                    pid = Cs  # pi_0
                    # build pi_d by recursion with same (u,a) for all levels (worst case constant schedule)
                    pis = [Cs]
                    for dd in range(d + 1):
                        Mdd = Cs / 8 ** dd
                        pis.append(pis[-1] + 8 * math.ceil(3 * Mdd / u) * 2 ** a + 8 * Mdd * (a + 1))
                    n += 1
                    if not all(pis[k + 1] >= pis[k] for k in range(len(pis) - 1)): bad += 1
                    if Md < 1: continue   # no edge can exist (A1: M <= M_d); grid fix, see DEVIATIONS.md
                    for M in (Md / 8, Md / 2, Md):
                        h = math.ceil(3 * M / u)
                        if M < 1: continue
                        for i in range(u):
                            for L in (1, 2 ** a):
                                D = L / 2 ** i
                                if D > 2 ** a: continue
                                pt_minus_p = 8 * h * D + 8 * M * (a + 1)
                                n += 1
                                if pt_minus_p > pis[d + 1] - pis[d] + 1e-9: bad += 1
    return {"grid_points": n, "violations": bad}

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    seed0 = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    res = {"N": N, "seed0": seed0, "stats": run(N, seed0), "schedule": schedule_check()}
    json.dump(res, open(f"o10_results_N{N}_s{seed0}.json", "w"), indent=1)
    print(json.dumps(res, indent=1))
