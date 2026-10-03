#!/usr/bin/env python3
"""Clone the pinned commits, run the attack scripts, check the qualitative expectations.
Usage: python3 run_all.py [workdir]    (needs git and network; Python 3.10+; stdlib only)
Threaded results are timing-dependent: the two race checks are retried up to three times.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "work")
REPOS = {}
for line in open(os.path.join(HERE, "PINS.txt")):
    if line.startswith("#") or not line.strip() or "(" in line.split("  ")[-1] and "original" in line:
        continue
    parts = line.split()
    REPOS[parts[0].rsplit("/", 1)[1]] = (parts[0], parts[1])


def sh(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout


def clone(name):
    url, sha = REPOS[name]
    dest = os.path.join(WORK, name)
    if not os.path.isdir(dest):
        sh("git", "clone", "--quiet", url + ".git", dest)
    sh("git", "checkout", "--quiet", sha, cwd=dest)
    return dest


def run(script, *args):
    out = subprocess.run([sys.executable, os.path.join(HERE, script), *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"{script} failed:\n{out.stderr}")
    return json.loads(out.stdout)


def check(cond, msg, fails):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


def main():
    os.makedirs(WORK, exist_ok=True)
    paths = {n: clone(n) for n in ("no-direct-bind", "ndb-gate", "commit-gate-core", "stop-machine")}
    fails = []
    # ndb-gate and the no-direct-bind witness
    for name, args in (("ndb-gate", [paths["ndb-gate"] + "/src"]),
                       ("no-direct-bind", [paths["no-direct-bind"] + "/witness/src", paths["no-direct-bind"] + "/proof"])):
        for attempt in range(3):
            r = run("attacks_ndb_generic.py", *args)
            if r["A5_concurrent_single_use"]["attack_threaded_trials_with_double_effect_of_300"] > 0:
                break
        a = r
        check(a["A1_forged_PROVED_label"]["control_self_labelled_weak"][0] == "HOLD" and a["A1_forged_PROVED_label"]["attack_self_labelled_PROVED"][0] == "ALLOW", f"{name} A1 forged evidence class", fails)
        check(a["A2_replay_by_copy"]["control_same_object_second_use"] == "DENY" and a["A2_replay_by_copy"]["attack_copy_second_use"] == "ALLOW", f"{name} A2 replay by value-equal copy", fails)
        check(a["A3_caller_supplied_clock"]["control_expired_real_clock"] == "HOLD" and a["A3_caller_supplied_clock"]["attack_now_param"] == "ALLOW", f"{name} A3 caller-supplied clock", fails)
        c = a["A4_receipt_chain"]
        check((not c["control_partial_edit_verifies"]) and c["attack_full_rewrite_verifies"] and c["attack_fabricated_chain_verifies"], f"{name} A4 receipt chain rewrite", fails)
        c = a["A5_concurrent_single_use"]
        check(c["control_sequential_trials_with_double_effect_of_300"] == 0 and c["attack_threaded_trials_with_double_effect_of_300"] > 0, f"{name} A5 concurrent single use", fails)
        check(a["A7_allow_receipt_without_effect"]["last_outcome"] == "ALLOW", f"{name} A7 ALLOW receipt without effect", fails)
        if "A6_model_with_revocation_between_check_and_effect" in a:
            m = a["A6_model_with_revocation_between_check_and_effect"]
            check(m["original_invariant_holds"] and not m["authority_present_at_execution_invariant_holds"], f"{name} A6 invariant holds, authority-at-execution does not", fails)
    # commit-gate-core
    r = run("attacks_cgc.py", paths["commit-gate-core"])
    check(r["C1_forgery"]["control_stale_signature"] == "DENY:INVALID_SIGNATURE" and r["C1_forgery"]["control_wrong_key"] == "DENY:INVALID_SIGNATURE" and r["C1_forgery"]["key_holder_mints_arbitrary_scope"] == "AUTHORIZED", "commit-gate-core C1 forgery needs the key; a key holder mints", fails)
    check(r["C2_replay"]["control_second_same_ledger"] == "DENY:NONCE_REPLAYED" and r["C2_replay"]["two_ledgers_second"] == "AUTHORIZED", "commit-gate-core C2 replay denied per ledger only", fails)
    check(r["C3_expiry"]["control_expired_record"] == "DENY:DECISION_EXPIRED" and r["C3_expiry"]["ticket_carries_expired_window_and_nothing_refuses_use"], "commit-gate-core C3 expiry enforced; ticket not execution authority", fails)
    check((not r["C4_receipt_hash_check"]["control_edited_without_rehash"]) and r["C4_receipt_hash_check"]["fabricated_receipt_with_recomputed_hash"], "commit-gate-core C4 receipt hash check is integrity only", fails)
    c = r["C5_concurrent_nonce"]
    check(c["control_sequential_trials_with_double_authorization_of_300"] == 0 and c["attack_threaded_trials_with_double_authorization_of_300"] == 0, "commit-gate-core C5 no double authorization under threads", fails)
    check(not r["C6_payload_snapshot"]["ticket_hash_matches_bytes_now_held"], "commit-gate-core C6 payload snapshot not re-checked after authorization", fails)
    check(r["C7_audit_failure"]["rollback_fails"][0].startswith("ERROR:AUTH_AUDIT_FAILED_ROLLBACK_FAILED") and r["C7_audit_failure"]["rollback_fails"][1] == ["nonce_001"], "commit-gate-core C7 rollback failure burns the nonce", fails)
    m = r["C8_malformed_calls"]
    check(m["payload_is_str"].get("raised") == "TypeError" and m["payload_is_str"]["audit_events_added"] == 0 and m["control_missing_field"]["audit_events_added"] == 1, "commit-gate-core C8 wrong-type arguments raise without an audit event", fails)
    c = r["C9_unauthenticated_fields_in_audit"]
    check(c["audit_decision_id"] == "dr_victim_77" and not c["nonce_consumed"], "commit-gate-core C9 unauthenticated ids reach refusal events", fails)
    check(r["C10_scope_string_variants"]["trailing_space_object_id"] == "DENY:SCOPE_MISMATCH:object_id", "commit-gate-core C10 string variants refused", fails)
    # stop-machine
    for attempt in range(3):
        r = run("attacks_stop_machine.py", paths["stop-machine"], "20000")
        if r["SM3_race_advance_vs_reset"]["threaded_trials_ending_GREEN"] > 0:
            break
    check(r["SM1_SM2_write_paths"]["control_public_assignment"] == "AttributeError" and r["SM1_SM2_write_paths"]["_set_private_method_from_RED"] == "GREEN", "stop-machine SM-1 private _set leaves RED", fails)
    check(r["SM3_race_advance_vs_reset"]["control_sequential_final_states"] == {"advance_then_reset": "RED", "reset_then_advance": "AMBER"} and r["SM3_race_advance_vs_reset"]["threaded_trials_ending_GREEN"] > 0, "stop-machine SM-3 race ends GREEN through public methods", fails)
    check(r["SM4_transition_table_poke"]["after_poke_three_advances"] == ["AMBER", "GREEN", "AMBER"], "stop-machine SM-4 transition table poke", fails)
    check(all(v == "AttributeError" for v in r["SM5_copy_pickle_of_RED"].values()), "stop-machine SM-5 halt state cannot be copied or pickled", fails)
    g = r["SG1_plural_and_synonyms"]
    check(g["control_singular"] == "DENY" and g["ignore previous instructions"] == "ALLOW", "stop-machine SG-1 plural form of the canonical phrase passes", fails)
    check(r["SG2_newline"]["newline_between_words"] == "ALLOW" and r["SG3_zero_width"]["zero_width_in_word"] == "ALLOW", "stop-machine SG-2/3 newline and zero-width evasion", fails)
    check(r["SG4_self_supplied_authority"]["control_no_flags"] == "HOLD" and r["SG4_self_supplied_authority"]["authority_present_and_allow_rotation_set_by_caller"] == "ALLOW", "stop-machine SG-4 authority is a caller flag", fails)
    check(r["SG5_statelessness"]["first_stop_state"] == "RED" and r["SG5_statelessness"]["next_clean_verdict"] == "ALLOW", "stop-machine SG-5 receipt stop_state does not persist", fails)
    check(r["AS1_caller_supplied_clock"]["control_honest_attempted_at"] == "authority.expired" and r["AS1_caller_supplied_clock"]["attempted_at_set_before_expiry"] == "ALLOW", "stop-machine AS-1 caller-supplied clock", fails)
    check(r["AS2_self_reported_flags"]["control_state_flag_false"] == "HOLD" and r["AS2_self_reported_flags"]["all_flags_true_nothing_verified"] == "ALLOW", "stop-machine AS-2 self-reported flags", fails)
    e = r["EG1_self_declared_sender"]
    check(e["control_agent_sender"][0] == "HOLD" and e["sender_declared_HUMAN"][0] == "ALLOW", "stop-machine EG-1 self-declared sender", fails)
    check(r["EG2_duplicate_fields"]["scope_values_present_in_raw_text"] == ["NON_EXEC", "EXEC_CONFIRMED"] and r["EG2_duplicate_fields"]["gate_parsed_scope_with_two_lines"] == "NON_EXEC", "stop-machine EG-2 duplicate fields parse first", fails)
    print(f"\n{'ALL CHECKS PASS' if not fails else str(len(fails)) + ' CHECK(S) FAILED'}")
    sys.exit(1 if fails else 0)


main()
