#!/usr/bin/env node
/* B3: defeated-authority matrix, defeat FORM x TIMING x GUARD. Usage: node b3_defeat_matrix.js <dir containing clones>   (harmonic-public and authority-continuity-primitive-public)
   Design and predictions were written before this file existed (internal history). Cell = whether the covered effect starts after the defeat. */
const path = require('node:path'), http = require('node:http'), crypto = require('node:crypto'), fs = require('node:fs'), os = require('node:os');
const { makeSystem } = require('./b1_registry_bound_guard.js');
const D = path.resolve(process.argv[2]); const H = path.join(D, 'harmonic-public');
const handler = require(path.join(H, 'api/evaluate.js')); const { guardedExecute } = require(path.join(H, 'examples/raw-vs-governed/guard.js'));
const FORMS = ['F1_listed_word', 'F2_unlisted_wording', 'F3_flag_only', 'F4_registry_only'];
const iso = (m) => new Date(m).toISOString(); const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
function packetFor(form, world) {
  let observation = 'At Tn the NDA remains valid for design-001.'; let authority = {};
  if (form === 'F1_listed_word' && !world.active) observation = 'At Tn the NDA is revoked.';
  if (form === 'F2_unlisted_wording' && !world.active) observation = 'At Tn the NDA was terminated.';
  if (form === 'F3_flag_only' && !world.active) authority = { revoked: true, expires_at: iso(Date.now() - 86400000) };
  // F4: the host does not read the registry; its packet always says valid
  return { packet_id: crypto.randomUUID(), requested_action: 'release_document', execution_request: { action: 'release_document' },
    truth: { claims: ['At T0 the NDA was valid and release was authorized.'], observations: [{ statement: observation }], evidence: [{ ref: 'registry://nda' }], last_verified_at: iso(Date.now()), stale_after_minutes: 1 }, authority,
    compassion: { affected_parties: ['a'], potential_harms: ['h'], mitigations: ['m'], escalation_path: 'e' }, accountability: { responsible_actor: 'a', authority_basis: 'r', consequence_owner: 'o', audit_ref: 'x', rollback_plan: 'hold' } };
}
const flipAfter = (world) => async (u, i) => { const r = await fetch(u, i); const b = await r.text(); world.active = false; return new Response(b, { status: r.status, headers: r.headers }); };

async function main() {
  const server = http.createServer((q, s) => q.url === '/api/evaluate' ? handler(q, s) : (s.statusCode = 404, s.end()));
  await new Promise((r) => server.listen(0, '127.0.0.1', r)); const baseUrl = `http://127.0.0.1:${server.address().port}`;
  const M = { G1_public: {}, G2_public_recheck: {}, G3_registry_bound: {}, G4_registry_bound_no_CAS: {}, G5_constant_endpoint: {} };
  const set = (g, t, f, v) => { (M[g][t] = M[g][t] || {})[f] = v; };
  // G1 public guard
  for (const f of FORMS) {
    { const w = { active: false }; let n = 0; await guardedExecute({ baseUrl, packet: packetFor(f, w), execute: async () => { n++; } }); set('G1_public', 'Ta', f, n === 1); }
    { const w = { active: true }; let n = 0; await guardedExecute({ baseUrl, packet: packetFor(f, w), fetchImpl: flipAfter(w), execute: async () => { n++; } }); set('G1_public', 'Tb', f, n === 1 && w.active === false); }
    { const w = { active: true }; let n = 0; await guardedExecute({ baseUrl, packet: packetFor(f, w), execute: async () => { n++; w.active = false; await sleep(3); } }); set('G1_public', 'Tc', f, n === 1); }
  }
  // G2 public guard, re-evaluated immediately before the effect (two nested real guard calls)
  const twice = (w, f, fetch1, fetch2, effect) => guardedExecute({ baseUrl, packet: packetFor(f, w), fetchImpl: fetch1, execute: () => guardedExecute({ baseUrl, packet: packetFor(f, w), fetchImpl: fetch2, execute: effect }) });
  for (const f of FORMS) {
    { const w = { active: false }; let n = 0; await twice(w, f, undefined, undefined, async () => { n++; }); set('G2_public_recheck', 'Ta', f, n === 1); }
    { const w = { active: true }; let n = 0; await twice(w, f, flipAfter(w), undefined, async () => { n++; }); set('G2_public_recheck', "Tb'", f, n === 1 && w.active === false); }
    { const w = { active: true }; let n = 0; await twice(w, f, undefined, flipAfter(w), async () => { n++; }); set('G2_public_recheck', 'Tb', f, n === 1 && w.active === false); }
    { const w = { active: true }; let n = 0; await twice(w, f, undefined, undefined, async () => { n++; w.active = false; await sleep(3); }); set('G2_public_recheck', 'Tc', f, n === 1); }
  }
  // G3 / G4 registry-bound
  for (const [g, mut] of [['G3_registry_bound', {}], ['G4_registry_bound_no_CAS', { noCAS: true }]]) for (const f of FORMS) {
    const mk = () => { const s = makeSystem({ mutations: mut }); s.registry.set('nda', true); return s; };
    { const s = mk(); s.registry.set('nda', false); const pid = crypto.randomUUID(); const r = s.evaluate({ standing_id: 'nda', action: 'release_document', packet_id: pid }); await s.execute({ receipt: r, packet_id: pid, action: 'release_document' }); set(g, 'Ta', f, s.effects.length === 1); }
    { const s = mk(); const pid = crypto.randomUUID(); const r = s.evaluate({ standing_id: 'nda', action: 'release_document', packet_id: pid }); s.registry.set('nda', false); await s.execute({ receipt: r, packet_id: pid, action: 'release_document' }); set(g, 'Tb', f, s.effects.length === 1); }
    { const s = mk(); const pid = crypto.randomUUID(); const r = s.evaluate({ standing_id: 'nda', action: 'slow_release', packet_id: pid }); const pending = s.execute({ receipt: r, packet_id: pid, action: 'slow_release' }); await sleep(5); s.registry.set('nda', false); await pending; set(g, 'Tc', f, s.effects.length === 1); }
  }
  // G5 guard over the constant endpoint (executes when decision == ALLOW)
  { const tmp = path.join(os.tmpdir(), 'stub_' + crypto.randomUUID() + '.mjs'); fs.copyFileSync(path.join(D, 'authority-continuity-primitive-public/api/evaluate.js'), tmp); const mod = await import(tmp); fs.unlinkSync(tmp);
    const call = () => { let got; mod.default({ method: 'POST', body: {} }, { status() { return this; }, json(x) { got = x; return this; } }); return got; };
    for (const f of FORMS) for (const t of ['Ta', 'Tb', 'Tc']) { let n = 0; if (call().decision === 'ALLOW') n++; set('G5_constant_endpoint', t, f, n === 1); } }
  server.close();
  console.log(JSON.stringify(M, null, 1));
}
main().catch((e) => { console.error(e); process.exit(1); });
