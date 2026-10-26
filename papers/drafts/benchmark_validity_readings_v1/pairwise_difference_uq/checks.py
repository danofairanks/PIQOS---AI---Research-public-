import numpy as np
rng=np.random.default_rng(0)
def counts(u,z):
    pos=u[z==1]; neg=u[z==0]
    d=pos[:,None]-neg[None,:]
    return (d>0).sum(),(d<0).sum(),(d==0).sum()
print("C1 on random scores: paper's C/(C+D) vs Goodman-Kruskal (C-D)/(C+D) vs AUC-excluding-ties; identity gamma = 2*AUC' - 1")
for trial in range(3):
    n=500; z=(rng.random(n)<0.2).astype(int); u=rng.normal(size=n)+0.8*z
    C,D,T=counts(u,z); auc_x=C/(C+D); gamma=(C-D)/(C+D)
    print(f"  trial {trial}: C/(C+D)={auc_x:.3f}  gamma={gamma:.3f}  2*C/(C+D)-1={2*auc_x-1:.3f}")
print("C2 tie handling: same underlying signal, tie-heavy (leaf-constant, 5 levels) vs continuous; gamma ignores tied pairs")
n=4000; z=(rng.random(n)<0.2).astype(int); s=rng.normal(size=n)+0.8*z
cont=s; tied=np.digitize(s,np.quantile(s,[0.2,0.4,0.6,0.8]))
for name,u in (("continuous",cont),("5 levels",tied)):
    C,D,T=counts(u,z); tot=C+D+T
    print(f"  {name:10s} gamma={(C-D)/(C+D):.3f}  AUC(ties=1/2)={(C+0.5*T)/tot:.3f}  share of pos-neg pairs tied={T/tot:.3f}")
