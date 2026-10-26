import numpy as np, sys
rng=np.random.default_rng(20261023)
sp=lambda t: np.logaddexp(0,t)
d1=lambda t: 1/(1+np.exp(-t))
def equil(W,A,b,x,tol=1e-15,it=200000):
    z=np.zeros(W.shape[0])
    for _ in range(it):
        zn=sp(W@z+A@x+b)
        if np.max(abs(zn-z))<tol: z=zn;break
        z=zn
    return z
def derivs(W,A,b,x,z):
    m,n=A.shape
    s=W@z+A@x+b; psi=d1(s); gam=psi*(1-psi)
    B=np.eye(m)-np.diag(psi)@W; S=np.linalg.inv(B)
    V=np.linalg.solve(np.eye(m)-W@np.diag(psi),A)
    J=S@np.diag(psi)@A
    return s,psi,gam,S,V,J
def randW(m,q,sparse=False):
    W=rng.random((m,m))**(4 if sparse else 1)
    W=W/W.sum(1,keepdims=True)*q
    return W
# Lemma 4.1 and Thm 4.2 / 4.6 (n=2), adversarial random search
worst={"L41":0,"T42":0,"T42q":0}
for q in (0.5,0.9,0.99):
  d=1-q
  for trial in range(400):
    m=int(rng.integers(1,9)); n=2
    W=randW(m,q,sparse=bool(trial%2))
    # random row norms of W: scale some rows lower
    W=W*rng.uniform(0.2,1,(m,1)); W[rng.integers(m)]*=q/max(W.sum(1).max(),1e-9)  # ensure some row near q
    W=W*(q/W.sum(1).max())
    A=rng.normal(size=(m,n))*rng.choice([0.1,1,5]); b=rng.normal(size=m)*rng.choice([0.5,3,10])
    w=rng.random(m)*rng.choice([0.1,1,5])
    x=rng.normal(size=n)
    # tune bias so psi near 1 where possible: shift b so s large
    b=b+rng.choice([0,5,10,20])
    z=equil(W,A,b,x)
    s,psi,gam,S,V,J=derivs(W,A,b,x,z)
    Sg=S@gam
    worst["L41"]=max(worst["L41"],Sg.max())
    beta=(S.T@w)*gam
    H=V.T@np.diag(beta)@V
    KA=max(np.linalg.norm(A[r]) for r in range(m))
    C2=w.sum()*KA**2*min(d**-2,1/(4*d**3))
    r=np.linalg.norm(H,2)/C2
    worst["T42"]=max(worst["T42"],r)
print("Lemma4.1 max S*gamma:",worst["L41"],"(claim <=1)")
print("Thm4.2 max ||H||/C2 over random draws:",worst["T42"],"(claim <=1)")
# targeted: sharp family
for eps in (0.2,0.05,0.01,0.002):
    q=1-eps; W=np.array([[q]]);A=np.array([[1.0]]);b=np.array([np.log(1-eps)-eps*np.log(eps)])
    x=np.array([0.0]); z=equil(W,A,b,x,tol=1e-16,it=2000000)
    s,psi,gam,S,V,J=derivs(W,A,b,x,z)
    H=(V.T@np.diag((S.T@np.array([1.0]))*gam)@V)[0,0]
    closed=(1-eps)/(eps**2*(2-eps)**3)
    # third derivative via finite differences of H(x)
    def Hx(xx):
        zz=equil(W,A,b,np.array([xx]),tol=1e-16,it=2000000); s,psi,gam,S,V,J=derivs(W,A,b,np.array([xx]),zz); return (V.T@np.diag((S.T@np.array([1.0]))*gam)@V)[0,0]
    h=eps**1.5*1e-1
    t3=(Hx(h)-Hx(-h))/(2*h)
    print(f"eps={eps}: z*={z[0]:.6f} vs -log eps={-np.log(eps):.6f} | u''={H:.6g} closed={closed:.6g} eps^2u''={eps**2*H:.5f} | u''' (fd)={t3:.6g} eps^3u'''={eps**3*t3:.5f} paper-closed eps^3u'''={(eps**3)*(1-eps)*(1-eps+eps**2)/(eps**3*(2-eps)**5):.5f}")
