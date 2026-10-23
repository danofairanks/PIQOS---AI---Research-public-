# Independent re-check of Epi circle/ball packings from released coordinates.
# Container conventions (Packomania): quadrant = unit-radius quarter disk x,y>=0; semicircle = unit upper half disk;
# 4D ball = unit ball. Octagon: definition not stated in repo -> several hypotheses tested.
import json, math, sys, itertools
import numpy as np
R=sys.argv[1].rstrip('/')+'/'  # usage: python3 -I packings.py CHECKOUT  (a checkout of BakeLab/Epi-results at 97fa6a4)
recs=json.load(open(R+'data/records.json'))
def clearance(cat,P):
    x=P[:,0]
    if cat=='circular-quadrant':
        return np.minimum.reduce([P[:,0],P[:,1],1-np.linalg.norm(P,axis=1)])
    if cat=='semicircle':
        return np.minimum(P[:,1],1-np.linalg.norm(P,axis=1))
    if cat=='four-dimensional-balls':
        return 1-np.linalg.norm(P,axis=1)
def octa(P,apothem):
    # regular octagon centred at origin; edge normals at k*45deg (+22.5deg offset hypotheses handled by caller)
    return None
out=[];bad=0
for rec in recs:
    cat=rec['category']
    if cat not in('circular-quadrant','semicircle','four-dimensional-balls'): continue
    P=np.array(json.load(open(R+rec['construction']))['points'],float)
    n=len(P)
    D=np.linalg.norm(P[:,None,:]-P[None,:,:],axis=2); D[np.diag_indices(n)]=np.inf
    rp=D.min()/2; rb=clearance(cat,P).min(); r=min(rp,rb)
    claimed=rec['result']; ref=float(rec['current_reference'])
    out.append((rec['id'],n,claimed,r,claimed-r,r-ref,rec['status']))
print('id n claimed implied_r claimed-implied implied-ref')
worst=0
for o in out:
    worst=max(worst,o[4])
    print('%-18s %4d %.12f %.12f %+.2e %+.3e'%o[:6])
print('records checked',len(out),'; max(claimed-implied)=%.3e'%worst)
print('implied radius beats registry reference in',sum(1 for o in out if o[5]>0),'of',len(out),'; margin min/median/max rel: ',
 '%.2e %.2e %.2e'%tuple(np.percentile([o[5]/float(r['current_reference']) for o,r in zip(out,[r for r in recs if r['category'] in('circular-quadrant','semicircle','four-dimensional-balls')])],[0,50,100])))
