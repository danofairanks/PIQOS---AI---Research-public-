"""Compare the authors' project site and repository README with the two paper versions.  Standard library + git.
Usage: python3 -I site_repo_check.py        (live fetch: the site may change; the output file records what was seen on the date it was run)
The site is fetched with a plain GET (User-Agent research-check/1.0); the README as a single file at the pinned commit; refs by git ls-remote."""
import re, html, subprocess, hashlib, urllib.request
def get(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'research-check/1.0'}), timeout=30).read()
    return r
site = get('https://dream-rsi.com')
print('site sha256', hashlib.sha256(site).hexdigest(), 'bytes', len(site))
x = site.decode('utf-8', 'replace')
x = re.sub(r'<script.*?</script>|<style.*?</style>', '', x, flags=re.S)
x = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x)))
readme = get('https://raw.githubusercontent.com/zhengkid/Dream-RSI/4149ea9181ab1db80f85717ffda2c9f0f130e85b/README.md').decode()
rd = re.sub(r'\s+', ' ', readme)
def cnt(label, text, s): print('%-9s %-3d | %s' % (label, text.count(s), s))
for lab, tx in (('site', x), ('README', rd)):
    print('--', lab)
    for s in ('1.7×', '1.7x', '162×', '162x', 'Three discovery domains', 'Eight discovery tasks', '8%20across%203%20domains', 'arXiv:XXXX.XXXXX', 'Terminal', 'harness', 'Opus', 'Being prepared', 'In progress', 'coming%20soon', '4 of 4'):
        cnt(lab, tx, s)
i = x.find('In the paper this cuts'); print('site sentence:', x[i:i + 130])
i = rd.find('1.22x'); print('README sentence:', rd[i - 40:i + 140])
print('-- refs')
print(subprocess.run(['git', 'ls-remote', 'https://github.com/zhengkid/Dream-RSI.git'], capture_output=True, text=True).stdout.strip())
