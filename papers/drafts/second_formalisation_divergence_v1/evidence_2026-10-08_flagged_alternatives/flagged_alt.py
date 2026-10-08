import json, re, sys
sys.path.insert(0,".")
import check, z3
DOMNORM = "--dom" in sys.argv
DOMS={"E06":"(and (>= pool 0) (>= reserve 0) (>= epoch 0) (>= stale 0))","E10":"(and (>= t 0) (or (= p 0) (= p 1)))"}
POS=lambda q: f"(ite (> {q} 0) {q} 0)"
CUE=re.compile(r"\b(could|may|or|alternative|alternatives|instead|unclear|rather|might|either|other)\b",re.I)
def D(a,b): return f"(define-fun spec ({a}) Bool {b})"
ITEMS={
 "batch1":{"dir":"../evidence_2026-10-08_boundary_divergence_rate","arms":{"B":("chatgpt.json","chatgpt_ambiguity.json"),"C":("claudeblind.json","claudeblind_ambiguity.json"),"D":("claudeincog.json","claudeincog_ambiguity.json"),"A":("claude.json",None)},
  "items":{
   "B01":{"labels":{"inclusive":D("(x Int)","(and (<= 5 x) (<= x 20))"),"exclusive":D("(x Int)","(and (< 5 x) (< x 20))")},"kw":{"inclusive":["include","inclusive"],"exclusive":["exclude","exclusive","strict"]}},
   "B09":{"labels":{"(x&y)|z":D("(x Int) (y Int) (z Int)","(or (and (> x 0) (> y 0)) (> z 0))"),"x&(y|z)":D("(x Int) (y Int) (z Int)","(and (> x 0) (or (> y 0) (> z 0)))")},"kw":{"(x&y)|z":["group","scope","precedence","binding"],"x&(y|z)":["group","scope","precedence","binding"]}},
   "B11":{"labels":{"at most 2 positive":D("(a Int) (b Int) (c Int)","(not (and (> a 0) (> b 0) (> c 0)))"),"at most 1 positive":D("(a Int) (b Int) (c Int)","(or (and (not (> a 0)) (not (> b 0))) (and (not (> a 0)) (not (> c 0))) (and (not (> b 0)) (not (> c 0))))")},"kw":{"at most 2 positive":[],"at most 1 positive":[]}},
   "B12":{"labels":{"ordered":D("(a Int) (b Int) (c Int)","(and (= b (+ a 1)) (= c (+ b 1)))"),"any order":D("(a Int) (b Int) (c Int)","(or (and (= (+ a 1) b) (= (+ b 1) c)) (and (= (+ a 1) c) (= (+ c 1) b)) (and (= (+ b 1) a) (= (+ a 1) c)) (and (= (+ b 1) c) (= (+ c 1) a)) (and (= (+ c 1) a) (= (+ a 1) b)) (and (= (+ c 1) b) (= (+ b 1) a)))")},"kw":{"ordered":["order","permutation","descending"],"any order":["order","permutation","descending"]}},
   "B13":{"labels":{"x>y and diff<=3":D("(x Int) (y Int)","(and (> x y) (<= (- x y) 3))"),"diff<=3 only":D("(x Int) (y Int)","(<= (- x y) 3)")},"kw":{"x>y and diff<=3":["precondition","only bound","only bounds","x > y","x>y","asserted"],"diff<=3 only":["precondition","only bound","only bounds","asserted"]}}}},
 "batch2":{"dir":"../evidence_2026-10-08_batch2","arms":{"B":("chatgptrepaired.json","chatgpt_ambiguity.json"),"C":("claudeC.json","claudeC_ambiguity.json"),"D":("claudeD.json","claudeD_ambiguity.json"),"A":("claude.json",None)},
  "items":{
   "E06":{"labels":{"exact":D("(pool Int) (reserve Int) (epoch Int) (stale Int)","(and (= pool 2) (= reserve 1) (<= epoch 4) (<= stale 1))"),"upper bound":D("(pool Int) (reserve Int) (epoch Int) (stale Int)","(and (<= pool 2) (<= reserve 1) (<= epoch 4) (<= stale 1))")},"kw":{"exact":["exact"],"upper bound":["upper bound","bounds","<="]}},
   "E10":{"labels":{"t>4":D("(t Int) (p Int)","(=> (> t 4) (= p 1))"),"t>=4":D("(t Int) (p Int)","(=> (>= t 4) (= p 1))")},"kw":{"t>4":["> 4",">4","strict","more than"],"t>=4":[">= 4",">=4","at 4","t = 4"]}},
   "K1":{"labels":{"gross":D("(C Int) (q1 Int) (q2 Int) (q3 Int)",f"(<= (+ {POS('q1')} {POS('q2')} {POS('q3')}) C)"),"net_final":D("(C Int) (q1 Int) (q2 Int) (q3 Int)","(<= (+ q1 q2 q3) C)"),"net_prefix":D("(C Int) (q1 Int) (q2 Int) (q3 Int)","(and (<= q1 C) (<= (+ q1 q2) C) (<= (+ q1 q2 q3) C))")},"kw":{"gross":["restoring nothing","restores no","contribute zero","or not","not release","never given back"],"net_final":["final sum","final total","only the final"],"net_prefix":["running","every prefix","prefix"]}},
   "K2":{"labels":{"gross":D("(C Int) (q1 Int) (q2 Int) (q3 Int)",f"(<= (+ {POS('q1')} {POS('q2')} {POS('q3')}) C)"),"net_final":D("(C Int) (q1 Int) (q2 Int) (q3 Int)","(<= (+ q1 q2 q3) C)"),"net_prefix":D("(C Int) (q1 Int) (q2 Int) (q3 Int)","(and (<= q1 C) (<= (+ q1 q2) C) (<= (+ q1 q2 q3) C))")},"kw":{"gross":["contribute zero","restor","zero"],"net_final":["net off","net","final"],"net_prefix":["prefix","running"]}}}}}
def classify(item,smt,st):
    s=st[item]
    for lab,ref in ITEMS_CUR["items"][item]["labels"].items():
        try:
            if DOMNORM and item in DOMS:
                fa,fb=check.rename(check.validate(smt),"specA"),check.rename(check.validate(ref),"specB")
                decl="".join(f"(declare-const {n} {t})\n" for n,t in s["args"]); call=lambda nm:f"({nm} {' '.join(n for n,_ in s['args'])})"
                def sat(p,q):
                    sv=z3.Solver(); sv.set("timeout",5000); sv.from_string(fa+"\n"+fb+"\n"+decl+f"(assert {DOMS[item]})\n(assert (and {call(p)} (not {call(q)})))"); return str(sv.check())
                if sat("specA","specB")=="unsat" and sat("specB","specA")=="unsat": return lab
            elif check.rel(s,smt,ref)[0]=="equivalent": return lab
        except Exception: return "INVALID"
    return "other"
res={}
for bn,cfg in ITEMS.items():
    ITEMS_CUR=cfg; st=json.load(open(cfg["dir"]+"/stimuli.json"))
    chosen={};notes={}
    for arm,(sf,nf) in cfg["arms"].items():
        smts=json.load(open(cfg["dir"]+"/"+sf)); nts=json.load(open(cfg["dir"]+"/"+nf)) if nf else {}
        for it in cfg["items"]:
            chosen[(arm,it)]=classify(it,smts[it],st); notes[(arm,it)]=nts.get(it,"")
    for it,ic in cfg["items"].items():
        for arm in cfg["arms"]:
            n=notes[(arm,it)]; named=set()
            if n and n.lower()!="no" and CUE.search(n):
                for lab,kws in ic["kw"].items():
                    if any(k.lower() in n.lower() for k in kws): named.add(lab)
            res[(bn,it,arm)]={"chosen":chosen[(arm,it)],"named":sorted(named),"note":n}
rows=[]
for bn,cfg in ITEMS.items():
    for it in cfg["items"]:
        for X in ("B","C","D"):
            x=res[(bn,it,X)]
            for Y in cfg["arms"]:
                if Y==X: continue
                y=res[(bn,it,Y)]
                if y["chosen"]!=x["chosen"]:
                    rows.append((bn,it,X,Y,y["chosen"], y["chosen"] in x["named"]))
print("per (batch,item,arm): chosen | named")
for k,v in res.items(): 
    if k[2]!="A": print(k,v["chosen"],"|",v["named"])
print("\nrecall by arm and batch (other arm chose a different label; was that label named by this arm?)")
out={}
for bn in ITEMS:
    for X in ("B","C","D"):
        r=[x for x in rows if x[0]==bn and x[2]==X and x[1]!="B11"]
        cov=sum(1 for x in r if x[5]); out[f"{bn}|{X}"]=(cov,len(r)); print(bn,X,f"{cov}/{len(r)}")
# precision: named labels that any arm chose
pr={}
for (bn,it,arm),v in res.items():
    if arm=="A": continue
    chosen_any={res[(bn,it,a)]["chosen"] for a in ITEMS[bn]["arms"]}
    for lab in v["named"]:
        pr.setdefault(arm,[0,0]); pr[arm][1]+=1; pr[arm][0]+= (lab in chosen_any)
print("\nprecision of named labels (named label chosen by some arm):",{a:f"{c}/{n}" for a,(c,n) in pr.items()})
print("\nK1 gross named by:",[a for a in "BCD" if "gross" in res[("batch2","K1",a)]["named"]])
print("B11 (error) named labels:",{a:res[("batch1","B11",a)]["named"] for a in "BCD"})
json.dump({str(k):v for k,v in res.items()},open("flagged_alt_results_dom.json" if DOMNORM else "flagged_alt_results.json","w"),indent=1)
