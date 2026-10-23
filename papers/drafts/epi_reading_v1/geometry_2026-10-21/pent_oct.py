import json, math, itertools, sys
import numpy as np
R=sys.argv[1].rstrip('/')+'/'  # usage: python3 -I pent_oct.py CHECKOUT
recs=json.load(open(R+'data/records.json'))
Rp=1/(2*math.sin(math.pi/5))
def verts(x,y,a):
    k=np.arange(5); t=a+math.pi/10+2*math.pi*k/5
    return np.stack([x+Rp*np.cos(t),y+Rp*np.sin(t)],1)
def axes(V):
    e=np.roll(V,-1,0)-V; n=np.stack([e[:,1],-e[:,0]],1); return n/np.linalg.norm(n,axis=1)[:,None]
def sep(V,W):
    best=-1e9
    for A in (axes(V),axes(W)):
        for n in A:
            pv=V@n; pw=W@n
            gap=max(pw.min()-pv.max(), pv.min()-pw.max())   # >0 separated, <0 overlap along this axis
            best=max(best,gap)
    return best   # = -(min penetration depth) if overlapping
def tri_side(P):
    best=1e9
    for sgn in (1,-1):
        ns=[np.array([0,-1.0]),np.array([math.sqrt(3)/2,.5]),np.array([-math.sqrt(3)/2,.5])]
        h=sum((sgn*P)@ (sgn*n)*0 for n in ns) if False else None
        hs=[(P@(sgn*n)).max() for n in ns]
        best=min(best,2*sum(hs)/math.sqrt(3))
    return best
print('PENTAGONS')
for r in recs:
    if r['category']!='pentagons': continue
    pc=json.load(open(R+r['construction']))['pieces']
    Vs=[verts(*p) for p in pc]; n=len(Vs)
    worst=-1e9
    for i,j in itertools.combinations(range(n),2):
        worst=max(worst,sep(Vs[i],Vs[j]))   # want >= -1e-12 for every pair
    # worst over pairs of the (max separating gap); overlap if gap<0; tolerance means gap>=-1e-12
    allv=np.vstack(Vs); side=tri_side(allv)
    mingap=min(sep(Vs[i],Vs[j]) for i,j in itertools.combinations(range(n),2))
    print('%-14s n=%2d min pair gap %+.2e  implied side %.12f claimed %.12f diff %+.2e  listed %s'%(r['id'],n,mingap,side,r['result'],side-r['result'],r['current_reference']))
print('OCTAGON')
r=[x for x in recs if x['category']=='octagon'][0]
P=np.array(json.load(open(R+r['construction']))['points'],float); n=len(P)
D=np.linalg.norm(P[:,None]-P[None],axis=2); D[np.diag_indices(n)]=np.inf; rp=D.min()/2
for name,off in (('vertices on axes',0.0),('flats on axes',math.pi/8)):
    # edge normals at off+pi/8+k pi/4 for vertex-on-axis (off=0); apothem cos(pi/8)
    nr=[(off+math.pi/8)+k*math.pi/4 for k in range(8)] if off==0 else [k*math.pi/4 for k in range(8)]
    ap=math.cos(math.pi/8)
    cl=min((ap-(P@np.array([math.cos(t),math.sin(t)]))).min() for t in nr)
    print('%-18s boundary clearance %.15f pair r %.15f implied r %.15f claimed %.15f'%(name,cl,rp,min(cl,rp),r['result']))
