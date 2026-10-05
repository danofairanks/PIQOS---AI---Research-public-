import json, time, sys, hashlib
from decimal import Decimal
from datetime import datetime, timezone
from src.gateway.governance.evidence.state_commitment import (
    canonicalize_state, verify_state_commitment, linkage_digest)
from src.gateway.governance.seams.state_commitment import StateCommitmentLinkage, STATE_COMMITMENT_METHOD
from src.gateway.governance.pii_sanitizer import _get_pii_sanitizer

R = {}
def h(x): return canonicalize_state(x)[2]
def st(x): return canonicalize_state(x)[0]

# A1
a1 = {}
a1['card']  = h({"n":"4111111111111111"}) == h({"n":"4222222222222222"})
a1['ssn']   = h({"n":"123-45-6789"}) == h({"n":"234-56-7890"})
a1['bic_labelled'] = h({"n":"BIC: DEUTDEFF"}) == h({"n":"BIC: BNPAFRPP"})
a1['email'] = h({"n":"a@example.com"}) == h({"n":"b@example.org"})
a1['control_plain'] = h({"n":"approve"}) != h({"n":"reject"})
R['A1']=a1

# A2
class O:
    def __str__(self): return "100.00"
a2={}
a2['decimal_vs_str']=h({"a":Decimal("100.00")})==h({"a":"100.00"})
a2['datetime_vs_str']=h({"a":datetime(2026,1,2,3,4,5,tzinfo=timezone.utc)})==h({"a":datetime(2026,1,2,3,4,5,tzinfo=timezone.utc).isoformat()})
a2['tuple_vs_list']=h({"a":(1,2)})==h({"a":[1,2]})
a2['obj_str_vs_str']=h({"a":O()})==h({"a":"100.00"})
a2['control_int_vs_str_differ']=h({"a":100})!=h({"a":"100"})
a2['float1_vs_int1']=h({"a":1.0})==h({"a":1})
R['A2']=a2

# A3
san=_get_pii_sanitizer()
variants = {
 'std_card':"4111 1111 1111 1111",'std_card_dash':"4111-1111-1111-1111",'std_ssn':"123-45-6789",
 'std_iban':"GB82WEST12345698765432",'std_email':"x@example.com",'std_bic_labelled':"BIC: DEUTDEFF",
 'fullwidth_card':"".join(chr(0xFF10+int(c)) if c.isdigit() else c for c in "4111 1111 1111 1111"),
 'zws_card':"4111​1111​1111​1111",
 'dot_card':"4111.1111.1111.1111",
 'spaced_iban':"GB82 WEST 1234 5698 7654 32",
 'lower_iban':"gb82west12345698765432",
 'bic_unlabelled':"route via DEUTDEFF",
 'ssn_space':"123 45 6789",
 'ssn_unicode_dash':"123–45–6789",
 'email_at_word':"x at example dot com",
 'email_fullwidth_at':"x＠example.com",
}
a3={}
for k,v in variants.items():
    out=san.sanitize(v)
    a3[k]={'in':v,'out':out,'redacted':out!=v}
# split across two items
out=san.sanitize_dict({"parts":["4111 1111","1111 1111"]})
a3['split_list_card']={'out':out,'redacted':out!={"parts":["4111 1111","1111 1111"]}}
R['A3']=a3

# A4 moved to probe_part_a4.py
# A5
L1=StateCommitmentLinkage("ns","b1","s1","t1","lbl")
L2=StateCommitmentLinkage("ns","b2","s2","t2","lbl")
state,_,sh=canonicalize_state({"k":"v"})
rec={"type":"STATE_COMMITMENT","stateHash":sh,"state":state,"linkage":L1.to_dict(),"linkageDigest":linkage_digest(L1),**STATE_COMMITMENT_METHOD}
a5={}
a5['no_linkage_arg_other_step']=verify_state_commitment(sh,json.dumps(rec))
a5['right_linkage']=verify_state_commitment(sh,json.dumps(rec),linkage=L1)
a5['wrong_linkage']=verify_state_commitment(sh,json.dumps(rec),linkage=L2)
rec2=dict(rec); rec2['callerIdentity']='spiffe://evil'
a5['callerIdentity_altered']=verify_state_commitment(sh,json.dumps(rec2),linkage=L1)
rec3=dict(rec); rec3['state']={"k":"x"}
a5['state_mutated']=verify_state_commitment(sh,json.dumps(rec3))
rec4=dict(rec); rec4['linkage']=L2.to_dict()
a5['linkage_wire_altered_digest_kept']=verify_state_commitment(sh,json.dumps(rec4),linkage=L1)
R['A5']=a5

# A6
a6={}
a6['bic_key']=san.sanitize_dict({"bic":"DEUTDEFF"})
a6['swift_code_key']=san.sanitize_dict({"swiftCode":"DEUTDEFF"})
a6['bank_key']=san.sanitize_dict({"bank":"DEUTDEFF"})
a6['dict_in_list_under_bic_key']=san.sanitize_dict({"bic":[{"v":"DEUTDEFF"}]})
a6['list_under_bic_key']=san.sanitize_dict({"bic":["DEUTDEFF"]})
R['A6']=a6

json.dump(R,open(sys.argv[1],'w'),indent=1,default=str)
print(json.dumps({k:(v if k!='A4' else '...') for k,v in R.items()},indent=1,default=str)[:6000])
