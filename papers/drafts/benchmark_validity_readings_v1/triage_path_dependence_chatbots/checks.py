"""Arithmetic behind the reading of arXiv 2611.09647v1 (path-dependent triage). Every number is typed from the paper's text, tables and supplement and recomputed here.
Run: python3 -I checks.py   (needs scipy)"""
import math
from scipy import stats
print("== C1 headline contrast")
print(f"  20.3 / 5.6 = {20.3/5.6:.2f} ('nearly four times')")
print(f"  share of the gap removed by the matched single message: (20.3-12.1)/(20.3-5.6) = {(20.3-12.1)/(20.3-5.6):.3f}; remaining {(12.1-5.6)/(20.3-5.6):.3f}")
print(f"  context-source ablation (Fig. S6): full transcript re-issued 22.7 -> questions removed 18.9 = {22.7-18.9:.1f} points of the {22.7-12.1:.1f} to the matched message = {(22.7-18.9)/(22.7-12.1):.2f} (comparison across separate analyses)")
print("== C2 per-model heterogeneity (emergency under-triage 3.6% to 82.1% across 13 chatbots)")
print(f"  equal-weight mean excluding the worst model, approximate: (20.3*13 - 82.1)/12 = {(20.3*13-82.1)/12:.1f}")
print("== C3 independence of the headline test")
print("  emergency cases 28 x 13 chatbots =", 28 * 13, "pairs possible; analysed 354; cases repeat across chatbots, chatbots repeat across cases")
print("== C4 sample arithmetic")
print("  completed conversations 11*112 + 109 + 110 =", 11 * 112 + 109 + 110, "(stated 1451); planned 13*112 =", 13 * 112)
print("== C5 clinician consensus (Table S10): 62 clear of 112 =", f"{62/112:.3f}", "; clear D labels 29 vs 28 prespecified D")
print("== C6 per-model turn-10 mean error and accuracy for the three chatbots at 3.6% emergency under-triage (Table S5)")
for m, e, a, ch in [("GPT-5.4", 0.54, 45.5, -2.7), ("GPT-5", 0.46, 50.0, 4.5), ("Claude Sonnet 4.6", 0.38, 61.6, 24.1)]:
    print(f"  {m:18s} mean error {e:+.2f} macro accuracy {a:.1f}% change over turns {ch:+.1f} points")
print("  Claude Opus 4.6 turn-1 macro accuracy 4.5% against 25% chance for four levels")
