"""Companion: recount AlphaFold 3 and Boltz-1 rates on Astex and DockGen-E from the released bust_results.csv files (Zenodo 19138652: alphafold3_ and boltz_benchmark_method_predictions.tar.gz; only the csv files extracted into af3/csv and boltz/csv). Run `python3 -I released_data_check_af3_boltz.py` from their parent directory. The PB-gated column uses every PoseBusters check; on DockGen-E that is near 0 because the identity checks fail for most complexes, see README flag 1."""
import csv, glob, re, statistics as st
def load(p):
    rows=list(csv.DictReader(open(p)))
    if not rows: return {}
    cols=list(rows[0].keys()); a=cols.index('mol_pred_loaded'); b=cols.index('volume_overlap_with_waters'); bc=cols[a:b+1]
    d={}
    for r in rows:
        try: rm=float(r['rmsd'])
        except: rm=float('nan')
        try: cd=float(r['centroid_distance'])
        except: cd=float('nan')
        d[r['mol_id']]=(rm,cd,all(r[c]!='False' for c in bc))
    return d
cfg=[('AF3','af3/csv','alphafold3_{ds}_outputs_[123]'),('AF3-SS','af3/csv','alphafold3_ss_{ds}_outputs_[123]'),('Boltz-1','boltz/csv','boltz_{ds}_outputs_[123]'),('Boltz-1-SS','boltz/csv','boltz_ss_{ds}_outputs_[123]')]
printed={('AF3','astex_diverse'):(69.0,64.3,54.8),('Boltz-1','astex_diverse'):(49.6,51.2,40.1),('AF3','dockgen'):(54.0,51.0,44.3),('Boltz-1','dockgen'):(31.3,32.0,29.3)}
for ds,nstated in (('astex_diverse',85),('dockgen',122)):
    print("==",ds,"stated n",nstated)
    for name,root,pat in cfg:
        ps=[p for p in sorted(glob.glob(f"{root}/**/{pat.format(ds=ds)}/bust_results.csv",recursive=True))]
        runs=[load(p) for p in ps]
        if len(runs)!=3: print(name,"runs found:",len(runs)); continue
        cnt=[(sum(1 for v in r.values() if v[1]<=1),sum(1 for v in r.values() if v[0]<=2),sum(1 for v in r.values() if v[0]<=2 and v[2])) for r in runs]
        m=[st.mean(c[k] for c in cnt) for k in range(3)]
        print(f" {name}: rows per run {[len(r) for r in runs]} counts {cnt}")
        for N in (84,85,100,122):
            print(f"    /N={N}: {[round(100*x/N,1) for x in m]}")
        if (name,ds) in printed: print("    printed:",printed[(name,ds)])
