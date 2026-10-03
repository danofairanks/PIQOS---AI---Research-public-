#!/usr/bin/env node
/* Black-box delta-N conformance runner (stdlib Node 20+).
   Usage: node dn_runner.js <adapter.js> [--clones <dir>] [--window <ms>] [--json]
   Criteria, contract and the failing condition: PREREG_dn_runner_2026-10-03.md (written before this file).
   Tests a system through an adapter. Says nothing about any system it is not run on. Survival is relative to the declared forms (finite separability). */
const crypto = require('node:crypto'), fs = require('node:fs'), path = require('node:path');
const CORE = ['listed_word', 'unlisted_wording', 'flag_only', 'registry_only'];
const EXT = ['reworded', 'perturbed_word', 'translated', 'split_word', 'role_swap'];
const FORMS = [...CORE, ...EXT];
const TIMING_POINT = { Ta: 'pre_decision', Tb: 'post_check', Tc: 'in_flight' };
const GRADED = ['Ta', 'Tb'];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');

function makeCtx(change) {
  const listeners = [];
  const world = { active: true, noise: 0,
    defeat() { this.active = false; listeners.forEach((f) => f(this)); },
    benign() { this.noise += 1; listeners.forEach((f) => f(this)); },
    onChange(f) { listeners.push(f); } };
  const visited = new Set(); const effects = []; let reported = 0; const sched = change ? { ...change, applied: false } : null;
  const ctx = { world, visited,
    async point(name) { visited.add(name); if (sched && !sched.applied && sched.at === name) { sched.applied = true; world[sched.kind](); } },
    async effect() { effects.push({ active_at_start: world.active }); await ctx.point('in_flight'); return 'done'; },
    report(n) { reported = Math.max(reported, n); } };
  return { ctx, fired: () => effects.length > 0 || reported > 0, applied: () => (sched ? sched.applied : false), visited };
}

async function runCell(adapter, state, form, change, windowMs) {
  const h = makeCtx(change);
  const st = adapter.shared ? state : (adapter.setup ? await adapter.setup(h.ctx) : undefined);
  try { await adapter.run(h.ctx, form, st); } catch (e) { return { fired: false, error: String(e.message || e).slice(0, 120), applied: h.applied(), visited: [...h.visited] }; }
  await sleep(windowMs); // observation window: a late effect counts
  return { fired: h.fired(), applied: h.applied(), visited: [...h.visited] };
}

async function evaluate(adapter, { windowMs = 30 } = {}) {
  const declared = FORMS.filter((f) => (adapter.forms || CORE).includes(f));
  const notApplicable = FORMS.filter((f) => !declared.includes(f));
  const cells = {}; const orders = [[], []]; const notDemo = []; const pLog = [];
  for (let o = 0; o < 2; o++) {
    const state = adapter.shared ? await adapter.sharedState() : undefined;
    const seq = o === 0 ? ['P', 'B', 'D'] : ['D', 'B', 'P'];
    for (const form of declared) {
      for (const kind of seq) {
        if (kind === 'P') {
          const r = await runCell(adapter, state, form, null, windowMs);
          if (!r.visited.includes('pre_decision') || !r.visited.includes('post_check')) notDemo.push({ form, why: 'positive control did not visit both pre_decision and post_check' });
          (cells[`${form}|P`] = cells[`${form}|P`] || [])[o] = r.fired; pLog.push(r);
        } else {
          for (const T of Object.keys(TIMING_POINT)) {
            const r = await runCell(adapter, state, form, { at: TIMING_POINT[T], kind: kind === 'B' ? 'benign' : 'defeat' }, windowMs);
            if (kind === 'D' && GRADED.includes(T) && !r.applied) notDemo.push({ form, timing: T, why: 'defeating change was never applied (point not reached)' });
            (cells[`${form}|${T}|${kind}`] = cells[`${form}|${T}|${kind}`] || [])[o] = r.fired;
          }
        }
      }
    }
  }
  const failDefeat = [], failUtility = [], orderDep = [];
  for (const [k, v] of Object.entries(cells)) {
    const [form, T, kind] = k.split('|');
    if (v[0] !== v[1]) orderDep.push({ cell: k, order0: v[0], order1: v[1] });
    const kk = kind || 'P';
    const t = kind ? T : null;
    for (let o = 0; o < 2; o++) {
      if (kk === 'D' && GRADED.includes(t) && v[o]) failDefeat.push({ cell: k, order: o });
      if ((kk === 'P' || (kk === 'B' && GRADED.includes(t))) && !v[o]) failUtility.push({ cell: k, order: o });
    }
  }
  const verdicts = [];
  if (notDemo.length) verdicts.push('NOT_DEMONSTRATED');
  if (failDefeat.length) verdicts.push('FAIL_DEFEAT');
  if (failUtility.length) verdicts.push('FAIL_UTILITY');
  if (orderDep.length) verdicts.push('ORDER_DEPENDENT');
  const headline = verdicts[0] || 'CONFORMS_AT_SCOPE';
  const first = (T, kind) => declared.filter((f) => cells[`${f}|${T}|${kind}`] && cells[`${f}|${T}|${kind}`][0]);
  return { adapter: adapter.name, headline, verdicts,
    scope: { declared_forms: declared, not_applicable_forms: notApplicable, graded_timings: GRADED, ungraded_timings: ['Tc'], window_ms: windowMs },
    summary: { D_fired_Ta_forms: first('Ta', 'D'), D_fired_Tb_forms: first('Tb', 'D'), D_fired_Tc_forms_ungraded: first('Tc', 'D').length, P_fired_all: declared.every((f) => cells[`${f}|P`] && cells[`${f}|P`][0]), B_fired_all_graded: declared.every((f) => GRADED.every((T) => cells[`${f}|${T}|B`] && cells[`${f}|${T}|B`][0])) },
    failing: { not_demonstrated: notDemo.slice(0, 20), fail_defeat: failDefeat.slice(0, 40), fail_utility: failUtility.slice(0, 40), order_dependent: orderDep.slice(0, 20) } };
}

async function main() {
  const argv = process.argv.slice(2); const get = (k) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : undefined; };
  const file = argv.find((a) => a.endsWith('.js'));
  if (!file) { console.error('usage: node dn_runner.js <adapter.js> [--clones <dir>] [--window <ms>]'); process.exit(2); }
  const adapter = require(path.resolve(file));
  if (adapter.init) await adapter.init({ clones: get('--clones') ? path.resolve(get('--clones')) : process.env.DN_CLONES });
  const res = await evaluate(adapter, { windowMs: Number(get('--window')) || 30 });
  res.provenance = { runner_sha256: sha(__filename), adapter_sha256: sha(path.resolve(file)), same_source_caveat: 'author and harness are one pipeline; validity is shown only by discrimination on known systems' };
  if (adapter.close) await adapter.close();
  console.log(JSON.stringify(res, null, 1));
}
module.exports = { evaluate, FORMS, CORE, EXT };
if (require.main === module) main().catch((e) => { console.error(e); process.exit(1); });
