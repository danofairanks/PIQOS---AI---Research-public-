"""Profile-weighted false-clean rate (preregistered B3), from the fault-simulation aggregate in partB_agg.json.
Weights come from Table 2 of arXiv 2610.32555v1 (MCP-Injector): counts of mined failure threads per mode,
summed over the injected persistence classes (intermittent + permanent + transient; 'uncertain' excluded).
Run after partB.py (it writes partB_agg.json). Standard library only."""
import json
T2 = {  # mode: (interm, perm, trans)
    "EXPLICIT_ERROR": (669, 9075, 97), "INCORRECT_OUTPUT": (155, 1733, 1), "INVALID_OUTPUT": (47, 511, 1),
    "MINOR_MISTAKE": (15, 177, 0), "DELAYED_RESPONSE": (51, 157, 1), "SILENT_DROP": (167, 963, 4)}
tot = sum(sum(v) for v in T2.values())
w = {k: sum(v) / tot for k, v in T2.items()}
print(f"injection-profile total {tot}; " + ", ".join(f"{k} {w[k]*100:.2f}%" for k in T2))
agg = json.load(open("partB_agg.json"))
# preregistered mapping: EXPLICIT_ERROR -> F1/F2 (half each); MINOR_MISTAKE -> F7; INCORRECT_OUTPUT -> F8;
# DELAYED_RESPONSE + SILENT_DROP -> F9; INVALID_OUTPUT -> F6/F5 (post-envelope variants, half each)
M = {"EXPLICIT_ERROR": [("F1_protocol_error", .5), ("F2_payload_error", .5)], "MINOR_MISTAKE": [("F7_char_corrupt", 1)],
     "INCORRECT_OUTPUT": [("F8_word_subst", 1)], "DELAYED_RESPONSE": [("F9_silent_drop", 1)], "SILENT_DROP": [("F9_silent_drop", 1)],
     "INVALID_OUTPUT": [("F5a_key_drift_post", .5), ("F6a_zeroed_post", .5)]}
M_pre = {**M, "INVALID_OUTPUT": [("F5b_key_drift_pre", .5), ("F6b_zeroed_pre", .5)]}
def rate(mapping, who): return sum(w[m] * sum(p * agg[f][who] for f, p in fs) for m, fs in mapping.items())
for label, mp in (("preregistered mapping, transport-level faults (F5a/F6a)", M), ("same, scanner-level faults (F5b/F6b)", M_pre)):
    print(f"{label}: naive {rate(mp,'naive')*100:.2f}%   envelope {rate(mp,'env')*100:.2f}%")
