#!/usr/bin/env node
/* B2: independent constituted-executor toy (stdlib Node 20+), built from the published freeze text of a frozen executor examination.
   Design and predictions were written before this file existed (internal history). It tests the property class, not any
   private implementation. BASELINE = the five features the freeze text names; HARDENED adds one-time nonce, audience, revocation epoch. */
const crypto = require('node:crypto');
const sha = (s) => crypto.createHash('sha256').update(s).digest('hex');
const canon = (v) => v === null || typeof v !== 'object' ? JSON.stringify(v) : Array.isArray(v) ? `[${v.map(canon).join(',')}]` : `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${canon(v[k])}`).join(',')}}`;
// flat-object parsers for the parse-differential attack: governance/verification layer reads the FIRST duplicate key, the effect layer uses JSON.parse (last wins)
function parseFirstWins(text) { const o = {}; for (const m of text.matchAll(/"([^"]+)"\s*:\s*("[^"]*"|-?\d+(?:\.\d+)?)/g)) if (!(m[1] in o)) o[m[1]] = JSON.parse(m[2]); return o; }
function hasDuplicateKeys(text) { const seen = new Set(); for (const m of text.matchAll(/"([^"]+)"\s*:/g)) { if (seen.has(m[1])) return true; seen.add(m[1]); } return false; }

function makeWorld({ variant = 'baseline', bind = 'bytes', mutations = {}, ttlMs = 30000, skewMs = 0 } = {}) {
  const hard = variant === 'hardened';
  const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519');
  const evidence = new Set(); const standing = new Map(); const ledger = []; const log = [];
  const sign = (p, key = privateKey) => crypto.sign(null, Buffer.from(canon(p)), key).toString('base64');
  const verify = (p, sig) => { try { return crypto.verify(null, Buffer.from(canon(p)), publicKey, Buffer.from(sig, 'base64')); } catch { return false; } };
  const setStanding = (id, active) => { const s = standing.get(id) || { epoch: 0 }; standing.set(id, { active, epoch: s.epoch + 1 }); };
  const execHash = (action, text) => {
    if (mutations.actionNotBound) return sha(bind === 'parsed' ? canon(parseFirstWins(text)) : text);
    return sha(action + '\n' + (bind === 'parsed' || bind === 'strict' ? canon(parseFirstWins(text)) : text));
  };
  const governance = {
    setStanding, revoke: (id) => setStanding(id, false), standing,
    // policy: PERMIT when the standing is active and the amount the governance layer reads is at most 100
    mint({ action, payloadText, standing_id, evidencePersisted = true, aud = 'exec-1', ttl = ttlMs }) {
      if (bind === 'strict' && hasDuplicateKeys(payloadText)) return { refused: 'duplicate_keys' };
      const amount = parseFirstWins(payloadText).amount; const s = standing.get(standing_id);
      const permit = s && s.active && Number(amount) <= 100;
      let evidence_id = null;
      if (evidencePersisted) { evidence_id = crypto.randomUUID(); evidence.add(evidence_id); }
      else if (mutations.mintWithoutEvidence) evidence_id = crypto.randomUUID(); // a faulty service minting with a fabricated id
      else return { refused: 'no_evidence' };
      const p = { decision: permit ? 'PERMIT' : 'REFUSE', action, execute_hash: execHash(action, payloadText), issued_at: Date.now(), expires_at: Date.now() + ttl, evidence_id };
      if (hard) { p.nonce = crypto.randomUUID(); p.aud = aud; p.epoch = s ? s.epoch : -1; }
      return { receipt: { payload: p, signature: sign(p) } };
    },
  };
  const executors = {};
  function executor(id) {
    if (executors[id]) return executors[id];
    const used = new Set();
    const consequence = async (action, text, slow) => { const v = JSON.parse(text); if (slow) await new Promise((r) => setTimeout(r, 15)); ledger.push({ executor: id, action, amount: v.amount }); };
    const ex = {
      consequence,
      async execute({ action, payloadText, receipt, slow = false }) {
        if (!receipt) return { executed: false, why: 'no_receipt' };
        const p = receipt.payload;
        if (!mutations.noSig && !verify(p, receipt.signature)) return { executed: false, why: 'bad_signature' };
        if (!mutations.noDecision && p.decision !== 'PERMIT') return { executed: false, why: 'not_permit' };
        if (bind === 'strict' && hasDuplicateKeys(payloadText)) return { executed: false, why: 'duplicate_keys' };
        if (!mutations.noHash && p.execute_hash !== execHash(action, payloadText)) return { executed: false, why: 'hash_mismatch' };
        if (!mutations.noExpiry && !(p.expires_at > Date.now() + skewMs)) return { executed: false, why: 'expired' };
        if (!mutations.noEvidence && !evidence.has(p.evidence_id)) return { executed: false, why: 'no_evidence' };
        if (hard) {
          if (!mutations.noAud && p.aud !== id) return { executed: false, why: 'audience' };
          if (!mutations.noNonce) { if (used.has(p.nonce)) return { executed: false, why: 'replay' }; used.add(p.nonce); }
        }
        // revocation epoch: checked at the start of the effect (synchronously with it); HARDENED only
        if (hard && !mutations.noEpoch) { const s = governance.standing.get(p.standing_id || 'nda'); if (!s || !s.active || s.epoch !== p.epoch) return { executed: false, why: 'epoch' }; }
        await consequence(action, payloadText, slow); return { executed: true };
      },
    };
    return (executors[id] = ex);
  }
  return { governance, executor, ledger, evidence, leak: { privateKey, sign, canon, execHash }, log };
}

async function run() {
  const out = {}; const T = '{"amount":10}'; const A = 'transfer';
  const world = (o) => { const w = makeWorld(o); w.governance.setStanding('nda', true); return w; };
  const mint = (w, extra = {}) => w.governance.mint({ action: A, payloadText: T, standing_id: 'nda', ...extra });
  const fires = (w) => w.ledger.length;
  const pathsFor = async (variant, mutations = {}) => {
    const r = {};
    { const w = world({ variant, mutations }); await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: null }); r.p1_no_receipt = fires(w); }
    { const w = world({ variant, mutations }); const other = crypto.generateKeyPairSync('ed25519'); const m = mint(w).receipt; const forged = { payload: { ...m.payload, evidence_id: [...w.evidence][0] }, signature: crypto.sign(null, Buffer.from(canon(m.payload)), other.privateKey).toString('base64') };
      await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: forged }); r.p2_forged = fires(w); }
    { const w = world({ variant, mutations }); const m = mint(w).receipt; await w.executor('exec-1').execute({ action: A, payloadText: '{"amount":1000000}', receipt: m }); r.p3_payload_mutated = fires(w); }
    { const w = world({ variant, mutations, ttlMs: 30000 }); const m = mint(w, { ttl: -1 }).receipt; await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: m }); r.p4_expired = fires(w); }
    { const w = world({ variant, mutations }); w.governance.revoke('nda'); const m = mint(w).receipt; const a = await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: m });
      const tamp = { payload: { ...m.payload, decision: 'PERMIT' }, signature: m.signature }; await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: tamp }); r.p5_refusal = fires(w); r.p5_decision_was = m.payload.decision; }
    { const w = world({ variant, mutations: { ...mutations, mintWithoutEvidence: true } }); const m = mint(w, { evidencePersisted: false }).receipt; await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: m }); r.p6_no_persisted_evidence = fires(w);
      const w2 = world({ variant, mutations }); r.p6_service_refuses_to_mint = !!mint(w2, { evidencePersisted: false }).refused; }
    return r;
  };
  out.baseline_paths_1_to_6 = await pathsFor('baseline');
  out.hardened_paths_1_to_6 = await pathsFor('hardened');
  // 7 parse differential
  const DUP = '{"amount":10,"amount":1000000}'; out.p7_parse_differential = {};
  for (const bind of ['parsed', 'bytes', 'strict']) { const w = world({ variant: 'baseline', bind }); const m = w.governance.mint({ action: A, payloadText: DUP, standing_id: 'nda' });
    if (m.refused) { out.p7_parse_differential[bind] = { minted: false, why: m.refused, consequence_amounts: [] }; continue; }
    const res = await w.executor('exec-1').execute({ action: A, payloadText: DUP, receipt: m.receipt }); out.p7_parse_differential[bind] = { minted: true, decision: m.receipt.payload.decision, executed: res.executed, why: res.why, consequence_amounts: w.ledger.map((x) => x.amount) }; }
  // 8 replay within ttl
  for (const variant of ['baseline', 'hardened']) { const w = world({ variant }); const m = mint(w).receipt; const e = w.executor('exec-1'); await e.execute({ action: A, payloadText: T, receipt: m }); await e.execute({ action: A, payloadText: T, receipt: m }); (out.p8_replay = out.p8_replay || {})[variant] = fires(w); }
  // 9 replay across two executors
  for (const variant of ['baseline', 'hardened']) { const w = world({ variant }); const m = mint(w, { aud: 'exec-1' }).receipt; await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: m }); await w.executor('exec-2').execute({ action: A, payloadText: T, receipt: m }); (out.p9_two_executors = out.p9_two_executors || {})[variant] = fires(w); }
  // 10 refusal after minting, before expiry
  for (const variant of ['baseline', 'hardened']) { const w = world({ variant }); const m = mint(w).receipt; m.payload.standing_id; w.governance.revoke('nda'); const r = await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: m }); (out.p10_refusal_after_mint = out.p10_refusal_after_mint || {})[variant] = { consequences: fires(w), why: r.why }; }
  // 11 cross-action reuse
  { const w = world({ variant: 'baseline' }); const m = w.governance.mint({ action: 'refund', payloadText: T, standing_id: 'nda' }).receipt; const r = await w.executor('exec-1').execute({ action: 'transfer', payloadText: T, receipt: m }); out.p11_cross_action = { bound: { consequences: fires(w), why: r.why } };
    const w2 = world({ variant: 'baseline', mutations: { actionNotBound: true } }); const m2 = w2.governance.mint({ action: 'refund', payloadText: T, standing_id: 'nda' }).receipt; await w2.executor('exec-1').execute({ action: 'transfer', payloadText: T, receipt: m2 }); out.p11_cross_action.action_not_bound_mutation = { consequences: w2.ledger.length }; }
  // 12 residuals on both variants
  out.p12_residuals = {};
  for (const variant of ['baseline', 'hardened']) { const rr = {};
    { const w = world({ variant }); const p = { decision: 'PERMIT', action: A, execute_hash: w.leak.execHash(A, '{"amount":1000000}'), issued_at: Date.now(), expires_at: Date.now() + 30000, evidence_id: [...w.evidence][0] || null, ...(variant === 'hardened' ? { nonce: 'x', aud: 'exec-1', epoch: 1 } : {}) };
      w.evidence.add('minted'); p.evidence_id = 'minted'; await w.executor('exec-1').execute({ action: A, payloadText: '{"amount":1000000}', receipt: { payload: p, signature: w.leak.sign(p) } }); rr.key_holder_mints = fires(w); }
    { const w = world({ variant }); await w.executor('exec-1').consequence(A, T); w.governance.revoke('nda'); await w.executor('exec-1').consequence(A, T); rr.direct_consequence_call_after_refusal = fires(w); }
    { const w = world({ variant, skewMs: -100000 }); const m = mint(w, { ttl: -50000 }).receipt; await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: m }); rr.executor_clock_behind_accepts_expired = fires(w); }
    { const w = world({ variant }); const m = mint(w).receipt; const pending = w.executor('exec-1').execute({ action: A, payloadText: T, receipt: m, slow: true }); await new Promise((r) => setTimeout(r, 3)); w.governance.revoke('nda'); await pending; rr.refusal_after_effect_started = fires(w); }
    out.p12_residuals[variant] = rr; }
  // mutation checks: each disabled check makes its path fire
  const mut = {}; const one = async (variant, m, key) => (await pathsFor(variant, m))[key];
  mut.noHash_p3 = await one('baseline', { noHash: true }, 'p3_payload_mutated'); mut.noSig_p2 = await one('baseline', { noSig: true }, 'p2_forged');
  mut.noExpiry_p4 = await one('baseline', { noExpiry: true }, 'p4_expired'); mut.noDecision_p5 = await one('baseline', { noDecision: true }, 'p5_refusal');
  mut.noEvidence_p6 = await one('baseline', { noEvidence: true }, 'p6_no_persisted_evidence');
  { const w = world({ variant: 'hardened', mutations: { noNonce: true } }); const m = mint(w).receipt; const e = w.executor('exec-1'); await e.execute({ action: A, payloadText: T, receipt: m }); await e.execute({ action: A, payloadText: T, receipt: m }); mut.noNonce_p8 = fires(w); }
  { const w = world({ variant: 'hardened', mutations: { noAud: true } }); const m = mint(w, { aud: 'exec-1' }).receipt; await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: m }); await w.executor('exec-2').execute({ action: A, payloadText: T, receipt: m }); mut.noAud_p9 = fires(w); }
  { const w = world({ variant: 'hardened', mutations: { noEpoch: true } }); const m = mint(w).receipt; w.governance.revoke('nda'); await w.executor('exec-1').execute({ action: A, payloadText: T, receipt: m }); mut.noEpoch_p10 = fires(w); }
  out.mutation_checks_consequences = mut;
  console.log(JSON.stringify(out, null, 1));
}
module.exports = { makeWorld };
if (require.main === module) run().catch((e) => { console.error(e); process.exit(1); });
