"""Recompute the paper's Table 2 aggregates and the extra statistics used in NOTE.md.
Delta% values transcribed from Table 2 of arXiv 2610.28763v1 (order: ATAT, CarbonGlobe, CheMixHub, CosmoBench,
DART-Eval, ESCAPE, GEO-Bench-2, gRNAde, GTPBD, LITHOS, Mars-Bench, MassSpecGym, MOTIVE, NeuroGraph, PFDelta,
ProteinGym, SR-CACO-2, TIDMAD, TreeFinder, UniSite). Standard library only."""
import statistics as st
from math import comb
names = "ATAT CarbonGlobe CheMixHub CosmoBench DART-Eval ESCAPE GEO-Bench-2 gRNAde GTPBD LITHOS Mars-Bench MassSpecGym MOTIVE NeuroGraph PFDelta ProteinGym SR-CACO-2 TIDMAD TreeFinder UniSite".split()
opus  = [0.8,14.7,11.9,4.8,6.1,1.4,9.6,2.6,5.1,-3.8,46.4,7.6,4.1,-0.2,64.4,0.3,0.9,7.4,17.8,6.7]
opus_s= [3.4,35.3,23.1,6.9,9.9,4.7,37.9,-0.6,6.4,7.0,61.4,39.5,10.4,5.6,91.0,0.4,2.9,30.0,19.8,6.2]
codex = [0.8,-1.3,15.4,3.0,0.6,2.1,-2.8,-2.3,4.5,4.8,7.6,14.2,2.8,4.6,4.6,-0.7,0.3,7.7,12.9,8.5]
codex_s=[-0.1,17.9,16.7,7.7,1.3,4.9,12.7,-6.1,5.6,-10.0,42.7,23.0,23.3,3.7,-12.8,0.0,-0.8,13.3,12.8,5.3]
def sign_p(k, n):  # two-sided exact sign test, H0: p=0.5
    return min(1.0, 2 * sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n)
for label, x in (("opus", opus), ("opus+skills", opus_s), ("codex", codex), ("codex+skills", codex_s)):
    print(f"{label:<13} mean {st.mean(x):6.2f}  median {st.median(x):6.2f}  negative benchmarks {sum(v < 0 for v in x)}")
for label, a, b in (("opus", opus, opus_s), ("codex", codex, codex_s)):
    better = sum(y > x for x, y in zip(a, b)); d = [y - x for x, y in zip(a, b)]
    print(f"{label}: skills better on {better}/20, two-sided sign p = {sign_p(better, 20):.4g}; "
          f"mean diff {st.mean(d):.2f}, median diff {st.median(d):.2f}, sd {st.stdev(d):.1f}")
drop = lambda x, ex: [v for n, v in zip(names, x) if n not in ex]
print("opus excl PFDelta+Mars-Bench:", round(st.mean(drop(opus, {'PFDelta', 'Mars-Bench'})), 2), "->",
      round(st.mean(drop(opus_s, {'PFDelta', 'Mars-Bench'})), 2))
ex = {'Mars-Bench', 'MOTIVE', 'CarbonGlobe'}
print("codex skill effect excl Mars-Bench, MOTIVE, CarbonGlobe (mean of diffs):",
      round(st.mean([y - x for n, x, y in zip(names, codex, codex_s) if n not in ex]), 2))
