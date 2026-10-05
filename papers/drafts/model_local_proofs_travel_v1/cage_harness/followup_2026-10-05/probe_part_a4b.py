import sys, time, importlib.util, json
sys.path.insert(0,'.')
spec=importlib.util.spec_from_file_location("old", sys.argv[1]); old=importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
import src.gateway.governance.pii_sanitizer as new
R={}
def tm(f,s):
    t0=time.perf_counter(); f(s); return round(time.perf_counter()-t0,4)
for n in (4096,8192,16384):
    s="swift "*(n//6)
    R[n]={'old_sanitizer@4b116e0':tm(old.PIISanitizer().sanitize,s),
          'new_sanitizer@7e07cba':tm(new.PIISanitizer().sanitize,s),
          'new_regex_only':tm(new._BIC_LABELLED.sub if False else (lambda x:new._BIC_LABELLED.search(x)),s)}
    print(n,R[n],flush=True)
# other repeated-label shapes, regex only, n=8192
shapes={'bic bic ':"bic bic ",'swift/bic ':"swift/bic ",'swift code ':"swift code ",'swift:':"swift:",'swift_':"swift_",'single swift then spaces':None}
for k,u in shapes.items():
    if u is None: s="swift"+" "*8192
    else: s=u*(8192//len(u))
    R['shape:'+k]=tm(lambda x:new._BIC_LABELLED.search(x),s); print(k,R['shape:'+k],flush=True)
json.dump(R,open(sys.argv[2],'w'),indent=1)
