# Recomputation of numbers read in the 2026-11-28 appendix extension (Tables C.4, C.5, C.7 of arXiv 2611.23476v1). Inputs typed from the PDF text layer.
from statistics import mean
w0   =[77.15,71.78,59.80,61.67,58.65]; gd=[77.15,71.78,61.40,61.67,60.28]   # C.5 local-gym ACC: Calendar, Drive, CSM, HR, ITSM
w0s  =[48.84,46.67,30.56,32.08,30.51]; gds=[48.84,46.67,25.00,32.08,38.98]  # C.5 Solved
print("W0 macro ACC %.2f (C.7 prints 65.81); GUARD %.2f (prints 66.46); diff %.2f (prints -0.65 from GUARD)"%(mean(w0),mean(gd),mean(gd)-mean(w0)))
print("W0 macro Solved %.2f (prints 37.73); GUARD %.2f (prints 38.31)"%(mean(w0s),mean(gds)))
print("domains with GUARD final ACC == W0:",[n for n,a,b in zip(["Calendar","Drive","CSM","HR","ITSM"],w0,gd) if a==b])
print("w/o Analyze vs W0: %.2f (text -6.68); w/o Gate vs W0: %.2f"%(59.13-65.81,56.11-65.81))
# C.4 Final Mean by stream (task counts: 30 held-out tasks per group)
S={"Workflow(K=2)":{"W0":65.00,"Hermes":65.00,"RRSI":60.00,"GEPA":70.00,"MetaH":63.33,"GUARD":70.00},
   "Topic(K=3)":{"W0":67.78,"Hermes":70.00,"RRSI":66.67,"GEPA":67.78,"MetaH":68.89,"GUARD":70.00},
   "Domain(K=3)":{"W0":76.05,"Hermes":76.26,"RRSI":79.17,"GEPA":79.31,"MetaH":79.29,"GUARD":78.69},
   "Compound(K=4)":{"W0":70.84,"Hermes":70.00,"RRSI":65.84,"GEPA":72.50,"MetaH":73.33,"GUARD":74.17}}
K={"Workflow(K=2)":2,"Topic(K=3)":3,"Domain(K=3)":3,"Compound(K=4)":4}
for s,d in S.items():
    ev={k:v for k,v in d.items() if k!="W0"}; best=max(ev.values()); n=K[s]*30
    ties=[k for k,v in ev.items() if abs(v-best)<1e-9 and k!="GUARD"]
    second=sorted(ev.values())[-2]
    print("%-14s GUARD %.2f best-evolving %.2f ties-with %s; gap to best non-GUARD %.2fpp = %.1f task(s) of %d"%(s,d["GUARD"],best,ties,d["GUARD"]-max(v for k,v in ev.items() if k!="GUARD"),(d["GUARD"]-max(v for k,v in ev.items() if k!="GUARD"))/100*n,n))
