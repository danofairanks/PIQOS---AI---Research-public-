import asyncio, json, sys, random, copy
import os; sys.path.insert(0, os.environ.get("RESEARCH_MCP_DIR", "../../../tools/research_mcp"))
from tests.conftest import _live_session
exec(open("partA.py").read().split("def summarize")[0])
SEED=20261027; N=200
# per-tool: count findings in a parsed response; zero it; drift (rename) findings key
def c_bifp(o): return sum(1 for v in o.values() if isinstance(v,dict) and v.get("flagged"))
def z_bifp(o):
    for v in o.values():
        if isinstance(v,dict) and "flagged" in v: v["flagged"]=False
def d_bifp(o):
    for k in list(o):
        if isinstance(o[k],dict): o["x_"+k]=o.pop(k)
SPEC={
 "bifp_scan_text":(c_bifp,z_bifp,d_bifp),
 "bifp_scan_hardcoded_assertion_style":(lambda o:len(o.get("matches",[])),lambda o:o.update(matches=[]),lambda o:o.update(match_list=o.pop("matches"))),
 "attractor_scan_text":(lambda o:len(o.get("flagged_maneuvers",[]))+len(o.get("flagged_laundering_cases",[])),lambda o:o.update(flagged_maneuvers=[],flagged_laundering_cases=[]),lambda o:(o.update(flagged_m=o.pop("flagged_maneuvers")),o.update(flagged_l=o.pop("flagged_laundering_cases")))),
 "rigor_cosplay_scan_text":(lambda o:len(o.get("signatures_hit",[])),lambda o:o.update(signatures_hit=[],any_signature_flagged=False),lambda o:o.update(sigs=o.pop("signatures_hit"))),
 "hedge_dogwhistle_scan_text":(lambda o:len(o.get("matches",[])),lambda o:o.update(matches=[]),lambda o:o.update(match_list=o.pop("matches"))),
 "paper_rigor_scan":(lambda o:int(o.get("total_gap_count",0)),lambda o:o.update(total_gap_count=0,structural_gap_count=0,ok=True),lambda o:o.update(gaps=o.pop("total_gap_count"))),
}
# R_naive: clean iff parses as JSON dict, no 'error' key, and findings (as extracted by the tool's own count fn) == 0 / key missing
def r_naive(raw, tool):
    if raw is None: return "unknown"
    try: o=json.loads(raw)
    except Exception: return "unknown"
    if not isinstance(o,dict): return "unknown"
    if "error" in o: return "unknown"
    try: n=SPEC[tool][0](o)
    except Exception: n=0   # missing/odd shape -> naive reads as no findings
    return "clean" if not n else "flagged"
RULES={t:None for t in SPEC}  # filled from clean-run structure
def envelope(tool, text, o):
    return {"ok":"error" not in o,"tool":tool,"schema_version":1,"scanned_chars":len(text),"rules_evaluated":RULES[tool],"n_findings":SPEC[tool][0](o),"result":o}
def r_env(raw, tool, sent_len):
    if raw is None: return "unknown"
    try: e=json.loads(raw)
    except Exception: return "unknown"
    if not isinstance(e,dict): return "unknown"
    need=("ok","tool","schema_version","scanned_chars","rules_evaluated","n_findings","result")
    if any(k not in e for k in need): return "unknown"
    if e["ok"] is not True or e["tool"]!=tool or e["schema_version"]!=1 or e["scanned_chars"]!=sent_len or not e["rules_evaluated"]: return "unknown"
    return "clean" if e["n_findings"]==0 else "flagged"
def f7(s,rng,p=0.05):
    cs=list(s)
    for i in range(len(cs)):
        if rng.random()<p: cs[i]=chr(rng.randint(33,126))
    return "".join(cs)
def f8(s,rng,p=0.10):
    w=s.split(" "); pool=[x for x in w if x]
    return " ".join(rng.choice(pool) if rng.random()<p else x for x in w)
def faults(base_obj, tool, text, mode):
    """mode 'naive' faults act on the bare response; 'env' faults act on the enveloped response. returns dict fault->list of raw strings (None=timeout/no payload)"""
    cp=lambda: copy.deepcopy(base_obj)
    rng=random.Random(SEED)
    def wrap(o): return envelope(tool,text,o) if mode=="env" else o
    out={}
    out["F1_protocol_error"]=[None]
    out["F2_payload_error"]=[json.dumps({"error":"upstream failure"})]
    out["F3_empty_object"]=["{}"]
    out["F4_empty_text"]=["", "null"]
    d=cp(); SPEC[tool][2](d) if mode=="naive" else None
    if mode=="env":
        e=wrap(cp()); SPEC[tool][2](e["result"]); out["F5a_key_drift_post"]=[json.dumps(e)]   # drift inside the result, envelope intact
        d=cp(); SPEC[tool][2](d); out["F5b_key_drift_pre"]=[json.dumps(wrap(d))]               # scanner returned drifted shape; envelope computed on it
        e=wrap(cp()); SPEC[tool][1](e["result"]); out["F6a_zeroed_post"]=[json.dumps(e)]       # result zeroed, envelope n_findings untouched
        d=cp(); SPEC[tool][1](d); out["F6b_zeroed_pre"]=[json.dumps(wrap(d))]                  # scanner returned zeroed; envelope computed on it
    else:
        out["F5a_key_drift_post"]=out["F5b_key_drift_pre"]=[json.dumps(d)]
        z=cp(); SPEC[tool][1](z); out["F6a_zeroed_post"]=out["F6b_zeroed_pre"]=[json.dumps(z)]
    base=json.dumps(wrap(cp()))
    out["F7_char_corrupt"]=[f7(base,rng) for _ in range(N)]
    out["F8_word_subst"]=[f8(base,rng) for _ in range(N)]
    out["F9_silent_drop"]=[None]
    out["F10_truncated"]=[base[:rng.randint(1,len(base)-1)] for _ in range(N)]
    return out
async def main():
    res={}; shapes={}
    async with _live_session() as s:
        for t in SPEC:
            r=await s.call_tool(t,{"text":CLEAN}); RULES[t]=len(json.loads(r.content[0].text))  # prototype: top-level rule groups seen on a clean run
            r=await s.call_tool(t,{"text":FLAGGED}); base=json.loads(r.content[0].text)
            gt=SPEC[t][0](base)
            if gt==0: res[t]="EXCLUDED (known-flagged text yields 0 findings: recall, not failure semantics)"; continue
            row={"ground_truth_findings":gt}
            for mode,fn in (("naive",lambda raw:r_naive(raw,t)),("env",lambda raw:r_env(raw,t,len(FLAGGED)))):
                fs=faults(base,t,FLAGGED,mode)
                for f,raws in fs.items():
                    # a fault is applied; client decides. false-clean = says 'clean' while findings exist
                    row.setdefault(f,{})[mode]=sum(fn(x)=="clean" for x in raws)/len(raws)
                # no-fault control
                ctl=json.dumps(envelope(t,FLAGGED,base)) if mode=="env" else json.dumps(base)
                row.setdefault("CONTROL_nofault",{})[mode]=fn(ctl)
            res[t]=row
    json.dump(res,open("partB_results.json","w"),indent=1,default=str)
    ok=[t for t,v in res.items() if isinstance(v,dict)]
    print("tools in sim:",ok); print({t:v for t,v in res.items() if not isinstance(v,dict)})
    fl=["F1_protocol_error","F2_payload_error","F3_empty_object","F4_empty_text","F5a_key_drift_post","F5b_key_drift_pre","F6a_zeroed_post","F6b_zeroed_pre","F7_char_corrupt","F8_word_subst","F9_silent_drop","F10_truncated","CONTROL_nofault"]
    print("%-20s %8s %8s"%("fault","naive","env"))
    agg={}
    for f in fl:
        for m in("naive","env"):
            vals=[res[t][f][m] for t in ok]
            agg.setdefault(f,{})[m]=(sum(vals)/len(vals)) if not isinstance(vals[0],str) else vals[0]
        print("%-20s %8s %8s"%(f,agg[f]["naive"] if isinstance(agg[f]["naive"],str) else "%.3f"%agg[f]["naive"],agg[f]["env"] if isinstance(agg[f]["env"],str) else "%.3f"%agg[f]["env"]))
    # profile weighting (post-hoc weights; mapping stated in RESULTS.md)
    W={"F1_protocol_error":.328,"F2_payload_error":.328,"F6a_zeroed_post":.0955,"F5a_key_drift_post":.0955,"F9_silent_drop":.097,"F7_char_corrupt":.028,"F8_word_subst":.028}
    for m in ("naive","env"):
        print("profile-weighted false-clean",m,"%.4f"%sum(w*agg[f][m] for f,w in W.items()))
    json.dump(agg,open("partB_agg.json","w"),indent=1)
    print({t:RULES[t] for t in RULES})
asyncio.run(main())
