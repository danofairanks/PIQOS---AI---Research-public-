# E1 checks on general_ml/Evaluation_DR-Schervish.pdf, using only numbers/equations printed in the paper.
import numpy as np, itertools, re
rng=np.random.default_rng(0)
print("== C1 cell count: feasible (subgroup,Ns) with Ns<=n")
n={'Cauc':2628,'AA':332,'Hisp':190,'Oth':108,'M':2050,'F':1316,'<50':718,'50-65':884,'65-80':1156,'80+':608}
L=[40,80,160,320,640]
cells={g:[s for s in L if s<=v] for g,v in n.items()}
tot=sum(len(v) for v in cells.values()); mino=sum(len(cells[g]) for g in ('AA','Hisp','Oth'))
print("total",tot,"minority(AA,Hisp,Oth)",mino,"rest",tot-mino,"| full grid 50")
print("== C2 Table 6 consistency")
ev={'Cauc':231,'AA':6,'Hisp':14,'Oth':14,'M':166,'F':112,'<50':18,'50-65':56,'65-80':101,'80+':104}
print("race n sum",sum(n[k] for k in('Cauc','AA','Hisp','Oth')),"events",sum(ev[k] for k in('Cauc','AA','Hisp','Oth')))
print("sex n sum",n['M']+n['F'],"events",ev['M']+ev['F'])
print("age n sum",sum(n[k] for k in('<50','50-65','65-80','80+')),"events",sum(ev[k] for k in('<50','50-65','65-80','80+')))
print("overall n 3366 events 280; prevalence",round(280/3366,4))
print("expected events in a draw of 40 from AA:",round(40*6/332,2),"; from Age<50:",round(40*18/718,2))
print("== C3 Brier >= ECE^2 using Table 1 columns 2 and 3 read as printed (ECE col=2nd value)")
rows={'Cauc':(.829,.062),'AA':(.889,.036),'Hisp':(.839,.044),'Oth':(.744,.128),'M':(.832,.062),'F':(.829,.062),'<50':(.931,.024),'50-65':(.875,.052),'65-80':(.805,.070),'80+':(.712,.106)}
for g,(e,b) in rows.items(): print(g,"ECE",e,"ECE^2",round(e*e,3),"Brier",b,"violates" if e*e>b else "ok")
print("== C4 Eq.8 Hermite envelope, fixed delta")
u,v,d=0.3,0.7,0.05
def H(s):
    if s<u+d: return u+d/np.pi*np.sin(np.pi*(s-u)/d)
    if s<=v-d: return s
    return v-d/np.pi*np.sin(np.pi*(v-s)/d)
print("value just below / at u+d:",H(u+d-1e-9),H(u+d),"(continuity)")
xs=np.linspace(u-0.05,v+0.05,200001); hs=np.array([H(x) for x in xs]); dh=np.diff(hs)
print("max |H'| ",round(abs(dh/np.diff(xs)).max(),3),"min H' ",round((dh/np.diff(xs)).min(),3),"non-monotone:",bool((dh<0).any()))
print("== C5 Prop A.1 / Eq.9 Bayes-equivalence, K=3 random cost matrices")
def trial(K):
    p=rng.dirichlet(np.ones(K)); C=rng.uniform(.1,10,(K,K)); np.fill_diagonal(C,0)
    r=[p[k]/(p[k]+sum(C[k,j]/C[j,k]*p[j] for j in range(K) if j!=k)) for k in range(K)]
    loss=[sum(C[d,y]*p[y] for y in range(K)) for d in range(K)]
    return int(np.argmax(r))!=int(np.argmin(loss))
for K in(2,3,5): print("K",K,"disagreement rate",np.mean([trial(K) for _ in range(20000)]))
print("== C6 Eq.5 vs Monte-Carlo MSE-optimal lambda, B=0, f=0 (no shift; m correct; w = 1+independent noise, mean 1 -> EIF unbiased)")
N=200000; reps=20000; n_s=40
x=rng.normal(size=N); m=1/(1+np.exp(-(x-2))); y=(rng.uniform(size=N)<m).astype(float); l=y
wn=1+rng.normal(0,0.3,N)
Ve=l.var();Cem=np.cov(l,m)[0,1];lam5=((Ve-Cem)/n_s)/(np.var(l-m)/n_s)
def mc(wv):
    P=[];E=[]
    for _ in range(reps):
        i=rng.integers(0,N,n_s); P.append(l[i].mean()); E.append((wv[i]*l[i]+(1-wv[i])*m[i]).mean())
    P=np.array(P);E=np.array(E);d=P-E
    return np.cov(P,d)[0,1]/d.var()
print("Eq.5 value",round(lam5,3))
print("MC optimum, EIF with w==0 (EIF=mean m):",round(mc(np.zeros(N)),3))
print("MC optimum, EIF with noisy w as in Eq.3:",round(mc(wn),3))
print("== C7 Table 3 reductions recomputed")
T=[('Cauc40',.0393,.0187,.0187,.0187),('Cauc160',.0184,.0093,.0092,.0092),('Cauc640',.0083,.0042,.0040,.0040),('AA40',.0701,.1384,.1406,.0659),('AA160',.0266,.1268,.1293,.0264),('AA320',.0047,.1260,.1284,.0047)]
for r in T: print(r[0],[round(100*(r[1]-a)/r[1],1) for a in r[2:]])
print("AA320 fraction of subgroup sampled f=",round(320/332,3),"; AA40 f=",round(40/332,3))
print("== C8 Table 4: LOO means and rank stats (10 subgroups, values from Table 1)")
g=['Cauc','AA','Hisp','Oth','M','F','<50','50-65','65-80','80+']
hard=[.931,.852,.943,.888,.927,.930,.935,.924,.924,.929]
soft=[.932,.852,.944,.889,.927,.930,.935,.924,.924,.929]
adapt=[.926,.946,1.015,.867,.942,.917,.972,.917,.898,.850]
prev=[.0879,.0181,.0737,.1296,.0810,.0851,.0251,.0633,.0874,.1711]
from math import comb
def rank(a):
    a=np.asarray(a,float); r=np.empty(len(a))
    for i,x in enumerate(a): r[i]=(a<x).sum()+((a==x).sum()-1)/2
    return r
def sp(a,b): return np.corrcoef(rank(a),rank(b))[0,1]
print("mean|adapt-hard|",round(np.mean(np.abs(np.array(adapt)-hard)),4),"(paper 0.0369/0.0370)")
print("Spearman adapt vs hard",round(sp(adapt,hard),3),"(paper 0.479)")
inv=sum(1 for i,j in itertools.combinations(range(10),2) if (adapt[i]-adapt[j])*(hard[i]-hard[j])<0)
print("pairwise inversions",inv,"of 45 (paper 13)")
print("Spearman hard vs prevalence",round(sp(hard,prev),3),"| adapt vs prevalence",round(sp(adapt,prev),3))
print("mean|soft-hard|",round(np.mean(np.abs(np.array(soft)-hard)),4),"max",max(abs(a-b) for a,b in zip(soft,hard)))
print("== C9 Table 2 arithmetic");print("34/43",round(34/43*100,1),"6/43",round(6/43*100,1),"bias ratio",round(.0690/.0084,2))
print("== C10 N* implied by RMSE ~ N^-1/2 from Table 3 Cauc640 (0.0083) to eps=0.008:",round(640*(.0083/.008)**2))
