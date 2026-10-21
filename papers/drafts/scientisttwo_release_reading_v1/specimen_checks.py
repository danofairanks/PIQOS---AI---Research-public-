# E1 arithmetic on tables transcribed from the generated paper "Fisher Channel-Damped Engram" (16 pp; page refs in README).
rows={ # Table 1: Overall, Mem, Util, Priv, EM, FQ
'Gold Retain90':(0.998,1.000,0.994,1.000,0.000,0.000),'GradDiff':(0.227,0.185,0.993,0.147,0.718,-15.83),
'RMU':(0.757,0.866,0.747,0.680,0.295,-0.236),'IDK-DPO':(0.889,0.953,0.966,0.775,0.116,-1.186),
'NPO':(0.944,0.934,0.950,0.948,0.095,-1.999),'SimNPO':(0.945,0.944,0.971,0.923,0.104,-0.090),
'AltPO':(0.955,0.925,0.986,0.955,0.095,-0.742),'Task Arithmetic':(0.584,0.900,0.678,0.392,0.128,None),
'RECE':(0.420,0.831,0.238,0.574,0.330,-0.613),'LEACE-style':(0.438,0.814,0.816,0.228,0.192,-7.972),
'Engram Plain (human baseline)':(0.705,0.922,0.871,0.495,0.004,-0.551),'ZeroUnlearn':(0.767,0.978,0.630,0.767,0.044,-0.003),
'Engram Adaptive':(0.860,0.932,0.894,0.771,0.156,-0.381),'UCE':(0.851,0.918,0.870,0.778,0.191,-0.811),
'FCD-Engram':(0.916,0.969,0.926,0.860,0.071,-0.001)}
hm=lambda a,b,c:3/(1/a+1/b+1/c)
print('Overall vs harmonic mean of (Mem,Util,Priv); EM and FQ do not enter:')
for k,v in rows.items():
    h=hm(v[1],v[2],v[3]); print('  %-30s reported %.3f  HM %.3f  diff %+.3f'%(k,v[0],h,h-v[0]))
ems=sorted((v[4],k) for k,v in rows.items() if k!='Gold Retain90')
print('Lowest EM among evaluated methods (excluding Gold):',ems[:4])
print('FCD EM / Engram Plain EM = %.1fx worse (lower is better)'%(0.071/0.004))
print('Overall gain of FCD over human baseline Engram Plain: %+.3f (%.1f%%); over Engram Adaptive: %+.3f (%.1f%%)'%(0.916-0.705,100*(0.916/0.705-1),0.916-0.860,100*(0.916/0.860-1)))
print('Table 11 decomposition of +0.211: adaptive scaling alone +%.3f (%.0f%% of gain); damping on top of adaptive scaling +%.3f (%.0f%%); damping alone on plain %+.3f'%(0.860-0.705,100*(0.860-0.705)/0.211,0.916-0.860,100*(0.916-0.860)/0.211,0.636-0.705))
print('Table 5 vs Table 9: "Channel damping only (gamma=0.5, lambda=0)" 0.880 and "Baseline (no ridge, gamma=0)" 0.860 at alpha=1.1;')
print('  Table 9 "Unregularized pinv (lambda=0, eps=0)" at its BEST alpha (1.2) = 0.761 < both; a config at its best alpha cannot score below the same config at alpha=1.1 unless settings differ (unreported).')
print('WMDP (Table 3b): fraction of base->chance forgetting achieved on Avg (base 0.598, chance 0.250):')
for k,a in (('Engram (cov.)',0.258),('UCE',0.266),('FCD',0.280)): print('  %-14s %.1f%%'%(k,100*(0.598-a)/(0.598-0.250)))
print('Table 2 units: 74.4P with P=1.24e9 -> %.3e (table says 9.2e16); 2.5P -> %.3e (table says 3.1e15); factor 1e6 unstated'%(74.4*1.24e9,2.5*1.24e9))
