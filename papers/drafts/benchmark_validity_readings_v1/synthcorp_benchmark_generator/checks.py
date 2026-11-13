# Usage: pdftotext -layout paper.pdf paper.txt, then python3 checks.py (reads paper.txt in the working directory).
# Arithmetic checks on numbers printed in arXiv 2611.14765v1 (typed/parsed from the PDF text layer). E1 = recomputed here.
import re
T=open('paper.txt').read()
n=[37,31,62,28,26,19,53]
print("== Table 4: tasks",sum(n),"printed 256; atomic/composite sums:",sum(a for a,_ in [(23,14),(23,8),(36,26),(17,11),(18,8),(14,5),(24,29)]),"/",sum(b for _,b in [(14,0),(8,0),(26,0),(11,0),(8,0),(5,0),(29,0)]) if False else sum([14,8,26,11,8,5,29]))
print("composite share",round(101/256*100,1),"printed 39.5; doc-required",32+25+48+24+18+13+45,"=",round((32+25+48+24+18+13+45)/256*100,1),"printed 80.1 (205)")
print("== Table 12 / Sec 5.3")
den=[29,21,48,23,20,14,43]; num=[3,2,47,11,15,8,33]; print("complexity-bearing",sum(den),"printed 198; requested",sum(num),round(100*sum(num)/sum(den),1),"printed 60.1")
print("doc-lookup/numeric",5+8+6+0+1+1+4,"/",13+10+12+10+6+6+21,"printed 25/78; db-required",round(100*(78-25)/78,1),"printed 68.0")
print("distinct skeletons",34+30+57+27+24+19+44,"/256 =",round(100*(34+30+57+27+24+19+44)/256,1),"printed 235 / 91.8")
for lab,v in [("join",[70,48,48,64,69,58,57]),("grouping",[70,87,84,64,92,84,85]),("nesting",[54,55,56,39,58,74,66])]: print(lab,"task-weighted",round(sum(a*b for a,b in zip(v,n))/256,1))
print("unweighted mean of the seven estates:",[round(sum(v)/7,1) for v in ([70,48,48,64,69,58,57],[70,87,84,64,92,84,85],[54,55,56,39,58,74,66])],"(printed 'on average across benchmarks' 59.3 / 81.0 / 57.4: the unweighted mean matches within rounding; the task-weighted join share is 57.7)")
print("== Table 5 error rates")
print("dependency violations smaller six",3+8+4+18+1+14,"/",105+104+129+253+75+109,"=",round(100*(3+8+4+18+1+14)/(105+104+129+253+75+109),2),"printed 6.2; Retail-1000 186/1.1K=",round(186/1100*100,1))
print("operator contract smaller six",1+3+6+13+0+3,"/",59+91+86+299+90+92,"=",round(100*(1+3+6+13+0+3)/(59+91+86+299+90+92),2),"printed 3.6; Retail-1000 93/1.3K=",round(93/1300*100,1),"printed 7.1")
print("Retail-1000 execution failures 33/15700 =",round(100*33/15700,2),"% (printed 0.2); 28 of the 33 are one daily write repeated over 28 days ->",round(100*(33-28+1)/15700,3),"% counting that write once")
print("== Table 7 parsed from text layer")
rows={}
cur=None
for ln in T.split('\n'):
    if ln.startswith(('Gemma 4','DeepSeek V4.1','Claude Opus 5.5')) and '±' not in ln: cur=ln.split()[0]; continue
    m=re.match(r'^(S[1-4]) \(.*?\)\s+(.*)$',ln)
    if m and cur:
        v=[float(x) for x in re.findall(r'(\d+\.\d)±',m.group(2))]
        if len(v)==8: rows[(cur,m.group(1))]=v
print("rows parsed",len(rows))
for k,v in rows.items():
    w=sum(a*b for a,b in zip(v[:7],n))/256
    print(f"  {k[0]:9s}{k[1]} task-weighted mean of estates {w:5.1f}  printed All {v[7]:5.1f}  diff {w-v[7]:+.1f}")
A={k:v[7] for k,v in rows.items()}
print("S1->S2 (All):",[round(A[(m,'S2')]-A[(m,'S1')],1) for m in ('Gemma','DeepSeek','Claude')],"printed 9 to 17")
print("S2->S3 (All):",[round(A[(m,'S3')]-A[(m,'S2')],1) for m in ('Gemma','DeepSeek','Claude')],"printed 12 to 20")
print("S3 vs S4 (All):",[(m,A[(m,'S3')],A[(m,'S4')]) for m in ('Gemma','DeepSeek','Claude')])
print("== per-estate ordering exceptions to 'Opus leads DeepSeek leads Gemma in every setting' (point estimates)")
cols=['Retail-10','Retail-100','Retail-1000','Music','Banking','Logistics','Insurance','All']
for s in ('S1','S2','S3','S4'):
    for i,c in enumerate(cols):
        g,d,o=rows[('Gemma',s)][i],rows[('DeepSeek',s)][i],rows[('Claude',s)][i]
        if not (o>=d>=g): print(f"  {s} {c}: Gemma {g} DeepSeek {d} Opus {o}")
print("== Opus 'All' standard errors vs gaps")
print("S3 vs S4 Opus gap",round(A[('Claude','S4')]-A[('Claude','S3')],1),"with SEs 1.9/1.7")
print("== format-tolerant rescoring claim: S4 Opus 88.8 -> printed 94; DeepSeek 77.7 -> 90: implied extra correct runs",round((94-88.8)/100*256,1),"and",round((90-77.7)/100*256,1),"task-equivalents out of 256")
