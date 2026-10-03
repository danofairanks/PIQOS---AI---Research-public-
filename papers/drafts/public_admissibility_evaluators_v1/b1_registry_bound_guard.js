#!/usr/bin/env node
/* B1: registry-bound guard toy and its attacks (stdlib Node 20+). Usage: node b1_registry_bound_guard.js [dir containing harmonic-public clone]
   Design and predictions were written before this file existed (internal history). Purpose: test whether the defeat
   conditions used against the public reference guard are achievable. The toy is not a product. */
const crypto = require('node:crypto'), path = require('node:path'), http = require('node:http');

const canon = (v) => v === null || typeof v !== 'object' ? JSON.stringify(v) : Array.isArray(v) ? `[${v.map(canon).join(',')}]` : `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${canon(v[k])}`).join(',')}}`;

function makeSystem({ mutations = {}, ttlMs = 60000 } = {}) {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  const items = new Map(), used = new Set(), effects = [];
  const registry = {
    set(id, active) { const s = items.get(id) || { revision: 0 }; items.set(id, { active, revision: s.revision + 1 }); },
    get(id) { const s = items.get(id); return s ? { ...s } : null; },
    // compare-and-swap: the revision check and the start of the effect happen in one synchronous step
    commit(id, expectedRevision, effect) {
      const s = items.get(id);
      if (!mutations.noCAS && (!s || !s.active || s.revision !== expectedRevision)) throw new Error('STALE_OR_REVOKED');
      return effect();
    },
  };
  const table = { // the effects are closures in this scope; the host names an action, it does not supply a function
    release_document: async (ctx) => { effects.push({ ...ctx, at: 'start', active_at_start: registry.get(ctx.standing_id)?.active }); return 'done'; },
    slow_release: async (ctx) => { await new Promise((r) => setTimeout(r, 20)); effects.push({ ...ctx, at: 'completion', active_at_completion: registry.get(ctx.standing_id)?.active }); return 'done'; },
  };
  const sign = (payload) => crypto.sign(null, Buffer.from(canon(payload)), privateKey).toString('base64');
  const verify = (payload, sig, pub = publicKey) => { try { return crypto.verify(null, Buffer.from(canon(payload)), pub, Buffer.from(sig, 'base64')); } catch { return false; } };
  // the host supplies only these three fields; anything else in the input is ignored
  function evaluate(input) {
    const { standing_id, action, packet_id } = input;
    const s = registry.get(standing_id);
    const payload = { packet_id, action, standing_id, revision: s ? s.revision : -1, decision: s && s.active ? 'allow' : 'deny', expires_at: Date.now() + ttlMs, nonce: crypto.randomUUID() };
    return { payload, signature: sign(payload) };
  }
  async function execute({ receipt, packet_id, action }) {
    const p = receipt && receipt.payload;
    if (!p || typeof receipt.signature !== 'string') return { executed: false, why: 'malformed' };
    if (!mutations.noSig && !verify(p, receipt.signature)) return { executed: false, why: 'bad_signature' };
    if (p.packet_id !== packet_id || p.action !== action) return { executed: false, why: 'binding' };
    if (p.decision !== 'allow') return { executed: false, why: 'not_allow' };
    if (!(p.expires_at > Date.now())) return { executed: false, why: 'expired' };
    if (!mutations.noNonce) { if (used.has(p.nonce)) return { executed: false, why: 'replay' }; used.add(p.nonce); }
    if (!table[action]) return { executed: false, why: 'unknown_action' };
    try { const r = await registry.commit(p.standing_id, p.revision, () => table[action]({ packet_id, standing_id: p.standing_id })); return { executed: true, result: r }; }
    catch (e) { return { executed: false, why: e.message }; }
  }
  return { registry, evaluate, execute, effects, publicKey, _leak: { privateKey, sign, effect: table.release_document, canon } };
}

async function run() {
  const out = {}; const id = () => 'pkt-' + crypto.randomUUID();
  const fresh = (mutations) => { const s = makeSystem({ mutations }); s.registry.set('nda', true); return s; };
  const runOnce = async (s, extra = {}, action = 'release_document') => { const pid = id(); const receipt = s.evaluate({ standing_id: 'nda', action, packet_id: pid, ...extra }); return { pid, receipt, res: await s.execute({ receipt, packet_id: pid, action }) }; };

  // control
  { const s = fresh(); const r = await runOnce(s); out.control_honest = { executed: r.res.executed, effects: s.effects.length }; }
  // A-words: host text has no influence; the defeat is read from the registry
  { const s = fresh(); s.registry.set('nda', false);
    const r = await runOnce(s, { claims: ['the NDA is valid'], observations: [{ statement: 'the NDA is valid and in force' }] });
    out.A_words = { registry_revoked_host_says_valid: { decision: r.receipt.payload.decision, executed: r.res.executed, effects: s.effects.length } };
    for (const t of ['the NDA ended', 'the NDA was terminated', 'The NDA has not been revoked.', 'the NDA is revoked']) {
      const s2 = fresh(); const r2 = await runOnce(s2, { observations: [{ statement: t }] });
      out.A_words['registry_active_host_text:' + t] = { decision: r2.receipt.payload.decision, executed: r2.res.executed }; } }
  // A-flag
  { const s = fresh(); s.registry.set('nda', false); const r = await runOnce(s, { authority: { revoked: false } });
    const s2 = fresh(); const r2 = await runOnce(s2, { authority: { revoked: true, expires_at: '2000-01-01' } });
    out.A_flag = { registry_revoked_flag_says_not: { decision: r.receipt.payload.decision, executed: r.res.executed }, registry_active_flag_says_revoked_and_expired: { decision: r2.receipt.payload.decision, executed: r2.res.executed } }; }
  // A-gap and ABA
  { const s = fresh(); const pid = id(); const receipt = s.evaluate({ standing_id: 'nda', action: 'release_document', packet_id: pid }); s.registry.set('nda', false);
    const res = await s.execute({ receipt, packet_id: pid, action: 'release_document' });
    out.A_gap = { decision_at_evaluate: receipt.payload.decision, revoked_before_effect: true, executed: res.executed, why: res.why, effects: s.effects.length };
    const s2 = fresh(); const pid2 = id(); const r2 = s2.evaluate({ standing_id: 'nda', action: 'release_document', packet_id: pid2 }); s2.registry.set('nda', false); s2.registry.set('nda', true);
    const res2 = await s2.execute({ receipt: r2, packet_id: pid2, action: 'release_document' });
    out.A_gap_revoke_then_restore = { executed: res2.executed, why: res2.why, effects: s2.effects.length, revision_now: s2.registry.get('nda').revision, receipt_revision: r2.payload.revision }; }
  // A-receipt
  { const s = fresh(); const pid = id(); const good = s.evaluate({ standing_id: 'nda', action: 'release_document', packet_id: pid });
    const other = crypto.generateKeyPairSync('ed25519'); const forgedPayload = { ...good.payload, nonce: 'forged-' + crypto.randomUUID() };
    const forged = { payload: forgedPayload, signature: crypto.sign(null, Buffer.from(canon(forgedPayload)), other.privateKey).toString('base64') };
    const rep = {};
    rep.forged_other_key = (await s.execute({ receipt: forged, packet_id: pid, action: 'release_document' })).why;
    const s2 = fresh(); s2.registry.set('nda', false); const denied = s2.evaluate({ standing_id: 'nda', action: 'release_document', packet_id: pid });
    const tampered = { payload: { ...denied.payload, decision: 'allow' }, signature: denied.signature };
    rep.tampered_decision_original_signature = (await s2.execute({ receipt: tampered, packet_id: pid, action: 'release_document' })).why;
    rep.wrong_action = (await s.execute({ receipt: good, packet_id: pid, action: 'slow_release' })).why;
    rep.wrong_packet = (await s.execute({ receipt: good, packet_id: id(), action: 'release_document' })).why;
    const se = fresh(); se; const sExp = makeSystem({ ttlMs: -1 }); sExp.registry.set('nda', true); const pe = id(); const re = sExp.evaluate({ standing_id: 'nda', action: 'release_document', packet_id: pe });
    rep.expired = (await sExp.execute({ receipt: re, packet_id: pe, action: 'release_document' })).why;
    const first = await s.execute({ receipt: good, packet_id: pid, action: 'release_document' }); const second = await s.execute({ receipt: good, packet_id: pid, action: 'release_document' });
    rep.replay = { first_executed: first.executed, second: second.why }; rep.effects_on_attack_system = s.effects.length + s2.effects.length;
    out.A_receipt = rep; }
  // residuals that still succeed
  { const s = fresh(); const pid = id(); const p = { packet_id: pid, action: 'release_document', standing_id: 'nda', revision: 1, decision: 'allow', expires_at: Date.now() + 60000, nonce: 'minted' };
    const res = await s.execute({ receipt: { payload: p, signature: s._leak.sign(p) }, packet_id: pid, action: 'release_document' });
    out.R_key_holder_mints = { executed: res.executed };
    const s2 = fresh(); const world_revoked = true; const r = await runOnce(s2); out.R_stale_registry = { world_revoked, registry_active: true, executed: r.res.executed };
    const s3 = fresh(); await s3._leak.effect({ packet_id: 'direct', standing_id: 'nda' }); s3.registry.set('nda', false); await s3._leak.effect({ packet_id: 'direct-after-revocation', standing_id: 'nda' }); out.R_bypass_direct_call = { effects_after_revocation_without_guard: s3.effects.length };
    const s4 = fresh(); const pid4 = id(); const r4 = s4.evaluate({ standing_id: 'nda', action: 'slow_release', packet_id: pid4 }); const pending = s4.execute({ receipt: r4, packet_id: pid4, action: 'slow_release' });
    await new Promise((r) => setTimeout(r, 5)); s4.registry.set('nda', false); const res4 = await pending;
    out.R_inflight = { executed: res4.executed, active_at_completion: s4.effects[0] && s4.effects[0].active_at_completion }; }
  // mutation checks
  { const s = fresh({ noCAS: true }); const pid = id(); const rc = s.evaluate({ standing_id: 'nda', action: 'release_document', packet_id: pid }); s.registry.set('nda', false);
    out.mutation_noCAS_gap = { executed: (await s.execute({ receipt: rc, packet_id: pid, action: 'release_document' })).executed };
    const sg = fresh({ noSig: true }); const pg = id(); const other = crypto.generateKeyPairSync('ed25519'); const fp = { packet_id: pg, action: 'release_document', standing_id: 'nda', revision: 1, decision: 'allow', expires_at: Date.now() + 60000, nonce: 'x' };
    out.mutation_noSig_forged = { executed: (await sg.execute({ receipt: { payload: fp, signature: crypto.sign(null, Buffer.from(canon(fp)), other.privateKey).toString('base64') }, packet_id: pg, action: 'release_document' })).executed };
    const sn = fresh({ noNonce: true }); const pn = id(); const rn = sn.evaluate({ standing_id: 'nda', action: 'release_document', packet_id: pn });
    await sn.execute({ receipt: rn, packet_id: pn, action: 'release_document' }); out.mutation_noNonce_replay = { second_executed: (await sn.execute({ receipt: rn, packet_id: pn, action: 'release_document' })).executed }; }

  // matrix: the same four defeat inputs against the public reference guard (if its clone is available)
  const hd = process.argv[2] && path.join(path.resolve(process.argv[2]), 'harmonic-public');
  if (hd) {
    const handler = require(path.join(hd, 'api/evaluate.js')); const { guardedExecute } = require(path.join(hd, 'examples/raw-vs-governed/guard.js'));
    const server = http.createServer((q, s) => q.url === '/api/evaluate' ? handler(q, s) : (s.statusCode = 404, s.end())); await new Promise((r) => server.listen(0, '127.0.0.1', r));
    const baseUrl = `http://127.0.0.1:${server.address().port}`; const iso = (m) => new Date(m).toISOString();
    const pk = (observation, authority = {}) => ({ packet_id: id(), requested_action: 'release_document', execution_request: { action: 'release_document' },
      truth: { claims: ['At T0 the NDA was valid and document release was authorized.'], observations: [{ statement: observation }], evidence: [{ ref: 'registry://nda' }], last_verified_at: iso(Date.now()), stale_after_minutes: 1 }, authority,
      compassion: { affected_parties: ['a'], potential_harms: ['h'], mitigations: ['m'], escalation_path: 'e' }, accountability: { responsible_actor: 'a', authority_basis: 'r', consequence_owner: 'o', audit_ref: 'x', rollback_plan: 'hold' } });
    const fired = async (packet, fetchImpl) => { let n = 0; await guardedExecute({ baseUrl, packet, fetchImpl, execute: async () => { n++; } }); return n === 1; };
    const m = {};
    m.A_words_unlisted_wording = await fired(pk('the NDA was terminated'));
    m.A_flag_only = await fired(pk('At Tn the NDA remains valid.', { revoked: true, expires_at: iso(Date.now() - 86400000) }));
    { let n = 0; const flip = async (u, i) => { const r = await fetch(u, i); const b = await r.text(); active = false; return new Response(b, { status: r.status, headers: r.headers }); }; var active = true;
      await guardedExecute({ baseUrl, packet: pk('At Tn the NDA remains valid.'), fetchImpl: flip, execute: async () => { n++; } }); m.A_gap_revocation_after_evaluate = n === 1; }
    { const p = pk('the NDA is revoked'); const r = await (await fetch(baseUrl + '/api/evaluate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p) })).json();
      const { artifact_hash, public_release, note, ...result } = r; const forged = { ...result, outcome: 'stable', admissible: true, recommended_action: 'allow', stability_boundary: 'intact' };
      const sha = (s) => crypto.createHash('sha256').update(String(s)).digest('hex'); const fr = { ...forged, artifact_hash: sha(canon({ packet: p, result: forged })), public_release: true, note };
      m.A_receipt_forged_with_recomputed_hash = await fired(p, async () => new Response(JSON.stringify(fr), { status: 200 })); }
    server.close(); out.matrix_public_guard_fires = m;
  }
  console.log(JSON.stringify(out, null, 1));
}
module.exports = { makeSystem, canon };
if (require.main === module) run().catch((e) => { console.error(e); process.exit(1); });
