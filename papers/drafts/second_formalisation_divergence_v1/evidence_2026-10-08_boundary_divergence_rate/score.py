"""usage: score.py A.json B.json [C.json] ; each file {id: smt} ; optional replies {name}_reply.json for self-report (id: {smt, ambiguity})"""
import json, sys, itertools
from check import rel
st=json.load(open("stimuli.json")); arms={}
for p in sys.argv[1:]:
    n=p.split(".")[0]; arms[n]=json.load(open(p))
rows={}
for (na,A),(nb,B) in itertools.combinations(arms.items(),2):
    for k,s in st.items():
        if k in A and k in B:
            try: r=rel(s,A[k],B[k])[0]
            except Exception as e: r="INVALID"
            rows.setdefault((na,nb),{})[k]=r
for pair,d in rows.items():
    for kind in ("ambiguous","control"):
        ks=[k for k in d if st[k]["kind"]==kind]
        inv=[k for k in ks if d[k]=="INVALID"]
        div=[k for k in ks if d[k] not in ("equivalent","INVALID")]
        print(pair,kind,f"{len(div)}/{len(ks)-len(inv)} divergent (valid items)",div,"invalid:",inv)
json.dump({f"{a}|{b}":d for (a,b),d in rows.items()},open("pair_relations.json","w"),indent=1)
