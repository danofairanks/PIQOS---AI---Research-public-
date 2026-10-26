# Table 2 (mined thread counts; interm, perm, trans per mode; UNCERTAIN persistence column excluded) and printed summary figures.
t={"DELAYED":(51,157,1),"EXPLICIT":(669,9075,97),"INCORRECT":(155,1733,1),"INVALID":(47,511,1),"MINOR":(15,177,0),"SILENT":(167,963,4)}
N=sum(sum(v) for v in t.values()); print("N included (six modes, three persistences):",N,"(paper: 13,824)")
P=sum(v[1] for v in t.values()); I=sum(v[0] for v in t.values()); T=sum(v[2] for v in t.values())
print("permanent %.2f / intermittent %.2f / transient %.2f  (paper 91.3 / 8.0 / 0.75)"%(100*P/N,100*I/N,100*T/N))
print("EXPLICIT_ERROR/PERMANENT %.2f (paper 65.6); all explicit errors %.2f (paper 71.2)"%(100*t['EXPLICIT'][1]/N,100*sum(t['EXPLICIT'])/N))
print("silent content modes %.2f (paper 19.1); timing modes %.2f (paper 9.7)"%(100*sum(sum(t[k]) for k in('INCORRECT','INVALID','MINOR'))/N,100*sum(sum(t[k]) for k in('DELAYED','SILENT'))/N))
print("cells 2x3x3x3x25 =",2*3*3*3*25)
print("task-completion drop 8.08 -> 3.23: %.1f%%"%(100*(8.08-3.23)/8.08))
print("pooled completion gap 95.6 - 91.1 = %.1f (paper 4.4; rounding of printed rates)"%(95.6-91.1))
print("fault-attributable drop difference 5.8 - 3.6 = %.1f (paper 2.2)"%(5.8-3.6))
print("zero-dose OPP cells 55 of 450 = %.1f%% (paper 12.2%%)"%(100*55/450))
