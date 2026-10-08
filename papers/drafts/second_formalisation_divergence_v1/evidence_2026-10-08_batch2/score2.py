"""usage: score2.py arm1.json arm2.json ... ; per-pair divergence + cap-family reading classification"""
import json, sys, itertools
from check import rel
st=json.load(open("stimuli.json")); arms={p.split(".")[0]:json.load(open(p)) for p in sys.argv[1:]}
rows={}
for (na,A),(nb,B) in itertools.combinations(arms.items(),2):
    for k,s in st.items():
        if k in A and k in B:
            try: r=rel(s,A[k],B[k])[0]
            except Exception: r="INVALID"
            rows.setdefault(f"{na}|{nb}",{})[k]=r
for pair,d in rows.items():
    for kind in ("external","control","cap"):
        ks=[k for k in d if st[k]["kind"]==kind]; inv=[k for k in ks if d[k]=="INVALID"]
        div=[k for k in ks if d[k] not in ("equivalent","INVALID")]
        print(pair,kind,f"{len(div)}/{len(ks)-len(inv)}",div,"invalid:",inv)
json.dump(rows,open("pair_relations.json","w"),indent=1)
ref={"gross":"(define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool (<= (+ (ite (> q1 0) q1 0) (ite (> q2 0) q2 0) (ite (> q3 0) q3 0)) C))",
     "net_final":"(define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool (<= (+ q1 q2 q3) C))",
     "net_prefix":"(define-fun spec ((C Int) (q1 Int) (q2 Int) (q3 Int)) Bool (and (<= q1 C) (<= (+ q1 q2) C) (<= (+ q1 q2 q3) C)))"}
print("\ncap-family reading by arm (gross / net_final / net_prefix / other / INVALID)")
for k in [k for k in st if st[k]["kind"]=="cap"]:
    out=[]
    for n,A in arms.items():
        lab="other"
        try:
            for name,r in ref.items():
                if rel(st[k],A[k],r)[0]=="equivalent": lab=name;break
        except Exception: lab="INVALID"
        out.append(f"{n}:{lab}")
    print(k,"  ".join(out))
