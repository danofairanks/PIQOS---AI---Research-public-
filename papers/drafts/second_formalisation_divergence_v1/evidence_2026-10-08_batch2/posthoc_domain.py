"""POST-HOC (not preregistered): compare formalisations under a shared natural-domain assumption (counts/durations >= 0, flags in {0,1}) so that domain-guard additions do not count as divergence. usage: posthoc_domain.py A.json B.json"""
import json, sys, re, z3
import check
st=json.load(open("stimuli.json"))
DOM={"E01":"(>= d 0)","E02":"(and (>= amt 0) (or (= v 0) (= v 1)))","E03":"(>= dp 0)","E04":"(and (>= h 0) (>= sev 1) (<= sev 3))",
"E05":"(and (>= age 0) (>= ttl 0) (>= skew 0))","E06":"(and (>= pool 0) (>= reserve 0) (>= epoch 0) (>= stale 0))","E07":"(and (>= lat 0) (or (= c 0) (= c 1)))",
"E08":"(and (>= b 0) (>= r 0))","E09":"(>= attempts 1)","E10":"(and (>= t 0) (or (= p 0) (= p 1)))","C11":"(>= n 0)","C12":"(>= skew 0)"}
A=json.load(open(sys.argv[1])); B=json.load(open(sys.argv[2]))
def rel_dom(s,a,b,dom):
    fa,fb=check.rename(check.validate(a),"specA"),check.rename(check.validate(b),"specB")
    decl="".join(f"(declare-const {n} {t})\n" for n,t in s["args"])
    call=lambda nm:f"({nm} {' '.join(n for n,_ in s['args'])})"
    def sat(p,q):
        sv=z3.Solver(); sv.set("timeout",5000)
        sv.from_string(fa+"\n"+fb+"\n"+decl+f"(assert {dom})\n(assert (and {call(p)} (not {call(q)})))"); return str(sv.check())
    ab,ba=sat("specA","specB"),sat("specB","specA")
    if "unknown" in (ab,ba): return "inconclusive"
    return "equivalent" if ab==ba=="unsat" else "A stronger" if ab=="unsat" else "B stronger" if ba=="unsat" else "incomparable"
out={}
for k,dom in DOM.items():
    try: out[k]=rel_dom(st[k],A[k],B[k],dom)
    except Exception as e: out[k]="INVALID"
print(out); print("divergent under domain normalisation:",[k for k,v in out.items() if v not in ("equivalent","INVALID")])
