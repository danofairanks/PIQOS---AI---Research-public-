// repo: harmonic-public @ 7fe1597  | run: node i3_gap_and_receipt.js <dir containing clones>
const path = require('path'), http = require('http'), crypto = require('crypto'), D = path.resolve(process.argv[2]);
const handler = require(path.join(D, 'harmonic-public/api/evaluate.js')), { guardedExecute } = require(path.join(D, 'harmonic-public/examples/raw-vs-governed/guard.js'));
const pk = (obs) => ({ packet_id: 'p-' + crypto.randomUUID(), requested_action: 'release_document',
  truth: { claims: ['At T0 the NDA was valid.'], observations: [{ statement: obs }], evidence: [{ ref: 'registry://nda' }], last_verified_at: new Date().toISOString(), stale_after_minutes: 60 },
  authority: {}, compassion: { affected_parties: ['a'], potential_harms: ['h'], mitigations: ['m'], escalation_path: 'e' },
  accountability: { responsible_actor: 'a', authority_basis: 'b', consequence_owner: 'o', audit_ref: 'x', rollback_plan: 'r' } });
const stable = (v) => v === null || typeof v !== 'object' ? JSON.stringify(v) : Array.isArray(v) ? `[${v.map(stable).join(',')}]` : `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${stable(v[k])}`).join(',')}}`;
const sha = (s) => crypto.createHash('sha256').update(String(s)).digest('hex');
const s = http.createServer((q, r) => q.url === '/api/evaluate' ? handler(q, r) : (r.statusCode = 404, r.end()));
s.listen(0, '127.0.0.1', async () => {
  const baseUrl = 'http://127.0.0.1:' + s.address().port;
  // (a) evaluate-to-effect gap: registry flips after /api/evaluate returns, before execute() runs
  const reg = { active: true }; let seen;
  const mk = () => pk(reg.active ? 'the NDA remains valid' : 'the NDA is revoked');
  const flip = async (u, i) => { const r = await fetch(u, i); const t = await r.text(); reg.active = false; return new Response(t, { status: r.status, headers: r.headers }); };
  const gap = await guardedExecute({ baseUrl, packet: mk(), fetchImpl: flip, execute: async () => { seen = reg.active; } });
  const ctl = await guardedExecute({ baseUrl, packet: mk(), execute: async () => {} });   // registry already revoked before evaluate
  console.log('gap: executed=' + gap.executed + ' registry.active at effect=' + seen + ' | control (revoked before evaluate) executed=' + ctl.executed);
  // (b) receipt forgery: artifact_hash is sha256(stable({packet,result}))
  const p = pk('the NDA is revoked');
  const r = await (await fetch(baseUrl + '/api/evaluate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p) })).json();
  const { artifact_hash, public_release, note, ...result } = r;
  console.log('real receipt for a revoked packet:', r.outcome, r.recommended_action, '| hash recomputes from receipt:', sha(stable({ packet: p, result })) === artifact_hash);
  const forged = { ...result, outcome: 'stable', admissible: true, recommended_action: 'allow', stability_boundary: 'intact' };
  const fr = { ...forged, artifact_hash: sha(stable({ packet: p, result: forged })), public_release: true, note };
  let n = 0; const ex = async () => { n++; };
  const ok = await guardedExecute({ baseUrl, packet: p, fetchImpl: async () => new Response(JSON.stringify(fr)), execute: ex });
  const bad1 = await guardedExecute({ baseUrl, packet: p, fetchImpl: async () => new Response(JSON.stringify({ ...fr, packet_id: 'other' })), execute: ex });
  const bad2 = await guardedExecute({ baseUrl, packet: p, fetchImpl: async () => new Response(JSON.stringify({ ...fr, public_release: false })), execute: ex });
  console.log('forged receipt executed=' + ok.executed + ' | controls: wrong packet_id=' + bad1.executed + ', public_release:false=' + bad2.executed);
  s.close();
});
