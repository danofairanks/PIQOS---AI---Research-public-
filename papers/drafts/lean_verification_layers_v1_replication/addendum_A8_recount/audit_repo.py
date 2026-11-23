#!/usr/bin/env python3 -I
"""Recount audit of the public Lean repository linked from the verified-debate note.
Usage: python3 -I audit_repo.py PATH_TO_FETCHED_REPO   (a directory holding MANIFEST.tsv, ISSUES.md, lean/**)
Standard library only. Reads files; runs no Lean. Fetch the files first (raw.githubusercontent.com), retrying on 'Rate limit' pages."""
import csv, json, hashlib, os, re, sys, collections
root = sys.argv[1]; os.chdir(root)
rows = list(csv.DictReader(open('MANIFEST.tsv'), delimiter='\t'))
files = sorted({r['lean_file'] for r in rows})
rl = [f for f in files if 'Rate limit' in open(f, encoding='utf-8', errors='replace').read(400)]
print('manifest rows', len(rows), dict(collections.Counter(r['status'] for r in rows)), '| sources', len(files), '| rate-limit pages in fetched set', len(rl))
sha = {f: hashlib.sha256(open(f, 'rb').read()).hexdigest() for f in files}
print('folder-name suffix != source sha prefix:', sum(1 for f, h in sha.items() if not f.split('/')[-2].endswith(h[:12])))
rec = {p.strip(): json.load(open(p.strip())) for p in open('receipts.txt') if p.strip()}
print('receipts', len(rec), 'exit codes', dict(collections.Counter((r.get('compiled'), r.get('exit_code')) for r in rec.values())))
def flat(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from flat(v)
    elif isinstance(o, list):
        for v in o: yield from flat(v)
def axl(r):
    out = '\n'.join(flat(r)); d = {}
    for m in re.finditer(r"'([^']+)' depends on axioms: \[(.*?)\]", out, flags=re.S):
        d[m.group(1)] = {a.strip() for a in m.group(2).replace('\n', ' ').split(',')}
    for m in re.finditer(r"'([^']+)' does not depend on any axioms", out): d[m.group(1)] = set()
    return d
def shaok(r, f):
    s = r.get('source_sha256'); return (sha[f] in s.values()) if isinstance(s, dict) else s == sha[f]
std = {'Classical.choice', 'Quot.sound', 'propext'}
res = collections.Counter(); unsup = []
for x in rows:
    f, decl, st = x['lean_file'], x['declaration'], x['status']; d = os.path.dirname(f)
    cands = [r for p, r in rec.items() if os.path.dirname(p) == d and shaok(r, f)]; ok = False
    for r in cands:
        a = axl(r); keys = [k for k in a if k == decl or decl.endswith('.' + k.split('.')[-1]) or k.endswith('.' + decl.split('.')[-1])]
        if st == 'checked' and r.get('exit_code') == 0 and keys and all(a[k] <= std for k in keys): ok = True; break
        if st.startswith('accepted') and keys and all(a[k] <= std for k in keys): ok = True; break
        if st == 'in a checked file': ok = True; break
    res[(st, ok)] += 1
    if not ok: unsup.append((st, decl))
print('declaration support by a hash-matching receipt:', dict(res)); print(' unsupported:', unsup[:6])
nopass = [f for f in files if not any(r.get('exit_code') == 0 and shaok(r, f) for p, r in rec.items() if os.path.dirname(p) == os.path.dirname(f))]
print('sources with no hash-matching exit-0 receipt:', len(nopass))
pat = {'sorry': r'\bsorry\b', 'declared assumption (Lean keyword)': r'^\s*axiom\s', 'native_decide': r'native_decide', 'opaque': r'^\s*opaque\s', 'unsafe': r'\bunsafe\b', 'maxHeartbeats': r'maxHeartbeats'}
cnt = collections.Counter(); fw = collections.defaultdict(set); lines = nb = 0; dist = set()
for f in files:
    for l in open(f, encoding='utf-8', errors='replace'):
        lines += 1; t = l.strip(); code = l.split('--')[0]
        if t and not t.startswith('--'): nb += 1; dist.add(t)
        for k, p in pat.items():
            if re.search(p, code): cnt[k] += 1; fw[k].add(f)
print('source lines', lines, '| non-blank non-comment', nb, '| distinct stripped', len(dist))
print('pattern counts (lines, files):', {k: (cnt[k], len(fw[k])) for k in pat})
sa = [(p, k) for p, r in rec.items() for k, v in axl(r).items() if 'sorryAx' in v]
print('receipts printing sorryAx:', len(sa), sorted({os.path.dirname(p).split('/')[-1] for p, k in sa}))
t = open('ISSUES.md').read()
print('ISSUES.md: issue sections', len(re.findall(r'^### Issue \d+', t, flags=re.M)))
