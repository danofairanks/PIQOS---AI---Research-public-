import json, re, sys, z3
def top_forms(s):
    forms=[];d=0;cur=""
    for ch in s:
        if ch=="(": d+=1
        if d>0: cur+=ch
        if ch==")":
            d-=1
            if d==0: forms.append(cur.strip());cur=""
    if d!=0: raise ValueError("unbalanced")
    return forms
def validate(smt):
    f=top_forms(smt)
    if len(f)!=1 or not re.match(r"^\(define-fun\s+spec\b",f[0]): raise ValueError("must be exactly one (define-fun spec ...) form")
    return f[0]
def rename(form,name): return re.sub(r"^\(define-fun\s+spec\b","(define-fun "+name,form,count=1)
import itertools
def candidate_preambles(pre):
    decls=re.findall(r"\(declare-fun\s+(\w+)\s+\(([^)]*)\)\s+(\w+)\)",pre)
    if not decls: return []
    per=[]
    for name,argt,res in decls:
        ats=argt.split(); vs=[f"x{i}" for i in range(len(ats))]
        sig=" ".join(f"({v} {t})" for v,t in zip(vs,ats))
        if res=="Int": bodies=["0","1",vs[0],f"(- {vs[0]})",f"(* 2 {vs[0]})"]
        else:
            bodies=["true","false",f"(> {vs[0]} 0)"]
            if len(vs)>1: bodies+= [f"(= {vs[0]} {vs[1]})",f"(> {vs[1]} {vs[0]})"]
        per.append([f"(define-fun {name} ({sig}) {res} {b})" for b in bodies])
    return ["\n".join(c) for c in itertools.product(*per)]
def rel(stim,A,B,timeout=5000):
    pre=stim["preamble"]; args=stim["args"]
    fa,fb=rename(validate(A),"specA"),rename(validate(B),"specB")
    decl="".join(f"(declare-const {n} {t})\n" for n,t in args)
    call=lambda nm: f"({nm} {' '.join(n for n,_ in args)})" if args else nm
    def run(pre_,p,q):
        s=z3.Solver(); s.set("timeout",timeout); s.set("smt.mbqi",True)
        s.from_string(pre_+"\n"+fa+"\n"+fb+"\n"+decl+f"(assert (and {call(p)} (not {call(q)})))")
        return str(s.check())
    def sat(p,q):
        r=run(pre,p,q)
        if r!="unknown": return r
        # sound countermodel fallback: try fixed interpretations of declared functions
        for pre2 in candidate_preambles(pre):
            try:
                if run(pre2,p,q)=="sat": return "sat"
            except Exception: pass
        return "unknown"
    ab=sat("specA","specB")  # sat => A does not imply B
    ba=sat("specB","specA")
    if "unknown" in (ab,ba): return "inconclusive",ab,ba
    if ab=="unsat" and ba=="unsat": return "equivalent",ab,ba
    if ab=="unsat": return "A stronger (A=>B only)",ab,ba
    if ba=="unsat": return "B stronger (B=>A only)",ab,ba
    return "incomparable",ab,ba
if __name__=="__main__":
    st=json.load(open("stimuli.json")); A=json.load(open(sys.argv[1])); B=json.load(open(sys.argv[2]))
    for k in st:
        if k in A and k in B:
            try: r=rel(st[k],A[k],B[k])
            except Exception as e: r=("ERROR "+str(e)[:80],"","")
            print(k,r)
        else: print(k,"missing in",("A" if k not in A else "B"))
