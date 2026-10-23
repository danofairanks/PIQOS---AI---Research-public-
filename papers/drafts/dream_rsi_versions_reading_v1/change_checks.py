"""Targeted checks of arXiv:2609.14858 v1 vs v2: presence/absence of specific strings, counts, and arithmetic.
Usage: python3 -I change_checks.py V1.pdf V2.pdf   (needs pdftotext; the PDFs are not stored here)
Expected sha256: v1 b2d13d5944d052c2b63d40e65dce116ebcc606e3b756f6acfc938afe21fe2db9 ; v2 9d632678c6c71da926ce2276e3c9d31697a5397d368bbdc4f221bd966d2e3476
Each row: label | count in v1 | count in v2 | string.  Strings are matched after whitespace normalisation, de-hyphenation and straightening of quotes."""
import re, subprocess, sys, hashlib
def load(pdf):
    h = hashlib.sha256(open(pdf, 'rb').read()).hexdigest()
    t = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
    t = t.replace('’', "'").replace('“', '"').replace('”', '"').replace('‘', "'")
    t = re.sub(r'-\n(?=[a-z])', '', t)
    return h, re.sub(r'\s+', ' ', t)
h1, a = load(sys.argv[1]); h2, b = load(sys.argv[2])
print('sha256 v1', h1); print('sha256 v2', h2)
def row(label, s, regex=False):
    f = (lambda t: len(re.findall(s, t))) if regex else (lambda t: t.count(s))
    print('%-30s v1=%-3d v2=%-3d | %s' % (label, f(a), f(b), s[:130]))
print('\n== preregistered checks (PREREG_v2_diff.md) ==')
row('C1 stamp v1', 'arXiv:2609.14858v1 [cs.CL] 14 Sep 2026'); row('C1 stamp v2', 'arXiv:2609.14858v2 [cs.CL] 6 Oct 2026')
for w in ('Limitation', 'Broader Impact', 'Ethic', 'Impact Statement', 'Safety', 'safety'): row('C2 ' + w, w)
row('C3 pkill line', 'Never execute pkill, kill, killall, or terminate unrelated processes.')
row('C3 read-only line', 'Everything else is read-only')
row('C4 boundary v1', 'Only the exploration-policy code changes; the underlying models, evaluator, and execution interfaces remain fixed')
row('C4 boundary v2', 'Only the policy code changes; the models, evaluator, and execution interfaces stay fixed')
for s in ('1.144047 1.145427', '2.635983', '3587.1 ms to 2931.0 ms', 'using only 317 discovery-agent calls, compared with 550 calls', '2.43× and 1.79×', '2.09× and 1.44×'): row('C5 headline', s)
row('C7 "release"', 'release', regex=False)
row('C7 repo link', 'github.com/zhengkid/Dream-RSI'); row('C7 site link', 'dream-rsi.com')
def pages(pdf, p0, p1):
    t = ''.join(subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), pdf, '-'], capture_output=True, text=True).stdout for p in range(p0, p1 + 1))
    t = re.sub(r'-\n', '', t); t = re.sub(r'\s+', ' ', t); i = t.find('References'); t = t[i:]
    for stop in (' A. Detailed Task Description', ' A. AI Use Statement'):
        j = t.find(stop)
        if j > 0: t = t[:j]
    return set(re.findall(r'arXiv:(\d{4}\.\d{4,5})', t))
r1, r2 = pages(sys.argv[1], 13, 16), pages(sys.argv[2], 12, 15)
print('C8 arXiv ids in the reference section: v1 %d, v2 %d ; only v1 %s ; only v2 %s' % (len(r1), len(r2), sorted(r1 - r2), sorted(r2 - r1)))
print('C6 pages: v1 36, v2 43 (from pdfinfo)')
print('\n== changes between versions ==')
row('F1 Terminal-Bench 2.1', 'Terminal-Bench 2.1'); row('F1 Opus 4.8', 'Claude Opus 4.8'); row('F1 0.7247', '0.7247'); row('F1 0.8090', '0.8090')
row('F1 comparators', 'outperforms Claude Code (0.75) and Meta-Harness (0.79) under the same evaluation setting')
row('F1 suite', 'full Terminal-Bench 2.1 (Merrill et al., 2026) suite of 89 tasks, with two independent runs per task')
row('F1 same model', 'We use Claude Opus 4.8 with Claude Code as both the discovery agent and the policydevelopment agent, while harness evaluation is also performed with Claude Opus 4.8')
row('F1 intro claim', 'improves the seed harness by over 8 points on Terminal-Bench 2.1')
row('F1 v1 abstract domains', 'Across algorithm engineering, mathematical optimization, and GPU kernel engineering')
row('F1 v1 intro domains', 'across three scientific discovery domains')
row('F2 target', 'improve the program surrounding a fixed language model, including how information is stored, retrieved, and presented during agent execution')
row('F3 comparator omitted', 'For harness optimization, we focus on end-to-end performance and omit the fixed-policy comparison due to its substantial cost: an additional full search is estimated to cost over $100,000')
row('F4 scope v1', 'Across all tasks, Dream-RSI and Recursive Fixed Exploration use the same discovery agent, evaluator, initialization, and resource constraints')
row('F4 scope v2', 'On the scientific discovery tasks, our main controlled baseline is Recursive Fixed Exploration')
row('F5 abstract v1', 'competitive or improved discovery quality while substantially reducing discovery cost in several settings')
row('F5 abstract v2', 'Across 9 tasks in 4 domains, Dream-RSI achieves competitive quality and improves discovery efficiency in several settings')
row('F5 1.7x v1', '1.7× over fixed-exploration baselines'); row('F5 50x v1', 'over 50× budget savings compared to SimpleTES')
row('F5 162x caveat v2', 'approximately 162× and 27× fewer discovery-agent calls, respectively, with lower average downstream runtime, although these comparisons use different model backbones')
row('F5 base agent', 'leaving the underlying base agent unchanged'); row('F5 coding agent v1', 'leaving the underlying coding agent unchanged')
row('F6 objective v1', 'penalizes the number of attempted generations'); row('F6 hypervolume v2', 'normalized area dominated by the quality–cost Pareto frontier')
row('F6 rho set v2', 'ρ ∈ R := {0, 0.25, 0.5, 0.75, 1}', ) if False else row('F6 rho v2', 'budget-control parameters')
row('F7 counts', 'Dream-RSI (All History) 1.90 786'); row('F7 counts', 'Current History Only 1.59 430')
row('F8 AI use', 'we use Gemini 3.1 Pro in the Section 4.1,4.2,4.3, Gemini 3.7 Flash in Section 4.3 and Claude Opus 4.8 with Claude Code in the Section4.4')
row('F8 AI use writing', 'we used Gemini 3.8 Flash for writing and grammar correction'); row('F8 reviewed', 'We have reviewed all AI-assisted work')
print('\n== keyword searches the draft relies on ==')
for w in ('held-out', 'seed', 'confidence interval', 'standard deviation', 'variance'): row('kw ' + w, w)
print('\n== arithmetic ==')
print('TB2.1 score x 178 trials (89 tasks x 2 runs): 0.7247 -> %.2f ; 0.8090 -> %.2f ; 0.75 -> %.1f ; 0.79 -> %.1f' % (0.7247 * 178, 0.8090 * 178, 0.75 * 178, 0.79 * 178))
import math
for name, v in (('Claude Code 0.75', 0.75), ('Meta-Harness 0.79', 0.79)):
    lo, hi = math.ceil((v - 0.005) * 178), math.floor((v + 0.005) * 178)
    print('%s is printed to two decimals: consistent with %d-%d passes of 178; Dream-RSI 0.8090 = 144 passes, so the gap is %d-%d trials' % (name, lo, hi, 144 - hi, 144 - lo))
print('Table 2: compute 786 vs 430 = %.2fx (%.0f%% more) ; performance 1.90 vs 1.59 = %.2fx' % (786 / 430, 100 * (786 / 430 - 1), 1.90 / 1.59))
