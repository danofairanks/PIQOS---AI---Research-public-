#!/usr/bin/env python3
"""Clone the pinned commits, run the Node attack script, check the qualitative expectations.
Usage: python3 run_all.py [workdir]   (needs git, network, Node 22+ for the TypeScript check; Python 3.10+; stdlib only)
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "work")
REPOS = {}
for line in open(os.path.join(HERE, "PINS.txt")):
    if line.startswith("#") or not line.strip():
        continue
    p = line.split()
    REPOS[p[0].rsplit("/", 1)[1]] = (p[0], p[1])

def sh(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout

def clone(name):
    url, sha = REPOS[name]
    dest = os.path.join(WORK, name)
    if not os.path.isdir(dest):
        sh("git", "clone", "--quiet", url + ".git", dest)
    sh("git", "checkout", "--quiet", sha, cwd=dest)

def check(cond, msg, fails):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)

def main():
    os.makedirs(WORK, exist_ok=True)
    for n in REPOS:
        clone(n)
    r = subprocess.run(["node", os.path.join(HERE, "attacks_public_evaluators.js"), WORK], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("attack script failed:\n" + r.stderr)
    o = json.loads(r.stdout)
    fails = []
    ok = lambda d: d["outcome"] == "stable" and d["admissible"] and d["action"] == "allow"
    check(ok(o["H1_controls"]["consistent"]) and o["H1_controls"]["claims_valid_observed_revoked"]["outcome"] == "blocked", "H1 controls: consistent allows; 'revoked' observation blocks", fails)
    p = o["H2_paraphrases"]
    check(all(ok(v) for k, v in p.items() if k != "the NDA is revoked") and p["the NDA is revoked"]["outcome"] == "blocked", "H2 eight paraphrases of ended standing pass; 'revoked' blocks", fails)
    check(o["H3_negation"]["outcome"] == "blocked", "H3 'has not been revoked' blocks (false positive)", fails)
    check(ok(o["H4_claims_without_term"]["claim_in_place_obs_revoked"]) and o["H4_claims_without_term"]["control_claim_valid_obs_revoked"]["outcome"] == "blocked", "H4 claim without a listed term bypasses the contradiction check", fails)
    f = o["H5_freshness"]
    check(f["control_stale_after_1"]["stale"] and ok(f["stale_after_omitted"]) and ok(f["stale_after_0"]), "H5 caller-chosen freshness window disables staleness", fails)
    a = o["H6_authority_flags"]
    check(ok(a["top_level"]) and a["authority_risk"]["revoked"] and a["authority_risk"]["expired"] and a["escalation_required"] and ok(a["control_no_authority_flags"]) and a["control_revoked_text_in_observation"]["outcome"] == "blocked", "H6 revoked/expired authority flags do not change the top-level decision", fails)
    check(o["H6_guard"]["executed"] and o["H6_guard"]["effects"] == 1, "H6 guard executes the effect for a revoked-flag packet", fails)
    g = o["H7_gap"]
    check(g["gap_case_executed"] and g["registry_active_at_effect"] is False and g["control_revoked_before_evaluate_executed"] is False, "H7 revocation between evaluate and effect is not caught; control withheld", fails)
    h = o["H8_receipt"]
    check(h["hash_recomputable_from_receipt"] and h["forged_stable_allow_receipt_executed"] and not h["control_wrong_packet_id_executed"] and not h["control_public_release_false_executed"], "H8 receipt hash is recomputable; forged receipt accepted; controls rejected", fails)
    x = o["H9_self_declared"]
    check(ok(x["all_x"]) and ok(x["evidence_empty_string_no_observations"]) and ok(x["evidence_zero_no_observations"]) and x["control_no_evidence_no_observations"]["outcome"] == "degraded", "H9 self-declared fields satisfy completeness; empty evidence counts", fails)
    v = o["H10_V114_runnable"]
    check(v["exit"] != 0 and v["missing_module"] and not v["secure_execution_file_in_api"], "H10 preserved V114 test cannot run in the public repository (disclosed)", fails)
    r1 = o["R1_status_and_lexical"]
    check(r1["control_valid"]["admissible"] and r1["status_terminated"]["admissible"] and r1["status_withdrawn"]["admissible"] and r1["signal_terminated"]["admissible"] and not r1["control_status_revoked"]["admissible"] and "runtime_state_contradiction" in r1["control_signal_revoked"]["codes"], "R1 status values and wording outside the lists pass; controls fail", fails)
    r2 = o["R2_invalid_timestamps"]
    check(not r2["control_expired_iso"]["admissible"] and r2["expires_at_unparseable"]["admissible"] and "state_freshness_expired" in r2["control_stale_iso"]["codes"] and r2["last_verified_unparseable"]["admissible"] and o["R2_harmonic_invalid_timestamp_for_contrast"]["codes"] is True, "R2 unparseable timestamps are treated as current; the other evaluator flags them", fails)
    s1, s2 = o["S1_authority_continuity_stub"], o["S2_consequence_boundary_stub"]
    check(s1["revoked_packet"] == s1["empty_body"] and s1["revoked_packet"]["decision"] == "ALLOW" and s2["revoked_packet"] == s2["empty_body"], "S1/S2 two api/evaluate.js files return constant responses", fails)
    fz = o["F1_solaceframe_computeAdmission"]
    check(fz["one_60"] == "admitted" and fz["one_59"] == "review" and fz["one_0"] == "rejected" and fz["two_80"] == "admitted", "F1 mean-based admission admits one weak dimension of 60", fails)
    n = o["N1_surfaces"]
    check(all(v["code_files"] == ["app/layout.tsx", "app/page.tsx"] and not v["api_dir"] for v in n.values()), "N1 three repositories are static web surfaces", fails)
    # B1: registry-bound counter-model toy (stdlib; also reruns four defeat inputs against the public guard)
    b = subprocess.run(["node", os.path.join(HERE, "b1_registry_bound_guard.js"), WORK], capture_output=True, text=True)
    if b.returncode != 0:
        raise SystemExit("b1 script failed:\n" + b.stderr)
    t = json.loads(b.stdout)
    check(t["control_honest"]["executed"] and t["control_honest"]["effects"] == 1, "B1 control: honest path executes once", fails)
    w = t["A_words"]
    check(w["registry_revoked_host_says_valid"]["decision"] == "deny" and not w["registry_revoked_host_says_valid"]["executed"] and all(v["decision"] == "allow" for k, v in w.items() if k.startswith("registry_active_host_text")), "B1 words: the registry decides; host text has no influence either way", fails)
    fl = t["A_flag"]
    check(fl["registry_revoked_flag_says_not"]["decision"] == "deny" and fl["registry_active_flag_says_revoked_and_expired"]["decision"] == "allow", "B1 flag: a host flag is not an input", fails)
    check(not t["A_gap"]["executed"] and t["A_gap"]["effects"] == 0 and not t["A_gap_revoke_then_restore"]["executed"], "B1 gap: revocation after evaluate is stopped by the compare-and-swap, including revoke-then-restore", fails)
    rc = t["A_receipt"]
    check(rc["forged_other_key"] == "bad_signature" and rc["tampered_decision_original_signature"] == "bad_signature" and rc["wrong_action"] == "binding" and rc["wrong_packet"] == "binding" and rc["expired"] == "expired" and rc["replay"]["second"] == "replay" and rc["effects_on_attack_system"] == 1, "B1 receipt: forged, tampered, mis-bound, expired and replayed receipts are rejected", fails)
    check(t["R_key_holder_mints"]["executed"] and t["R_stale_registry"]["executed"] and t["R_bypass_direct_call"]["effects_after_revocation_without_guard"] == 2 and t["R_inflight"]["executed"] and t["R_inflight"]["active_at_completion"] is False, "B1 residuals still succeed: key holder, stale registry, direct effect call, in-flight revocation", fails)
    check(t["mutation_noCAS_gap"]["executed"] and t["mutation_noSig_forged"]["executed"] and t["mutation_noNonce_replay"]["second_executed"], "B1 mutations: removing the compare-and-swap, signature check or nonce check makes the attack fire", fails)
    check(all(t["matrix_public_guard_fires"].values()), "B1 matrix: the same four defeat inputs fire on the public reference guard", fails)
    # B3: defeat form x timing x guard matrix
    m3 = subprocess.run(["node", os.path.join(HERE, "b3_defeat_matrix.js"), WORK], capture_output=True, text=True)
    if m3.returncode != 0:
        raise SystemExit("b3 script failed:\n" + m3.stderr)
    X = json.loads(m3.stdout)
    forms = ["F1_listed_word", "F2_unlisted_wording", "F3_flag_only", "F4_registry_only"]
    row = lambda g, t: [X[g][t][f] for f in forms]
    check(row("G1_public", "Ta") == [False, True, True, True] and all(row("G1_public", "Tb")) and all(row("G1_public", "Tc")), "B3 G1 public guard: only the listed word is held (before evaluation); every form fires after evaluation", fails)
    check(row("G2_public_recheck", "Ta") == [False, True, True, True] and row("G2_public_recheck", "Tb'") == [False, True, True, True] and all(row("G2_public_recheck", "Tb")) and all(row("G2_public_recheck", "Tc")), "B3 G2 a recheck before the effect narrows the window but does not close it", fails)
    check(not any(row("G3_registry_bound", "Ta")) and not any(row("G3_registry_bound", "Tb")) and all(row("G3_registry_bound", "Tc")), "B3 G3 registry-bound with compare-and-swap holds every form before the effect starts; none after it starts", fails)
    check(not any(row("G4_registry_bound_no_CAS", "Ta")) and all(row("G4_registry_bound_no_CAS", "Tb")), "B3 G4 removing the compare-and-swap reopens the gap", fails)
    check(all(all(row("G5_constant_endpoint", t)) for t in ("Ta", "Tb", "Tc")), "B3 G5 a guard over the constant endpoint fires in every cell", fails)
    # B2: independent constituted-executor toy built from the published freeze text
    q = subprocess.run(["node", os.path.join(HERE, "b2_constituted_executor.js")], capture_output=True, text=True)
    if q.returncode != 0:
        raise SystemExit("b2 script failed:\n" + q.stderr)
    Y = json.loads(q.stdout)
    zero = lambda d: all(d[k] == 0 for k in ("p1_no_receipt", "p2_forged", "p3_payload_mutated", "p4_expired", "p5_refusal", "p6_no_persisted_evidence"))
    check(zero(Y["baseline_paths_1_to_6"]) and zero(Y["hardened_paths_1_to_6"]) and Y["baseline_paths_1_to_6"]["p6_service_refuses_to_mint"], "B2 the six frozen unauthorized paths are blocked in an independent toy built from the freeze text", fails)
    d = Y["p7_parse_differential"]
    check(d["parsed"]["consequence_amounts"] == [1000000] and d["bytes"]["consequence_amounts"] == [1000000] and d["strict"]["consequence_amounts"] == [], "B2 binding the exact bytes does not close a decision/effect parse differential; a strict parse does", fails)
    check(Y["p8_replay"] == {"baseline": 2, "hardened": 1} and Y["p9_two_executors"] == {"baseline": 2, "hardened": 1}, "B2 replay inside the TTL and across two executors fires on the baseline, not on the hardened variant", fails)
    check(Y["p10_refusal_after_mint"]["baseline"]["consequences"] == 1 and Y["p10_refusal_after_mint"]["hardened"]["consequences"] == 0, "B2 a refusal recorded after minting is stopped only by the revocation epoch", fails)
    check(Y["p11_cross_action"]["bound"]["consequences"] == 0 and Y["p11_cross_action"]["action_not_bound_mutation"]["consequences"] == 1, "B2 cross-action reuse is blocked when the action is inside the hashed bytes", fails)
    check(all(v == 1 or v == 2 for rr in Y["p12_residuals"].values() for v in rr.values()) and all(rr["key_holder_mints"] == 1 and rr["executor_clock_behind_accepts_expired"] == 1 and rr["refusal_after_effect_started"] == 1 and rr["direct_consequence_call_after_refusal"] == 2 for rr in Y["p12_residuals"].values()), "B2 residuals fire on both variants: key holder, direct call, executor clock, in-flight refusal", fails)
    mc = Y["mutation_checks_consequences"]
    check(all(mc[k] >= 1 for k in ("noHash_p3", "noSig_p2", "noExpiry_p4", "noDecision_p5", "noEvidence_p6", "noEpoch_p10")) and mc["noNonce_p8"] == 2 and mc["noAud_p9"] == 2, "B2 mutations: removing each check makes its attack fire", fails)
    # semantic shuffling: meaning kept with the surface changed, surface kept with the meaning changed, and the registry vocabulary
    z = subprocess.run(["node", os.path.join(HERE, "semantic_shuffle_probes.js"), WORK], capture_output=True, text=True)
    if z.returncode != 0:
        raise SystemExit("semantic shuffle script failed:\n" + z.stderr)
    W = json.loads(z.stdout)
    allow = "stable/allow"; deny = "blocked/deny"
    check(W["controls"] == {"revoked": deny, "valid": allow} and all(x == allow for x in W["rewording"].values()) and all(x == allow for x in W["surface_perturbation"].values()) and all(x == allow for x in W["translation"].values()) and W["split_across_statements"] == allow and W["role_swap"] == allow and all(x == deny for x in W["order_permutation"].values()) and all(x == deny for x in W["mention_negation_modality"].values()), "S-shuffle the wording check evades rewording, perturbation, translation, splitting and role swap, blocks mention, negation and modality, and is order invariant", fails)
    rv = W["registry_vocabulary"]; unlisted = ("terminated", "withdrawn", "lapsed", "cyrillic_e_revoked")
    check(rv["A_allow_list_exact"]["active"] == "allow" and all(v == "deny" for k, v in rv["A_allow_list_exact"].items() if k != "active") and all(rv["B_deny_list_raw"][k] == "allow" for k in unlisted) and all(rv["C_deny_list_lower_trim"][k] == "allow" for k in unlisted) and rv["C_deny_list_lower_trim"]["Revoked_trailing_space"] == "deny", "S-shuffle a registry status vocabulary holds only as an allow-list with default deny", fails)
    # Appendix A: survival in finite math (exhaustive, model-local)
    sp = subprocess.run([sys.executable, os.path.join(HERE, "check_separability.py")], capture_output=True, text=True)
    if sp.returncode != 0:
        raise SystemExit("separability check failed:\n" + sp.stderr)
    F = json.loads(sp.stdout)
    check(F["worlds"] == 10756 and all(F[k] == 0 for k in ("T1_fail", "T2_fail", "T3_fail", "T4_fail", "T5a_fail", "T5b_fail")) and F["witness_worlds_with_survival_and_utility"] > 0 and F["T4_checked"] > 0 and F["T5a_separating_worlds"] > 0, "Appendix A the finite statements T1-T5 hold in every enumerated world", fails)
    # dn_runner: the black-box conformance runner discriminates the nine preregistered systems (about 40 s: observation windows)
    dn = subprocess.run(["node", os.path.join(HERE, "dn_runner", "selftest.js"), "--clones", WORK], capture_output=True, text=True, cwd=os.path.join(HERE, "dn_runner"))
    check(dn.returncode == 0 and "all 9 checked passed" in dn.stdout, "dn_runner nine preregistered verdicts match (public guard fails, registry-bound with compare-and-swap and atomic check conform, controls discriminate)", fails)
    # dn_runner reality mode: the runner serves the registry and the effect sink; six preregistered systems (about 15 s)
    rl = subprocess.run(["node", os.path.join(HERE, "dn_runner", "reality", "selftest_reality.js")], capture_output=True, text=True, cwd=os.path.join(HERE, "dn_runner", "reality"))
    check(rl.returncode == 0 and "all 6 passed" in rl.stdout, "dn_runner reality mode six preregistered verdicts match (fenced allow-list conforms; unfenced, constant, deny-list and caching systems fail where predicted)", fails)
    # Appendix D: probes of the public harness repository (pinned); no network call to the hosted evaluator
    hp = os.path.join(HERE, "harness_probe"); hw = os.path.join(WORK, "harmonic-test-harness")
    sr = subprocess.run(["node", "--experimental-strip-types", os.path.join(hp, "probe_sink_route.mjs"), hw], capture_output=True, text=True)
    S = json.loads(sr.stdout[sr.stdout.index("{"):])
    check([S[k]["status"] for k in ("C1_no_receipt", "C2_deny_receipt", "C3_expired", "C4_wrong_key", "C5_payload_mismatch")] == [401, 403, 403, 403, 403] and S["C6_valid"]["status"] == 200 and S["C7_alt_header"]["status"] == 200, "Appendix D sink route controls: receiptless, DENY, expired, wrong-key and mismatched payload are refused; valid and alternate-header receipts execute", fails)
    check(S["A1_replay"] == [200] * 5 and S["A2_proto_smuggle"]["status"] == 200 and S["A2_proto_nested"]["status"] == 200 and S["A2_proto_string"]["status"] == 200 and S["A2_evidence"]["hashes_equal"] and S["A3_dupkey_vs_last_wins_receipt"]["status"] == 200 and S["A3_dupkey_vs_first_wins_receipt"]["status"] == 403, "Appendix D sink route: replay is accepted, a __proto__ member is not covered by the payload hash, duplicate keys show no parse differential inside the route", fails)
    dp = subprocess.run(["node", os.path.join(hp, "probe_disposition.mjs"), hw], capture_output=True, text=True)
    Dd = json.loads(dp.stdout)
    check(Dd["control_allow"] == "ALLOW" and Dd["control_block"] == "BLOCK" and Dd["control_pass_only"] == "UNRESOLVED" and Dd["control_permit_not_admissible"] == "BLOCK" and Dd["control_block_and_allow"] == "BLOCK" and Dd["conflict_hold_vs_allowed"] == "ALLOW" and Dd["nested_governance_over_toplevel_block"] == "ALLOW", "Appendix D gate: controls behave as intended; conflicting fields and a nested object resolve toward execution", fails)
    # live-probe runner: classifies and stops as designed against loopback stand-ins (no call leaves the machine)
    lp = subprocess.run(["node", os.path.join(hp, "live", "selftest_live.mjs"), hw], capture_output=True, text=True)
    check(lp.returncode == 0 and "all passed" in lp.stdout, "Appendix D live-probe runner: refusals, controls gate, abort and classification behave as preregistered against local stand-ins", fails)
    print(f"\n{'ALL CHECKS PASS' if not fails else str(len(fails)) + ' CHECK(S) FAILED'}")
    sys.exit(1 if fails else 0)

main()
