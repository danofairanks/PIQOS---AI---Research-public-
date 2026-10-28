"""Per-n log2-cost model of the Appendix D (tensor contraction) algorithm of the ETH preprint.
Leading-order explicit constants from D.4.2-D.4.7; see DEVIATIONS.md."""
import math, json
from math import isqrt, log2, log, pi, sqrt
EPS = 1/(128*1024)

def contraction_bits(s, C):
    """bits of exponent for Theorem D.1 on a network of <= C s edges, s=2^lam-ish. Returns F/s."""
    lam = max(2, math.ceil(log2(s)) if s > 1 else 2)
    Hs = 1/ math.floor(math.sqrt(lam))                   # leaf cost 2^H, H = s/floor(sqrt(lam)); per s
    tot = Hs
    d = 0
    while True:
        Md = C*8.0**(-d)                                  # M_d / s
        if Md <= Hs: break
        ud = EPS*lam/2**d
        # ln N_d <= 2 pi sqrt(M p_t / D_t), p_t ~ 24 M D_t / u  =>  2 pi sqrt(24) M / sqrt(u)
        tot += (2*pi*sqrt(24)*Md/ sqrt(ud))/log(2)
        d += 1
        if d > 200: break
    return tot, d

def lam_s(lam_n):
    return lam_n

def fixed_density_total(lam, k, D):
    # clause network: s = n + m, edges <= 4 k m (C = 4kD/(1+D)); exponent per n = (1+D) * F/s
    s_over_n = 1 + D
    C = 4*k*D/(1+D)
    f, depth = contraction_bits(2.0**min(lam, 1000) if lam > 1000 else 2.0**lam, C) if lam <= 1000 else (None, None)
    return None

def contraction_per_s(lam, C):
    """same as contraction_bits but with lam given directly (no 2^lam float)."""
    Hs = 1/math.floor(math.sqrt(lam))
    tot = Hs; d = 0
    while True:
        Md = C*8.0**(-d)
        if Md <= Hs or d > 400: break
        ud = EPS*lam/2**d
        tot += (2*pi*sqrt(24)*Md/ sqrt(ud))/log(2)
        d += 1
    return tot, d

def fixed_density(lam, k, D):
    C = 4*k*D/(1+D)
    f, d = contraction_per_s(lam, C)
    return (1+D)*f, d, C

def tree_params_fixed_s(lam, k, s):
    Gam = 2*(3**(k-1)-1)
    M = 1
    while M < Gam: M *= 2
    while True:
        Cc = 4*sum((3*M)**j for j in range(0, k-1))
        h = (4*Cc*M-1).bit_length()
        if Gam*h*s <= M: break
        M *= 2
    B = 2*sum(M**j for j in range(0, k))
    return M, B

def general(lam, k):
    nu = (lam-1).bit_length()
    s = isqrt(lam-1)+1                                    # sigma = 1/ceil(sqrt(lam))
    M, B = tree_params_fixed_s(lam, k, s)
    mu = lam + B.bit_length() + 1
    D0 = 320000*B*B*mu**3
    # D.3: s_size = n*nu wires; wires M_w <= K log2(e (N+K)/K), K = k(6n + 2n) = 8kn, N <= 6n * k 2^k D0
    K = 8*k
    N = 6*k*(2**k)*D0
    Cw = K*(log2(N+K) - log2(K) + log2(math.e))/nu                        # edges per s (s = n nu)
    f, d = contraction_per_s(lam, Cw)
    sigma = 1/s
    branch = 1/sqrt(lam)
    total = sigma + branch + nu*f
    return dict(lam=lam, k=k, nu=nu, B=B, log2_D0=log2(D0), C_edges_per_s=Cw, levels=d, f_per_s=f, sigma=sigma,
                branch=branch, total=total)

def crossover(fn, lo=1e6, hi=1e22):
    x = lo; pts = []
    while x < hi:
        r = fn(int(x)); pts.append(r); x *= 1.15
    first = next((r for r in pts if r['total'] < 1), None)
    if not first: return None
    i = pts.index(first)
    a, b = (pts[i-1]['lam'] if i else int(lo)), first['lam']
    while b - a > 1:
        m = (a+b)//2
        if fn(m)['total'] < 1: b = m
        else: a = m
    bad = sum(1 for j in range(3000) if fn(int(b*(1+0.003*j)))['total'] >= 1)
    return b, fn(b), bad

if __name__ == "__main__":
    out = {}
    print("level sum factor sum_d 2^(-5d/2) =", sum(2**(-2.5*d) for d in range(60)))
    print("per-level constant (bits) 2 pi sqrt(24)/ln2 / sqrt(eps) =", 2*pi*sqrt(24)/log(2)/sqrt(EPS))
    # fixed density
    for k in (3,):
        for D in (1, 4.27, 10, 100):
            def fn(l, k=k, D=D):
                t, d, C = fixed_density(l, k, D); return dict(lam=l, total=t, levels=d, C=C)
            res = crossover(fn, 1e6, 1e20)
            out[f"fixed_k{k}_D{D}"] = res
            print(f"fixed density k={k} D={D}: lambda* = {res[0]:,}  total {res[1]['total']:.6f} levels {res[1]['levels']} C {res[1]['C']:.2f}  recross {res[2]}")
    # general density
    for k in (2, 3, 4):
        res = crossover(lambda l, k=k: general(l, k), 1e8, 1e24)
        out[f"general_k{k}"] = res
        g = res[1]
        print(f"general k={k}: lambda* = {res[0]:,}  total {g['total']:.5f} nu {g['nu']} log2D0 {g['log2_D0']:.1f} C/s {g['C_edges_per_s']:.1f} levels {g['levels']} sigma {g['sigma']:.2e} recross {res[2]}")
    # literal (D.5) validity threshold
    for C in (12, 144):
        print("literal u>=lam^(4/5) at last level needs lam >= (C^(1/3)/eps)^30 = 2^%.0f for C=%d" % (30*log2(C**(1/3)/EPS), C))
    json.dump(out, open("appendixD_results.json", "w"), indent=1, default=str)
