# Independent check of Appendix A.10 (linear-Gaussian model) written from the paper's printed model and formulas, NOT the authors' scripts (those are unavailable).
# Reading used (state of the extraction: math glyphs partly garbled, reconstructed and cross-checked against printed numbers):
#   x ~ N(0, I_d), w ~ N(0, (sw2/d) I_d), y = w.x + eps, eps ~ N(0, s2); rho = sw2/s2; alpha = d/N; base predictive = prior predictive of y|x.
import numpy as np, math
rng=np.random.default_rng(11)
def mp_m(alpha,lam): return (-(lam+1-alpha)+math.sqrt((lam+1-alpha)**2+4*alpha*lam))/(2*alpha*lam)
print("== A: printed number check: adapter ceiling 1/2 log2((1+rho)/(1+(1-k/d)rho)) at rho=4, k=d/4 vs cache ceiling 1/2 log2(1+rho)")
rho=4; ad=0.5*math.log2((1+rho)/(1+(1-0.25)*rho)); ce=0.5*math.log2(1+rho); print(f" adapter {ad:.4f} bits, ceiling {ce:.4f} bits, ratio {ad/ce*100:.1f}% (paper: 14%)")
def sim(d,N,s2=1.0,rho=4.0,reps=4000,Q=64):
    sw2=rho*s2; g_bayes=[];err_la={}
    etas=np.linspace(0.0,2.0,81)/ (sw2/d*N+ s2*0+1)  # grid, rescaled below
    for _ in range(reps):
        w=rng.normal(0,math.sqrt(sw2/d),d); X=rng.normal(size=(N,d)); y=X@w+rng.normal(0,math.sqrt(s2),N)
        A=X.T@X/s2+np.eye(d)*d/sw2; Sig=np.linalg.inv(A); mu=Sig@(X.T@y)/s2
        xq=rng.normal(size=(Q,d)); yq=xq@w+rng.normal(0,math.sqrt(s2),Q)
        m=xq@mu; v=s2+np.einsum('ij,jk,ik->i',xq,Sig,xq)
        lb=-0.5*np.log2(2*math.pi*v)-((yq-m)**2)/(2*v)/math.log(2)
        v0=s2+sw2*(xq**2).sum(1)/d; l0=-0.5*np.log2(2*math.pi*v0)-(yq**2)/(2*v0)/math.log(2)
        g_bayes.append((lb-l0).mean())
    return np.mean(g_bayes)
def excess_la(d,N,s2=1.0,rho=4.0,reps=6000):
    # E||eta X^T y - w||^2 minimised over eta; Monte Carlo over (w,X,eps) with a shared eta grid
    sw2=rho*s2; so2=sw2/d; best=None
    etas=np.linspace(0.02,1.2,60)*so2/(so2*N+s2)*N  # grid around the scalar that scales as so2/(so2*N+s2)
    acc=np.zeros(len(etas))
    for _ in range(reps):
        w=rng.normal(0,math.sqrt(so2),d); X=rng.normal(size=(N,d)); y=X@w+rng.normal(0,math.sqrt(s2),N)
        z=X.T@y
        acc+=np.array([((e*z-w)**2).sum() for e in etas/N*1.0*N/N])
    acc/=reps; return acc.min()
def formula_la(d,N,s2=1.0,rho=4.0):
    sw2=rho*s2; so2=sw2/d
    return so2*d*(so2*(d+1)+s2)/(so2*(N+d+1)+s2)
print("== B: Eq.26 (one linear-attention layer, exact at finite N,d) vs Monte Carlo minimum over a scalar step")
for d,N in [(10,10),(10,40),(20,30),(20,100)]:
    # exact optimum over eta: minimise numerically with a fine grid built from the formula's own scale
    so2=4.0/d; eta0=so2/(so2*(N+d+1)+1.0)
    sw2=4.0; reps=6000; etas=eta0*np.linspace(0.5,1.5,41); acc=np.zeros(41)
    for _ in range(reps):
        w=rng.normal(0,math.sqrt(so2),d); X=rng.normal(size=(N,d)); y=X@w+rng.normal(0,1,N); z=X.T@y
        acc+=np.array([((e*z-w)**2).sum() for e in etas])
    acc/=reps
    print(f" d={d:3d} N={N:4d}: MC min excess risk {acc.min():.4f}  Eq.26 {formula_la(d,N):.4f}")
print("== C: Eq.24-25 ideal cache in (near) the proportional limit: simulated mean gain vs 1/2 log2((s2+sw2)/(s2+E_B)), E_B = s2*alpha*m_alpha(lambda), lambda = alpha/rho")
for d,N in [(100,200),(100,400),(100,800),(200,400)]:
    alpha=d/N; lam=alpha/4.0; EB=alpha*mp_m(alpha,lam); pred=0.5*math.log2((1+4)/(1+EB)); g=sim(d,N,reps=300)
    print(f" d={d} N={N} alpha={alpha:.2f}: simulated {g:.4f} bits, closed form {pred:.4f} bits (E_B={EB:.4f})")
print("== D: ordering at rho=4: E_B (limit) <= E_LA (exact finite) over n/d = 0.1..10")
ok=True
for r in (0.1,0.25,0.5,1,2,4,10):
    d=100; N=int(r*d); alpha=d/N; EB=alpha*mp_m(alpha,alpha/4.0); EL=formula_la(d,N); ok&=EB<=EL+1e-9; print(f" n/d={r:5.2f}: E_B {EB:.4f} <= E_LA {EL:.4f}: {EB<=EL+1e-9}")
print(" ordering holds on all points:",ok)
print("== E: Monte Carlo spread of the Eq.24-25 check (d=200, N=400; 5 independent runs of 300 repeats, 64 query points each)")
vals=[sim(200,400,reps=300) for _ in range(5)]
alpha=0.5; EB=alpha*mp_m(alpha,alpha/4.0); pred=0.5*math.log2(5/(1+EB))
print(" runs:",[round(v,4) for v in vals],"mean",round(float(np.mean(vals)),4),"sd of a run",round(float(np.std(vals,ddof=1)),4),"closed form",round(pred,4))
print(" mean of 5 runs minus closed form:",round(float(np.mean(vals))-pred,4),"bits (the paper reports a largest gap of 0.005 bits at d=200 over 300 repeats)")
