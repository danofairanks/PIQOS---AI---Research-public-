import numpy as np
exec(open("check_bounds_and_sharpness.py").read().split("# Lemma 4.1")[0])
rng=np.random.default_rng(7)
def exact(W,A,b,x):
    z=equil(W,A,b,x); s,psi,gam,S,V,J=derivs(W,A,b,x,z)
    m=W.shape[0]; B=np.eye(m)-np.diag(psi)@W; K={}
    v=[A[:,i]+W@J[:,i] for i in range(2)]
    for i in range(2):
        for j in range(2): K[i,j]=S@(gam*v[i]*v[j])
    return z,J,K
viol=0;maxr={"z":0,"J":0,"K":0,"H":0,"det":0};N=0
for trial in range(3000):
    q=rng.choice([0.3,0.7,0.9,0.97]); d=1-q; m=int(rng.integers(2,9)); n=2
    W=rng.random((m,m)); W=W/W.sum(1,keepdims=True)*q*rng.uniform(0.5,1,(m,1)); W*=q/W.sum(1).max()
    A=rng.normal(size=(m,n))*0.5; b=rng.normal(size=m)*0.5; w=rng.uniform(0.1,1,m); x=rng.uniform(-1,1,2)
    z,J,K=exact(W,A,b,x)
    sc=10**rng.uniform(-8,-1)
    zh=z+rng.normal(size=m)*sc; Jh=J+rng.normal(size=J.shape)*sc*rng.choice([0.1,1,10])
    Kh={}; 
    for i in range(2):
        for j in range(i,2):
            Kh[i,j]=K[i,j]+rng.normal(size=m)*sc*rng.choice([0.1,1,10]); Kh[j,i]=Kh[i,j]
    sh=W@zh+A@x+b; psih=d1(sh); gamh=psih*(1-psih); Bh=np.eye(m)-np.diag(psih)@W
    rho=abs(zh-sp(sh)).max()
    vh=[A[:,i]+W@Jh[:,i] for i in range(2)]; U=[abs(v).max() for v in vh]
    rho_i=[abs(Bh@Jh[:,i]-psih*A[:,i]).max() for i in range(2)]
    rho_ij={(i,j):abs(Bh@Kh[i,j]-gamh*vh[i]*vh[j]).max() for i in range(2) for j in range(2)}
    Ez=rho/d; al=q*Ez/4
    Ei=[(rho_i[i]+al*U[i])/d for i in range(2)]; De=[q*e for e in Ei]
    Eij={}
    for i in range(2):
        for j in range(2):
            Q=al*U[i]*U[j]+0.25*(De[i]*U[j]+U[i]*De[j]+De[i]*De[j])
            Eij[i,j]=(rho_ij[i,j]+Q+al*q*abs(Kh[i,j]).max())/d
    ok=True
    r=abs(z-zh).max()/Ez; maxr["z"]=max(maxr["z"],r)
    for i in range(2): maxr["J"]=max(maxr["J"],abs(J[:,i]-Jh[:,i]).max()/Ei[i])
    for i in range(2):
        for j in range(2): maxr["K"]=max(maxr["K"],abs(K[i,j]-Kh[i,j]).max()/Eij[i,j])
    H=np.array([[w@K[i,j] for j in range(2)] for i in range(2)]); Hh=np.array([[w@Kh[i,j] for j in range(2)] for i in range(2)])
    EH=w.sum()*np.sqrt(Eij[0,0]**2+2*Eij[0,1]**2+Eij[1,1]**2)
    maxr["H"]=max(maxr["H"],np.linalg.norm(H-Hh,2)/EH)
    Edet=2*np.linalg.norm(Hh,2)*EH+EH**2
    maxr["det"]=max(maxr["det"],abs(np.linalg.det(H)-np.linalg.det(Hh))/Edet)
print("max error/bound ratios over 3000 perturbed cases (claim <=1):",maxr)
