"""Executable oracle: observed behaviour of the installed libraries gives the ground-truth predicate for each doc sentence (run BEFORE any translator sees the items). Output oracle_truth.json: {item: {"args":[...], "rows":[[argvals..., 0/1], ...]}}"""
import asyncio, itertools, json, time
R={}
# L01 aiolimiter acquire: amount valid? args (amount, max_rate)
from aiolimiter import AsyncLimiter
async def aio_valid(amount,mr):
    lm=AsyncLimiter(mr,3600)
    try: await asyncio.wait_for(lm.acquire(amount),timeout=0.05); return 1
    except asyncio.TimeoutError: return 1   # accepted by validator, merely blocked
    except ValueError: return 0
R["L01"]={"args":["amount","max_rate"],"rows":[[a,m,asyncio.run(aio_valid(a,m))] for m in range(1,5) for a in range(-1,6)]}
# L02 aiolimiter: n unit acquisitions proceed without blocking? args (n, max_rate)
async def aio_nb(n,mr):
    lm=AsyncLimiter(mr,3600)
    for _ in range(n):
        try: await asyncio.wait_for(lm.acquire(1),timeout=0.05)
        except asyncio.TimeoutError: return 0
    return 1
R["L02"]={"args":["n","max_rate"],"rows":[[n,m,asyncio.run(aio_nb(n,m))] for m in range(1,5) for n in range(0,7)]}
# L03 limits FixedWindow hit: args (limit, used, cost)
from limits import parse
from limits.storage import MemoryStorage
from limits.strategies import FixedWindowRateLimiter, SlidingWindowCounterRateLimiter
rows=[]
for lim in range(1,5):
    for used in range(0,lim+1):
        for cost in range(1,lim+3):
            st=MemoryStorage(); lm=FixedWindowRateLimiter(st); it=parse(f"{lim}/hour")
            if used: assert lm.hit(it,"k",cost=used)
            rows.append([lim,used,cost,int(lm.hit(it,"k",cost=cost))])
R["L03"]={"args":["limit","used","cost"],"rows":rows}
# L09 limits sliding-window counter: args (existing, amount, limit)
rows=[]
for lim in range(1,5):
    for ex in range(0,lim+1):
        for am in range(1,lim+3):
            st=MemoryStorage(); lm=SlidingWindowCounterRateLimiter(st); it=parse(f"{lim}/hour")
            if ex: assert lm.hit(it,"k",cost=ex)
            rows.append([ex,am,lim,int(lm.hit(it,"k",cost=am))])
R["L09"]={"args":["existing","amount","limit"],"rows":rows}
# L04 token-bucket: args (requested, available)
import token_bucket as tb
rows=[]
for cap in range(1,5):
    for a in range(0,cap+1):
        for req in range(1,6):
            l=tb.Limiter(1e-12,cap,tb.MemoryStorage())
            if a: assert l.consume("k",a)
            rows.append([req,cap-a,int(l.consume("k",req))])
R["L04"]={"args":["requested","available"],"rows":sorted(set(map(tuple,rows)))}
R["L04"]["rows"]=[list(r) for r in R["L04"]["rows"]]
# L10 token-bucket capacity: args (n, capacity)
rows=[]
for cap in range(1,5):
    for n in range(1,7):
        l=tb.Limiter(1e-12,cap,tb.MemoryStorage()); rows.append([n,cap,int(l.consume("k",n))])
R["L10"]={"args":["n","capacity"],"rows":rows}
# L05/L06 ratelimit
from ratelimit import limits, RateLimitException
rows=[]
for calls in range(1,5):
    for k in range(0,7):
        @limits(calls=calls,period=3600)
        def f(): return 1
        ok=1
        for _ in range(k):
            try: f()
            except RateLimitException: ok=0;break
        rows.append([k,calls,ok])
R["L05"]={"args":["k","calls"],"rows":rows}
rows=[]
for calls in range(-1,4):
    try:
        @limits(calls=calls,period=3600)
        def g(): return 1
        g(); ok=1
    except Exception: ok=0
    rows.append([calls,ok])
R["L06"]={"args":["calls"],"rows":rows}
# L07/L08 pyrate
from pyrate_limiter import Limiter, Rate, Duration
rows=[]
for lim in range(1,5):
    for w in range(1,7):
        lm=Limiter(Rate(lim,Duration.HOUR)); ok=lm.try_acquire("k",weight=w,blocking=False); rows.append([w,lim,int(not ok)])   # never-fits on a fresh limiter
R["L07"]={"args":["weight","limit"],"rows":rows}
rows=[]
for lim in range(1,5):
    for n in range(0,7):
        lm=Limiter(Rate(lim,Duration.HOUR)); ok=1
        for _ in range(n):
            if not lm.try_acquire("k",weight=1,blocking=False): ok=0;break
        rows.append([n,lim,ok])
R["L08"]={"args":["n","limit"],"rows":rows}
json.dump(R,open("oracle_truth.json","w"))
# summarise each oracle as the simple rule it satisfies (sanity)
rules={"L01":lambda a,m:0<=a<=m,"L02":lambda n,m:n<=m,"L03":lambda l,u,c:u+c<=l,"L09":lambda e,a,l:e+a<=l,"L04":lambda r,a:r<=a,"L10":lambda n,c:n<=c,"L05":lambda k,c:k<=c,"L06":lambda c:c>0,"L07":lambda w,l:w>l,"L08":lambda n,l:n<=l}
for k,f in rules.items():
    bad=[r for r in R[k]["rows"] if bool(f(*r[:-1]))!=bool(r[-1])]
    print(k,"rows",len(R[k]["rows"]),"rule-mismatch",len(bad),bad[:4])
