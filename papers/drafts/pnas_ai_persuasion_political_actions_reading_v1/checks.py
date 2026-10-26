# E1 checks using only numbers printed in the main text of "AI can persuade people to take political actions" (PNAS 2026). SI not available.
import math
from math import sqrt,atanh,tanh,erf
def pt(t,df):
    # two-sided p for t via numeric integration of the t density (no scipy)
    import math
    f=lambda x:(math.gamma((df+1)/2)/(math.sqrt(df*math.pi)*math.gamma(df/2)))*(1+x*x/df)**(-(df+1)/2)
    n=200000;a=0;b=abs(t);h=(b-a)/n
    s=f(a)+f(b)+sum((4 if i%2 else 2)*f(a+i*h) for i in range(1,n))
    cdf=0.5+s*h/3
    return 2*(1-cdf)
def pr(r,n): t=r*sqrt((n-2)/(1-r*r)); return pt(t,n-2)
print("== C1 p-values for the printed condition-level correlations")
for r,n,p in [(.05,15,.85),(.18,8,.68),(.87,15,'<.01'),(-.15,15,.59),(.85,8,'<.01'),(-.16,8,.70),(.44,15,.10),(.63,8,.10),(.93,15,'<.01'),(.89,8,'<.01')]:
    print(f"r={r:5.2f} n={n:2d} p_recomputed={pr(r,n):.3f} printed {p}")
print("== C2 95% CIs for r (Fisher z) and minimal detectable |r| at 80% power, alpha .05")
def ci(r,n):
    z=atanh(r);se=1/sqrt(n-3);return tanh(z-1.96*se),tanh(z+1.96*se)
for r,n in [(.05,15),(.18,8),(-.15,15),(-.16,8),(.44,15),(.63,8)]:
    lo,hi=ci(r,n); print(f"r={r:5.2f} n={n:2d} CI [{lo:5.2f},{hi:5.2f}]")
for n in (15,8):
    zc=(1.96+0.8416)/sqrt(n-3); print(f"n={n}: minimal detectable r at 80% power = {tanh(zc):.2f}")
print("== C3 sample arithmetic")
print("S1:",8412-339-73,round(339/8412*100,2),"% attrition; S2:",10317-301-66,round(301/10317*100,2),"%; total responses",8000+9950,"; overlap implied (17950-14779) =",17950-14779)
print("== C4 observed vs adjusted effects")
print("S1 signing observed",round(37.8-25.2,1),"vs adjusted 12.8; S2 signing observed",round(40.4-21.1,1),"vs adjusted 19.7; S2 charity observed",round(39.2-33.4,1),"vs adjusted 6.1")
print("== C5 spread comparison in a common unit (assumption: SD of a binary outcome at p~0.36, treatment ~80% of sample)")
p=0.2*0.211+0.8*0.40; sd=sqrt(p*(1-p))
beh_range=(0.237-0.162); print("signing ATE range 7.5pp = ",round(beh_range/sd,3),"SD (binary SD",round(sd,3),")")
att_range=0.25-0.02; print("attitude ATE range printed 0.02..0.25 SD = ",att_range,"SD; ratio of ranges attitude/behavior =",round(att_range/(beh_range/sd),2))
print("ratio of extremes: attitude 0.25/0.02 =",round(0.25/0.02,1)," behavior 23.7/16.2 =",round(23.7/16.2,2))
print("== C6 sampling noise of condition-level ATEs (binomial, rough)")
import math
def se(p1,n1,p0,n0): return sqrt(p1*(1-p1)/n1+p0*(1-p0)/n0)
# S1: 15 conditions, ~20% control of 8000 = 1600 control; treated 6400 over 15 conditions? 3 conv types x5 models, one control per model unknown -> use all control
s1=se(.378,6400/15*1,.252,1600); s2=se(.404,1000,.211,2000)
print(f"S1 per-condition SE of signing ATE ~{s1*100:.1f}pp (assumes 6400/15 treated per condition vs pooled control); S2 per-strategy SE ~{s2*100:.1f}pp")
sd_est=beh_range/ (math.sqrt(12)/ (8-1) * 1 + 1e-9) if False else None
# S2 reliability of strategy ATEs: observed range 7.5pp over 8 strategies; assume SD of estimates ~ range/2.85 for n=8
sdobs=beh_range*100/2.85; rel=max(0,1-(s2*100)**2/sdobs**2)
print(f"S2 observed SD of 8 signing ATEs ~{sdobs:.1f}pp; implied reliability ~{rel:.2f}; expected observed r = r_true*sqrt(rel_x*rel_y) with rel_y~0.8 -> factor ~{sqrt(rel*0.8):.2f}")
print("== C7 info-prompt contrast in S2: 7 other strategies' mean must be 20.0 (printed); known three 23.7,21.2,20.6 -> remaining four avg =",round((7*20.0-23.7-21.2-20.6)/4,1))
