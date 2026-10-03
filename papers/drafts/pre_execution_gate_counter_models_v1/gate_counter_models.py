#!/usr/bin/env python3
"""Generic counter-models for arguments made for pre-execution authority gates.

Companion to ../pre_execution_gate_counter_models_v1.md.
These toys test ARGUMENTS as stated, not any implementation (none was available). Status vocabulary, fixed before any run:
  DEFEATED-AT-SCOPE  the stated observable occurred in a run of the toy
  NOT-REACHED        the toy could not produce the observable
  BLOCKED            needs an artifact the public text does not supply (not run)
stdlib only. Seeded random.Random in toys only (internal measurement, not a derivation).
Usage: python3 gate_counter_models.py [--selftest]
"""
import math
import random
import sys
from collections import deque


# ---------------- T1: reject option (claim C1, defeat D1) ----------------
def t1_reject_option(seed=1, n=2000, sigma=0.8, theta=0.8, k=4.0):
    """Probabilistic scorer with a reject option inside the same decision function.
    Input signal s in [-1, 1]; s > 0 means the request is prohibited.
    HALT = no output, no state transition. DENY = refusal message, no effect.
    ALLOW = effect appended to the log.
    A deterministic rule gate (DENY iff s > 0, emits a refusal message) is run on the
    same inputs as the control for premise 3 ('any output means the core function executed').
    """
    rng = random.Random(seed)
    log, outputs_prob, outputs_rule = [], 0, 0
    halts = halts_with_output_or_effect = denies = allows_of_prohibited = rule_refusals = 0
    for i in range(n):
        s = rng.uniform(-1, 1)
        noisy = s + rng.gauss(0, sigma)
        p = 1 / (1 + math.exp(-k * noisy))          # P(prohibited)
        conf = max(p, 1 - p)
        log_before, out_before = len(log), outputs_prob
        if conf < theta:
            halts += 1
        elif p >= 0.5:
            denies += 1
            outputs_prob += 1                         # refusal message
        else:
            log.append(("effect", i))
            outputs_prob += 1
            if s > 0:
                allows_of_prohibited += 1
        if conf < theta and (len(log) != log_before or outputs_prob != out_before):
            halts_with_output_or_effect += 1
        if s > 0:                                     # rule gate refuses with a message
            rule_refusals += 1
            outputs_rule += 1
    return {
        "halts": halts,
        "halts_with_output_or_effect": halts_with_output_or_effect,
        "denies": denies,
        "allows_of_prohibited": allows_of_prohibited,
        "rule_gate_refusal_messages": rule_refusals,
        "d1_triggered": halts > 0 and halts_with_output_or_effect == 0,
        "narrowed_claim_support": allows_of_prohibited > 0,   # reject option gives no denial guarantee
        # premise 2 as phrased ('authority requires no output') fails for the rule gate too:
        "premise3_proves_too_much": outputs_rule > 0,
    }


# ---------------- T2: deterministic sensitivity (claim C2, defeat D2) ----------------
def logistic_traj(r, x0, n):
    x, out = x0, []
    for _ in range(n):
        x = r * x * (1 - x)
        out.append(x)
    return out


def t2_determinism_vs_stability(n=200, eps=1e-10):
    a = logistic_traj(3.9, 0.2, n)
    b = logistic_traj(3.9, 0.2 + eps, n)
    again = logistic_traj(3.9, 0.2, n)
    first = next((i + 1 for i in range(n) if abs(a[i] - b[i]) > 0.1), None)
    sa = logistic_traj(2.5, 0.2, n)
    sb = logistic_traj(2.5, 0.2 + eps, n)
    return {
        "deterministic_repeat_identical": a == again,
        "chaotic_first_step_diverged_over_0.1": first,
        "stable_max_diff_after_100": max(abs(sa[i] - sb[i]) for i in range(100, n)),
        "d2_triggered": a == again and first is not None,
    }


# ---------------- T3: latent-state gate (claim C3, defeat D3) ----------------
E_LIMIT = 0.3


def t3_latent_gate(steps=100):
    """E = {latent risk <= 0.3}. Two generators: HONEST reports its latent state; MASKING
    reports compliant while its latent state violates every 10th step. Two gates:
    REPORTED reads the system's own report; INDEPENDENT reads the latent through a probe
    the governed system does not control (channel-collapse exit 1)."""
    counts = {}
    for gen in ("HONEST", "MASKING"):
        for gate in ("REPORTED", "INDEPENDENT"):
            passed = 0
            for t in range(steps):
                latent = 0.9 if t % 10 == 9 else 0.2
                reported = latent if gen == "HONEST" else 0.1
                seen = reported if gate == "REPORTED" else latent
                gate_passes = seen <= E_LIMIT
                if gate_passes and latent > E_LIMIT:
                    passed += 1                       # a violating step the gate let through
            counts[f"{gen}/{gate}"] = passed
    # trivial-invariance check: T_E = clamp into E makes S(t+1) in E for ANY f
    rng = random.Random(7)
    fs = [(lambda s, c=rng.uniform(0, 1), m=rng.uniform(-2, 2): (s * m + c) % 1.3 - 0.15) for _ in range(50)]
    fs.append(lambda s: 0.99)                          # an adversarial f
    all_hold, altered, total = True, 0, 0
    for f in fs:
        for j in range(21):
            raw = f(j / 20)
            clamped = min(max(raw, 0.0), E_LIMIT)
            all_hold = all_hold and (0.0 <= clamped <= E_LIMIT)
            altered += clamped != raw
            total += 1
    return {
        "violations_passed": counts,
        "guarantee_holds_for_every_f": all_hold,
        "fraction_of_successors_altered_by_projection": round(altered / total, 3),
        "d3_triggered": counts["MASKING/REPORTED"] > 0,
    }


# ---------------- T4: model vs real graph (claims C4/C6, defeats D4/D5) ----------------
def reach(edges, start, targets, only_unmediated=False):
    seen, q = {start}, deque([start])
    while q:
        u = q.popleft()
        if u in targets:
            return True
        for (a, b, mediated) in edges:
            if a == u and b not in seen and not (only_unmediated and mediated):
                seen.add(b)
                q.append(b)
    return False


def blocked_model(edges):
    """The modeled state space: mediated edges are blocked by the gate, nothing else removed."""
    return [(a, b, m) for (a, b, m) in edges if not m]


def trace_derived_model(edges, seed=3, walks=300, length=30):
    """Model rebuilt from observed traces of the real system (random walks, gate absent)."""
    rng = random.Random(seed)
    seen = set()
    out = {}
    for (a, b, m) in edges:
        out.setdefault(a, []).append((a, b, m))
    for _ in range(walks):
        u = "init"
        for _ in range(length):
            nxt = out.get(u)
            if not nxt:
                break
            e = rng.choice(nxt)
            seen.add(e)
            u = e[1]
    return [e for e in seen if not e[2]]


BASE = [("init", "work", False), ("work", "commit", False), ("work", "idle", False),
        ("idle", "work", False), ("work", "prohibited", True)]  # gated edge, mediated
P = {"prohibited"}


def t4_worlds():
    worlds = {
        "W0_real_equals_model": BASE,
        "W1_side_channel": BASE + [("work", "prohibited", False)],
        "W2_host_kills_gate": BASE + [("work", "gate_off", False), ("gate_off", "prohibited", False)],
    }
    out = {}
    for name, R in worlds.items():
        M = blocked_model(BASE)
        proof_over_model = not reach(M, "init", P)
        real_path = reach(R, "init", P, only_unmediated=True)
        M2 = trace_derived_model(R)
        proof_over_trace_model = not reach(M2, "init", P)
        out[name] = {
            "proof_over_model_holds": proof_over_model,
            "executable_path_in_real": real_path,
            "d4_d5_triggered": proof_over_model and real_path,
            "trace_derived_model_proof_holds": proof_over_trace_model,
            "trace_derived_model_agrees_with_real": proof_over_trace_model == (not real_path),
        }
    return out


# ---------------- T5: nondeterministic stage before deterministic gate (claim C7, defeat D6) ----------------
def t5_pipeline(margin, noise, runs=500, seed=11):
    rng = random.Random(seed)
    outcomes = []
    for _ in range(runs):
        s = margin + (rng.gauss(0, noise) if noise else 0.0)
        interpreted_prohibited = s > 0
        outcomes.append("DENY" if interpreted_prohibited else "ALLOW")   # deterministic gate
    return {"distinct_outcomes": sorted(set(outcomes)), "deny_fraction": round(outcomes.count("DENY") / runs, 3)}


def t5_all():
    res = {
        "deterministic_parser_margin_0.1": t5_pipeline(0.1, 0.0),
        "noisy_parser_margin_0.1": t5_pipeline(0.1, 0.5),
    }
    sweep = {}
    for m in (0.05, 0.5, 1.0, 2.0, 3.0):
        sweep[m] = t5_pipeline(m, 0.5)["distinct_outcomes"]
    res["noisy_parser_stability_sweep"] = sweep
    res["d6_triggered"] = len(res["noisy_parser_margin_0.1"]["distinct_outcomes"]) > 1
    res["deterministic_control_single_outcome"] = len(res["deterministic_parser_margin_0.1"]["distinct_outcomes"]) == 1
    return res


# ---------------- matrix ----------------
BLOCKED = {
    "C5_ethics_score_threshold": "EthicsScore and truth score undefined in the public text",
    "C8_exists_runs_exercised": "no artifact, trace or hash supplied",
    "C6_implementation_specific": "no placement or trust root disclosed",
    "C4_implementation_specific": "no model or placement disclosed",
}


def run_all():
    t1, t2, t3, t4, t5 = t1_reject_option(), t2_determinism_vs_stability(), t3_latent_gate(), t4_worlds(), t5_all()
    matrix = {
        "C1_D1": "DEFEATED-AT-SCOPE" if t1["d1_triggered"] else "NOT-REACHED",
        "C1_narrowed_(no denial guarantee)": "SUPPORTED" if t1["narrowed_claim_support"] else "NOT-REACHED",
        "C2_D2": "DEFEATED-AT-SCOPE" if t2["d2_triggered"] else "NOT-REACHED",
        "C3_D3_reported_gate": "DEFEATED-AT-SCOPE" if t3["d3_triggered"] else "NOT-REACHED",
        "C3_D3_independent_gate": "NOT-REACHED" if t3["violations_passed"]["MASKING/INDEPENDENT"] == 0 else "DEFEATED-AT-SCOPE",
        "C3_honest_control_reported_gate": "NOT-REACHED" if t3["violations_passed"]["HONEST/REPORTED"] == 0 else "DEFEATED-AT-SCOPE",
        "C3_trivial_invariance": "HOLDS-FOR-EVERY-f" if t3["guarantee_holds_for_every_f"] else "NOT-REACHED",
        "C4_D4_W1": "DEFEATED-AT-SCOPE" if t4["W1_side_channel"]["d4_d5_triggered"] else "NOT-REACHED",
        "C4_D4_W2": "DEFEATED-AT-SCOPE" if t4["W2_host_kills_gate"]["d4_d5_triggered"] else "NOT-REACHED",
        "C4_D4_W0": "DEFEATED-AT-SCOPE" if t4["W0_real_equals_model"]["d4_d5_triggered"] else "NOT-REACHED",
        "C6_D5_W1": "DEFEATED-AT-SCOPE" if t4["W1_side_channel"]["executable_path_in_real"] else "NOT-REACHED",
        "C7_D6": "DEFEATED-AT-SCOPE" if t5["d6_triggered"] else "NOT-REACHED",
        "C7_deterministic_control": "NOT-REACHED" if t5["deterministic_control_single_outcome"] else "DEFEATED-AT-SCOPE",
    }
    for k in BLOCKED:
        matrix[k] = "BLOCKED"
    return {"T1": t1, "T2": t2, "T3": t3, "T4": t4, "T5": t5, "matrix": matrix}


PINNED_MATRIX = {
    "C1_D1": "DEFEATED-AT-SCOPE",
    "C1_narrowed_(no denial guarantee)": "SUPPORTED",
    "C2_D2": "DEFEATED-AT-SCOPE",
    "C3_D3_reported_gate": "DEFEATED-AT-SCOPE",
    "C3_D3_independent_gate": "NOT-REACHED",
    "C3_honest_control_reported_gate": "NOT-REACHED",
    "C3_trivial_invariance": "HOLDS-FOR-EVERY-f",
    "C4_D4_W1": "DEFEATED-AT-SCOPE",
    "C4_D4_W2": "DEFEATED-AT-SCOPE",
    "C4_D4_W0": "NOT-REACHED",
    "C6_D5_W1": "DEFEATED-AT-SCOPE",
    "C7_D6": "DEFEATED-AT-SCOPE",
    "C7_deterministic_control": "NOT-REACHED",
    "C5_ethics_score_threshold": "BLOCKED",
    "C8_exists_runs_exercised": "BLOCKED",
    "C6_implementation_specific": "BLOCKED",
    "C4_implementation_specific": "BLOCKED",
}


def main(argv):
    r = run_all()
    import json
    print(json.dumps(r, indent=2, sort_keys=True, default=str))
    if "--selftest" in argv:
        assert r["matrix"] == PINNED_MATRIX, "matrix drifted from pinned reads"
        assert r["T1"]["halts"] > 0 and r["T1"]["halts_with_output_or_effect"] == 0
        assert r["T2"]["deterministic_repeat_identical"]
        assert r["T3"]["violations_passed"] == {"HONEST/REPORTED": 0, "HONEST/INDEPENDENT": 0, "MASKING/REPORTED": 10, "MASKING/INDEPENDENT": 0}
        assert r["T4"]["W1_side_channel"]["trace_derived_model_agrees_with_real"]
        assert r["T4"]["W2_host_kills_gate"]["trace_derived_model_agrees_with_real"]
        assert r["T5"]["deterministic_control_single_outcome"]
        print("selftest OK")


if __name__ == "__main__":
    main(sys.argv[1:])
