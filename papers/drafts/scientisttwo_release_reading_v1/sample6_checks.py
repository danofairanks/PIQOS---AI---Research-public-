# E1 arithmetic on tables transcribed from six generated papers (ScientistTwo site repo). Tables as printed; page/table refs in README.
print('== p1 UNI-XDLM ==')
tab4={'SEDD':(705.63,1666.69),'MDLM':(597.32,1494.52),'GIDD':(585.46,1470.50),'UDLM':(514.03,1202.48),'XDLM':(489.94,1182.22),'UNI-XDLM':(469.54,1192.91),'RADD':(437.33,1092.10)}
for j,name in ((0,'OWT valid'),(1,'zero-shot avg')):
    r=sorted(tab4.items(),key=lambda kv:kv[1][j]); print(' L=512 rank by %-13s'%name,[ (k,v[j]) for k,v in r][:4],'... worst:',r[-1][0],r[-1][1][j],'; UNI-XDLM rank',[k for k,_ in r].index('UNI-XDLM')+1,'of 7')
print(' L=512 zero-shot: UNI-XDLM minus XDLM = %+.2f (positive = worse)'%(1192.91-1182.22))
mdlm=[460.42,151.56,210.70,776.93,513.47,468.37,263.58]; uni=[490.23,148.58,222.93,653.37,434.46,448.13,267.54]
d=[m-u for m,u in zip(mdlm,uni)]; print(' zero-shot vs MDLM (L=128): UNI better on %d/7 datasets; PTB accounts for %.0f%% of the summed PPL difference (%.1f of %.1f)'%(sum(x>0 for x in d),100*d[3]/sum(d),d[3],sum(d)))
print(' in-domain valid PPL (lower better): MDLM 136.93 < UNI-XDLM 146.39 < XDLM 155.35; GIDD 113.45')
print(' 8B CPT: GSM8K base 40.8 -> UNI-XDLM 34.2 (%.1f pts, %.0f%% rel.); MDLM CPT 37.5'%(34.2-40.8,100*(34.2-40.8)/40.8))
print('== p3 ALOT-DRO ==')
cov=[('UCI type-1',0.841),('UCI type-2',0.880),('S&P k=3',0.904),('S&P k=10',0.861)]
print(' Table 3 coverage vs target 0.90:',[(n,c,'below' if c<0.90 else 'ok') for n,c in cov],'-> below target on',sum(c<0.90 for _,c in cov),'of 4')
print(' Table 3 loss, ALOT vs OT-DRO (lower better): UCI t1 0.4670 vs 0.4767 (ALOT better); t2 0.6277 vs 0.5118 (ALOT worse %.0f%%); S&P k3 3.758 vs 3.541 (worse %.0f%%); k10 1.798 vs 1.782 (worse %.0f%%)'%(100*(0.6277/0.5118-1),100*(3.758/3.541-1),100*(1.798/1.782-1)))
print(' Table 2 portfolio k=3 CVaR (lower better): ALOT -0.025 vs DiffDRO -0.071, OT-DRO -0.068, PtC -0.019')
print(' time ratio 551.4/4.08 = %.0fx ; coupling-ablation dist ratio 112.26/0.44 = %.0fx (the abstract\'s ~880x not found in any table)'%(551.4/4.08,112.26/0.44))
print('== p4 ScaleMode-NeuralSurv (Table 1: [base mean, base sd, SM mean, SM sd]) ==')
T={'COLON':(.609,.092,.639,.056),'METABRIC':(.559,.070,.624,.092),'GBSG':(.647,.078,.681,.092),'NWTCO':(.611,.124,.695,.145),'WHAS':(.606,.142,.634,.147),'SUPPORT':(.523,.039,.643,.084),'VLC':(.672,.083,.692,.032),'SAC3':(.518,.040,.560,.063)}
n=0
for k,(bm,bs,sm,ss) in T.items():
    dlt=sm-bm; mx=max(bs,ss); n+=dlt<mx
    print('  %-9s dC %+.3f  max(sd) %.3f  delta<max sd: %s'%(k,dlt,mx,dlt<mx))
print(' datasets where the C-index gain is smaller than the larger fold-sd:',n,'of 8')
picp={'COLON':(.640,.704),'METABRIC':(.648,.552),'GBSG':(.656,.632),'NWTCO':(.632,.536),'WHAS':(.496,.568),'SUPPORT':(.264,.440),'VLC':(.392,.608),'SAC3':(.584,.800)}
print(' PICP km (target 0.95) decreased on',[k for k,(b,s) in picp.items() if s<b],'; aggregate 0.539 -> 0.605 (still %.2f below 0.95)'%(0.95-0.605))
dcal={'COLON':(.740,.855),'METABRIC':(.809,.598),'GBSG':(.672,.580),'NWTCO':(.931,.950),'WHAS':(.222,.414),'SUPPORT':(.068,.147),'VLC':(.314,.600),'SAC3':(.587,.214)}
print(' D-calp aggregate 0.543 -> 0.545 (+0.002); decreased on',[k for k,(b,s) in dcal.items() if s<b],'; IBS worse on SAC3 (0.209 -> 0.240)')
print(' Table 3 "aggregate" = mean over 3 datasets (COLON, METABRIC, GBSG): ScaleMode C %.3f, NeuralSurv %.3f; abstract calls 0.648 the identical-splits aggregate'%((.639+.624+.681)/3,(.609+.559+.647)/3))
print(' Table 2: ScaleMode COLON C-index 0.639 < literature NeuralSurv 0.671 (literature = full-data training vs ScaleMode N=125)')
print('== p5 Overdamped DAVE (Table 2, ViT-B/16 | DeiT-III GridPG, EPG) ==')
print(' vanilla N=1 GridPG 48.56 | 56.22 vs vanilla N=100 41.23 | 47.15 at the same 6.76 ms vs 629.75 ms: vanilla N=1 already beats vanilla N=100 on GridPG')
print(' overdamped N=1 minus vanilla N=100: GridPG %+.2f | %+.2f ; EPG %+.2f | %+.2f'%(64.22-41.23,85.00-47.15,53.09-76.35,80.53-81.38))
print(' Table 3 identical Faith 0.7227: power-law(eta=.25) GridPG 62.95 EPG 86.09; Exponential(lambda=4) GridPG 73.96 EPG 90.15 (better on both, same faithfulness)')
print('== p6 DRO-ROCP ==')
rac=[3.379,3.192,2.667]; dro=[3.383,3.213,2.715]
print(' COVID base matrix realized loss at alpha .001/.01/.05: DRO-ROCP',dro,'RAC',rac,' -> RAC lower at all three (all 7 alphas in Table 4)')
print(' Table 2 (alpha .05, base matrix) COVID->No-Action failure: standard ROCP 10.59%, shipped DRO-ROCP 11.28%, full 9.45%; 10x matrix: all 0.00%')
print(' BDD100K alpha=0.001 empirical miscoverage: DRO-ROCP 0.0020, ROCP 0.0012, target 0.001; realized loss 4.370 vs 4.906')
