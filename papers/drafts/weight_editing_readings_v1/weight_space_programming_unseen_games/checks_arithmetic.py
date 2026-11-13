# Arithmetic checks on numbers printed in arXiv 2611.16981v1 (typed from the PDF tables). E1 = recomputed here.
from math import sqrt
def wilson(k,n,z=1.96):
    p=k/n; d=1+z*z/n; c=(p+z*z/(2*n))/d; h=z*sqrt(p*(1-p)/n+z*z/(4*n*n))/d; return round(c-h,2),round(c+h,2)
print("== Table 5 entries")
E=[15232,9248,3104,2304,528,12416,12864,1544,49]; print(sum(E),"printed 57289")
print("W1",19*5*5*32+32,"W2",32*32*9+32,"W3",32*96+32,"Wh",16*16*9,"Uh,bh",16*32+16,"Wz",128*96+128,"Wm..",64*64+64*128+64*8+64,"Wo",8*192+8,"Wc",48+1)
print("== GMAC (positions 4096; U_h F3 applied once, outside the loop)")
pos=4096; conv=(19*5*5*32+32*32*9+32*96)*pos; Uh=16*32*pos; wh=16*16*9*pos
for T in (128,8): print("T",T,round((conv+Uh+T*wh)/1e9,3))
print("noaxial T128",round((conv-32*32*pos+Uh+128*wh)/1e9,3),"printed 1.32 / 0.19 / 1.31")
print("params ratio FreeArch cap",round(150000/57289,2),"printed 2.6x")
print("== Table 9 totals (parsed from the PDF text layer of p.24, saved as page24_text_layer.txt)")
rows=[];tot=None
for ln in open('page24_text_layer.txt'):
    if ln.strip().startswith('Total'): pass
    t=ln.split()
    if t and t[0]=='•': break
    if not t or t[0] in('Private','Public','Arm','Requests','Table'): continue
    nums=[x.replace(',','') for x in t]
    if t[0]=='Total':
        tot=[int(x.replace(',','')) for x in t[1:8]]; continue
    # arm name then numbers: find first purely numeric token
    i=next((k for k,x in enumerate(nums) if x.isdigit()),None)
    if i is None or len(nums)-i<9: continue
    try: v=[int(x) for x in nums[i:i+9]]
    except ValueError: continue
    rows.append((' '.join(t[:i]),v))
print("rows parsed",len(rows))
for name,v in rows:
    wr,sess,req,comp,tr,ref,err,intr,rer=v
    assert req==comp+tr+ref+err+intr,(name,v)
print("row identity Req=Compl+Trunc+Ref+Err+Interr holds for all rows")
col=lambda i:sum(v[i] for _,v in rows)
print("sessions",col(1),"requests",col(2),"completed",col(3),"trunc/ref/err/interr",[col(i) for i in (4,5,6,7)],"re-run",col(8))
print("printed totals (Wr,Sess,Req,Compl,Trunc,Ref,Err):",tot)
print("== pooled means")
W2=[.56,.43,.36,.33];F2=[.90,.84,.68,.74];B=[.98,.91,.87,.87];P2=[1,1,.97,.98];A=[.58,.44,.35,.37];Bg=[.88,.78,.56,.68]
m=lambda x:round(sum(x)/4,3)
print("W2",m(W2),"FA",m(F2),"Bounded",m(B),"P2",m(P2),"A",m(A),"B",m(Bg),"B-A",round(m(Bg)-m(A),3),"Bounded-FA",round(m(B)-m(F2),3))
print("W2 gain over W1 per main writer", [round(a-b,2) for a,b in zip(W2,[.40,.32,.15,.21])],"printed 11-21")
print("== Table 19 macro (3/11/5/1 families)")
fam=[3,11,5,1]
for n,v in [("W2",[.89,.40,.27,0]),("P2",[.98,.99,.99,.96]),("W1",[.65,.25,.14,0]),("best learned",[.32,.16,.05,0])]: print(n,round(sum(f*x for f,x in zip(fam,v))/20,3))
print("== Wilson 95% for runs>=0.5 (Table 18)")
for n,k in [("Astra W2",31),("Sol W2",25),("Opus W2",18),("Terra W2",21),("Astra FA",56),("Sol FA",53),("Opus FA",44),("Terra FA",49)]: print(n,k,wilson(k,60))
print("P2 60/60",wilson(60,60),"59/60",wilson(59,60))
print("== noise: halving point and robust ratio  1e-3/1e-7 =",1e-3/1e-7, "; PPO first-update ratio robust/standard",round(1.0e-3/2.9e-5,1))
print("== counts: Table 7 held-out totals not recomputed; Table 2 deltas vs printed")
for w,a,b,d in [("Astra",.90,.56,.34),("Sol",.84,.43,.41),("Opus",.68,.36,.33),("Terra",.74,.33,.41),("Luna",.14,.11,.04),("Sonnet",.39,.19,.20),("Haiku",.14,.06,.07),("GPT-5.6",.48,.25,.23),("Opus5",.33,.16,.17)]: print(w,round(a-b,2),"printed",d)
print("== Table 4 vs Tables 11/12 agreement: fixed-all 0.51/0.31/0.05 vs 0.51/0.31/0.05(1e-4); FA 0.95/0.72/0.44 vs 0.95/0.72/0.44 -> consistent (read, not computed)")
