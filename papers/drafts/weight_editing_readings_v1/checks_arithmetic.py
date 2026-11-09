"""Arithmetic behind the readings; every number is typed from the cited source and recomputed here. Run: python3 -I checks_arithmetic.py (needs scipy)."""
import math
from scipy import stats
print("== Post: edit vs original on two coding benchmarks (counts back-computed from stated percentages)")
for name, n, pcts in (("MBPP+", 378, (59.5, 57.4, 64.6)), ("HumanEval+", 164, (65.2, 61.6, 68.3))):
    ints = [round(x / 100 * n) for x in pcts]
    print(f"  {name} n={n}: counts {ints}; back-percent {[round(i / n * 100, 1) for i in ints]} (stated {list(pcts)})")
net = (244 - 225) + (112 - 107)
print("  net edit minus original:", net, "; fixed minus broken:", 40 - 16)
p = stats.binomtest(40, 56, 0.5).pvalue
print(f"  exact two-sided sign test 40 vs 16: p = {p:.4f}; Bonferroni x4 = {min(1, 4 * p):.4f}; Sidak (4) = {1 - (1 - p) ** 4:.4f}")
print("  fixed share of the 56 discordant items:", round(40 / 56, 3))
print("== Othello Elo claims (typed from the post and the author's reply)")
elo = lambda s: 400 * math.log10(s / (1 - s))
print("  4,926 openings x 2 colours =", 4926 * 2, "games; 52.3% -> Elo", round(elo(.523), 1))
for g, lab in ((9852, "9,852 games"), (2 * 3581, "7,162 games (3,581 pairs)")):
    se = math.sqrt(.523 * .477 / g)
    print(f"  95% interval for 52.3% over {lab}: {.523 - 1.96 * se:.3f}-{.523 + 1.96 * se:.3f} -> Elo {elo(.523 - 1.96 * se):+.1f} to {elo(.523 + 1.96 * se):+.1f}")
print("  games needed to resolve +16 Elo at 95% (fixed sample, two-sided):", round((347.4 * 1.96 / 16) ** 2))
print("== Developer post: weather AUC and test-set precision (counts from the shipped data file: 1,220 test city-days, 373 rain)")
n1, n0 = 373, 1220 - 373
for auc in (0.809, 0.839, 0.747, 0.719):
    q1 = auc / (2 - auc); q2 = 2 * auc * auc / (1 + auc)
    se = math.sqrt((auc * (1 - auc) + (n1 - 1) * (q1 - auc ** 2) + (n0 - 1) * (q2 - auc ** 2)) / (n1 * n0))
    print(f"  AUC {auc}: Hanley-McNeil 95% half-width {1.96 * se:.3f}")
print("  share of the gain over persistence recovered by the zero-label model:", round((0.809 - 0.719) / (0.839 - 0.719), 2))
print("== Adaptive-agent paper (arXiv 2605.20189v1) Table 1 averages")
T = {"LoRA": [47.4, 39.7, 14.7, 26.3, 51.5, 15.6, 6.8, 20.3, 39.5, 29.8], "TTL": [24.4, 24.7, 44.4, 25.9, 51.9, 23.5, 19.7, 26.2, 34.9, 29.7],
     "DOM": [56.5, 38.9, 33.2, 28.3, 18.8, 17.7, 2.6, 24.7, 51.3, 31.6], "DnD": [70.9, 48.1, 51.9, 26.5, 47.8, 20.8, 24.1, 21.0, 33.5, 29.1],
     "SOLAR": [74.7, 55.5, 58.8, 48.3, 60.1, 30.3, 24.5, 25.1, 55.0, 35.6]}
for m, v in T.items(): print(f"  {m:6s} in-domain {sum(v[:5]) / 5:.1f}  out-of-domain {sum(v[5:]) / 5:.1f}")
print("  cells at or below chance (BoolQ 50, PIQA 50, 4-way 25):", [(m, c, x) for m, v in T.items() for c, x, ch in zip(["ARC-e", "ARC-c", "BoolQ", "HellaSwag", "PIQA"], v[:5], [25, 25, 50, 25, 50]) if x <= ch + 1])
print("== Vendor model card: perplexity arithmetic (typed from the 6.9B card)")
print("  9.0508/8.7188 =", round(9.0508 / 8.7188, 5), "-> +", round((9.0508 / 8.7188 - 1) * 100, 2), "%; ln =", round(math.log(9.0508 / 8.7188), 5), "(card: paired delta-NLL +0.03737)")
print("  738,197,504 trainable parameters = 11 layers x", 738197504 // 11, "(= 16,384 x 4,096:", 16384 * 4096, ")")
print("  facts 'genuinely added': by prefix 499-1 =", 499 - 1, "; by anywhere 499-9 =", 499 - 9)
print("== Math-model edit (MIT release): bootstrap numbers are in the entry; shares typed from the release table")
print("  50-pass run: MATH-500 7.9 -> 48.1 = +", round(48.1 - 7.9, 1), "points; GSM8K 13.8 -> 67.1 = +", round(67.1 - 13.8, 1))
