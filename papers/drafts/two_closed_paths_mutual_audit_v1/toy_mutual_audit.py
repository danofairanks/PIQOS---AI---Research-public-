"""Toy for two_closed_paths_mutual_audit_v1.md.  Stdlib only.  Run: python toy_mutual_audit.py

Two verifiers built from the same flawed specification agree with each other on every input the
specification talks about, so a spec-derived conformance suite (and the pair's agreement) can never
reveal the flaw.  The referent T is outside both.  See PREREG.md for the predictions this checks.
"""
import math, random

SEED, MAX = 20261016, 100.0
MIX = [("typical", 66), ("above_limit", 10), ("huge", 2), ("zero", 2),
       ("negative", 8), ("neg_inf", 3), ("pos_inf", 3), ("nan", 6)]
SPEC_CLASSES = [("typical", 85), ("above_limit", 15)]     # what the spec text talks about
COMMON_MODE = {"zero", "negative", "neg_inf"}            # A and B both wrongly ALLOW these


def draw(cls, r):
    return {"typical": lambda: r.uniform(1e-3, MAX), "above_limit": lambda: r.uniform(MAX * 1.0001, 100 * MAX),
            "huge": lambda: 10 ** r.uniform(12, 15), "zero": lambda: 0.0, "negative": lambda: -10 ** r.uniform(-3, 3),
            "neg_inf": lambda: -math.inf, "pos_inf": lambda: math.inf, "nan": lambda: math.nan}[cls]()


def sample(mix, n, r):
    names, w = zip(*mix)
    return [(c, draw(c, r)) for c in r.choices(names, weights=w, k=n)]


def truth(d):  return math.isfinite(d) and 0 < d <= MAX
def A(d):      return d <= MAX                      # shared spec S, one expression
def B(d):      return not (d > MAX)                 # shared spec S, another expression (differs on NaN)
def B2(d):     return d >= 0 and d <= MAX           # a second spec S2, flawed differently
def M1(d):     return A(d) or d >= 1e12             # mutant of A: also allows huge values
def M2(d):     return A(d) and not (0 < d < 1)      # mutant of A: wrongly denies small positives


def rates(f, g, data):
    n = len(data)
    jfa = sum(1 for c, d in data if f(d) and g(d) and not truth(d)) / n
    dis = [c for c, d in data if f(d) != g(d)]
    return jfa, len(dis) / n, set(dis)


def spec_suite(r, n=200):
    """Conformance suite derived from the spec: inputs from the spec's classes + boundaries; expected = spec S."""
    xs = [d for _, d in sample(SPEC_CLASSES, n, r)] + [MAX, MAX * (1 + 1e-9), 1.0]
    return [(d, d <= MAX) for d in xs]


def passes(f, suite):  return all(f(d) == exp for d, exp in suite)


def check(label, ok, detail):
    print(f"  {label}: {'PASS' if ok else 'FAIL'}  ({detail})")
    return ok


if __name__ == "__main__":
    r = random.Random(SEED)
    data = sample(MIX, 20000, r)
    res = []
    print(f"seed={SEED}  MAX={MAX}  referent draws=20000")

    # P1
    reps = 500
    okA = okB = 0
    for _ in range(reps):
        s = spec_suite(r); okA += passes(A, s); okB += passes(B, s)
    print("\nTable 1: spec-derived conformance suite (200 draws) on A and B")
    print(f"  pass rate A={okA/reps:.3f}  B={okB/reps:.3f}  over {reps} repeated suites")
    res.append(check("P1", okA == reps and okB == reps, "both pass 100% of suites, by construction"))

    # P2, P3
    jfa, dis, dcls = rates(A, B, data)
    print("\nTable 2: referent distribution")
    print(f"  pair (A,B)  : joint false-allow={jfa:.4f}  disagreement={dis:.4f}  disagreement classes={sorted(dcls)}")
    res.append(check("P2", abs(jfa - 0.13) <= 0.02 and abs(dis - 0.06) <= 0.01 and dcls == {"nan"},
                     "joint false-allow 0.13+-0.02; disagreement 0.06+-0.01; all NaN"))
    jfa2, dis2, dcls2 = rates(A, B2, data)
    print(f"  pair (A,B2) : joint false-allow={jfa2:.4f}  disagreement={dis2:.4f}  disagreement classes={sorted(dcls2)}")
    res.append(check("P3", abs(jfa2 - 0.02) <= 0.01 and abs(dis2 - 0.11) <= 0.015,
                     "joint false-allow 0.02+-0.01; disagreement 0.11+-0.015"))

    # P4: detecting the common-mode class by sampling n=20
    def detect_common(mix, n, reps=500):
        hit = 0
        for _ in range(reps):
            xs = sample(mix, n, r)
            hit += any(f(d) and g(d) and not truth(d) for f, g in [(A, B)] for _, d in xs)
        return hit / reps
    p_ref, p_spec = detect_common(MIX, 20), detect_common(SPEC_CLASSES, 20)
    print("\nTable 3: detecting the common-mode class (zero, negative, -inf), n=20 draws")
    print(f"  referent sampler={p_ref:.3f}   spec-derived sampler={p_spec:.3f}")
    res.append(check("P4", p_ref >= 0.90 and p_spec == 0.0, "referent >= 0.90; spec-derived exactly 0"))

    # P5, P6: mutants of A
    def spec_detect(m, reps=500):
        return sum(not passes(m, spec_suite(r)) for _ in range(reps)) / reps
    def disagree_detect(m, n=200, reps=500):
        hit = 0
        for _ in range(reps):
            xs = sample(MIX, n, r)
            # a detection = a disagreement with B on a class where the unmutated pair (A,B) agrees
            hit += any(m(d) != B(d) and A(d) == B(d) for _, d in xs)
        return hit / reps
    big = sample(MIX, 20000, r)
    j_base = rates(A, B, big)[0]; j_m1 = rates(M1, B, big)[0]
    s1, d1, s2 = spec_detect(M1), disagree_detect(M1), spec_detect(M2)
    print("\nTable 4: mutants of A")
    print(f"  M1 (also allows huge): spec-suite detect={s1:.3f}  disagreement-audit (n=200) detect={d1:.3f}  "
          f"joint false-allow {j_base:.4f} -> {j_m1:.4f} (conjunction masks the bug)")
    print(f"  M2 (denies 0<d<1)    : spec-suite detect={s2:.3f}")
    res.append(check("P5", s1 == 0.0 and abs(j_m1 - j_base) < 1e-12 and d1 >= 0.95,
                     "spec-suite 0; joint unchanged; disagreement audit >= 0.95"))
    res.append(check("P6", 0.70 <= s2 <= 0.95, "spec-suite detects M2 with probability in [0.70, 0.95]"))

    print(f"\nSUMMARY: {sum(res)}/{len(res)} preregistered checks PASS")
