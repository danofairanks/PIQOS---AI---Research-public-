import asyncio, base64, json, os, sys, time, unicodedata
from decimal import Decimal
from datetime import datetime, timezone
from src.gateway.governance.jcs_canonicalizer import jcs_canonicalize_plan
R={}
def canon(x):
    try: return ('ok', jcs_canonicalize_plan(x).decode('utf-8','replace'))
    except Exception as e: return ('raises', type(e).__name__+': '+str(e)[:80])
# ---- Part C
C={}
C['C1_nan']=canon({"a":float('nan')}); C['C1_inf']=canon({"a":float('inf')}); C['C1_control_finite']=canon({"a":1.5})
a=canon({"a":9007199254740993}); b=canon({"a":9007199254740992}); C['C2_bigints']={'a':a,'b':b,'equal':a==b}
a=canon({"a":1.0}); b=canon({"a":1}); C['C3_1.0_vs_1']={'a':a,'b':b,'equal':a==b}
a=canon({"a":-0.0}); b=canon({"a":0}); C['C4_negzero_vs_0']={'a':a,'b':b,'equal':a==b}
a=canon({1:"a"}); b=canon({"1":"a"}); C['C5_nonstr_key']={'int_key':a,'str_key':b,'equal':a==b}
class O:
    def __str__(self): return "x"
for name,v in [('Decimal',Decimal("1.5")),('datetime',datetime(2026,1,1,tzinfo=timezone.utc)),('set',{1,2}),('bytes',b"ab"),('object',O()),('tuple',(1,2))]:
    C['C6_'+name]=canon({"a":v})
C['C6_control_str_vs_dict']=canon({"a":"x"})!=canon({"a":{"b":"x"}})
C['C8_nfc_vs_nfd_differ']=canon({"a":unicodedata.normalize('NFC','é')})!=canon({"a":unicodedata.normalize('NFD','é')})
R['C']=C
# ---- Part P (construction/posture)
from src.integrations.provider_07.adapter import Provider07NormativeProvider
from src.integrations.provider_07.jwks_client import Provider07JwksClient
from src.gateway.governance.env_posture import resolve_posture, is_enforcing
P1={}
vals=[None,"","production","PROD","prod","Production","production ","staging","stage","uat","preprod","prd","live","development","test"]
for v in vals:
    for k in ("CAGE_ENV","ENVIRONMENT"): os.environ.pop(k,None)
    if v is not None: os.environ["CAGE_ENV"]=v
    row={}
    try: Provider07NormativeProvider("http://x",allow_step1_unsigned=True); row['unsigned_flag']='constructs'
    except RuntimeError: row['unsigned_flag']='refused'
    try: Provider07NormativeProvider("http://x",allow_step1_unsigned=False); row['flag_off']='constructs'
    except Exception as e: row['flag_off']='raises '+type(e).__name__
    row['central_posture']=resolve_posture().value; row['central_enforcing']=is_enforcing()
    P1[repr(v)]=row
for k in ("CAGE_ENV","ENVIRONMENT"): os.environ.pop(k,None)
R['P1']=P1
# P4
P4={}
try: Provider07JwksClient("http://insecure.example/jwks.json"); P4['http_url_accepted']=True
except Exception as e: P4['http_url_accepted']=False; P4['err']=str(e)[:80]
ad=Provider07NormativeProvider("https://svc.example")
P4['default_jwks_url']=ad._jwks_client._jwks_url
R['P4']=P4
json.dump(R,open(sys.argv[1],'w'),indent=1,default=str)
print(json.dumps(R,indent=1,default=str)[:7000])
