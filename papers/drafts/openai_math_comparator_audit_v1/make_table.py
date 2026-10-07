import json,os,re,glob,sys
M="/tmp/claude-0/-home-user/94b10564-62ee-5779-8d97-f5ce11793cb8/scratchpad/oaimath/math/lean/"
names=sys.argv[1:]
imp_re=re.compile(r'^\s*import\s+(\S+)',re.M)
def path(m): return m.replace('.','/')+'.lean'
def closure(mod,seen):
    if mod in seen or not mod.startswith('OAI'): return
    seen.add(mod)
    for m in imp_re.findall(open(M+path(mod)).read()): closure(m,seen)
rows=[]
for n in names:
    d=json.load(open(M+f"ComparatorChallenges/{n}.json")); s=set(); closure(d['solution_module'],s)
    sol=sum(len(open(M+path(m)).read().splitlines()) for m in s)
    chl=len(open(M+f"ComparatorChallenges/{n}.lean").read().splitlines())
    lg=f"/srv/lean/cmp_{n}.log"
    t=open(lg).read() if os.path.exists(lg) else ""
    if "Your solution is okay!" in t: res="accepted"
    elif "uncaught exception" in t: res="rejected: "+t.strip().splitlines()[-1][:80]
    elif t: res="not finished"
    else: res="not run"
    rows.append((n,d['theorem_names'][0].split('.')[-1],chl,len(s),sol,res))
print("| Config | Main theorem | Challenge lines | Solution modules | Solution lines | Comparator result |\n|---|---|---|---|---|---|")
for r in rows: print("| `%s` | `%s` | %d | %d | %d | %s |"%r)
