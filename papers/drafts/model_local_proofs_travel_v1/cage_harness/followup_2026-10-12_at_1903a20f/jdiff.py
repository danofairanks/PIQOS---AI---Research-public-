import json,sys,re
def walk(a,b,path,out):
    if isinstance(a,dict) and isinstance(b,dict):
        for k in sorted(set(a)|set(b)):
            if k not in a: out.append((path+"/"+k,"<absent>",json.dumps(b[k],default=str)[:160]))
            elif k not in b: out.append((path+"/"+k,json.dumps(a[k],default=str)[:160],"<absent>"))
            else: walk(a[k],b[k],path+"/"+k,out)
    elif isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,f"{path}[{i}]",out)
    elif a!=b: out.append((path,json.dumps(a,default=str)[:160],json.dumps(b,default=str)[:160]))
old=json.load(open(sys.argv[1])); new=json.load(open(sys.argv[2])); out=[]; walk(old,new,"",out)
vol=re.compile(r"(time|elapsed|_s$|_ms$|seconds|nonce|jti|iat|exp|ts$|timestamp|sig|hash|digest|id$)",re.I)
real=[o for o in out if not vol.search(o[0].split("/")[-1])]
print(f"{sys.argv[2].split('/')[-1]}: {len(out)} differing leaves, {len(real)} non-volatile")
for p,a,b in real[:25]: print("  ",p,"\n      old:",a,"\n      new:",b)
