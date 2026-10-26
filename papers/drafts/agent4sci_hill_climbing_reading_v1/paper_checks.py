"""Verbatim checks of the draft's quotes and printed numbers against the arXiv 2610.28763v1 text layer.
Run: python3 -I paper_checks.py /path/to/2610.28763v1.pdf     (needs pdftotext; the PDF is not stored here)
Part A: the 20x4 delta% values of Table 2 as transcribed in recompute_table2.py equal the printed ones.
Part B: each quoted string or printed count in the draft occurs in the paper text (whitespace-normalised).
Part C: derived claims the draft makes about the paper (counts it infers) are re-derived from printed numbers."""
import hashlib, re, subprocess, sys, ast
pdf = sys.argv[1]
EXPECT = "d329c1a5dfd6ff3a6820f083ee39196f1caf84be4111af46c1cd0e4e5dbd57ba"
sha = hashlib.sha256(open(pdf, "rb").read()).hexdigest()
print("pdf sha256", sha, "MATCH" if sha == EXPECT else "MISMATCH")
raw = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
norm = re.sub(r"\s+", " ", raw)
# ---- Part A
src = open("recompute_table2.py").read()
arr = {k: ast.literal_eval(re.search(rf"^{k}\s*=\s*(\[.*?\])", src, re.M).group(1)) for k in ("opus", "opus_s", "codex", "codex_s")}
names = "ATAT CarbonGlobe CheMixHub CosmoBench DART-Eval ESCAPE GEO-Bench-2 gRNAde GTPBD LITHOS Mars-Bench MassSpecGym MOTIVE NeuroGraph PFDelta ProteinGym SR-CACO-2 TIDMAD TreeFinder UniSite".split()
printed = {}
for line in raw.splitlines():
    f = line.split()
    if f and f[0] in names and len(f) >= 9:
        nums = [x for x in f if re.fullmatch(r"-?\d+(?:\.\d+)?", x)]
        if len(nums) >= 9 and f[0] not in printed:  # first occurrence in the text = Table 2 (page 8)
            printed[f[0]] = [float(x) for x in nums[-9:]]
bad = 0
for i, n in enumerate(names):
    if n not in printed: print("Part A MISSING row", n); bad += 1; continue
    p = printed[n]  # [base, opus_abs, opus_d, os_abs, os_d, cx_abs, cx_d, cxs_abs, cxs_d]
    got = [p[2], p[4], p[6], p[8]]
    want = [arr["opus"][i], arr["opus_s"][i], arr["codex"][i], arr["codex_s"][i]]
    if got != want: print("Part A MISMATCH", n, got, want); bad += 1
print(f"Part A: {len(names)-bad}/{len(names)} Table 2 rows match the transcription")
# ---- Part B
checks = [
 "bag of ML-engineering tricks", "Plug-in skills nearly double the mean improvement",
 "the comparable proportional gain on Codex suggests the design generalizes", "auto-engineering, not auto-research",
 "20 benchmarks across 11 domains", "8 × H200 GPUs · 12-hour wall-clock budget",
 "5 of 12 tasks exhibit one or more severe evaluation-gaming behaviors", "40 trajectories in total",
 "each with three auditors from different model families", "five pilot-study trajectories with known evaluation gaming",
 "We manually inspect 15 audit reports sampled from the main experiments",
 "the best agent on 9 of 20 benchmarks, versus 6 for Opus", "more than 10× over the reproduction baseline",
 "All agents used to assist benchmark selection and standardization are Claude Opus 4.6",
 "Fixed hyperparameters only 10", "ATAT 0.8 0.5 0.9 -0.3 0.5 ± 0.5 0.2", "CheMixHub 11.9 12.4 10.7 11.3 11.6 ± 0.7 1.4",
 "PFDelta 64.4 65.3 32.5 29.4 47.9 ± 19.6 4.6", "DART-Eval 6.1 5.8 6.4 6.2 6.1 ± 0.3 2.7", "TIDMAD 7.4 7.7 7.1 7.8 7.5 ± 0.3 3.5",
 "Average ∆% 10.4 20.1 4.4 8.1", "A.6 Absence of a Human-Researcher Baseline", "A.5 Potential Overfitting of Plug-in Skills",
 "A.2 Single-Agent Harness Coverage", "we treat AGENT 4S CI as a discovery probe rather than a leaderboard",
]
miss = [c for c in checks if re.sub(r"\s+", " ", c) not in norm]
print(f"Part B: {len(checks)-len(miss)}/{len(checks)} quoted strings and printed counts found" + ("" if not miss else "; MISSING: " + "; ".join(miss)))
# ---- Part C
half_runs = 40; total_runs = 2 * half_runs
print(f"Part C: re-audit of half of each agent's runs = 40 trajectories -> {total_runs} main runs; 4 agents x 20 benchmarks = {4*20}: {'consistent' if total_runs == 4*20 else 'inconsistent'}")
print("Part C: 3 auditors x 40 trajectories =", 3 * 40, "audit reports")
# ---- Part D: absence claims, by keyword search of the text layer (a search is not a reading; figures are text only)
absent = ["placebo", "per-skill", "skill ablation", "held-out benchmark", "expert rat", "human rat", "inter-rater", "Cohen"]
found = {k: len(re.findall(k, norm, re.I)) for k in absent}
print("Part D: keyword counts for terms the draft says are absent:", found)
print("Part D: 'ablat' occurs", len(re.findall("ablat", norm, re.I)), "times (the HPO-only ablation, Table 6); 'word cloud' occurs", len(re.findall("word cloud", norm, re.I)), "time(s)")
