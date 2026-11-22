# Probe 4: unseen failure mass among Lean checkers. Inputs: /tmp/arena_results.json, /tmp/arena_test_dates.json (first-commit dates from the arena repo).
import json,re,collections,math,datetime,random
d=json.load(open('/tmp/arena_results.json')); dates=dict(json.load(open('/tmp/arena_test_dates.json')))
tests={t['name']:t for t in d['tests']}
units=[t for t in tests if tests[t]['outcome']=='reject' and t.startswith(('bugs/','other/'))]
RULES=[('nested','nested_inductive'),('proof-irrel','proof_irrelevance'),('rec','recursor_rules'),('inductive','inductive_declaration'),('ctor','inductive_declaration'),('proj','projections'),('level','universe_levels'),('universe','universe_levels'),('closure','closure_context_caching'),('cache','closure_context_caching'),('bvar','closure_context_caching'),('context','closure_context_caching'),('eta','eta'),('large-elim','large_elimination'),('lit','literals')]
def coarse(name):
    n=name.split('/',1)[1]
    for k,c in RULES:
        if k in n: return c
    return 'other'
def fine(name): return re.sub(r'[-_]?\d+$','',name.split('/',1)[1])
def finder(name):
    s=re.sub(r'\s+',' ',tests[name].get('description') or '')
    if re.search(r'differential',s,re.I): return 'differential_run'
    if re.search(r'Aristotle',s): return 'ai_assisted_human'
    if re.search(r'Origin: reported as leanprover/lean4#14576',s): return 'ai_assisted_human'
    if re.search(r'found by \S+ in a draft|Found while reading',s): return 'human_review'
    return 'unknown'
ev=[]
for u in units:
    ev.append({'id':u,'coarse':coarse(u),'fine':fine(u),'finder':finder(u),'date':dates.get(u),'src':'arena'})
# postmortem items: variant A = prereg-listed six; variant B = only those not cited by an arena test (14613,14616,14838,14833)
PM={'#14613':('universe_levels','vendor_internal_model','2026-08-20'),'#14616':('nested_inductive','vendor_internal_model','2026-08-20'),'#14806':('closure_context_caching','vendor_internal_model','2026-08-20'),'#14807':('prop_sort_check','vendor_internal_model','2026-08-20'),'#14838':('runtime_refcount','vendor_internal_model','2026-08-20'),'#14833':('build_supply_chain','vendor_internal_model','2026-08-20')}
def with_pm(keys):
    out=list(ev)
    for k in keys:
        c,f,dt=PM[k]; out.append({'id':'pm'+k,'coarse':c,'fine':'pm'+k,'finder':f,'date':dt,'src':'postmortem'})
    return out
variants={'A_all_six_pm':with_pm(PM.keys()),'B_four_not_in_arena':with_pm(['#14613','#14616','#14838','#14833']),'C_arena_only':list(ev)}
def stats(events,key):
    c=collections.Counter(e[key] for e in events); N=len(events); S=len(c)
    n1=sum(1 for v in c.values() if v==1); n2=sum(1 for v in c.values() if v==2)
    gt=n1/N; chao=S+n1*(n1-1)/(2*(n2+1))
    return {'N':N,'S_obs':S,'n1':n1,'n2':n2,'GT_missing_mass':gt,'Chao1':chao,'ratio':chao/S,'class_counts':dict(c.most_common())}
out={'n_arena_units':len(units),'class_rules':[r for r in RULES]}
for vn,evs in variants.items():
    o={'coarse':stats(evs,'coarse'),'fine':stats(evs,'fine')}
    ind={'nested_inductive','recursor_rules','proof_irrelevance','inductive_declaration'}
    o['inductive_share']=sum(1 for e in evs if e['coarse'] in ind)/len(evs)
    # Chao2 over finder types
    inc=collections.defaultdict(set)
    for e in evs:
        if e['finder']!='unknown': inc[e['coarse']].add(e['finder'])
    Q=collections.Counter(len(v) for v in inc.values()); Q1=Q.get(1,0); Q2=Q.get(2,0); S=len(inc)
    o['chao2']={'classes_with_known_finder':S,'Q1':Q1,'Q2':Q2,'Qge2':sum(v for k,v in Q.items() if k>=2),'estimate':S+Q1*Q1/(2*max(Q2,1)),'incidence':{k:sorted(v) for k,v in inc.items()}}
    out[vn]=o
# bug-level overlap: each unit has at most one finder by construction (single attribution): check multi-finder text
multi=[u for u in units if len({m for m in ['differential','Aristotle','draft','Found while'] if m.lower() in (tests[u].get('description') or '').lower()})>1]
out['bug_level_multi_finder_units']=multi
# timeline: post-import events (dates after the bulk import day 2026-09-17)
def dt(s): return datetime.datetime.fromisoformat(s[:10]) if s else None
bulk=datetime.datetime(2026,9,17)
byday=collections.Counter((dt(e['date']).date().isoformat()) for e in ev if e['date'])
out['arena_first_commit_days']=dict(sorted(byday.items()))
post=sorted([e for e in ev if e['date'] and dt(e['date'])>bulk],key=lambda e:e['date'])
pre=[e for e in ev if e['date'] and dt(e['date'])<=bulk]
out['n_pre_or_bulk']=len(pre); out['n_post']=len(post)
seen={e['coarse'] for e in pre}; seen_fine={e['fine'] for e in pre}
cnt=collections.Counter(e['coarse'] for e in pre); N=len(pre)
cal=[]; newc=0
cnt_c=collections.Counter(cnt)
for e in post:
    n1=sum(1 for v in cnt_c.values() if v==1); Nn=sum(cnt_c.values())
    pred=n1/Nn; isnew=int(e['coarse'] not in cnt_c); cal.append((e['id'],e['date'][:10],e['coarse'],round(pred,3),isnew))
    cnt_c[e['coarse']]+=1
out['prospective']={'events':cal,'mean_pred':sum(c[3] for c in cal)/len(cal) if cal else None,'obs_new_frac':sum(c[4] for c in cal)/len(cal) if cal else None,'brier':sum((c[3]-c[4])**2 for c in cal)/len(cal) if cal else None}
# new classes over time among post events (month buckets)
seen_c=set(e['coarse'] for e in pre); new_by_month=collections.Counter(); ev_by_month=collections.Counter()
for e in post:
    m=e['date'][:7]; ev_by_month[m]+=1
    if e['coarse'] not in seen_c: new_by_month[m]+=1; seen_c.add(e['coarse'])
out['post_events_by_month']=dict(ev_by_month); out['post_new_classes_by_month']=dict(new_by_month)
# official-kernel-only subset: tests whose description says the official kernel accepted/ cites a lean4 PR
off=[u for u in units if re.search(r'official kernel|leanprover/lean4#\d+',tests[u].get('description') or '')]
out['official_subset']={'n':len(off),'coarse':dict(collections.Counter(coarse(u) for u in off))}
json.dump(out,open('probe4_results.json','w'),indent=1)
for vn in variants:
    o=out[vn]; c=o['coarse']; f=o['fine']
    print(f"{vn}: N={c['N']} classes={c['S_obs']} n1={c['n1']} n2={c['n2']} GT={c['GT_missing_mass']:.3f} Chao1={c['Chao1']:.1f} ratio={c['ratio']:.2f} | fine S={f['S_obs']} n1={f['n1']} GT={f['GT_missing_mass']:.3f} | inductive share={o['inductive_share']:.2f} | chao2 Q1={o['chao2']['Q1']} Q2={o['chao2']['Q2']} Qge2={o['chao2']['Qge2']} est={o['chao2']['estimate']:.1f}")
print('class counts (B):',out['B_four_not_in_arena']['coarse']['class_counts'])
print('chao2 incidence (B):',out['B_four_not_in_arena']['chao2']['incidence'])
print('multi-finder units:',multi)
print('first-commit days:',out['arena_first_commit_days'])
print('n pre/bulk',len(pre),'post',len(post)); print('prospective:',out['prospective'])
print('post by month',dict(ev_by_month),'new classes',dict(new_by_month)); print('official subset',out['official_subset'])
