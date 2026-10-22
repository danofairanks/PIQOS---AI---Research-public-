# Counter-model toys for the Chlon-Huang specimen (see toys_preregistration_2026-10-22.md). numpy only; race toys call the repo's bitsy.core.race unchanged (commit cf81a50).
import sys, math, time, numpy as np
import os; sys.path.insert(0, os.environ.get('BITSY_PATH', './bitsy'))   # a checkout of the repository at commit cf81a50
from bitsy.core import race
t0=time.time()
print("== CM1 certificates with an estimated answer law (V=16, C=0, 64 episodes, prompt code length sd 0.3 bits, z=1.96)")
V=16; EP=64
def cm1(n_est, delta, trials, rng):
    issued=0
    for _ in range(trials):
        P=rng.dirichlet(np.ones(V)); H=-(P*np.log2(P)).sum()
        Q=rng.choice(V,size=EP,p=P)
        if n_est is None: q=P
        else:
            cnt=np.bincount(rng.choice(V,size=n_est,p=P),minlength=V); q=(cnt+1)/(n_est+V)
        prior=-np.log2(q[Q])                                   # prior code length per episode under the (estimated) law
        prompt=rng.normal(H+delta,0.3,EP)                       # true mean margin = H - (H+delta) = -delta
        m=prior-prompt; lo=m.mean()-1.96*m.std(ddof=1)/math.sqrt(EP)
        issued+= lo>0
    return issued/trials
rng=np.random.default_rng(101)
res={}
for label,n in (('exact',None),('n=50',50),('n=500',500),('n=5000',5000)):
    for d in (0.05,0.10):
        res[(label,d)]=cm1(n,d,3000,rng); print(f" law {label:6s} delta={d:.2f}: false-issue rate {res[(label,d)]*100:5.1f}%")
print(f" CM1a exact<=2.5% at 0.05: {res[('exact',0.05)]<=0.025} | CM1b n=50 >=20% at 0.05: {res[('n=50',0.05)]>=0.20} | CM1c n=5000 <=5% at 0.05: {res[('n=5000',0.05)]<=0.05} | CM1d n=50 >=10% at 0.10: {res[('n=50',0.10)]>=0.10}")
print("== CM2 betting test on an ordered stream (T=2000, c=4, overall mean 0): first 300 queries mean +0.5, then -0.0882")
c=4.0; T=2000; R=2000
def stream(rng,mean_a,n_a,mean_b):
    m=np.concatenate([np.full(n_a,mean_a),np.full(T-n_a,mean_b)])
    return np.clip(m+rng.normal(0,1,(R,T)),-c,c)
def calls(x):
    call,stop,_,_=race(x,-x,c,c,0.05); return call
rng=np.random.default_rng(202)
x=stream(rng,0.5,300,-0.5*300/1700); cl=calls(x); fc=np.mean(cl!='')
perm=np.array([rng.permutation(T) for _ in range(R)]); xs=np.take_along_axis(x,perm,axis=1); fs=np.mean(calls(xs)!='')
print(f" ordered stream false-call rate {fc*100:.1f}% (A {np.mean(cl=='A')*100:.1f}%, B {np.mean(cl=='B')*100:.1f}%); same values randomly reordered {fs*100:.2f}%")
x2=stream(rng,0.1,T,0.1); c2=calls(x2); print(f" CM2c stream mean +0.1 (deployment -0.1): A called in {np.mean(c2=='A')*100:.1f}% of streams, B in {np.mean(c2=='B')*100:.1f}%, none {np.mean(c2=='')*100:.1f}%")
print(f" CM2a >=15%: {fc>=0.15} | CM2b <=5%: {fs<=0.05} | CM2c >=95%: {np.mean(c2=='A')>=0.95}")
print("== CM3 leakage of held-out answers into channel A's context (clean Delta=-0.1 favours B; leaked Delta=+1.85; noise sd 0.5; 2000 streams x 2000 queries)")
rng=np.random.default_rng(303)
flip=None; rows={}
for f in (0.0,0.02,0.03,0.04,0.05,0.06,0.08,0.10):
    leak=rng.random((R,T))<f; x=np.where(leak,1.85,-0.1)+rng.normal(0,0.5,(R,T)); x=np.clip(x,-c,c); cl=calls(x)
    rows[f]=(np.mean(cl=='A'),np.mean(cl=='B'),np.mean(cl==''))
    print(f" f={f*100:4.1f}%: A called {rows[f][0]*100:5.1f}%  B called {rows[f][1]*100:5.1f}%  none {rows[f][2]*100:5.1f}%")
flipf=[f for f in rows if rows[f][0]>rows[f][1]]
print(f" CM3a first f where A is called more than B: {min(flipf)*100 if flipf else None}% (arithmetic crossing of the mean at f=0.1/1.95={0.1/1.95*100:.2f}%)")
print(f" CM3b f=10% A>=95%: {rows[0.10][0]>=0.95} | f=0: B>=95% {rows[0.0][1]>=0.95}, A<=2.5% {rows[0.0][0]<=0.025}")
print("elapsed %.0fs"%(time.time()-t0))
