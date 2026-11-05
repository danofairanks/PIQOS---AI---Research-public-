"""T1 and T2: formal-level counter-models for MEM Eqs (6)-(9), (13)-(14) (arXiv 2609.20437 as read). numpy only, seeded.
Prereg: PREREG_DEFEAT_CONDITIONS.md (sha256 fffcde5f...). Equality here is algebraic; the run checks my implementation (fidelity), it is not a finding about nature."""
import numpy as np
rng=np.random.default_rng(20261105)
def softmax(x):
    x=x-x.max(); e=np.exp(x); return e/e.sum()
def t1(n=10000):
    worst={'dot':0,'cos':0,'rbf':0}; agree={'dot':0,'cos':0,'rbf':0}
    for _ in range(n):
        M=int(rng.integers(5,41)); D=int(rng.integers(8,33))
        h=rng.normal(size=D); b=rng.normal(size=D); mu=rng.normal(size=(M,D)); rho=rng.normal(size=(M,D)); v=rng.normal(size=M)
        a_s,b_b,x_v=rng.uniform(.1,2,3)
        # (i) dot
        u=a_s*(mu@h)+b_b*(rho@b)+x_v*v
        W=np.hstack([a_s*mu,b_b*rho]); z=np.concatenate([h,b]); u2=W@z+x_v*v
        worst['dot']=max(worst['dot'],np.abs(u-u2).max()); agree['dot']+=int(u.argmax()==u2.argmax())
        # (ii) cosine
        nh=h/np.linalg.norm(h); nb=b/np.linalg.norm(b); nmu=mu/np.linalg.norm(mu,axis=1,keepdims=True); nrho=rho/np.linalg.norm(rho,axis=1,keepdims=True)
        u=a_s*(nmu@nh)+b_b*(nrho@nb)+x_v*v
        W=np.hstack([a_s*nmu,b_b*nrho]); z=np.concatenate([nh,nb]); u2=W@z+x_v*v
        worst['cos']=max(worst['cos'],np.abs(u-u2).max()); agree['cos']+=int(u.argmax()==u2.argmax())
        # (iii) RBF: additive kernel machine k = a_s k1 + b_b k2 + bias (kernel form built separately)
        s=1.0+D/4
        k1=lambda x,Y: np.exp(-((Y-x)**2).sum(1)/(2*s*s)); u=a_s*k1(h,mu)+b_b*k1(b,rho)+x_v*v
        Z=np.hstack([mu,rho]); zz=np.concatenate([h,b])
        K=lambda zz,Z: a_s*np.exp(-((Z[:,:D]-zz[:D])**2).sum(1)/(2*s*s))+b_b*np.exp(-((Z[:,D:]-zz[D:])**2).sum(1)/(2*s*s))
        u2=K(zz,Z)+x_v*v
        worst['rbf']=max(worst['rbf'],np.abs(u-u2).max()); agree['rbf']+=int(u.argmax()==u2.argmax())
    return worst,{k:v/n for k,v in agree.items()}
def mem_pipeline(h,b,mu,rho,v,L,par):
    a_s,b_b,x_v,K,lamL,tau,lam=par
    u=a_s*(mu@h)+b_b*(rho@b)+x_v*v                         # Eq 6
    C=np.argsort(-u)[:K]                                    # Eq 8 TopK
    uc=np.maximum(u[C],0)
    q=np.array([sum(L[m,n]*uc[j] for j,n in enumerate(C) if n!=m) for m in C])  # Eq 9 lateral priming, excluding self
    ut=u[C]+lamL*q
    a=softmax(ut/tau)                                       # Eq 9 softmax over candidate set
    hhat=(a[:,None]*mu[C]).sum(0)                           # Eq 13
    return (1-lam)*h+lam*hhat                               # Eq 14
def attn_counter(h,b,mu,rho,v,L,par):
    a_s,b_b,x_v,K,lamL,tau,lam=par
    # standard sparse softmax attention: query [h;b;1], keys [a_s mu; b_b rho; x_v v], pairwise bias from relu scores, top-k mask, values = mu
    Q=np.concatenate([h,b,[1.0]]); Kmat=np.hstack([a_s*mu,b_b*rho,(x_v*v)[:,None]])
    s=Kmat@Q
    idx=np.argsort(-s)[:K]
    r=np.zeros_like(s); r[idx]=np.maximum(s[idx],0)
    Lm=L.copy(); np.fill_diagonal(Lm,0); mask=np.zeros(len(s),bool); mask[idx]=True
    bias=Lm@r                                               # sum_n L_mn relu(s_n) over candidates only (r zero elsewhere)
    logits=np.full(len(s),-np.inf); logits[idx]=(s[idx]+lamL*bias[idx])/tau
    w=np.exp(logits-logits[idx].max()); w/=w.sum()
    out=w@mu                                                # attention output over values
    return (1-lam)*h+lam*out                                # residual mix
def t2(n=3000):
    worst=0
    for _ in range(n):
        M=int(rng.integers(6,31)); D=int(rng.integers(8,25))
        h=rng.normal(size=D); b=rng.normal(size=D); mu=rng.normal(size=(M,D)); rho=rng.normal(size=(M,D)); v=rng.normal(size=M)
        L=rng.uniform(0,1,(M,M)); a_s,b_b,x_v=rng.uniform(.1,2,3); K=int(rng.integers(2,min(8,M)+1)); lamL=rng.uniform(0,1); tau=rng.uniform(.2,3); lam=rng.uniform(0,1)
        par=(a_s,b_b,x_v,K,lamL,tau,lam)
        worst=max(worst,np.abs(mem_pipeline(h,b,mu,rho,v,L,par)-attn_counter(h,b,mu,rho,v,L,par)).max())
    return worst
if __name__=="__main__":
    w,a=t1(); print("T1 max|u-u'| per sim:",w,"argmax agreement:",a)
    print("T1 D1 (defeated at scope iff all <1e-9 and agreement==1):", all(x<1e-9 for x in w.values()) and all(x==1.0 for x in a.values()))
    w2=t2(); print("T2 max|h_eff - h_eff'|:",w2); print("T2 D2 (defeated at scope iff <1e-12):", w2<1e-12)
