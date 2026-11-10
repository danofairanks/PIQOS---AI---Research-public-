"""TCSExam Appendix A / E.1 contamination read: source years of the 20 theorem tasks (Appendix A.1) against per-theorem outcomes (Table 12) and per-attempt resource use (Table 11). Run: python3 -I checks_appendixA.py"""
import math
# (theorem index per Table 12, source year from Appendix A.1, Astra success /1, K3.1 Pro successes /3, K3 /3)
rows = [(1,2025,0,0,0),(2,2026,1,3,3),(3,2024,1,2,2),(4,2026,1,2,0),(5,2026,1,0,0),(6,2026,1,3,0),(7,2025,0,0,0),(8,2024,0,3,0),(9,2025,1,3,0),(10,2025,1,0,0),
        (11,2023,1,0,0),(12,2024,0,0,0),(13,2024,1,0,0),(14,2026,1,0,0),(15,2023,1,3,0),(16,2024,0,0,0),(17,2024,1,1,0),(18,2025,1,0,0),(19,2026,1,3,2),(20,2023,0,0,0)]
by = {}
for i, y, a, k31, k3 in rows: by.setdefault(y, []).append((a, k31, k3))
print("== C1 theorem tasks by source year; solved by Astra (1 attempt) / tasks; K3.1 Pro tasks solved at least once; K3 tasks solved at least once")
for y in sorted(by):
    v = by[y]; print(f"  {y}: {len(v)} tasks | Astra {sum(x[0] for x in v)}/{len(v)} | K3.1 Pro {sum(1 for x in v if x[1] > 0)}/{len(v)} | K3 {sum(1 for x in v if x[2] > 0)}/{len(v)}")
new = [r for r in rows if r[1] == 2026]; old = [r for r in rows if r[1] < 2026]
print("  Astra: 2026-sourced", sum(r[2] for r in new), "/", len(new), "; 2023-2025-sourced", sum(r[2] for r in old), "/", len(old))
n, K, k = 20, 14, 6   # 14 solved of 20; probability that the 6 newest are all among the solved
p = math.comb(K, k) / math.comb(n, k)
print(f"  chance that all six 2026-sourced tasks fall among Astra's 14 solved (hypergeometric) = {p:.3f}; two-sided Fisher is larger; the direction (newer sources solved more often) is the opposite of a simple age-based contamination pattern, at n = 20")
print("  K3.1 Pro: solved at least once:", sum(1 for r in rows if r[3] > 0), "of 20; 2026-sourced", sum(1 for r in new if r[3] > 0), "/6; 2023-2025", sum(1 for r in old if r[3] > 0), "/14")
print("== C2 theorem-track resource per attempt (Table 11, bare theorems): input tokens (M), output tokens (k), hours")
t11 = {"GPT-6 Astra": (6.51, 91.1, 0.68), "Kimi K3.1 Pro": (253.45, 1101.9, 4.90), "Kimi K3": (183.66, 1599.8, 9.32), "GLM-5.3": (29.34, 586.0, 4.26), "Qwen3.8 Max (0902)": (43.03, 655.3, 8.22), "Grok 4.6": (93.06, 478.6, 3.28), "DeepSeek V4.1 Flash 0910": (15.48, 553.5, 1.24), "DeepSeek V4.1 Flash 1017": (189.86, 1581.8, 2.91)}
for a, v in t11.items(): print(f"  {a:26s} {v}")
print("  max/min ratios: input tokens", round(max(v[0] for v in t11.values()) / min(v[0] for v in t11.values()), 1), "; output tokens", round(max(v[1] for v in t11.values()) / min(v[1] for v in t11.values()), 1), "; hours", round(max(v[2] for v in t11.values()) / min(v[2] for v in t11.values()), 1), "(all under the same 12-hour cap)")
