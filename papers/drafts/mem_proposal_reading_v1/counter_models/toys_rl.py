"""T3, T4, T5: tabular agents on small allostatic tasks, per PREREG_DEFEAT_CONDITIONS.md (sha256 fffcde5f...). stdlib + math only, seeded.
MEM terms as read from arXiv 2609.20437: Eq 3 A=tanh(w.d+c), Eq 4 C=sum alpha*d^2, Eq 17 eta=eta0(1+kappa|A|), Eq 26 eps=eps_min+(eps_max-eps_min)*I (I:=|A| here, simplification disclosed)."""
import random, math, sys, statistics as st

# ---------------- T3: disconnect/restore (one variable) ----------------
def t3_step(n,a,rng):
    if a==0: n2=n-1-(1 if rng.random()<0.1 else 0); task=1.0
    else: n2=n+2; task=0.0
    n2=max(0,min(10,n2)); return n2,task
def dcost(n): d=max(0,3-n); return d*d
def train_T3(kind,seed,eps=0.1,eta0=0.1,gamma=0.9,kappa=2.0,episodes=600,T=200):
    rng=random.Random(seed); Q=[[0.0,0.0] for _ in range(11)]; etas=[];As=[]
    for ep in range(episodes):
        n=10
        for t in range(T):
            s=n if kind!='c' else 0
            a=rng.randrange(2) if rng.random()<eps else (0 if Q[s][0]>=Q[s][1] else 1)
            n2,task=t3_step(n,a,rng)
            if kind=='a': r=task-0.5*dcost(n2)
            elif kind=='b': r=task+(dcost(n)-dcost(n2))
            else: r=task-0.5*dcost(n2)
            s2=n2 if kind!='c' else 0
            if kind=='b':
                d=max(0,3-n2); A=math.tanh(0.5*d); eta=eta0*(1+kappa*abs(A)); etas.append(eta); As.append(abs(A))
            else: eta=eta0; etas.append(eta); As.append(0.0)
            Q[s][a]+=eta*(r+gamma*max(Q[s2])-Q[s][a]); n=n2
    return Q,etas,As
def test_T3(kind,Q,seed,windows=4,W=60):
    rng=random.Random(seed); n=7; freqs=[]
    for w in range(windows):
        rc=0
        for t in range(W):
            reading = 10 if w==1 else n          # window 1 = disconnected (sensor reads 'full')
            s=reading if kind!='c' else 0
            a=0 if Q[s][0]>=Q[s][1] else 1
            rc+=a; n,_=t3_step(n,a,rng)
        freqs.append(rc/W)
    return freqs
def run_T3(nseeds=40):
    out={}
    for kind in 'abc':
        F=[];corr=[]
        for sd in range(nseeds):
            Q,etas,As=train_T3(kind,sd)
            F.append(test_T3(kind,Q,10_000+sd))
            if kind=='b' and st.pstdev(As)>0:
                mx,my=st.mean(etas),st.mean(As); num=sum((e-mx)*(a-my) for e,a in zip(etas,As)); den=math.sqrt(sum((e-mx)**2 for e in etas)*sum((a-my)**2 for a in As)); corr.append(num/den)
        m=[st.mean(f[i] for f in F) for i in range(4)]
        out[kind]=(m,corr)
        pre,dis,post1,post2=m
        passed=abs(dis-pre)>=0.20 and abs(post2-pre)<=0.05
        print(f"T3 agent ({kind}) recharge freq windows pre/disc/restore1/restore2 = {[round(x,3) for x in m]}  change_on_disconnect={dis-pre:+.3f}  recovery_gap={post2-pre:+.3f}  PASS_6.3={passed}  eta-|A| corr={'n/a' if not corr else round(st.mean(corr),3)}")
    return out

# ---------------- T4/T5: two variables, non-stationary food ----------------
ACTS=5
def env_step(e,tp,a,patch,rng):
    if rng.random()<0.5: e-=1
    if rng.random()<0.5: tp-=1
    if a==1: tp+=2
    elif a>=2:
        k=a-2
        if k==patch: e+=3
        else: e-=1
    e=max(0,min(8,e)); tp=max(0,min(8,tp)); return e,tp
def C(e,tp): return max(0,3-e)**2+max(0,3-tp)**2
def run_agent(cfg,seed,episodes=300,T=100):
    rng=random.Random(seed); Q={}
    def q(s): 
        if s not in Q: Q[s]=[0.0]*ACTS
        return Q[s]
    total=0.0; gamma=0.9
    for ep in range(episodes):
        patch=(ep//100)%3
        e,tp=6,6; cost_ep=0.0
        for t in range(T):
            c0=C(e,tp); d=max(0,3-e)+max(0,3-tp)
            if cfg['mode']=='mem': mod=abs(math.tanh(0.5*d))
            elif cfg['mode']=='sched': mod=min(1.0,c0/9.0)
            elif cfg['mode']=='fac': mod=abs(math.tanh(0.5*d))
            else: mod=0.0
            if cfg['mode']=='hrl': eta=cfg['eta0']; eps=cfg['eps']
            elif cfg['mode'] in('mem','sched'): eta=cfg['eta0']*(1+cfg['kappa']*mod); eps=cfg['emin']+(cfg['emax']-cfg['emin'])*mod
            else: eta=cfg['eta0']*(1+cfg.get('kappa',0)*mod); eps=cfg['eps'] if not cfg.get('emod',False) else cfg['emin']+(cfg['emax']-cfg['emin'])*mod
            s=(e,tp); qs=q(s)
            a=rng.randrange(ACTS) if rng.random()<eps else max(range(ACTS),key=lambda i:(qs[i],-i))
            e2,tp2=env_step(e,tp,a,patch,rng); c1=C(e2,tp2); r=c0-c1
            q2=q((e2,tp2)); qs[a]+=eta*(r+gamma*max(q2)-qs[a]); e,tp=e2,tp2; cost_ep+=c1
        total+=cost_ep/T
    return total
def mean_se(x): return st.mean(x),st.pstdev(x)/math.sqrt(len(x))*math.sqrt(len(x)/(len(x)-1))
def tune(mode,grid,seeds):
    best=None
    for cfg in grid:
        m=st.mean(run_agent(cfg,s) for s in seeds)
        if best is None or m<best[0]: best=(m,cfg)
    return best
def run_T4():
    tune_seeds=list(range(1000,1010)); eval_seeds=list(range(2000,2030))
    g_hrl=[dict(mode='hrl',eta0=e0,eps=ep) for e0 in (0.05,0.1,0.2,0.4,0.8) for ep in (0.02,0.05,0.1)]
    g_mem=[dict(mode='mem',eta0=0.1,kappa=k,emin=0.02,emax=em) for k in (0.5,1,2,4,8) for em in (0.15,0.3,0.5)]
    g_sch=[dict(mode='sched',eta0=0.1,kappa=k,emin=0.02,emax=em) for k in (0.5,1,2,4,8) for em in (0.15,0.3,0.5)]
    chosen={}
    for name,g in (('HRL',g_hrl),('MEM-A',g_mem),('HRL-sched',g_sch)):
        m,cfg=tune(name,g,tune_seeds); chosen[name]=cfg; print("T4 tuned",name,cfg,"tuning-mean",round(m,4))
    res={}
    for name,cfg in chosen.items():
        res[name]=[run_agent(cfg,s) for s in eval_seeds]
        m,se=mean_se(res[name]); print(f"T4 {name}: mean AUC cost {m:.4f} se {se:.4f}")
    mA,sA=mean_se(res['MEM-A']); mH,sH=mean_se(res['HRL']); mS,sS=mean_se(res['HRL-sched'])
    diff_ah=mH-mA; se_ah=math.sqrt(sA**2+sH**2); diff_as=mS-mA; se_as=math.sqrt(sA**2+sS**2)
    print(f"T4 P4a MEM-A better than HRL by {diff_ah:.4f} (se {se_ah:.4f}, {diff_ah/se_ah:.2f} SE) -> {'holds' if diff_ah>2*se_ah else 'does not hold'}")
    print(f"T4 P4b HRL-sched minus MEM-A = {diff_as:+.4f} (se {se_as:.4f}, {abs(diff_as)/se_as:.2f} SE) -> gap closed (<=1 SE): {abs(diff_as)<=se_as}; HRL-sched worse by >2SE: {diff_as>2*se_as}")
    return chosen,res
def boot_int(cells,fn,B=2000,seed=7):
    r=random.Random(seed); vals=[]
    for _ in range(B):
        m=[st.mean(fn(c[i]) for i in [r.randrange(len(c)) for _ in c]) for c in cells]  # cells: c00,c10,c01,c11
        vals.append(m[3]-m[1]-m[2]+m[0])
    vals.sort(); return vals[int(.025*B)],vals[int(.975*B)]
def run_T5():
    seeds=list(range(3000,3030))
    def cell(k,em):
        cfg=dict(mode='fac',eta0=0.1,kappa=k,eps=0.1,emod=em,emin=0.02,emax=0.3)
        return [run_agent(cfg,s) for s in seeds]
    c00=cell(0,False);c10=cell(2.0,False);c01=cell(0,True);c11=cell(2.0,True)
    cells=[c00,c10,c01,c11]
    means=[st.mean(c) for c in cells]; print("T5 cell means (00,10,01,11):",[round(m,4) for m in means])
    raw=means[3]-means[1]-means[2]+means[0]; lo,hi=boot_int(cells,lambda x:x)
    lm=[st.mean(math.log(x) for x in c) for c in cells]; lraw=lm[3]-lm[1]-lm[2]+lm[0]; llo,lhi=boot_int(cells,lambda x:math.log(x))
    print(f"T5 interaction raw scale {raw:+.4f} CI [{lo:+.4f},{hi:+.4f}] excludes0={not(lo<=0<=hi)}")
    print(f"T5 interaction log scale {lraw:+.4f} CI [{llo:+.4f},{lhi:+.4f}] excludes0={not(llo<=0<=lhi)}")
    return raw,(lo,hi),lraw,(llo,lhi)
if __name__=="__main__":
    which=sys.argv[1] if len(sys.argv)>1 else 'all'
    if which in('t3','all'): run_T3()
    if which in('t4','all'): run_T4()
    if which in('t5','all'): run_T5()
