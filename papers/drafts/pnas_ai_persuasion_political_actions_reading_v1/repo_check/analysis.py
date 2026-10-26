# Summary statistics from the public data of the PNAS persuasion paper (read-only clone, commit d7025d1). Run: python3 -I analysis.py /path/to/ai-action-persuasion
import json,csv,sys,collections,math
csv.field_size_limit(10**9)
root=sys.argv[1]
def load(s): return json.load(open(f'{root}/data/processed/{s}.json'))['participants']
S={'S1':load('study1'),'S2':load('study2')}
def ctrl(p): return p['conversation_type'].startswith('control')
def rate(xs): return (sum(xs)/len(xs)*100 if xs else float('nan'),len(xs))
def wilson(k,n,z=1.96):
    if n==0: return (float('nan'),)*2
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return ((c-h)/d*100,(c+h)/d*100)
def fmt(xs):
    k=sum(xs);n=len(xs);lo,hi=wilson(k,n); return f"{k/n*100:5.1f}% (n={n}, 95% [{lo:4.1f},{hi:4.1f}])" if n else "n=0"
print("== R1 replication (processed analytic samples)")
for s,P in S.items():
    c=[p['outcomes']['signed_petition'] for p in P if ctrl(p)]; t=[p['outcomes']['signed_petition'] for p in P if not ctrl(p)]
    print(s,"N",len(P),"control",fmt(c),"treated",fmt(t),"diff",round(sum(t)/len(t)*100-sum(c)/len(c)*100,1))
print("== R2 direct ask (S2 raw, merged by participant id)")
raw={}
for r in csv.DictReader(open(f'{root}/data/raw/study2_raw.csv',encoding='utf-8')):
    raw[r.get('participantId') or r.get('participant_id')]=r
P2=S['S2']; hit=[p for p in P2 if p['participant_id'] in raw]; print("processed S2 ids found in raw:",len(hit),"of",len(P2))
def ask(p):
    v=raw[p['participant_id']].get('direct_ask','').strip().lower(); return v in ('true','1','yes')
by=collections.defaultdict(list)
for p in hit: by[p['conversation_type']].append(ask(p))
for k in sorted(by): print(f"  {k:26s} ask rate {sum(by[k])/len(by[k])*100:5.1f}% (n={len(by[k])})")
ct=[ask(p) for p in hit if ctrl(p)]; print("  control overall",round(sum(ct)/len(ct)*100,2),"% ; treated overall",round(sum(ask(p) for p in hit if not ctrl(p))/len([p for p in hit if not ctrl(p)])*100,1),"%")
print("== R3 signing by ask among treated (S2; observational, NOT randomized)")
tr=[p for p in hit if not ctrl(p)]
a=[p['outcomes']['signed_petition'] for p in tr if ask(p)]; n=[p['outcomes']['signed_petition'] for p in tr if not ask(p)]
c2=[p['outcomes']['signed_petition'] for p in hit if ctrl(p)]
print(" ask    ",fmt(a)); print(" no ask ",fmt(n)); print(" control",fmt(c2))
print(" by n_ask_messages (treated):")
cnt=collections.defaultdict(list)
for p in tr:
    k=raw[p['participant_id']].get('n_ask_messages','').strip(); k=int(float(k)) if k not in ('','NA') else -1; cnt[min(k,4)].append(p['outcomes']['signed_petition'])
for k in sorted(cnt): print("   n_ask =",k if k<4 else '4+',fmt(cnt[k]))
print("== R4 treatment effect on signing by prior petition support (pre agreement)")
bins=[('<=2',lambda x:x<=2),('3',lambda x:x==3),('4',lambda x:x==4),('>=5',lambda x:x>=5),('<=4',lambda x:x<=4),('<=3',lambda x:x<=3)]
for s,P in S.items():
    print(s)
    for name,f in bins:
        c=[p['outcomes']['signed_petition'] for p in P if ctrl(p) and f(p['pre_treatment']['agreement'])]; t=[p['outcomes']['signed_petition'] for p in P if not ctrl(p) and f(p['pre_treatment']['agreement'])]
        if c and t: print(f"  pre {name:4s} control {sum(c)/len(c)*100:5.1f}% (n={len(c)}) treated {sum(t)/len(t)*100:5.1f}% (n={len(t)}) diff {sum(t)/len(t)*100-sum(c)/len(c)*100:5.1f} pp")
print("== R5 funnel: wants_to_sign and conversion to signed")
for s,P in S.items():
    for lab,sel in (('control',True),('treated',False)):
        G=[p for p in P if ctrl(p)==sel]; w=[p for p in G if p['outcomes']['wants_to_sign_petition']]
        print(f" {s} {lab}: wants {len(w)/len(G)*100:5.1f}% ; signed|wants {sum(p['outcomes']['signed_petition'] for p in w)/len(w)*100:5.1f}% (n={len(w)}) ; signed overall {sum(p['outcomes']['signed_petition'] for p in G)/len(G)*100:5.1f}%")
print("== R6 perceived bias (ratings.biased, 0-100) among treated")
for s,P in S.items():
    T=[p for p in P if not ctrl(p) and p['ratings']['biased'] is not None]
    def m(xs): return sum(xs)/len(xs) if xs else float('nan')
    sg=m([p['ratings']['biased'] for p in T if p['outcomes']['signed_petition']]); ns=m([p['ratings']['biased'] for p in T if not p['outcomes']['signed_petition']])
    op=m([p['ratings']['biased'] for p in T if p['pre_treatment']['agreement']<=3]); su=m([p['ratings']['biased'] for p in T if p['pre_treatment']['agreement']>=5])
    print(f" {s}: biased signers {sg:5.1f} non-signers {ns:5.1f} | opponents(<=3) {op:5.1f} supporters(>=5) {su:5.1f}")
print("== R7 conversation length (turns) among treated, by signing")
for s,P in S.items():
    T=[p for p in P if not ctrl(p) and p['conversation']['length'] is not None]
    def m(xs): return sum(xs)/len(xs)
    print(f" {s}: signers {m([p['conversation']['length'] for p in T if p['outcomes']['signed_petition']]):.2f} non-signers {m([p['conversation']['length'] for p in T if not p['outcomes']['signed_petition']]):.2f}")
print("== R8 signing among treated opponents (pre<=3)")
for s,P in S.items():
    t=[p['outcomes']['signed_petition'] for p in P if not ctrl(p) and p['pre_treatment']['agreement']<=3]; print(f" {s}: {fmt(t)}")
print("== R9 (added after the preregistered set; post-hoc) composition and decomposition of the headline effect")
for s,P in S.items():
    n=len(P); sup=[p for p in P if p['pre_treatment']['agreement']>=5]; oth=[p for p in P if p['pre_treatment']['agreement']<=4]
    def d(G):
        c=[p['outcomes']['signed_petition'] for p in G if ctrl(p)]; t=[p['outcomes']['signed_petition'] for p in G if not ctrl(p)]; return sum(t)/len(t)-sum(c)/len(c)
    ws,wo=len(sup)/n,len(oth)/n; ds,do=d(sup),d(oth)
    print(f" {s}: prior supporters {ws*100:.1f}% of sample, others {wo*100:.1f}%; effect among supporters {ds*100:.1f} pp, others {do*100:.1f} pp; contribution to headline: supporters {ws*ds*100:.1f} pp, others {wo*do*100:.1f} pp (sum {(ws*ds+wo*do)*100:.1f})")
print("== R10 (post-hoc) S2 treated: signing by direct ask within prior-support groups (observational)")
for lab,f in (('opponents (<=3)',lambda x:x<=3),('neutral (4)',lambda x:x==4),('supporters (>=5)',lambda x:x>=5)):
    G=[p for p in hit if not ctrl(p) and f(p['pre_treatment']['agreement'])]
    a=[p['outcomes']['signed_petition'] for p in G if ask(p)]; n0=[p['outcomes']['signed_petition'] for p in G if not ask(p)]
    cc=[p['outcomes']['signed_petition'] for p in hit if ctrl(p) and f(p['pre_treatment']['agreement'])]
    print(f" {lab:18s} ask {fmt(a)} | no ask {fmt(n0)} | control {fmt(cc)}")
print("== R11 (post-hoc) S2 treated: share with no ask by prior-support group (does the model ask less of opponents?)")
for lab,f in (('opponents (<=3)',lambda x:x<=3),('neutral (4)',lambda x:x==4),('supporters (>=5)',lambda x:x>=5)):
    G=[p for p in hit if not ctrl(p) and f(p['pre_treatment']['agreement'])]
    print(f" {lab:18s} no-ask share {sum(not ask(p) for p in G)/len(G)*100:5.1f}% (n={len(G)}); mean n_ask {sum(max(0,int(float(raw[p['participant_id']].get('n_ask_messages') or 0))) for p in G)/len(G):.2f}")
