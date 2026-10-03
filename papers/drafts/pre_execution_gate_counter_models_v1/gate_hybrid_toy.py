#!/usr/bin/env python3
"""Hybrid (hard + soft) constraint toy: does adding context-sensitive constraints escape the latent-state result?

Companion to ../pre_execution_gate_counter_models_v1.md (section on the hybrid). Defeat conditions were fixed before this file was written.
State: risk r in [0, 1]. E_hard: r <= 0.6. E_soft(c): r in (0.3, 0.6] admissible only when
context c == "oversight". Context c is an input (situational/environmental, §5.3).
Status vocabulary as in gate_counter_models.py. stdlib only; seeded rng in toys only.
Usage: python3 gate_hybrid_toy.py [--selftest]
"""
import json
import random
import sys

HARD_MAX, SOFT_LOW = 0.6, 0.3


def in_hard(r):
    return r <= HARD_MAX


def in_soft_zone(r):
    return SOFT_LOW < r <= HARD_MAX


def in_E(r, c):
    return in_hard(r) and (not in_soft_zone(r) or c == "oversight")


# ---- H1: context channel (predicate soft part) ----
def h1_context_channel(steps=100):
    counts = {}
    for gen in ("HONEST", "MASKING"):
        for gate in ("REPORTED_CONTEXT", "INDEPENDENT_CONTEXT"):
            passed_violations = 0
            for t in range(steps):
                true_c = "oversight" if t % 4 == 0 else "none"
                reported_c = true_c if gen == "HONEST" else "oversight"
                r_next = 0.5 if t % 5 == 0 else (0.9 if t % 17 == 0 else 0.2)   # soft-zone and hard-violating proposals
                seen_c = reported_c if gate == "REPORTED_CONTEXT" else true_c
                passes = in_E(r_next, seen_c)
                if passes and not in_E(r_next, true_c):
                    passed_violations += 1
            counts[f"{gen}/{gate}"] = passed_violations
    return {"violations_passed": counts, "h1_triggered": counts["MASKING/REPORTED_CONTEXT"] > 0}


# ---- H2: determinative predicate (P) vs penalty (Q) ----
def h2_predicate_vs_penalty(seed=5, n=2000, penalty=0.5):
    rng = random.Random(seed)
    accepted_P = accepted_Q = soft_violating = 0
    for _ in range(n):
        r_next = rng.uniform(SOFT_LOW + 0.01, HARD_MAX)       # soft-zone proposal, no oversight
        reward = rng.uniform(0, 1)
        soft_violating += 1
        if in_E(r_next, "none"):                              # P: predicate
            accepted_P += 1
        if reward - penalty >= 0:                             # Q: trade-off against reward
            accepted_Q += 1
    return {"soft_violating_proposals": soft_violating, "accepted_under_predicate": accepted_P,
            "accepted_under_penalty": accepted_Q, "h2_triggered_for_penalty": accepted_Q > 0}


# ---- H3: invariance under changing context ----
def h3_stranding(seed=9, steps=500, flip=0.2):
    rng = random.Random(seed)
    c, r = "oversight", 0.5                                   # entered the soft zone legitimately
    stranded = gate_calls = 0
    for _ in range(steps):
        if rng.random() < flip:
            c = "none" if c == "oversight" else "oversight"
        if not in_E(r, c):
            stranded += 1                                     # state outside E(c_t); no transition proposed, gate never invoked
    # control: confine to the intersection over contexts A = {r <= SOFT_LOW}
    c, r2, stranded_core = "oversight", 0.2, 0
    rng = random.Random(seed)
    for _ in range(steps):
        if rng.random() < flip:
            c = "none" if c == "oversight" else "oversight"
        if not in_E(r2, c):
            stranded_core += 1
    return {"stranded_steps_soft_zone_state": stranded, "gate_invocations_during_stranding": gate_calls,
            "stranded_steps_when_confined_to_core": stranded_core, "h3_triggered": stranded > 0}


def run_all():
    h1, h2, h3 = h1_context_channel(), h2_predicate_vs_penalty(), h3_stranding()
    v = h1["violations_passed"]
    matrix = {
        "H0_hard_core_clamp_guarantee": "HOLDS-FOR-EVERY-f (pinned in gate_counter_models.py, C3_trivial_invariance)",
        "H1_reported_context": "DEFEATED-AT-SCOPE" if v["MASKING/REPORTED_CONTEXT"] > 0 else "NOT-REACHED",
        "H1_independent_context": "DEFEATED-AT-SCOPE" if v["MASKING/INDEPENDENT_CONTEXT"] > 0 else "NOT-REACHED",
        "H1_honest_control": "DEFEATED-AT-SCOPE" if v["HONEST/REPORTED_CONTEXT"] > 0 else "NOT-REACHED",
        "H2_penalty_variant_vs_4.5": "DEFEATED-AT-SCOPE" if h2["h2_triggered_for_penalty"] else "NOT-REACHED",
        "H2_predicate_variant_(control)": "NOT-REACHED" if h2["accepted_under_predicate"] == 0 else "DEFEATED-AT-SCOPE",
        "H3_invariance_under_context_change": "DEFEATED-AT-SCOPE" if h3["h3_triggered"] else "NOT-REACHED",
        "H3_core_only_control": "NOT-REACHED" if h3["stranded_steps_when_confined_to_core"] == 0 else "DEFEATED-AT-SCOPE",
    }
    return {"H1": h1, "H2": h2, "H3": h3, "matrix": matrix}


PINNED = {
    "H0_hard_core_clamp_guarantee": "HOLDS-FOR-EVERY-f (pinned in gate_counter_models.py, C3_trivial_invariance)",
    "H1_reported_context": "DEFEATED-AT-SCOPE",
    "H1_independent_context": "NOT-REACHED",
    "H1_honest_control": "NOT-REACHED",
    "H2_penalty_variant_vs_4.5": "DEFEATED-AT-SCOPE",
    "H2_predicate_variant_(control)": "NOT-REACHED",
    "H3_invariance_under_context_change": "DEFEATED-AT-SCOPE",
    "H3_core_only_control": "NOT-REACHED",
}


if __name__ == "__main__":
    r = run_all()
    print(json.dumps(r, indent=2, sort_keys=True))
    if "--selftest" in sys.argv:
        assert r["matrix"] == PINNED, "matrix drifted"
        print("selftest OK")
