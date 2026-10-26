R={ # All,Cutoff,InDom,NovAvg, Rel,Clar,Spec,Act,Sound,Imp,QAvg, Overall
"ClaudeCode(Opus)":(68.3,70.4,17.0,51.9,98.2,89.9,89.2,84.7,73.7,77.4,85.5,68.7),
"IS-Base(Opus)":(77.6,77.0,54.9,69.8,99.5,89.6,90.8,83.5,72.2,78.3,85.7,77.7),
"Codex(GPT5.4)":(72.4,71.8,19.9,54.7,97.1,87.4,88.5,83.4,73.6,76.1,84.4,69.5),
"IS-Base(GPT5.4)":(67.8,67.5,47.7,61.0,98.2,91.3,82.1,78.4,71.9,75.0,82.8,71.9),
"DeepScientist(Q)":(57.6,58.5,15.2,43.8,94.0,85.8,77.8,74.9,61.9,70.6,77.5,60.6),
"AI-Researcher(Q)":(54.6,56.7,19.5,43.6,94.9,85.4,73.4,69.7,57.7,70.5,75.3,59.4),
"IS-Base(Q)":(66.0,67.1,67.5,66.9,96.2,89.9,80.6,77.3,62.8,73.4,80.0,73.5),
"IS-Trained(Q)":(67.3,68.3,70.9,68.8,98.2,90.3,77.9,77.8,64.5,73.5,80.4,74.6)}
print("identities (tol 0.1)")
for n,r in R.items():
    a,c,i,nv,*q,qa,ov=r; q=q[:6]
    print(f" {n:18s} nov {sum((a,c,i))/3-nv:+.2f} qual {sum(q)/6-qa:+.2f} overall {(nv+qa)/2-ov:+.2f}")
def exid(r): return ((r[0]+r[1])/2 + r[10])/2
print("Overall excluding In-domain term: (mean(All,Cutoff)+QualAvg)/2")
for n,r in R.items(): print(f" {n:18s} full {r[11]:.1f}  exID {exid(r):.1f}")
T=R["IS-Trained(Q)"]
for n in ("ClaudeCode(Opus)","Codex(GPT5.4)","DeepScientist(Q)","AI-Researcher(Q)"):
    r=R[n]; print(f"Trained - {n}: overall {T[11]-r[11]:+.1f}; In-domain share of overall gap {(T[2]-r[2])/6:.1f}; exID gap {exid(T)-exid(r):+.1f}")
B=R["IS-Base(Q)"]
print(f"Trained-Base overall {T[11]-B[11]:+.1f}, qual {T[10]-B[10]:+.1f}, nov {T[3]-B[3]:+.1f}; Base-DeepScientist overall {B[11]-R['DeepScientist(Q)'][11]:+.1f}")
print("Base vs Codex on GPT-5.4: All",R['IS-Base(GPT5.4)'][0]-R['Codex(GPT5.4)'][0],"Cutoff",R['IS-Base(GPT5.4)'][1]-R['Codex(GPT5.4)'][1],"QAvg",R['IS-Base(GPT5.4)'][10]-R['Codex(GPT5.4)'][10])
print("In-domain share of Base-DeepScientist novelty-Avg gap:", (B[2]-R['DeepScientist(Q)'][2])/((B[0]-R['DeepScientist(Q)'][0])+(B[1]-R['DeepScientist(Q)'][1])+(B[2]-R['DeepScientist(Q)'][2])))
