# Independent re-implementation of the box check + mutation tests on the checker (vacuity probe).
import gzip, json, itertools as it, copy, sys, importlib.util  # usage: python3 -I tuza_checks.py DIR   (DIR holds verify.py and certificate.json.gz from the results repository)
R=sys.argv[1].rstrip('/')+'/'
art=json.loads(gzip.decompress(open(R+'certificate.json.gz','rb').read()))
spec=importlib.util.spec_from_file_location('v',R+'verify.py'); v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
targets=v.remaining_classes()
print('keys',list(art), 'profiles',len(art['profiles']), 'box keys',list(art['profiles'][0]['boxes'][0]))
# --- own check (no numpy, no shared code): per box
def build(masks,counts):
    E=set(it.combinations(range(8),2)); T=list(it.combinations(range(8),3)); x=8
    for m,c in zip(masks,counts):
        N=[i for i in range(8) if m>>i&1]
        for _ in range(c):
            E|={(u,x) for u in N}; T+=[(a,b,x) for a,b in it.combinations(N,2)]; x+=1
    return E,T
nb=0; ok=True; cells=0
for p in art['profiles']:
    covered=set()
    for b in p['boxes']:
        lo,hi=b['lo'],b['hi']
        E,T=build(p['masks'],hi)
        F={tuple(sorted(e)) for e in b['cover']}
        ok&=F<=E and all(any(e in F for e in it.combinations(t,2)) for t in T)
        E2,_=build(p['masks'],lo); used=set()
        for t in b['packing']:
            t=tuple(sorted(t)); es=set(it.combinations(t,2))
            ok&=len(set(t))==3 and es<=E2 and not(es&used)
            # triangle must be a real triangle of low graph
            ok&=all(e in E2 for e in es); used|=es
        ok&=len(F)<=2*len(b['packing'])
        for c in it.product(*[range(l,h+1) for l,h in zip(lo,hi)]): covered.add(c)
        nb+=1
    cells+=len(covered); ok&= len(covered)==29**3
print('own checker: boxes',nb,'all ok',ok,'cells covered per profile 29^3 each ->',cells==560*29**3)
# --- mutation tests on THEIR checker
def run(a):
    try:
        r=v.tuza(a,targets); return 'accepted' if r['complete_profiles']==560 and not r['incomplete'] else 'rejected(incomplete)'
    except Exception as e: return 'rejected: '+str(e)
base=run(art); print('baseline:',base)
a=copy.deepcopy(art); a['profiles'][0]['boxes'][0]['cover'].pop(); print('drop a cover edge       ->',run(a))
a=copy.deepcopy(art); a['profiles'][0]['boxes'][0]['packing'].append(a['profiles'][0]['boxes'][0]['packing'][0]); print('duplicate a packing tri ->',run(a))
a=copy.deepcopy(art); a['profiles'][0]['boxes'].pop(); print('drop a box              ->',run(a))
a=copy.deepcopy(art); a['profiles'][0]['masks'][0]^=1; print('flip a mask bit         ->',run(a))
a=copy.deepcopy(art); a['profiles'].pop(); print('drop a profile          ->',run(a))
# find a box with tight ratio and shrink packing
for p in a['profiles']:
    pass
b=copy.deepcopy(art)
bx=b['profiles'][0]['boxes'][0]; bx['packing']=bx['packing'][:max(0,len(bx['cover'])//2-1)]; print('shrink packing below |F|/2 ->',run(b))
tight=sum(1 for p in art['profiles'] for bx in p['boxes'] if len(bx['cover'])==2*len(bx['packing'])); print('boxes with |F|==2|P| exactly:',tight,'of',nb)
