#!/usr/bin/env node
/* Asserts the six preregistered verdicts (PREREG_reality_mode_2026-10-03.md). Usage: node selftest_reality.js */
const path = require('node:path'), fs = require('node:fs'); const { evaluate } = require('./dn_reality.js');
const six = ['revoked', 'expired'];
const EXP = [
  ['s1_fenced_allowlist', (r) => r.headline === 'CONFORMS_AT_SCOPE' && r.summary.D_fired_Tc_ungraded === 8 && !r.flags.length, 'CONFORMS_AT_SCOPE; Tc accepted (ungraded)'],
  ['s2_unfenced_check_then_act', (r) => r.headline === 'FAIL_DEFEAT' && r.summary.D_fired_Ta.length === 0 && r.summary.D_fired_Tr_last.length === 8 && r.summary.P_fired, 'FAIL_DEFEAT at Tr1 only (8 of 8), Ta held'],
  ['s3_constant_allow', (r) => r.headline === 'FAIL_DEFEAT' && r.summary.D_fired_Ta.length === 8 && r.flags.includes('REALITY_NOT_CONSULTED') && r.summary.D_fired_Tr_last === null, 'FAIL_DEFEAT at Ta 8 of 8; REALITY_NOT_CONSULTED; no Tr cells'],
  ['s4_always_deny', (r) => r.headline === 'FAIL_UTILITY' && r.verdicts.length === 1 && r.summary.D_fired_Ta.length === 0 && r.summary.D_fired_Tr_last.length === 0, 'FAIL_UTILITY only'],
  ['s5_fenced_denylist', (r) => r.headline === 'FAIL_DEFEAT' && r.summary.D_fired_Ta.length === 6 && !r.summary.D_fired_Ta.some((f) => six.includes(f)) && r.summary.D_fired_Tr_last.length === 0, 'FAIL_DEFEAT at Ta for 6 of 8 (not revoked, expired); Tr1 held 8 of 8'],
  ['s6_caching_shared', (r) => r.verdicts.includes('ORDER_DEPENDENT'), 'ORDER_DEPENDENT among the verdicts'],
];
(async () => { let bad = 0; const out = {};
  for (const [f, pred, want] of EXP) { const t = require('./systems/' + f + '.js'); const r = await evaluate(t); out[f] = { headline: r.headline, verdicts: r.verdicts, flags: r.flags, summary: r.summary };
    const ok = pred(r); if (!ok) bad++; console.log(`${ok ? 'PASS' : 'FAIL'}  ${f}: got ${r.headline} [${r.verdicts.join(',')}] ${r.flags.join(',')} expected ${want}`); }
  fs.writeFileSync(path.join(__dirname, 'out_selftest_reality.json'), JSON.stringify(out, null, 1));
  console.log(bad ? `${bad} FAILED` : `all ${EXP.length} passed`); process.exit(bad ? 1 : 0); })();
