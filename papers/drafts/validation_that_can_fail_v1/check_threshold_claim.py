"""Worked example for validation_that_can_fail_v1.md.

Illustrative claim (constructed to match a pattern common in self-published
work; it is not attributed to anyone):

    "For a recursive sequence with memory depth k, the correlation between the
     first k values and the window ending at step n decays to ~0 at n = 4k --
     and not before."

A validation that can fail needs (1) an explicit pass/fail rule fixed before
running, (2) a null process that is not supposed to show the effect, and
(3) a statement of what the rule is sensitive to.  This script does all three.

Run:  python check_threshold_claim.py        (numpy only, ~1 minute)
"""
import numpy as np

SEED, TRIALS, N, TH = 20261015, 2000, 64, 0.05
rng = np.random.default_rng(SEED)


def generate(kind, k):
    if kind == "noisy_moving_average":   # mean of last k values + small noise
        s = list(rng.standard_normal(k))
        for _ in range(k, N):
            s.append(sum(s[-k:]) / k + 0.1 * rng.standard_normal())
        return np.array(s)
    if kind == "k_step_sum":             # x_n = sum of previous k values
        s = list(rng.standard_normal(k))
        for _ in range(k, N):
            s.append(sum(s[-k:]))
        return np.array(s)
    if kind == "iid_noise":              # null: no recursion at all
        return rng.standard_normal(N)
    if kind == "ar1":                    # null: recursion with memory 1, k-independent
        s = [rng.standard_normal()]
        for _ in range(1, N):
            s.append(0.9 * s[-1] + 0.1 * rng.standard_normal())
        return np.array(s)
    raise ValueError(kind)


def mean_acf(kind, k):
    """Mean over trials of corr(first k values, window of k ending at step n), n = k..N-1."""
    rows = []
    for _ in range(TRIALS):
        s = generate(kind, k)
        ini = s[:k]
        row = []
        for n in range(k, N):
            cur = s[n - k:n]
            row.append(0.0 if ini.std() == 0 or cur.std() == 0
                       else np.corrcoef(ini, cur)[0, 1])
        rows.append(row)
    a = np.array(rows)
    return a.mean(axis=0), np.abs(a).mean(axis=0)   # index i  <->  n = k + i


def settle(m, k, th=TH):
    """First n/k after which |mean ACF| < th for every remaining n; None if never."""
    last = -1
    for i, v in enumerate(m):
        if abs(v) >= th:
            last = i
    return None if last == len(m) - 1 else (k + last + 1) / k


def claim_holds(settle_by_k):
    """Pre-stated rule: settle point == 4.0 for every k tested."""
    return all(v is not None and abs(v - 4.0) < 1e-9 for v in settle_by_k.values())


if __name__ == "__main__":
    ks = range(2, 11)
    print(f"seed={SEED} trials={TRIALS} steps={N} threshold={TH}")
    print("settle point n/k (None = never within 63 steps); claim requires 4.0 for every k\n")
    for kind in ["noisy_moving_average", "k_step_sum", "iid_noise", "ar1"]:
        res = {k: mean_acf(kind, k) for k in ks}
        sk = {k: settle(res[k][0], k) for k in ks}
        shown = "  ".join(f"k{k}:{'-' if v is None else f'{v:.2f}'}" for k, v in sk.items())
        print(f"{kind:22s} {shown}   claim_holds={claim_holds(sk)}")
        at4 = "  ".join(f"k{k}:{res[k][0][3*k]:+.3f}/{res[k][1][3*k]:.2f}" for k in ks if 4*k < N)
        print(f"{'':22s} mean ACF / mean |ACF| at n=4k -> {at4}")
    print("\nA null that 'settles' by 2k means the 'no later than 4k' observation is not")
    print("specific to the recursion.  A process whose settle point drifts with k means")
    print("there is no single threshold at 4k.")
