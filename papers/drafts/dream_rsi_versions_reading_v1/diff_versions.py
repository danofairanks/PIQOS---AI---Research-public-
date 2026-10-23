"""Word-level diff of arXiv:2609.14858 v1 vs v2.
Usage: python3 -I diff_versions.py V1.pdf V2.pdf OUT_BLOCKS.txt   (needs pdftotext; the PDFs are not stored here)
Expected sha256: v1 b2d13d5944d052c2b63d40e65dce116ebcc606e3b756f6acfc938afe21fe2db9 ; v2 9d632678c6c71da926ce2276e3c9d31697a5397d368bbdc4f221bd966d2e3476
Text is extracted with pdftotext (reading order), page-header lines and bare page numbers removed, hyphenation joined,
curly quotes straightened, whitespace collapsed; then difflib.SequenceMatcher over word lists (autojunk off).
Math glyph rendering differs between builds, so blocks that differ only in symbols are expected; blocks of fewer than MINW words are counted, not listed."""
import re, subprocess, sys, hashlib, difflib
MINW = 12
def load(pdf):
    h = hashlib.sha256(open(pdf, 'rb').read()).hexdigest()
    t = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
    t = t.replace('Dream-RSI: Recursive Self-Improvement through Evolving Worlds', ' ')
    t = re.sub(r'(?m)^\s*\d{1,2}\s*$', ' ', t)
    t = re.sub(r'-\n(?=[a-z])', '', t)
    t = t.replace('’', "'").replace('“', '"').replace('”', '"').replace('‘', "'")
    t = re.sub(r'\s+', ' ', t).strip()
    return h, t.split(' ')
h1, a = load(sys.argv[1]); h2, b = load(sys.argv[2])
print('sha256 v1', h1); print('sha256 v2', h2)
print('words v1', len(a), 'v2', len(b))
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
print('similarity ratio %.4f' % sm.ratio())
ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
ins = sum(j2 - j1 for t, i1, i2, j1, j2 in ops if t in ('insert', 'replace'))
dele = sum(i2 - i1 for t, i1, i2, j1, j2 in ops if t in ('delete', 'replace'))
print('changed blocks', len(ops), '; words in v2 not matched', ins, '; words in v1 not matched', dele)
big = [o for o in ops if max(o[2] - o[1], o[4] - o[3]) >= MINW]
print('blocks with >=%d words on either side: %d' % (MINW, len(big)))
with open(sys.argv[3], 'w') as f:
    for n, (t, i1, i2, j1, j2) in enumerate(big, 1):
        f.write('--- block %d  %s  v1[%d:%d] (%d words) -> v2[%d:%d] (%d words)\n' % (n, t, i1, i2, i2 - i1, j1, j2, j2 - j1))
        f.write('v1: ' + ' '.join(a[i1:i2])[:700] + '\n')
        f.write('v2: ' + ' '.join(b[j1:j2])[:700] + '\n\n')
print('blocks written to', sys.argv[3])
