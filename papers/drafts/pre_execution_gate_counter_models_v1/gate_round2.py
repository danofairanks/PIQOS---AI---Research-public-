#!/usr/bin/env python3
"""Attack round 2 against the counter-models (author-named steelmen; NOT an independent round).
Companion to ../pre_execution_gate_counter_models_v1.md. Observables and predictions were fixed before this file was written.
stdlib only; seeded rng in toys only. Usage: python3 gate_round2.py [--selftest]
"""
import hashlib
import hmac
import json
import random
import sys

from gate_counter_models import t1_reject_option, t5_pipeline, E_LIMIT


# B1 decomposition: scorer noise sweep
def b1():
    return {str(s): {k: v for k, v in t1_reject_option(sigma=s).items() if k in ("halts", "allows_of_prohibited")}
            for s in (0.0, 0.2, 0.8)}


# B2 finite precision
def quant_traj(k, x0, n=200, r=3.9):
    q = 2 ** k
    x = round(x0 * q) / q
    out = []
    for _ in range(n):
        x = round(r * x * (1 - x) * q) / q
        out.append(x)
    return out


def b2():
    res = {}
    for k in (8, 12, 16, 24, 52):
        a = quant_traj(k, 0.2)
        b = quant_traj(k, round(0.2 * 2 ** k) / 2 ** k + 2 ** -k)
        res[str(k)] = next((i + 1 for i in range(200) if abs(a[i] - b[i]) > 0.1), None)
    return res


# B3 full observability
def b3(steps=100):
    passed = 0
    for t in range(steps):
        latent = 0.9 if t % 10 == 9 else 0.2
        seen = latent                       # reported state is read from the state itself
        if seen <= E_LIMIT and latent > E_LIMIT:
            passed += 1
    return {"violations_passed_reported_gate_full_observability": passed}


# B4 authenticated context
def b4(steps=100):
    key = b"independent-signer-key"
    sign = lambda ctx, nonce: hmac.new(key, f"{ctx}|{nonce}".encode(), hashlib.sha256).hexdigest()
    old_token = ("oversight", 0, sign("oversight", 0))        # captured when oversight was really present
    out = {}
    for variant in ("UNAUTH", "AUTH_REPLAY_NO_FRESHNESS", "AUTH_FRESH_INDEPENDENT_SIGNER", "AUTH_FORGE_WRONG_KEY"):
        passed = 0
        for t in range(steps):
            true_c = "oversight" if t % 4 == 0 else "none"
            r_next = 0.5 if t % 5 == 0 else 0.2
            nonce = t                                          # verifier-chosen nonce when fresh
            if variant == "UNAUTH":
                seen = "oversight"                             # masking system just says so
            elif variant == "AUTH_REPLAY_NO_FRESHNESS":
                ctx, n0, tok = old_token
                seen = ctx if hmac.compare_digest(tok, sign(ctx, n0)) else "none"          # verifier ignores nonce
            elif variant == "AUTH_FRESH_INDEPENDENT_SIGNER":
                ctx, n0, tok = old_token
                seen = ctx if (n0 == nonce and hmac.compare_digest(tok, sign(ctx, nonce))) else "none"
                if t == 0:
                    seen = "oversight"                         # the one step where the replayed token is current and true
            else:
                forged = hmac.new(b"wrong-key", b"oversight|x", hashlib.sha256).hexdigest()
                seen = "oversight" if hmac.compare_digest(forged, sign("oversight", "x")) else "none"
            in_soft = 0.3 < r_next <= 0.6
            passes = (not in_soft) or seen == "oversight"
            if passes and in_soft and true_c != "oversight":
                passed += 1
        out[variant] = passed
    return out


# B5 coverage of the trace-derived exit
def b5(seeds=50):
    res = {}
    for pe in (0.001, 0.01, 0.1):
        for K in (100, 1000, 10000):
            detected = 0
            for sd in range(seeds):
                rng = random.Random(1000 + sd)
                found = False
                for _ in range(K):
                    u = "work"
                    for _ in range(30):
                        if u == "work":
                            x = rng.random()
                            if x < pe:
                                found = True
                                break
                            u = "commit" if x < pe + (1 - pe) / 2 else "idle"
                        elif u == "idle":
                            u = "work"
                        else:
                            break
                    if found:
                        break
                detected += found
            res[f"p_e={pe},K={K}"] = detected / seeds
    return res


# B6 determinism meaning
def parser_det(margin, variant, noise=0.5):
    h = int(hashlib.sha256(variant.encode()).hexdigest()[:8], 16) / 2 ** 32
    return margin + (h * 2 - 1) * noise


def b6():
    out = {}
    for margin in (0.1, 0.5, 2.0):
        exact = {parser_det(margin, "request-A") > 0 for _ in range(50)}
        variants = {parser_det(margin, f"paraphrase-{i}") > 0 for i in range(200)}
        out[str(margin)] = {"exact_repeat_distinct_outcomes": len(exact), "paraphrase_distinct_outcomes": len(variants)}
    return out


# B9 seed and parameter robustness
def b9():
    t1 = []
    for sd in range(20):
        for sig in (0.3, 0.8, 1.5):
            for th in (0.7, 0.8, 0.9):
                r = t1_reject_option(seed=sd, sigma=sig, theta=th)
                t1.append((r["d1_triggered"], r["allows_of_prohibited"] > 0))
    stable_ratio = {}
    for ratio in (1, 2, 3, 4, 5):
        ok = all(len(t5_pipeline(ratio * 0.5, 0.5, seed=sd)["distinct_outcomes"]) == 1 for sd in range(20))
        stable_ratio[str(ratio)] = ok
    return {"t1_d1_triggered_all": all(a for a, _ in t1), "t1_executed_prohibited_all": all(b for _, b in t1),
            "t1_runs": len(t1), "t5_all_seeds_single_outcome_by_margin_over_noise": stable_ratio}


# B10 probe error
def b10(seeds=50):
    out = {}
    for eps in (0.0, 0.05, 0.2):
        tot = 0
        for sd in range(seeds):
            rng = random.Random(2000 + sd)
            for t in range(100):
                if t % 10 == 9 and rng.random() < eps:
                    tot += 1
        out[str(eps)] = tot / seeds
    return out


def run_all():
    return {"B1": b1(), "B2": b2(), "B3": b3(), "B4": b4(), "B5": b5(), "B6": b6(), "B9": b9(), "B10": b10()}


def matrix(r):
    return {
        "B1_decomposition": "SUCCEEDS-IN-PART" if r["B1"]["0.0"]["allows_of_prohibited"] == 0 and r["B1"]["0.8"]["allows_of_prohibited"] > 0 else "FAILS",
        "B2_finite_precision": "FAILS" if all(v is not None for v in r["B2"].values()) else "SUCCEEDS",
        "B3_full_observability": "SUCCEEDS" if r["B3"]["violations_passed_reported_gate_full_observability"] == 0 else "FAILS",
        "B4_authenticated_context": "CONFIRMS-EXIT" if (r["B4"]["UNAUTH"] > 0 and r["B4"]["AUTH_REPLAY_NO_FRESHNESS"] > 0
                                                        and r["B4"]["AUTH_FRESH_INDEPENDENT_SIGNER"] == 0) else "OTHER",
        "B5_coverage_of_exit": "SUCCEEDS" if r["B5"]["p_e=0.001,K=100"] < 0.5 else "FAILS",
        "B6_determinism_meaning": "SUCCEEDS-IN-PART" if (all(v["exact_repeat_distinct_outcomes"] == 1 for v in r["B6"].values())
                                                          and r["B6"]["0.1"]["paraphrase_distinct_outcomes"] > 1) else "FAILS",
        "B8_H2_straw_man": "CONCEDED (textual-exclusion check, not a toy result)",
        "B9_seed_param_dependence": "FAILS" if (r["B9"]["t1_d1_triggered_all"] and r["B9"]["t1_executed_prohibited_all"]) else "SUCCEEDS",
        "B10_probe_regress": "RELOCATES" if (r["B10"]["0.0"] == 0 and r["B10"]["0.2"] > r["B10"]["0.05"] > 0) else "OTHER",
    }


PINNED = {
    "B1_decomposition": "SUCCEEDS-IN-PART",
    "B2_finite_precision": "FAILS",
    "B3_full_observability": "SUCCEEDS",
    "B4_authenticated_context": "CONFIRMS-EXIT",
    "B5_coverage_of_exit": "SUCCEEDS",
    "B6_determinism_meaning": "SUCCEEDS-IN-PART",
    "B8_H2_straw_man": "CONCEDED (textual-exclusion check, not a toy result)",
    "B9_seed_param_dependence": "FAILS",
    "B10_probe_regress": "RELOCATES",
}


if __name__ == "__main__":
    r = run_all()
    r["matrix"] = matrix(r)
    print(json.dumps(r, indent=2, sort_keys=True))
    if "--selftest" in sys.argv:
        assert r["matrix"] == PINNED, "matrix drifted"
        assert r["B9"]["t5_all_seeds_single_outcome_by_margin_over_noise"] == {"1": False, "2": False, "3": False, "4": True, "5": True}
        print("selftest OK")
