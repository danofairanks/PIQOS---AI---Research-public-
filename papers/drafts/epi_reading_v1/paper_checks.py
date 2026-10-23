"""Checks on arXiv:2610.24944v1 ("Epi: Towards a Persistent, Self-Improving Agent for Autonomous Research").
Usage: python3 -I paper_checks.py PAPER.pdf   (needs pdftotext; the PDF is not stored here).
Expected sha256 of the v1 PDF: 0ddaa6e7f1f2729204f3ee6a5ad291b44593191a3219771ce63cf2a4b865480b
Part A verifies that each string the draft quotes occurs verbatim; part B recomputes arithmetic from numbers printed in the paper."""
import re, subprocess, sys, hashlib, itertools, math
from collections import Counter
pdf = sys.argv[1]
print('sha256', hashlib.sha256(open(pdf, 'rb').read()).hexdigest())
raw = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
t = re.sub(r'\s+', ' ', raw).replace('’', "'").replace('“', '"').replace('”', '"')
print('== A. quotes and counts present in the paper text ==')
Q = [
 'Épi produced 120 record-setting results, comprising 20 numerical bound records across 12 families and 100 construction records across eight families',
 'We count one final result per distinct instance or parameter setting',
 'Multiple parameter settings within a family count separately; repeated improvements to the same setting count once',
 'All record comparisons are based on literature and registry references available as of September 16, 2026',
 'Some evolving registries already list the new results. Our tables retain the earlier values used for comparison so the improvement remains traceable after those updates',
 'Of the 100 construction records, 97 concern geometric packing',
 'a fixed verifier evaluates their outputs',
 'We use a different model for an independent review and record the reviewer\'s identity',
 'research on reward hacking further motivates checking whether a score increase reflects the intended task',
 'Independent review and extra validation are optional in Épi-turbo. On short tasks, their cost was larger than their benefit in our tests. Both components were off in the runs below',
 'The baseline is Codex (OpenAI, 2026), a widely used coding agent, with GPT-6-Astra as its model. Épi-turbo uses the same model with the same reasoning effort',
 'We selected 30 tasks that were new to both systems. We took them in the official hardness order of the benchmark and excluded tasks with unreliable reference values',
 'We did one run for each task and system, so we do not report statistical significance',
 'The reference values come from a commercial solver, and some of them are weak',
 'Thus we also compare the two systems on each instance directly, with their objective values only',
 'It counts only when the solution is within 1% of the reference value',
 'Épi-turbo gets the higher total score, 53.96 against 51.21. It has the higher score on 18 tasks, and Codex has the higher score on 12. On 10 of these tasks, the difference is less than 0.01',
 'On the 18 tasks where Épi-turbo is higher, the total gain is 4.54. On the other 12 tasks, the total loss is 1.79',
 'The higher score comes mainly from the speed term',
 'Mean quality term 1.030 1.032 Mean speed term 0.784 0.675',
 'Instances with the better solution (119 comparable, 40 ties) 18 61',
 'Instances more than 1% worse than the other system 29 10',
 'Infeasible solutions (120 held-out runs) 1 0',
 'On the 13 tasks of the hard split, Épi-turbo has the higher score on 9 tasks, and its total score is 10% higher',
 'Codex used more than 30 minutes on 17 of the 120 held-out runs, in 7 tasks',
 'Zeng (2026) proved the conjecture for |C | = 8 and at most two types',
 "Zeng's multiplicity-truncation lemma (Zeng, 2026) preserves both",
 'Another 277 satisfy Zeng\'s maximum-cut criterion',
 'The remaining 560 profiles are covered by exact certificates containing 18,444 integer boxes',
 'We ran Épi over a few days using OpenAI frontier models (GPT-5.6 Sol and GPT-6-Astra)',
 'The interval width decreases from 3.30 × 10−7 to approximately 3.94 × 10−9 , a factor of approximately 84',
 'The relative separations, Ld /Ud − 1, are approximately 0.35% and 1.92%',
 'discrepancy exactly 5',
]
miss = 0
for q in Q:
    n = len(re.findall(re.escape(q), t)); miss += n == 0
    print(('OK  ' if n else 'MISS'), n, q[:100])
print('MISSES:', miss, 'of', len(Q))
for w in ['ablat', 'human review', 'human expert', 'domain expert', 'Limitations', 'confidence interval', 'seed']:
    print('absent-check', repr(w), len(re.findall(w, t, re.I)))
print('\n== B. arithmetic on printed numbers ==')
# B1 Spencer matrix: read the 8x8 block from Figure 5's text layer
i = t.find('Spencer discrepancy -1')
nums = [int(x) for x in re.findall(r'-?\d+', t[i:i + 400].replace('Spencer discrepancy', ''))[:64]]
A = [nums[r * 8:(r + 1) * 8] for r in range(8)]
print('B1 matrix read from the text layer:'); [print('  ', row) for row in A]
vals = Counter(max(abs(sum(a * e for a, e in zip(row, eps))) for row in A) for eps in itertools.product((-1, 1), repeat=8))
print('   row-maximum norm over all 256 sign vectors:', dict(sorted(vals.items())), ' minimum =', min(vals))
# B2 Cohn-Elkies separations (Table 2)
print('B2 Cohn-Elkies: L/U - 1')
for d, L, U in ((10, 0.056433853144, 0.05623600), (11, 0.057731808202, 0.05664550)):
    print(f'   d={d}: {100*(L/U-1):.3f}%')
# B3 interval ratios
print('B3 n-queens: widths 3.30e-7 -> 3.94e-9, ratio %.1f ; from endpoints in eq. (4): new width %.3e' % (3.30e-7 / 3.94e-9, 1.9440010262694 - 1.9440010223327))
print('   quartic dimension: 7.80e-3 -> 2.13e-9, ratio %.3e (paper: more than 3.6 million)' % (7.80e-3 / 2.13e-9))
# B4 Table 3
print('B4 Table 3 (30 tasks)')
E_tot, C_tot = 53.96, 51.21
print('   total gap %.2f (%.2f%%); gains - losses = 4.54 - 1.79 = %.2f' % (E_tot - C_tot, 100 * (E_tot / C_tot - 1), 4.54 - 1.79))
print('   cost ratio 7.30/11.35 = %.3f ; instance counts 18 + 61 + 40 ties = %d (paper: 119 comparable instances of 120 held-out runs; one infeasible)' % (7.30 / 11.35, 18 + 61 + 40))
for name, tot, q, s in (('Codex', C_tot, 1.032, 0.675), ('Epi-turbo', E_tot, 1.030, 0.784)):
    mean = tot / 30; sm = q + s
    # each printed mean carries +-0.0005, so the sum of two means carries at most +-0.001 per task, i.e. +-0.03 points on a 30-task total
    print(f'   {name}: quality+speed = {sm:.3f} ; total/30 = {mean:.4f} ; difference x30 = {30*(sm-mean):+.2f} points ; rounding allows at most +-0.03')
# B5 Tuza profile count
print('B5 Tuza: three distinct neighbourhood types over an 8-clique, each of size >= 2, up to clique relabelling and type permutation')
pats = list(itertools.product((0, 1), repeat=3))
def canon(ms):
    return min(tuple(sorted(tuple(p[i] for i in perm) for p in ms)) for perm in itertools.permutations(range(3)))
seen = set(); nested = set()
for ms in itertools.combinations_with_replacement(pats, 8):
    cols = [frozenset(i for i, p in enumerate(ms) if p[c]) for c in range(3)]
    if any(len(s) < 2 for s in cols) or len(set(cols)) < 3: continue
    k = canon(ms); seen.add(k)
    S = sorted(cols, key=len)
    if all(S[a] <= S[a + 1] for a in range(2)): nested.add(k)
print('   profiles:', len(seen), '; nested:', len(nested), '(paper: 872 and 35)')
