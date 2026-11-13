# Checks for the TRUST reading (arXiv 2611.10787v1). Three parts, run in order: (1) Table 1 arithmetic; (2) Appendix H tables and the leakage arithmetic; (3) the constants of Appendices D and E at the experiments' configuration.
# Table values are typed from the PDF text layer (E2); every number below is arithmetic on them (E1). Run: python3 -I checks.py
import math
print('#### PART 1: Table 1')
# order within each setting: Greedy, PACE, SGM-B, SGM-H, TRUST ; tuples (mean, se)
S={
('DeepSeek','HotpotQA'):dict(gain=[(7.87,.55),(10.15,.75),(0,0),(0,0),(11.58,1.30)],fer=[(64.67,3.28),(0,0),(0,0),(0,0),(10.00,10.00)],ter=[(40.03,5.06),(12.63,3.65),(0,0),(0,0),(18.11,8.39)],mdd=[(4.96,.93),(0,0),(0,0),(0,0),(.02,.02)]),
('DeepSeek','DROP'):dict(gain=[(36.24,2.19),(29.70,.59),(0,0),(0,0),(31.47,1.42)],fer=[(35.28,1.68),(0,0),(0,0),(0,0),(0,0)],ter=[(60.12,7.77),(6.68,1.67),(0,0),(0,0),(11.93,1.29)],mdd=[(5.38,1.58),(0,0),(0,0),(0,0),(0,0)]),
('DeepSeek','APPS'):dict(gain=[(33.89,2.71),(28.68,2.66),(0,0),(0,0),(34.55,1.04)],fer=[(41.08,4.31),(0,0),(0,0),(0,0),(0,0)],ter=[(50.83,2.89),(5.19,1.00),(0,0),(0,0),(11.64,3.53)],mdd=[(8.48,2.23),(0,0),(0,0),(0,0),(0,0)]),
('Qwen','HotpotQA'):dict(gain=[(20.66,2.45),(26.42,1.60),(0,0),(5.77,5.77),(27.72,.81)],fer=[(44.67,5.23),(6.67,6.67),(0,0),(0,0),(0,0)],ter=[(58.40,9.39),(16.31,2.94),(0,0),(1.25,1.25),(20.82,3.69)],mdd=[(4.01,.49),(.06,.06),(0,0),(0,0),(0,0)]),
('Qwen','DROP'):dict(gain=[(15.15,2.22),(13.22,3.77),(0,0),(0,0),(17.22,1.49)],fer=[(37.38,6.04),(0,0),(0,0),(0,0),(0,0)],ter=[(56.33,5.65),(5.23,1.78),(0,0),(0,0),(10.76,2.82)],mdd=[(3.37,1.03),(0,0),(0,0),(0,0),(0,0)]),
('Qwen','APPS'):dict(gain=[(28.03,.32),(26.24,.46),(0,0),(10.84,6.65),(26.53,.11)],fer=[(50.44,4.85),(0,0),(0,0),(0,0),(6.67,6.67)],ter=[(38.02,4.36),(4.44,.48),(0,0),(2.62,1.70),(12.52,3.42)],mdd=[(3.59,.68),(0,0),(0,0),(0,0),(.27,.27)]),
}
G=['Greedy','PACE','SGM-B','SGM-H','TRUST']
def mean(k,i): return sum(S[s][k][i][0] for s in S)/6
print('== headline recomputation (paper quotes: gain 24.84; FER0 45.59 -> 2.78; MDD 4.963 -> 0.047)')
for i,g in enumerate(G): print(f'{g:7s} mean gain {mean("gain",i):6.3f} | FER0 {mean("fer",i):6.3f} | TER {mean("ter",i):6.3f} | MDD {mean("mdd",i):6.3f}')
def z(a,b):
    d=a[0]-b[0]; se=math.sqrt(a[1]**2+b[1]**2); return d,se,(d/se if se else float('nan'))
print('\n== final-gain differences, TRUST minus comparator, per setting: diff, combined SE, z (SE over 5 seeds; Welch-style, E1 arithmetic only)')
for s in S:
    for j,name in ((0,'Greedy'),(1,'PACE')):
        d,se,zz=z(S[s]['gain'][4],S[s]['gain'][j]); print(f'{s[0]:8s}{s[1]:9s} vs {name:6s}: {d:+6.2f}  SE {se:5.2f}  z {zz:+5.2f}')
print('\nsettings where |z|<2 (TRUST vs PACE):',sum(1 for s in S if abs(z(S[s]["gain"][4],S[s]["gain"][1])[2])<2),'of 6; TRUST vs Greedy:',sum(1 for s in S if abs(z(S[s]["gain"][4],S[s]["gain"][0])[2])<2),'of 6')
print('TRUST gain > Greedy gain in',sum(1 for s in S if S[s]['gain'][4][0]>S[s]['gain'][0][0]),'of 6; > PACE in',sum(1 for s in S if S[s]['gain'][4][0]>S[s]['gain'][1][0]),'of 6')
print('TER: TRUST / Greedy ratio per setting:',[round(S[s]['ter'][4][0]/S[s]['ter'][0][0],2) for s in S])
print('Greedy FER0 > 30% in',sum(1 for s in S if S[s]['fer'][0][0]>30),'of 6; TRUST FER0 <= 30% in',sum(1 for s in S if S[s]['fer'][4][0]<=30),'of 6')
print('PACE vs TRUST FER0: TRUST lower in',sum(1 for s in S if S[s]['fer'][4][0]<S[s]['fer'][1][0]),'equal in',sum(1 for s in S if S[s]['fer'][4][0]==S[s]['fer'][1][0]),'higher in',sum(1 for s in S if S[s]['fer'][4][0]>S[s]['fer'][1][0]),'(paper: 1 / 3 / 2)')
print('\n== ablations (HotpotQA / DeepSeek only; final scores as quoted: TRUST 44.91+-1.36, without LLM 43.78+-1.18)')
d,se,zz=z((44.91,1.36),(43.78,1.18)); print(f'LLM allocator vs none: diff {d:.2f}, combined SE {se:.2f}, z {zz:.2f}')
print('beta ablation quoted: 11.58 at beta=0.01 vs 10.97 without correction; difference',round(11.58-10.97,2),'against the setting SE of 1.30 for TRUST in Table 1')
print('\n== assumption checks against the main configuration (q=0.30, eps=0.10, beta=0.01, betting fractions 0.10, 0.25, 0.50, 0.75; N=200, n<=40)')
eps=0.10; ub=2*eps/(1+eps)
print(f'Assumption 2(c) requires every betting fraction below 2*eps/(1+eps) = {ub:.4f}; fractions above it:',[e for e in (0.10,0.25,0.50,0.75) if e>=ub])
print('Assumption 2(b) requires n/N -> 0; configuration has n/N =',40/200)
print('\n#### PART 2: Appendix H and leakage arithmetic')
q ={0.1:(6.82,4.10),0.3:(11.58,18.11),0.5:(11.33,22.54)}         # gain, TER (FER0 for q: 0, 10.00, 18.00)
qf={0.1:0.0,0.3:10.0,0.5:18.0}
eps={0.0:(0.00,0.0,0.00),0.05:(4.87,0.0,2.23),0.10:(11.58,10.0,18.11),0.15:(11.59,57.68,65.88)}   # gain, FER0, TER
beta={0.0:(10.97,23.33,19.79),0.01:(11.58,10.0,18.11),0.03:(7.13,0.0,12.73),0.05:(2.80,0.0,10.0)}
print('q grid  : gain-max at',max(q,key=lambda k:q[k][0]),'(gain',q[max(q,key=lambda k:q[k][0])][0],')')
print('eps grid: gain-max at',max(eps,key=lambda k:eps[k][0]),'; best gain with FER0<=30:',max((k for k in eps if eps[k][1]<=30),key=lambda k:eps[k][0]))
print('beta grid: gain-max at',max(beta,key=lambda k:beta[k][0]))
print('defaults (q,eps,beta) = (0.30, 0.10, 0.01) are the gain-maximising value of each grid subject to FER0 <= 30%: ',
      max((k for k in q if True),key=lambda k:q[k][0])==0.3, max((k for k in eps if eps[k][1]<=30),key=lambda k:eps[k][0])==0.10, max(beta,key=lambda k:beta[k][0])==0.01)
print('eps jump: FER0 at eps 0.10 =',eps[0.10][1],'at 0.15 =',eps[0.15][1])
print('eps = 0.10 on the [0,1] score scale = a tolerated per-update loss of',0.10*100,'pp; paper main gains per setting range 7.87 to 36.24 pp over 30 rounds')
N=200; n=40; eps0=0.10; p_eps=(1-eps0)/2
print('\nleakage arithmetic (illustrative, E1 under stated simplifications): memory operator ADD_LOCAL adds 1 to 3 closed validation cases per candidate')
for k in (1,2,3,10):
    hit=k/N; excess=hit*(1-p_eps)
    print(f'  k={k:2d} stored validation cases: chance one given validation draw is a stored case = {hit:.4f}; mean excess of Y over the null boundary p_eps={p_eps:.2f} if each hit flips D from 0 to +1 and null mean were p_eps: {excess:.4f}   (beta used = 0.01)')
print('\n#### PART 3: Appendix D/E constants')
eps=0.10; p=(1-eps)/2            # p_eps = 0.45
q=0.30; T=30; N=200; n=40
def phi0(eta): return 0.5*math.log(1-eta)+0.5*math.log(1-eta+eta/p)   # phi(0, eta) from App. D.1 step 3
def h(eta): return math.log((1-eta+eta/p)/(1-eta))                    # width of the log increments, eq. (22), with eta+ = eta
print('p_eps =',p,'; admissible betting fraction (Assumption 2(c)) < 2e/(1+e) =',round(2*eps/(1+eps),4))
for eta in (0.10,0.25,0.50,0.75):
    print(f'eta {eta:.2f}: phi(0,eta) = {phi0(eta):+.5f}   (worst-case drift per draw against an arbitrarily small improvement)')
eta=0.10; g0=phi0(eta); hh=h(eta); kappa=g0**2/(8*hh**2)
print(f'\nDesignated component eta = {eta}: g0 = {g0:.5f}, h = {hh:.5f}, kappa = g0^2/(8 h^2) = {kappa:.3e}')
print(f'miss bound exp(-kappa n) at n = {n}: {math.exp(-kappa*n):.4f}  (i.e. Theorem 3/4 factor 1 - e^(-kappa n) = {1-math.exp(-kappa*n):.4f})')
for target in (0.5,0.05): print(f'n needed for exp(-kappa n) <= {target}: {math.log(1/target)/kappa:,.0f}')
Lam_min=math.log(1/q)   # alpha* <= rho_min*q*(1-rho_max)^(T-1) < q  =>  Lambda = log(1/alpha*) > log(1/q)
print(f'\nLambda = log(1/alpha*) > log(1/q) = {Lam_min:.3f}; the proof needs n >= 4*Lambda/g0 >= {4*Lam_min/g0:,.0f} per round (n <= N = {N}; n used <= {n})')
print('cumulative exposure bound zeta_bar = min(1, (T-1)n/(N-n+1)) =',min(1,(T-1)*n/(N-n+1)),'(1 = every sample may have been used before)')
print('rounds until (t-1)n >= N (pool fully exposed in the worst case):',math.ceil(N/n)+1)
