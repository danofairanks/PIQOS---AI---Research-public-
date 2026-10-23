"""Verify the repository statements in the draft against public files at the pinned commits.
Fetches single files from raw.githubusercontent.com (no clone).  Standard library only.
Usage: python3 -I repo_quote_checks.py"""
import re, urllib.request
A = 'https://raw.githubusercontent.com/Gen-Verse/DiscoveryRSI/7389e0b58ae50486ab35aa3dcbfa2fa15fea1a91/'
B = 'https://raw.githubusercontent.com/Gen-Verse/DFM-Bench/224712b3407f543a077ff8b656167fb41f441963/'
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'research-check/1.0'}), timeout=30) as r:
            return r.status, re.sub(r'\s+', ' ', r.read().decode('utf-8', 'replace'))
    except urllib.error.HTTPError as e:
        return e.code, ''
T = [
 (A + 'README.md', ['achieves the highest actionable-reference rate at 6.3%**, followed by DeepSeek (**5.4%**), GLM (**2.8%**), GPT (**2.5%**), and Claude (**2.3%**)',
                    'DiscoveryRSI can produce plausible but unsupported claims, omit relevant evidence, misread sources, or propose infeasible experiments']),
 (A + 'LICENSE', ['Apache License']),
 (B + 'docs/EVALUATION.md', ['This is an **internal AI-reviewed preview**; human calibration is pending, and the scores do not establish scientific truth or verified discoveries',
                             'A maximum score increasing over episodes does not prove learning']),
 (B + 'src/dfm_bench/protocols/PROTOCOL-V1.json', ['"weight_status": "locked_internal_pilot_convention_not_validated"',
                             '"forbidden_claims": [ "expert_calibrated", "online_as_of_progress", "confirmed_discovery", "system_superiority" ]',
                             '"release_claim": "Implementation and internal pilot release; no claim of completed human calibration, system superiority or verified discoveries"',
                             '"expert_calibration_status": "pending"', '"time_mode": "retrospective_final_snapshot"',
                             'Scientific proposal merit conditional on supplied evidence, not truth or verified novelty']),
 (B + 'docs/FIVE-LEVEL-PROTOCOL.md', ['Historical archive (2026-09-27)', 'canonical five objects: hypothesis, transition, trajectory, campaign and discovery',
                             'no new absolute hypothesis scale is invented', '(child wins + 0.5 ties) / assessable pairs',
                             'Only DeepSeek V4 Flash is authorized for this pilot', '142 EHR and 367 battery edge comparisons']),
]
for u, qs in T:
    s, t = get(u); print(s, u.split('/')[-1], u.split('/')[4])
    for q in qs: print('   ', 'OK  ' if q in t else 'MISS', q[:120])
# absence checks (HTTP 404 on these names; other names are not excluded)
for u in [B + 'LICENSE', B + 'LICENSE.md', B + 'LICENSE.txt', B + 'COPYING']:
    print(get(u)[0], u.split('/')[-1], 'DFM-Bench root')
s, t = get(B + 'pyproject.toml'); print('DFM-Bench pyproject.toml: status', s, '; occurrences of "license":', len(re.findall('license', t, re.I)))
s, t = get(A + 'README.md'); print('DiscoveryRSI README occurrences of gate/cutoff/window/retriev:', [len(re.findall(w, t, re.I)) for w in ('gate', 'cutoff', 'window', 'retriev')])
