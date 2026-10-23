"""Verify that each string the draft quotes or counts from arXiv:2610.23839v2 occurs in the paper's text.
Usage: python3 -I quote_checks.py PAPER.pdf   (needs pdftotext; the PDF is not stored here.
Expected sha256 of the v2 PDF: f9df65e4c75059e879b7384725d8e4f6942f9335c577a94fe00cd88ea82a1bb0)
Whitespace is normalised; curly quotes are straightened.  A MISS means the draft's quote is not verbatim."""
import re, subprocess, sys, hashlib
pdf = sys.argv[1]
print('sha256', hashlib.sha256(open(pdf, 'rb').read()).hexdigest())
raw = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
t = re.sub(r'\s+', ' ', raw).replace('’', "'").replace('“', '"').replace('”', '"')
Q = [
 'correlated AI perspectives, not three independent expert opinions',
 'The current panel uses separate prompts to the same model family',
 'it remains pending',
 'Prompt-role agreement alone does not establish validity',
 'descriptive percentages without significance tests',
 'they do not identify internal model knowledge cutoffs',
 'a retrospective maximum over final-snapshot scores is monotone by construction and cannot demonstrate learning',
 'frozen internal protocol conventions, not empirically established optimal weights',
 'The hypothesis profile uses eight dimensions: importance, novelty, grounding, falsifiability, data resolvability, feasibility, alternatives, and actionability. Their weights are 20, 20, 15, 10, 10, 10, 10, and 5',
 'largely outperform GPT-6 with 2.5% and Claude Opus 5 with 2.3%',
 'Preliminary human assessments show',
 'Empirical evidence for learning from scientific research',
 'Expert-supervised assessment shows greater human-rated improvement along research paths',
 'The overall numerator and denominator are 74/1,176',
 'DeepSeek (14/257), GLM (1/36), GPT (59/2,341), and Claude (3/131)',
 'Only 15 of its 131 proposals pass the retrieval gate (11.5%), compared with 355 of 1,176 for DiscoveryRSI27B (30.2%)',
 'the positive-judgment fractions are similar: 20.0% and 20.8%',
 "Claude's median proposal length is 41,134 characters, while retrieval uses the first 6,000 characters and the semantic audit sees the first 2,500",
 'GPT-6 Luna supplied the semantic judgments, with 145 successful judgments from 149 sampled records',
 'propagated to 903 registered hypothesis versions',
 'The resulting labels are correlated automated assessments rather than independent expert reviews',
 'from 1 April 2025 through 14 October 2026',
 'Qwen (April 2025, a provisional family proxy), Claude Opus 5 (May 2026)',
 'Prospective tracking is needed to determine whether researchers adopt these hypotheses',
 'The assessment involved 27 medical doctors, medical students and bioscience PhD students',
 'The review cohort contains 292 proposals from six dataset groups',
 'under three senior supervisors',
 'Falsifiability rises from 4.00 to 6.20, consideration of alternative explanations from 4.44 to 5.98, data resolvability from 3.73 to 4.99, and feasibility from 4.79 to 5.87',
 'importance declines from 6.48 to 6.04 and novelty from 4.87 to 4.58',
 'The observed improvement therefore concerns investigation design more strongly than the perceived significance or originality of research questions',
 'The additional gain decreases from 0.32 in the first round to 0.21 in the second',
 '4.86 for the base model to 5.18 after the first research round and 5.39 after the second',
 'We train for one epoch',
 'accept on dev set',
 '41% of revisions improve the mean human score, 47% leave it unchanged, and 12% reduce it',
 'The corresponding proportions are 31%, 37%, and 32% for GPT-5.6 Sol, and 25%, 44%, and 31% for GPT-6 Luna',
 'DiscoveryRSI-27B scores higher than GPT-6 Luna on importance (3.10 versus 2.94) and plausible, evidence-bounded claims (3.37 versus 3.16)',
 'Both receive 2.31 for advance over known work, while GPT-6 Luna scores higher on data fit, alternative explanations, and informative results',
 'Clinical and population health 13 557 2.3% Therapeutic target prioritization 30 178 16.9% Disease mechanisms 17 251 6.8% Population multi-omics 14 190 7.4% Total 74 1,176 6.3%',
 'Clinical & population health 2.3% 5.2% 5.9% 2.3% 4.4%',
 'DiscoveryRSI 27B DeepSeek GLM GPT Claude',
 'Group sizes and domain composition differ, and some strata are small',
 'Automated quality evaluation covers 241 research questions across the four domains using GPT-5.6 Sol as the judge',
 'Behavioral analysis examines six campaigns of 20 episodes per evaluated model variant',
 'substantive progress on 214 of 366 transitions',
 'Reviewer bias, scientific uncertainty, and dependence between repeated critiques are not fully represented',
 '2,397 agent trajectories',
 'Improvements concentrate on the specification of testable investigations',
 'fresh questions for rediscovery',
 'Definition 1 (Valuable and testable research hypothesis)',
 'a research hypothesis is represented as H = ( 𝑐, 𝜋, 𝑑, 𝑎)',
 'using Qwen3.8-27B as initialization',
 'Group sizes and domain composition differ, and some strata are small',
 'from 4.86 for the base model to 5.39 after two rounds of self-improvement',
 'a 6.3% rate of hypothesis correspondence with research published after the model cutoff',
 'Absolute quality ratings show a mixed profile',
 'DeepSeek V4.1 (September 2026, a release-month proxy), and GLM-5.3 (August 2026, a releasemonth proxy)',
 'DFM-Bench evaluates five objects: individual hypotheses, revisions, development paths, research runs, and scientific contributions',
]
miss = 0
for q in Q:
    n = len(re.findall(re.escape(q), t))
    miss += n == 0
    print(('OK  ' if n else 'MISS'), n, q[:110])
print('MISSES:', miss, 'of', len(Q))
# strings that should be ABSENT (keyword searches the draft relies on)
for w in ['inter-rater', 'kappa', 'Krippendorff', 'Cohen', 'self-preference', 'seed', 'disjoint', 'Limitations section']:
    print('absent-check', repr(w), len(re.findall(w, t, re.I)))
