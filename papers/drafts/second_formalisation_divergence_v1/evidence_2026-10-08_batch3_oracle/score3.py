"""usage: score3.py arm1.json [arm2.json ...] [--notes arm1_ambiguity.json ...] ; arms formalise L-items; ground truth = oracle_truth.json (observed library behaviour)."""
import json, sys, re, z3, itertools
import check
O=json.load(open("oracle_truth.json")); st=json.load(open("stimuli.json"))
VAR={ # alternative readings as python predicates over the oracle's arg order; first = oracle reading
 "L01":{"oracle 0<=a<=m":lambda a,m:0<=a<=m,"exclusive 0<a<m":lambda a,m:0<a<m,"no upper bound a>=0":lambda a,m:a>=0,"a>0 and a<=m":lambda a,m:0<a<=m},
 "L02":{"oracle n<=max":lambda n,m:n<=m,"n<max":lambda n,m:n<m},
 "L03":{"oracle used+cost<=limit":lambda l,u,c:u+c<=l,"used+cost<limit":lambda l,u,c:u+c<l,"cost<=limit":lambda l,u,c:c<=l,"used<=limit":lambda l,u,c:u<=l},
 "L04":{"oracle r<=avail":lambda r,a:r<=a,"r<avail":lambda r,a:r<a},
 "L05":{"oracle k<=calls":lambda k,c:k<=c,"k<calls":lambda k,c:k<c},
 "L07":{"oracle w>limit":lambda w,l:w>l,"w>=limit":lambda w,l:w>=l},
 "L08":{"oracle n<=limit":lambda n,l:n<=l,"n<limit":lambda n,l:n<l},
 "L09":{"oracle existing+amount<=limit":lambda e,a,l:e+a<=l,"existing<=limit (new amount excluded)":lambda e,a,l:e<=l,"existing+amount<limit":lambda e,a,l:e+a<l},
 "L10":{"oracle n<=cap":lambda n,c:n<=c,"n<cap":lambda n,c:n<c}}
BOUNDARY=re.compile(r"inclusive|exclusive|strict|boundary|equal|<=|>=|include|exclude|at most|at least|off-by-one|endpoint",re.I)
CUE=re.compile(r"\b(could|may|or|alternative|instead|unclear|rather|might|either|other)\b",re.I)
def truth(smt,item):
    f=check.validate(smt); args=[n for n,_ in st[item]["args"]]; out=[]
    for row in O[item]["rows"]:
        s=z3.Solver(); s.set("timeout",3000)
        call="("+"spec "+" ".join(str(v) if v>=0 else f"(- {-v})" for v in row[:-1])+")"
        s.from_string(f+"\n"+f"(assert {call})")
        out.append(1 if s.check()==z3.sat else 0)
    return out
arms={}; notes={}
a=sys.argv[1:]
files=[x for x in a if not x.startswith("--")]
i=0
for f in sys.argv[1:]:
    pass
nf=[]
if "--notes" in sys.argv:
    k=sys.argv.index("--notes"); files=sys.argv[1:k]; nf=sys.argv[k+1:]
for f,n in zip(files,nf+[None]*len(files)):
    name=f.split(".")[0]; arms[name]=json.load(open(f)); notes[name]=json.load(open(n)) if n else {}
T={}
for nm,A in arms.items():
    for it in O:
        if it in A:
            try: T[(nm,it)]=truth(A[it],it)
            except Exception as e: T[(nm,it)]=None
def label(it,t):
    rows=O[it]["rows"]
    for lab,fn in VAR[it].items():
        if t==[1 if fn(*r[:-1]) else 0 for r in rows]: return lab
    return "other"
orc={it:[r[-1] for r in O[it]["rows"]] for it in O}
print("arm-by-item chosen reading (oracle match marked *)")
res={}
for it in [k for k in O if k in st]:
    line=[it]
    for nm in arms:
        t=T.get((nm,it)); 
        if t is None: lab="INVALID"
        else: lab=label(it,t)
        res[(nm,it)]=lab; line.append(f"{nm}:{lab}{'*' if lab.startswith('oracle') else ''}")
    print("  ".join(line))
print("\noracle match rate:",{nm:f"{sum(1 for it in st if res.get((nm,it),'').startswith('oracle'))}/{len(st)}" for nm in arms})
print("\nmismatches and flagged-alternative coverage of the oracle reading (boundary/alternative keyword rule + cue):")
for it in st:
    for nm in arms:
        lab=res.get((nm,it))
        if lab and not lab.startswith("oracle"):
            n=notes[nm].get(it,"")
            named=bool(n and n.lower()!="no" and CUE.search(n) and (BOUNDARY.search(n) or it in("L03","L09") and re.search(r"new|already|existing|requested|before|include",n,re.I)))
            print(f"  {it} {nm}: chose {lab} | note names a boundary/alternative: {named} | note: {n[:110]}")
print("\nshared non-oracle readings (>=2 arms choose the same non-oracle label):")
for it in st:
    labs=[res.get((nm,it)) for nm in arms if res.get((nm,it)) and not res.get((nm,it)).startswith("oracle")]
    for l in set(labs):
        if labs.count(l)>=2: print("  ",it,l,labs.count(l),"arms")
print("\nself-test rows:",{it:len(O[it]["rows"]) for it in st})
