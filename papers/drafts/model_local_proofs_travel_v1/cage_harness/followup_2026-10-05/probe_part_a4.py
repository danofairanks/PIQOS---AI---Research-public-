import time, sys, json, signal
from src.gateway.governance.evidence.state_commitment import canonicalize_state
class TO(Exception): pass
def h(*a): raise TO()
signal.signal(signal.SIGALRM,h)
def t(s,cap=20):
    signal.alarm(cap); t0=time.perf_counter()
    try:
        try: canonicalize_state({"v":s}); r='ok'
        except TO: r='TIMEOUT>%ds'%cap
        except Exception as e: r=type(e).__name__
    finally: signal.alarm(0)
    return round(time.perf_counter()-t0,4), r
fam = {
 'plain_a': lambda n:"a"*n,
 'swift_labels': lambda n:"swift "*(n//6),
 'swift_slash': lambda n:"swift/bic "*(n//10),
 'swift_sep_run': lambda n:"swift"+" "*n,
 'digits': lambda n:"1"*n,
 'digit_spaces': lambda n:"4111 "*(n//5),
 'ats': lambda n:"a@"*(n//2),
 'dash_digits': lambda n:"4111-"*(n//5),
 'upper': lambda n:"A"*n,
 'bicshape_words': lambda n:"APPROVED "*(n//9),
}
R={}
for k,f in fam.items():
    row={}
    for n in (8192,16384,32768,65536,131072):
        row[n]=t(f(n))
        print(k,n,row[n],flush=True)
        if row[n][1].startswith('TIMEOUT'): break
    R[k]=row
json.dump(R,open(sys.argv[1],'w'),indent=1)
