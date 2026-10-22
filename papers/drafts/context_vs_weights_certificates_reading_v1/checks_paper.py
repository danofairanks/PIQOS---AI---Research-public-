# E1 checks on arXiv:2610.29419v1 using the paper's own definitions and printed numbers. No model downloads, no network.
import numpy as np, math
rng=np.random.default_rng(7)
def H(p): p=p[p>0]; return -(p*np.log2(p)).sum()
def KL(p,q): m=p>0; return (p[m]*np.log2(p[m]/q[m])).sum()
print("== C1 Theorem 2 (exact law), Corollary 3 and Proposition 6(iii) on random discrete joints")
worst=0; viol3i=0; viol6iii=0; trials=2000
for _ in range(trials):
    nD,nQ=rng.integers(2,6),rng.integers(2,5)
    pD=rng.dirichlet(np.ones(nD)); Pq_D=rng.dirichlet(np.ones(nQ),size=nD)          # true P*(Q|D)
    joint_DQ=pD[:,None]*Pq_D; PQ=joint_DQ.sum(0)
    p0=rng.dirichlet(np.ones(nQ))                                                    # base predictive
    # memory Z = f(D) (deterministic, many-to-one possible), channel predictor p_c(Q|Z) arbitrary
    nZ=rng.integers(1,nD+1); f=rng.integers(0,nZ,size=nD)
    pc=rng.dirichlet(np.ones(nQ),size=nZ)
    # expected gain E[log p_c(Q|Z)/p0(Q)]
    gain=sum(joint_DQ[d,q]*math.log2(pc[f[d],q]/p0[q]) for d in range(nD) for q in range(nQ))
    # terms
    pZ=np.zeros(nZ); joint_ZQ=np.zeros((nZ,nQ))
    for d in range(nD): pZ[f[d]]+=pD[d]; joint_ZQ[f[d]]+=joint_DQ[d]
    PQ_Z=np.array([joint_ZQ[z]/pZ[z] if pZ[z]>0 else np.ones(nQ)/nQ for z in range(nZ)])
    I_QZ=sum(pZ[z]*KL(PQ_Z[z],PQ) for z in range(nZ) if pZ[z]>0)
    KL0=KL(PQ,p0); dec=sum(pZ[z]*KL(PQ_Z[z],pc[z]) for z in range(nZ) if pZ[z]>0)
    worst=max(worst,abs(gain-(I_QZ+KL0-dec)))
    # Corollary 3(i): E[gain] <= G* = I(Q;D)+KL0
    I_QD=sum(pD[d]*KL(Pq_D[d],PQ) for d in range(nD)); G=I_QD+KL0
    if gain>G+1e-9: viol3i+=1
    # Prop 6(iii): channel A keeps D (Z_A=D, pc_A arbitrary, stor_A=0); B any memory: E[Gamma_B]-E[Gamma_A] <= dec_A
    pcA=rng.dirichlet(np.ones(nQ),size=nD)
    gainA=sum(joint_DQ[d,q]*math.log2(pcA[d,q]/p0[q]) for d in range(nD) for q in range(nQ)); decA=sum(pD[d]*KL(Pq_D[d],pcA[d]) for d in range(nD))
    if gain-gainA>decA+1e-9: viol6iii+=1
print(f"max |E[gain] - (I + KL0 - dec)| over {trials} random joints: {worst:.2e}")
print(f"Cor 3(i) violations: {viol3i}; Prop 6(iii) violations: {viol6iii}  (both are consequences of the identity, expected 0)")
print("== C1b the identity needs the TRUE posterior P*; with an estimated P (model's own), it is an accounting identity w.r.t. whatever distribution is called 'true'")
print("   (not a numerical test: the identity holds for any joint, so it cannot fail; the paper's tests are of Assumption 1, the estimators and the certificates' preconditions)")
print("== C4 printed counts")
print("GPT-2 Table 13 rows: 7 rows x 8000 + 5948 =",7*8000+5948,"calls (abstract 61,948); +4 wrong +2048 undecided =",7*8000+5948+4+2048,"(64,000 = 32 x 2000 =",32*2000,")")
print("decided share:",round(61952/64000*100,2),"% ; wrong among decided:",round(4/61952*100,4),"%")
print("Table 14 sums: window",8+2+2,"/",30+5+3,"capacity",17+3+4,"/",48+6+4,"; issued",12+24,"of",38+58,"; checks",50+14+22)
print("Table 10 means vs text: phoneme TabPFN",round((0.587+0.605+0.640)/3,3),"(text 0.61) XGB",round((0.761+0.691+0.965)/3,3),"(0.81); spambase TabPFN",round((0.379+0.299+0.318)/3,3),"(0.33) XGB",round((0.716+0.501+0.454)/3,3),"(0.56); airfoil surrogate",round((2.412+2.384+2.227)/3,3),"(2.34) in-context",round((3.654+3.623+3.670)/3,3),"(3.65)")
def wil(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return (c+h)/d*100
print("Table 12 Wilson upper bounds (10,000 streams):",{k:round(wil(round(v*10000),10000),2) for k,v in {'sym 3.25%':.0325,'skew 2.87%':.0287,'chg var 3.31%':.0331,'tie 0%':.0,'adv .005 1.21%':.0121}.items()},"(printed 3.62, 3.22, 3.68, 0.04, 1.44)")
print("== C4 AUROC saturation: clipped gap bound 0.95-1e-12 ->",round(-math.log2(1e-12)*0 + (0.95*math.log2(0.95/1e-12)+0.05*math.log2(0.05/(1-1e-12))),2),"bits? (paper: 37.58); share of scores within 0.1 bit of it: Qwen 47.0%, GPT-4.1-mini 51.5%")
print("   d2(0.95 || 1e-12) =",round(0.95*math.log2(0.95/1e-12)+0.05*math.log2(0.05/(1-1e-12)),2))
