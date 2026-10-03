#!/usr/bin/env node
/* Asserts the nine preregistered verdicts (PREREG_dn_runner_2026-10-03.md). Usage: node selftest.js [--clones <dir>]  (A1 is skipped without a clone, and the skip is printed) */
const path = require('node:path'); const { evaluate } = require('./dn_runner.js');
const argv = process.argv.slice(2); const i = argv.indexOf('--clones'); const clones = i >= 0 ? path.resolve(argv[i + 1]) : process.env.DN_CLONES;
const EXP = [
  ['a1_public_guard', (r) => r.headline === 'FAIL_DEFEAT' && r.summary.D_fired_Ta_forms.length === 8 && !r.summary.D_fired_Ta_forms.includes('listed_word') && r.summary.D_fired_Tb_forms.length === 9 && r.summary.P_fired_all && r.summary.B_fired_all_graded, 'FAIL_DEFEAT; D fires at Ta for 8 of 9 (not listed_word), Tb 9 of 9; P,B fire'],
  ['a2_registry_bound', (r) => r.headline === 'CONFORMS_AT_SCOPE' && r.summary.D_fired_Tc_forms_ungraded === 9, 'CONFORMS_AT_SCOPE; Tc fires (ungraded)'],
  ['a3_registry_bound_no_cas', (r) => r.headline === 'FAIL_DEFEAT' && r.summary.D_fired_Ta_forms.length === 0 && r.summary.D_fired_Tb_forms.length === 9, 'FAIL_DEFEAT at Tb only'],
  ['a4_constant_allow', (r) => r.headline === 'FAIL_DEFEAT' && r.summary.D_fired_Ta_forms.length === 9 && r.summary.D_fired_Tb_forms.length === 9 && r.summary.P_fired_all, 'FAIL_DEFEAT at Ta and Tb, all forms'],
  ['a5_always_deny', (r) => r.headline === 'FAIL_UTILITY' && r.verdicts.length === 1 && r.summary.D_fired_Ta_forms.length === 0 && r.summary.D_fired_Tb_forms.length === 0, 'FAIL_UTILITY only'],
  ['a6_check_then_act', (r) => r.headline === 'FAIL_DEFEAT' && r.summary.D_fired_Ta_forms.length === 0 && r.summary.D_fired_Tb_forms.length === 9, 'FAIL_DEFEAT at Tb only'],
  ['a7_atomic_check', (r) => r.headline === 'CONFORMS_AT_SCOPE', 'CONFORMS_AT_SCOPE'],
  ['a8_no_points', (r) => r.headline === 'NOT_DEMONSTRATED', 'NOT_DEMONSTRATED'],
  ['a9_order_dependent', (r) => r.verdicts.includes('ORDER_DEPENDENT'), 'ORDER_DEPENDENT among the verdicts (headline is a FAIL class; see README)'],
];
(async () => {
  let bad = 0, skipped = 0; const out = {};
  for (const [f, pred, want] of EXP) {
    if (f === 'a1_public_guard' && !clones) { console.log(`SKIP  ${f} (no --clones)`); skipped++; continue; }
    const a = require('./adapters/' + f + '.js'); if (a.init) await a.init({ clones });
    const r = await evaluate(a); if (a.close) await a.close(); out[f] = { headline: r.headline, verdicts: r.verdicts, summary: r.summary };
    const ok = pred(r); if (!ok) bad++; console.log(`${ok ? 'PASS' : 'FAIL'}  ${f}: got ${r.headline} [${r.verdicts.join(',')}] expected ${want}`);
  }
  require('fs').writeFileSync(path.join(__dirname, 'out_selftest.json'), JSON.stringify(out, null, 1));
  console.log(bad ? `${bad} FAILED` : `all ${EXP.length - skipped} checked passed${skipped ? ` (${skipped} skipped)` : ''}`); process.exit(bad ? 1 : 0);
})();
