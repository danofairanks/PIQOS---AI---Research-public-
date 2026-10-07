#!/usr/bin/env python3
"""Static census of github.com/openai/math (pin adc7f1241). Usage: python3 -I census.py <path to clone>. stdlib + PyYAML."""
import glob, json, os, re, sys, collections
import yaml
R = sys.argv[1].rstrip('/'); L = R + '/lean/'
t = open(R + '/CONTENTS.md').read()
fams = []; cur = None
for m in re.finditer(r'\*\*(\d{3})\. (.*?)\*\* (.*?)(?:\n\n</td>)|&emsp;\[(.*?)\]\((preprints/[^)]+)\)', t, re.S):
    if m.group(1): cur = {'id': m.group(1), 'title': re.sub(r'<[^>]+>', '', m.group(2)).strip(), 'ms': []}; fams.append(cur)
    elif cur is not None: cur['ms'].append(m.group(5))
y = yaml.safe_load(open(L + 'formalization.yaml'))
ids = set(re.findall(r'id: \.\./(preprints/[^\n]+)', open(L + 'formalization.yaml').read()))
nms = sum(len(f['ms']) for f in fams); fm = sum(1 for f in fams for p in f['ms'] if p in ids)
ff = sum(1 for f in fams if any(p in ids for p in f['ms']))
print('families', len(fams), 'manuscripts', nms, '| formalized manuscripts', fm, 'families with >=1', ff)
print('formalization.yaml review/automation/scope:', y['review'], y['automation'], y['status']['scope'])
cfgs = sorted(glob.glob(L + 'ComparatorChallenges/*.json'))
ax = collections.Counter(); nanoda = collections.Counter(); thm = 0
for c in cfgs:
    d = json.load(open(c)); ax[tuple(sorted(d['permitted_axioms']))] += 1; nanoda[d.get('enable_nanoda')] += 1; thm += len(d['theorem_names'])
print('comparator configs', len(cfgs), 'theorem names', thm, 'permitted-axiom sets', dict(ax), 'nanoda', dict(nanoda))
def count(pat, root):
    n = 0
    for dp, _, fs in os.walk(L + root):
        for f in fs:
            if f.endswith('.lean') and re.search(pat, open(os.path.join(dp, f), errors='ignore').read(), re.M): n += 1
    return n
for pat in (r'\bsorry\b', r'^\s*axiom ', r'native_decide', r'ofReduceBool', r'^\s*unsafe ', r'implemented_by', r'@\[extern', r'sorryAx'):
    print('%-18s OAI/ files %d  ComparatorChallenges/ files %d' % (pat, count(pat, 'OAI'), count(pat, 'ComparatorChallenges')))
imp = re.compile(r'^\s*import\s+(\S+)', re.M)
def closure(mod, seen):
    if mod in seen or not mod.startswith('OAI'): return
    seen.add(mod)
    for m in imp.findall(open(L + mod.replace('.', '/') + '.lean').read()): closure(m, seen)
narrow = []
for c in cfgs:
    d = json.load(open(c)); ch = open(c.replace('.json', '.lean')).read()
    if 'import Mathlib\n' in ch + '\n' and re.search(r'^import Mathlib\s*$', ch, re.M): continue
    s = set(); closure(d['solution_module'], s)
    txt = ''.join(open(L + m.replace('.', '/') + '.lean').read() for m in s)
    if re.search(r'^import Mathlib\s*$', txt, re.M): continue
    if any(re.match(r'(?!OAI|Mathlib|Lean|Std|Batteries|Aesop|Qq|Plausible)', m) for m in imp.findall(txt)): continue
    narrow.append(os.path.basename(c)[:-5])
print('configs whose challenge and solution closure avoid a full `import Mathlib` and external packages:', len(narrow))
