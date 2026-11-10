"""Recount PoseBench (arXiv 2405.14108v7) success rates from the released PoseBusters-software outputs (Zenodo record 19138652: diffdock_ and vina_benchmark_method_predictions.tar.gz). Only the bust_results.csv files are read; nothing from the authors repository is executed.
Setup: extract the bust_results.csv files into diffdock/csv and vina/csv, run `python3 -I released_data_check.py` from their parent directory.
Success = rmsd <= 2 A (and PoseBusters checks mol_pred_loaded..volume_overlap_with_waters all pass, empty cells count as pass). The printed rates are recomputed over several candidate denominators."""
import csv, glob, os, re, sys, statistics as st
def load(p):
    rows=list(csv.DictReader(open(p)))
    cols=rows[0].keys() if rows else []
    order=list(cols); a=order.index('mol_pred_loaded'); b=order.index('volume_overlap_with_waters'); boolcols=order[a:b+1]
    out={}
    for r in rows:
        try: rmsd=float(r['rmsd'])
        except: rmsd=float('nan')
        try: cd=float(r['centroid_distance'])
        except: cd=float('nan')
        valid=all(r[c]!='False' for c in boolcols)
        out[r['mol_id']]=(rmsd,cd,valid)
    return out, len(boolcols)
res={}
for method,root in (('DiffDock-L','diffdock/csv'),('P2Rank-Vina','vina/csv')):
    for p in sorted(glob.glob(root+'/**/bust_results.csv',recursive=True)):
        d=os.path.basename(os.path.dirname(p))
        if 'relaxed' in d: continue
        m=re.search(r'(astex_diverse|posebusters_benchmark|dockgen)',d).group(1); run=int(re.search(r'_(\d)$',d).group(1))
        o,nb=load(p)
        res.setdefault((method,m),{})[run]=o
print("method / dataset: per-run rows | n(RMSD<=2) | n(RMSD<=2 & PB-valid) | n(cRMSD<=1)")
for (method,m),runs in sorted(res.items()):
    stats=[]
    for run,o in sorted(runs.items()):
        v=list(o.values())
        stats.append((len(v), sum(1 for x in v if x[0]<=2), sum(1 for x in v if x[0]<=2 and x[2]), sum(1 for x in v if x[1]<=1)))
    print(method,m,stats)
    ids=set().union(*[set(o) for o in runs.values()])
    print("   union of mol_ids across runs:",len(ids),"| ids in all 3 runs:",len(set.intersection(*[set(o) for o in runs.values()])))
    for N in (84,85,122,130,280,308):
        r2=[100*s[1]/N for s in stats]; rv=[100*s[2]/N for s in stats]; rc=[100*s[3]/N for s in stats]
        print(f"   /N={N}: cRMSD<=1 {st.mean(rc):.1f}  RMSD<=2 {st.mean(r2):.1f}  RMSD<=2&PB {st.mean(rv):.1f}")
    rr=[100*s[1]/s[0] for s in stats]; rvv=[100*s[2]/s[0] for s in stats]
    print(f"   /rows: RMSD<=2 {st.mean(rr):.1f}  RMSD<=2&PB {st.mean(rvv):.1f}")
