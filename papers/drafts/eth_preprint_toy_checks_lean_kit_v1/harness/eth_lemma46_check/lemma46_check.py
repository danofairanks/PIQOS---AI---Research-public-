import itertools, json, math, random, sys
from fractions import Fraction
from math import comb, factorial, log2
import numpy as np

def setup(r, Q):
    base = r*r; D = r**(2*Q)
    idx = np.arange(D, dtype=np.int64)
    digits = [(idx // base**s) % base for s in range(Q)]            # pair index per position
    swap = lambda pa: (pa % r)*r + pa//r
    perm = []
    for s in range(Q):
        sw = swap(digits[s])
        perm.append(idx + (sw - digits[s])*base**s)
    permV = idx.copy()
    for s in range(Q):
        permV = permV + (swap(digits[s]) - digits[s])*base**s
    return D, digits, perm, permV

def row_of_dden_M0(u_rows, r, Q, R, A0, D, perm, permV):
    """(R-1)! * M0[u,:] for the given rows u (array), as int64 matrix len(u_rows) x D."""
    sig = permV[u_rows]
    X = np.zeros((len(u_rows), D), dtype=np.int64)
    X[np.arange(len(u_rows)), sig] = 1                  # rows of identity at sigma(u)
    total = np.zeros_like(X)
    for j in range(R):
        coef = (-1)**(A0+j) * (factorial(R-1)//factorial(j))
        total += coef*X
        # X <- X (N - 2(A0+j) I),  N = Q I - sum_s Pi_s  (symmetric)
        Y = Q*X - 2*(A0+j)*X
        for s in range(Q):
            Y -= X[:, perm[s]]
        X = Y
        if np.abs(X).max() > 2**60: raise OverflowError
    return total

def check(r, Q, R, rows_sample=None, seed=0):
    D, digits, perm, permV = setup(r, Q)
    p = (r-1)/(2*r)
    A0 = max(0, min(int(round(Q*p-(R-1)/2)), Q+1-R))
    rng = np.random.default_rng(seed)
    u_rows = np.arange(D) if (rows_sample is None or D <= rows_sample) else rng.choice(D, rows_sample, replace=False)
    dM = row_of_dden_M0(u_rows, r, Q, R, A0, D, perm, permV)   # (R-1)! M0 rows
    fR = factorial(R-1); fQ = factorial(Q); dden = fR*fQ
    # phi_E scaled: Q! * phi_E integer coefficients, cached per E
    cache = {}
    def phiE(E):
        if E not in cache:
            poly = [Fraction(1)]
            for s in E:
                new = [Fraction(0)]*(len(poly)+1)
                for a, c in enumerate(poly):
                    new[a] += c; new[a+1] -= c/s
                poly = new
            sc = [c*fQ for c in poly]
            assert all(c.denominator == 1 for c in sc)
            cache[E] = [int(c) for c in sc]
        return cache[E]
    nonint = 0; maxrow = 0; maxcoef = 0; maxM0norm = Fraction(0); maxdeg = 0; maxE = 0
    for ii, u in enumerate(u_rows):
        du = [int(digits[s][u]) % r for s in range(Q)]
        row = dM[ii]
        m0norm = Fraction(int(np.abs(row).sum()), fR)
        maxM0norm = max(maxM0norm, m0norm)
        rowsum = 0
        nz = np.nonzero(row)[0]
        # delta_u (I - M0) part: d_den (delta_uw - M0[u,w]) = fQ*(fR*delta - dM)
        # sum over all w: contributions from w in nz and from w=u (delta)
        support = set(nz.tolist()) | {int(u)}
        for w in support:
            m = int(row[w])
            aw = [int(digits[s][w]) // r for s in range(Q)]
            E = tuple(s+1 for s in range(Q) if aw[s] != du[s])
            if m: maxE = max(maxE, len(E))
            ph = phiE(E)
            # poly = fQ*(fR*[u==w] - m) + m*ph   (m*ph already scaled by fQ since ph = fQ*phi)
            poly = [m*c for c in ph]
            poly[0] += fQ*(fR*(1 if w == u else 0) - m)
            rowsum += sum(abs(c) for c in poly)
            maxcoef = max(maxcoef, max(abs(c) for c in poly))
            maxdeg = max(maxdeg, max((i for i, c in enumerate(poly) if c), default=0))
        maxrow = max(maxrow, rowsum)
    bound = dden*(1 + (1 + 2**Q)*R*(4*Q)**(R-1))
    m0bound = R*(4*Q)**(R-1)
    return dict(r=r, Q=Q, R=R, D=D, A0=A0, rows_checked=len(u_rows), dden=dden, nonintegral=nonint,
                maxrowsum=maxrow, bound_lemma46=bound, log2_maxrow=round(log2(maxrow), 2), log2_bound=round(log2(bound), 2),
                slack_bits=round(log2(bound)-log2(maxrow), 2), maxM0norm=float(maxM0norm), M0norm_bound=m0bound,
                max_deg_P=maxdeg, deg_ok=maxdeg <= R-1, max_E=maxE, sparsity_ok=maxE <= R-1,
                bound_holds=maxrow <= bound and float(maxM0norm) <= m0bound)

if __name__ == "__main__":
    out = []
    specs = [(2,3,1),(2,3,2),(2,3,3),(2,3,4),(3,2,3),(2,4,2),(2,4,4),(2,4,5),(3,3,2),(3,3,4),(2,5,3),(2,5,5),(2,5,6),
             (2,6,3),(2,6,5),(2,6,7),(3,4,3),(3,4,5),(4,3,3)]
    for (r, Q, R) in specs:
        try:
            res = check(r, Q, R, rows_sample=700)
        except (OverflowError, MemoryError) as e:
            print("skip", r, Q, R, type(e).__name__); continue
        out.append(res)
        print({k: res[k] for k in ['r','Q','R','D','rows_checked','nonintegral','log2_maxrow','log2_bound','slack_bits','maxM0norm','M0norm_bound','deg_ok','sparsity_ok','bound_holds']}, flush=True)
    json.dump(out, open("lemma46_results.json", "w"), indent=1)
    print("ALL bound_holds:", all(o['bound_holds'] for o in out), " ALL deg_ok:", all(o['deg_ok'] for o in out), " ALL sparsity:", all(o['sparsity_ok'] for o in out))
