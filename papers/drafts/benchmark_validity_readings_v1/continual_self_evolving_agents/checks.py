"""Checks on Table 1 / Fig. 2 of arXiv 2610.25858v1 (values typed from the paper's Table 1 "Average" rows and Overall row).
Run: python3 -I checks.py   (needs only the standard library; no paper data or code is used beyond the typed numbers)"""
import math, random, statistics as st
# (P, S) per method per stream, from Table 1 'Average' rows
D = {
 'Topic':    {'RB': (0.7, -1.1), 'GEPA': (1.7, -4.8), 'MH': (-2.0, -0.3)},
 'Workflow': {'RB': (8.5, -4.8), 'GEPA': (11.0, -6.5), 'MH': (3.8, -0.5)},
 'Domain':   {'RB': (1.1, -0.4), 'GEPA': (4.7, -2.4), 'MH': (4.2, -3.1)},
 'Compound': {'RB': (3.1, -1.4), 'GEPA': (7.5, -3.3), 'MH': (2.9, -4.4)},
}
def pearson(x, y):
    mx, my = st.mean(x), st.mean(y)
    return sum((a-mx)*(b-my) for a, b in zip(x, y)) / math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
P = [v[0] for s in D.values() for v in s.values()]; S = [v[1] for s in D.values() for v in s.values()]
r = pearson(P, S); n = len(P)
t = r*math.sqrt((n-2)/(1-r*r))
print('pooled r (n=12)', round(r, 3), 't', round(t, 2))
# demean by scenario (remove scenario fixed effects) -> within-scenario correlation, n=12, 8 d.o.f. after removing 4 means
Pd, Sd = [], []
for s in D.values():
    mp = st.mean(v[0] for v in s.values()); ms = st.mean(v[1] for v in s.values())
    for v in s.values(): Pd.append(v[0]-mp); Sd.append(v[1]-ms)
rw = pearson(Pd, Sd); tw = rw*math.sqrt((n-4-1)/(1-rw*rw))
print('within-scenario r', round(rw, 3), 't', round(tw, 2), '(df=7)')
# demean by method (remove method effects) -> does anything remain beyond which method it is
Pm, Sm = [], []
for m in ('RB', 'GEPA', 'MH'):
    ps = [D[s][m][0] for s in D]; ss = [D[s][m][1] for s in D]
    for a, b in zip(ps, ss): Pm.append(a-st.mean(ps)); Sm.append(b-st.mean(ss))
rm = pearson(Pm, Sm); print('within-method r', round(rm, 3))
# identity bound: S <= -mean(max(0,P_k-Term_k)) <= -(Pbar-Termbar); Overall row values
overall = {'RB': (3.3, -1.9, 2.5), 'GEPA': (6.2, -4.3, 3.7), 'MH': (2.2, -2.1, 1.4)}
for m, (p, s, term) in overall.items():
    print(m, 'P', p, 'Term', term, 'bound S <=', round(-(p-term), 2), 'observed S', s)
# null-floor Monte Carlo: zero true effect, only rollout noise in each evaluation (sigma_e per eval, pp)
def null_S(T, K, sigma_e, trials=20000, seed=1):
    rnd = random.Random(seed); ckpt = list(range(50, T+1, 50)); out = []
    for _ in range(trials):
        B = [rnd.gauss(0, sigma_e) for _ in range(K)]
        A = {(m, k): rnd.gauss(0, sigma_e) for m in ckpt for k in range(K)}
        I = []; F = []
        for k in range(K):
            sig = 50*k; tau = 50*(k+1)
            pre = [t for t in ckpt if 0 < t <= sig]
            I.append(sum(max(0, B[k]-A[(t, k)]) for t in pre)/len(pre) if pre else 0.0)
            F.append(max(0, A[(tau, k)]-A[(T, k)]) if tau < T else 0.0)
        out.append(-(st.mean(I)+st.mean(F)))
    return st.mean(out)
for sig in (1.5, 1.9, 2.5):
    print('sigma_e', sig, 'null-floor S: topic', round(null_S(150, 3, sig), 2), 'workflow', round(null_S(100, 2, sig), 2),
          'domain', round(null_S(150, 3, sig), 2), 'compound', round(null_S(200, 4, sig), 2))
# rollout-noise SD of a 50-task accuracy averaged over 8 rollouts at mean per-task p(1-p) = v
for v in (0.10, 0.15, 0.20):
    print('v', v, 'SD single eval (pp)', round(100*math.sqrt(v/(8*50)), 2), 'SD paired diff', round(100*math.sqrt(2*v/(8*50)), 2))
