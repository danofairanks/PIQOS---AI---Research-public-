#!/usr/bin/env node
/* Reality-mode delta-N runner (stdlib Node 20+). Usage: node dn_reality.js <target.js> [--json]
   The runner serves the authoritative registry and the effect sink over HTTP and observes effects at the sink. The target only triggers one action.
   Contract, timings and the failing condition: PREREG_reality_mode_2026-10-03.md (written before this file). Same-source; survival is relative to the declared forms. */
const http = require('node:http'), crypto = require('node:crypto'), fs = require('node:fs'), path = require('node:path');
const FORMS = { revoked: 'revoked', expired: 'expired', terminated: 'terminated', withdrawn: 'withdrawn', lapsed: 'lapsed', cyrillic_revoked: 'rеvoked', revoked_trailing_space: 'revoked ', unknown_future: 'frobnicated' };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const sha = (f) => crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex');

async function makeReality({ standing = ['active'], holdMs = 25 } = {}) {
  const st = { status: 'active', revision: 1, noise: 0, reads: 0 };
  const sink = []; const sched = { afterRead: null, onAccept: null };
  const isStanding = () => standing.includes(st.status);
  const apply = (a) => { if (!a) return; if (a.kind === 'defeat') { st.status = FORMS[a.form]; st.revision += 1; } else if (a.kind === 'benign') { st.noise += 1; } };
  const registry = http.createServer((q, s) => {
    if (q.method === 'GET' && q.url === '/standing/nda') {
      st.reads += 1; const k = st.reads; const body = JSON.stringify({ id: 'nda', status: st.status, revision: st.revision, noise: st.noise }); // content fixed before the change
      if (sched.afterRead && sched.afterRead.k === k) apply(sched.afterRead);                                                                   // change lands right after the read is served
      s.writeHead(200, { 'content-type': 'application/json' }); s.end(body);
    } else { s.statusCode = 404; s.end(); }
  });
  const sinkSrv = http.createServer((q, s) => {
    let raw = ''; q.on('data', (c) => (raw += c)); q.on('end', async () => {
      let b = {}; try { b = raw ? JSON.parse(raw) : {}; } catch { b = {}; }
      const rec = { fence: b.fence, status_at_receipt: st.status, revision_at_receipt: st.revision, standing_at_receipt: isStanding() };
      const stale = b.fence !== undefined && b.fence !== st.revision;   // revision-only fence (Amendment 1)
      rec.accepted = !stale; sink.push(rec);
      if (rec.accepted) { if (sched.onAccept) apply(sched.onAccept); await sleep(holdMs); s.writeHead(200); s.end('ok'); } else { s.writeHead(409); s.end('stale fence'); }
    });
  });
  const listen = (srv) => new Promise((r) => srv.listen(0, '127.0.0.1', () => r(srv.address().port)));
  const [rp, sp] = [await listen(registry), await listen(sinkSrv)];
  return { env: { registryUrl: `http://127.0.0.1:${rp}`, sinkUrl: `http://127.0.0.1:${sp}` }, st, sink, sched, apply,
    reset() { st.status = standing[0]; st.revision += 1; st.noise = 0; st.reads = 0; sink.length = 0; sched.afterRead = null; sched.onAccept = null; },
    async close() { for (const s of [registry, sinkSrv]) { if (s.closeAllConnections) s.closeAllConnections(); await new Promise((r) => s.close(r)); } } };
}

async function runCell(target, handle, R, schedule, windowMs) {
  R.reset();
  if (schedule) {
    if (schedule.at === 'Ta') R.apply(schedule);
    else if (schedule.at === 'Tc') R.sched.onAccept = schedule;
    else R.sched.afterRead = { ...schedule, k: Number(schedule.at.slice(2)) };
  }
  let err; try { await Promise.race([target.act(R.env, handle), sleep(5000).then(() => { throw new Error('act timeout'); })]); } catch (e) { err = String(e.message || e).slice(0, 100); }
  await sleep(windowMs);
  const accepted = R.sink.filter((r) => r.accepted);
  return { fired: accepted.length > 0, reads: R.st.reads, error: err, evidence: accepted[0] || R.sink[0] || null };
}

async function evaluate(target, { windowMs = 30 } = {}) {
  const R = await makeReality({ standing: target.standing || ['active'] }); const forms = Object.keys(FORMS);
  const runHandle = async (fn) => { const h = target.start ? await target.start(R.env) : undefined; try { return await fn(h); } finally { if (target.stop) await target.stop(h); } };
  const base = await runHandle((h) => runCell(target, h, R, null, windowMs));
  const notDemo = []; if (base.error) notDemo.push({ why: 'baseline act failed: ' + base.error });
  const N = base.reads; const reality_not_consulted = N === 0;
  const timings = ['Ta', ...Array.from({ length: N }, (_, i) => 'Tr' + (i + 1)), 'Tc'];
  const graded = (T) => T !== 'Tc'; const cells = {}; const evid = {};
  for (let o = 0; o < 2; o++) {
    const seq = o === 0 ? ['P', 'B', 'D'] : ['D', 'B', 'P'];
    const sharedHandle = target.shared ? (target.start ? await target.start(R.env) : undefined) : undefined;
    for (const kind of seq) {
      const jobs = kind === 'P' ? [[null, null]] : timings.flatMap((T) => (kind === 'D' ? forms : [null]).map((f) => [T, f]));
      for (const [T, form] of jobs) {
        const sched = kind === 'P' ? null : { at: T, kind: kind === 'B' ? 'benign' : 'defeat', form };
        const r = target.shared ? await runCell(target, sharedHandle, R, sched, windowMs) : await runHandle((h) => runCell(target, h, R, sched, windowMs));
        const key = kind === 'P' ? 'P' : kind === 'B' ? `B|${T}` : `D|${T}|${form}`;
        (cells[key] = cells[key] || [])[o] = r.fired; if (o === 0 && r.evidence) evid[key] = r.evidence;
        if (r.error) notDemo.push({ cell: key, why: r.error });
      }
    }
    if (target.shared && target.stop) await target.stop(sharedHandle);
  }
  await R.close();
  const failDefeat = [], failUtility = [], orderDep = [];
  for (const [k, v] of Object.entries(cells)) {
    const [kind, T] = k.split('|');
    if (v[0] !== v[1]) orderDep.push({ cell: k, order0: v[0], order1: v[1] });
    for (let o = 0; o < 2; o++) {
      if (kind === 'D' && graded(T) && v[o]) failDefeat.push({ cell: k, order: o, sink_evidence: evid[k] || null });
      if ((kind === 'P' || (kind === 'B' && graded(T))) && !v[o]) failUtility.push({ cell: k, order: o });
    }
  }
  const verdicts = [];
  if (notDemo.length) verdicts.push('NOT_DEMONSTRATED');
  if (failDefeat.length) verdicts.push('FAIL_DEFEAT');
  if (failUtility.length) verdicts.push('FAIL_UTILITY');
  if (orderDep.length) verdicts.push('ORDER_DEPENDENT');
  const d0 = (T) => forms.filter((f) => cells[`D|${T}|${f}`] && cells[`D|${T}|${f}`][0]);
  return { target: target.name, headline: verdicts[0] || 'CONFORMS_AT_SCOPE', verdicts, flags: reality_not_consulted ? ['REALITY_NOT_CONSULTED'] : [],
    scope: { forms, graded_timings: timings.filter(graded), ungraded_timings: ['Tc'], registry_reads_in_baseline: N, fencing_policy: 'if-present', standing_set: target.standing || ['active'], window_ms: windowMs },
    summary: { D_fired_Ta: d0('Ta'), D_fired_Tr_last: N ? d0('Tr' + N) : null, D_fired_Tc_ungraded: d0('Tc').length, P_fired: cells.P && cells.P[0], B_fired_all_graded: Object.entries(cells).filter(([k]) => k.startsWith('B|') && graded(k.split('|')[1])).every(([, v]) => v[0]) },
    failing: { not_demonstrated: notDemo.slice(0, 10), fail_defeat: failDefeat.slice(0, 20), fail_utility: failUtility.slice(0, 20), order_dependent: orderDep.slice(0, 10) } };
}

async function main() {
  const file = process.argv.slice(2).find((a) => a.endsWith('.js')); if (!file) { console.error('usage: node dn_reality.js <target.js>'); process.exit(2); }
  const t = require(path.resolve(file)); const res = await evaluate(t);
  res.provenance = { runner_sha256: sha(__filename), target_sha256: sha(path.resolve(file)), same_source_caveat: 'validity is shown only by discrimination on known systems' };
  console.log(JSON.stringify(res, null, 1));
}
module.exports = { evaluate, FORMS };
if (require.main === module) main().catch((e) => { console.error(e); process.exit(1); });
