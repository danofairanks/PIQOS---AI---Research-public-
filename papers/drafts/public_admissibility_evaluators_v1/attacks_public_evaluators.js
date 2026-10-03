#!/usr/bin/env node
/* Attack suite on the public repositories listed in PINS.txt (exact clones). Usage: node attacks_public_evaluators.js <dir containing the clones> [harmonic_root_override]
   Predictions were written before the first attack run (internal history); each attack has a control in the same script. Node 20+, no packages. */
const path = require('node:path'), fs = require('node:fs'), http = require('node:http'), os = require('node:os');
const crypto = require('node:crypto'), cp = require('node:child_process');
const D = path.resolve(process.argv[2]);
const H = path.join(D, 'harmonic-public');
const { evaluateHarmonicStabilizer: harm } = require(path.join(H, 'api/evaluate.js'));
const handler = require(path.join(H, 'api/evaluate.js'));
const { guardedExecute } = require(path.join(H, 'examples/raw-vs-governed/guard.js'));
const out = {};
const now = Date.now(), iso = (ms) => new Date(ms).toISOString();
const short = (r) => ({ outcome: r.outcome, admissible: r.admissible, action: r.recommended_action });

function packet(over = {}) {
  const p = {
    packet_id: 'pkt-' + crypto.randomUUID(), requested_action: 'release_document',
    execution_request: { action: 'release_document' },
    truth: { claims: ['At T0 the NDA was valid and document release was authorized.'],
      observations: [{ statement: 'At Tn the NDA remains valid for design-001 and supplier-001.' }],
      evidence: [{ ref: 'registry://nda/supplier-001' }], last_verified_at: iso(now), stale_after_minutes: 1 },
    authority: {},
    compassion: { affected_parties: ['owner', 'supplier'], potential_harms: ['Unauthorized disclosure'], mitigations: ['Hold'], escalation_path: 'reviewer' },
    accountability: { responsible_actor: 'agent', authority_basis: 'registry', consequence_owner: 'owner', audit_ref: 'a', rollback_plan: 'hold' },
  };
  return deepMerge(p, over);
}
function deepMerge(a, b) {
  for (const k of Object.keys(b)) {
    if (b[k] && typeof b[k] === 'object' && !Array.isArray(b[k]) && a[k] && typeof a[k] === 'object' && !Array.isArray(a[k])) deepMerge(a[k], b[k]); else a[k] = b[k];
  }
  return a;
}
const obs = (s) => ({ truth: { observations: [{ statement: s }] } });

// H1 controls
out.H1_controls = { consistent: short(harm(packet())), claims_valid_observed_revoked: short(harm(packet(obs('At Tn the NDA is revoked for supplier-001.')))) };
// H2 lexical evasion
out.H2_paraphrases = {};
for (const s of ['the registry now lists the NDA as terminated', 'the NDA ended on 2026-10-01', 'the NDA was withdrawn by the supplier', 'the NDA is no longer in force', 'the NDA lapsed', 'the NDA was cancelled', 'the NDA was rescinded', 'the NDA was superseded by a new agreement', 'the NDA is revoked'])
  out.H2_paraphrases[s] = short(harm(packet(obs(s))));
// H3 negation
out.H3_negation = short(harm(packet(obs('The NDA has not been revoked.'))));
// H4 claims without a listed stable term
out.H4_claims_without_term = { claim_in_place_obs_revoked: short(harm(packet({ truth: { claims: ['NDA is in place'], observations: [{ statement: 'NDA revoked' }] } }))),
  control_claim_valid_obs_revoked: short(harm(packet({ truth: { claims: ['NDA is valid'], observations: [{ statement: 'NDA revoked' }] } }))) };
// H5 freshness chosen by the caller
const old = iso(now - 200 * 60000);
const f = (t) => { const r = harm(packet({ truth: { last_verified_at: old, ...t } })); return { ...short(r), stale: r.runtime_continuity.continuity_flags.stale_basis }; };
{ const p1 = packet({ truth: { last_verified_at: old, stale_after_minutes: 1 } }); const p2 = packet({ truth: { last_verified_at: old } }); delete p2.truth.stale_after_minutes; const p3 = packet({ truth: { last_verified_at: old, stale_after_minutes: 0 } });
  const g = (p) => { const r = harm(p); return { ...short(r), stale: r.runtime_continuity.continuity_flags.stale_basis }; };
  out.H5_freshness = { control_stale_after_1: g(p1), stale_after_omitted: g(p2), stale_after_0: g(p3) }; }

// H6 authority revoked / expired flags
{ const base = packet({ authority: { revoked: true, expires_at: iso(now - 86400000) } });
  const r = harm(base);
  out.H6_authority_flags = { top_level: short(r), survivability: r.runtime_continuity.survivability, escalation_required: r.runtime_continuity.escalation_required,
    authority_risk: r.runtime_continuity.authority_risk, pressure_score: r.runtime_continuity.pressure_score,
    control_no_authority_flags: short(harm(packet())), control_revoked_text_in_observation: short(harm(packet(obs('NDA revoked')))) }; }

// real HTTP server over the repository handler, as the example does
async function withServer(fn) {
  const server = http.createServer((req, res) => { if (req.url === '/api/evaluate') return handler(req, res); res.statusCode = 404; res.end(); });
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const baseUrl = `http://127.0.0.1:${server.address().port}`;
  try { return await fn(baseUrl); } finally { await new Promise((r) => server.close(r)); }
}
async function main() {
  await withServer(async (baseUrl) => {
    // H6 over the guard
    { const ledger = []; const p = packet({ authority: { revoked: true, expires_at: iso(now - 86400000) } });
      const res = await guardedExecute({ baseUrl, packet: p, execute: async () => { ledger.push('effect'); return 'done'; } });
      out.H6_guard = { executed: res.executed, effects: ledger.length, receipt_outcome: res.receipt && res.receipt.outcome }; }
    // H7 evaluate-to-effect gap
    { const reg = { active: true }; const ledger = [];
      const mk = () => packet(obs(reg.active ? 'At Tn the NDA remains valid.' : 'At Tn the NDA is revoked.'));
      const flipAfterEvaluate = async (url, init) => { const r = await fetch(url, init); const body = await r.text(); reg.active = false; return new Response(body, { status: r.status, headers: r.headers }); };
      const res1 = await guardedExecute({ baseUrl, packet: mk(), fetchImpl: flipAfterEvaluate, execute: async () => { ledger.push({ active_at_effect: reg.active }); } });
      reg.active = false; const res2 = await guardedExecute({ baseUrl, packet: mk(), execute: async () => { ledger.push('control_effect'); } });
      out.H7_gap = { gap_case_executed: res1.executed, registry_active_at_effect: ledger[0] && ledger[0].active_at_effect, control_revoked_before_evaluate_executed: res2.executed }; }
    // H8 receipt authenticity
    { const p = packet(obs('At Tn the NDA is revoked.')); const r = await (await fetch(baseUrl + '/api/evaluate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p) })).json();
      const stable = (v) => v === null || typeof v !== 'object' ? JSON.stringify(v) : Array.isArray(v) ? `[${v.map(stable).join(',')}]` : `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${stable(v[k])}`).join(',')}}`;
      const sha = (s) => crypto.createHash('sha256').update(String(s)).digest('hex');
      const { artifact_hash, public_release, note, ...result } = r;
      const recomputed = sha(stable({ packet: p, result })) === artifact_hash;
      const forged = { ...result, outcome: 'stable', admissible: true, recommended_action: 'allow', stability_boundary: 'intact' };
      const forgedReceipt = { ...forged, artifact_hash: sha(stable({ packet: p, result: forged })), public_release: true, note };
      const fake = async () => new Response(JSON.stringify(forgedReceipt), { status: 200 }); const ledger = [];
      const accepted = await guardedExecute({ baseUrl, packet: p, fetchImpl: fake, execute: async () => { ledger.push(1); } });
      const wrongId = await guardedExecute({ baseUrl, packet: p, fetchImpl: async () => new Response(JSON.stringify({ ...forgedReceipt, packet_id: 'other' }), { status: 200 }), execute: async () => { ledger.push(2); } });
      const notPublic = await guardedExecute({ baseUrl, packet: p, fetchImpl: async () => new Response(JSON.stringify({ ...forgedReceipt, public_release: false }), { status: 200 }), execute: async () => { ledger.push(3); } });
      out.H8_receipt = { real_receipt_for_revoked_packet: { outcome: r.outcome, action: r.recommended_action }, hash_recomputable_from_receipt: recomputed,
        forged_stable_allow_receipt_executed: accepted.executed, control_wrong_packet_id_executed: wrongId.executed, control_public_release_false_executed: notPublic.executed, effects: ledger }; }
  });
  // H9 self-declared completeness
  { const x = { packet_id: 'x', requested_action: 'x', truth: { claims: ['x valid'], observations: ['x'], evidence: ['x'], last_verified_at: iso(now), stale_after_minutes: 60 },
      compassion: { affected_parties: ['x'], potential_harms: ['x'], mitigations: ['x'], escalation_path: 'x' }, accountability: { responsible_actor: 'x', authority_basis: 'x', consequence_owner: 'x', audit_ref: 'x', rollback_plan: 'x' } };
    const ev = (e) => { const p = JSON.parse(JSON.stringify(x)); p.truth.observations = []; p.truth.evidence = e; return short(harm(p)); };
    out.H9_self_declared = { all_x: short(harm(x)), evidence_empty_string_no_observations: ev(['']), evidence_zero_no_observations: ev([0]), control_no_evidence_no_observations: ev([]) }; }
  // H10 V114 test runnable?
  { const r = cp.spawnSync(process.execPath, [path.join(H, 'evidence/examinations/v114-execution-boundary/V114_TEST.js')], { cwd: path.join(H, 'evidence/examinations/v114-execution-boundary'), encoding: 'utf8' });
    out.H10_V114_runnable = { exit: r.status, missing_module: /Cannot find module '..\/api\/secure-execution'/.test(r.stderr), secure_execution_file_in_api: fs.existsSync(path.join(H, 'api/secure-execution.js')) }; }

  // R1/R2 runtime-admissibility-core evaluator
  { const R = path.join(D, 'runtime-admissibility-core-public/api/evaluate.js'); let ra;
    try { ra = require(R).evaluateRuntimeAdmissibility; } catch (e) { out.R_load_error = String(e.message).slice(0, 120); }
    if (ra) {
      const pk = (over = {}) => deepMerge({ packet_id: 'r', authority_context: { issuer: 'registry', status: 'valid' }, runtime_state: { state_valid: true, last_verified_at: iso(now), assumptions: ['delegation valid'] },
        constraint_context: { allowed_actions: ['release'] }, consequence_boundary: { level: 'high' }, runtime_signals: [{ statement: 'registry reachable' }], freshness_policy: { state_stale_after_minutes: 1 } }, over);
      const s = (r) => ({ outcome: r.outcome, admissible: r.admissible, codes: r.admissibility_signals.map((x) => x.code) });
      out.R1_status_and_lexical = { control_valid: s(ra(pk())), control_status_revoked: s(ra(pk({ authority_context: { status: 'revoked' } }))), status_terminated: s(ra(pk({ authority_context: { status: 'terminated' } }))),
        status_withdrawn: s(ra(pk({ authority_context: { status: 'withdrawn' } }))), signal_terminated: s(ra(pk({ runtime_signals: [{ statement: 'registry reports the delegation terminated' }] }))),
        control_signal_revoked: s(ra(pk({ runtime_signals: [{ statement: 'registry reports the delegation revoked' }] }))) };
      out.R2_invalid_timestamps = { control_expired_iso: s(ra(pk({ authority_context: { expires_at: iso(now - 1000) } }))), expires_at_unparseable: s(ra(pk({ authority_context: { expires_at: 'tomorrow' } }))),
        control_stale_iso: s(ra(pk({ runtime_state: { last_verified_at: iso(now - 3600000) } }))), last_verified_unparseable: s(ra(pk({ runtime_state: { last_verified_at: 'garbage' } }))) };
      const hv = harm(packet({ truth: { last_verified_at: 'garbage', stale_after_minutes: 1 } }));
      out.R2_harmonic_invalid_timestamp_for_contrast = { codes: hv.runtime_continuity.continuity_flags.stale_basis, ...short(hv) };
    } }
  // S1/S2 stubs
  async function callStub(rel, body) {
    const tmp = path.join(os.tmpdir(), 'stub_' + crypto.randomUUID() + '.mjs'); fs.copyFileSync(path.join(D, rel), tmp);
    const mod = await import(tmp); let got; const res = { status() { return this; }, json(x) { got = x; return this; } };
    mod.default({ method: 'POST', body }, res); fs.unlinkSync(tmp); return got;
  }
  out.S1_authority_continuity_stub = { revoked_packet: await callStub('authority-continuity-primitive-public/api/evaluate.js', { authority: { revoked: true, status: 'revoked', expires_at: '2000-01-01' } }), empty_body: await callStub('authority-continuity-primitive-public/api/evaluate.js', {}) };
  out.S2_consequence_boundary_stub = { revoked_packet: await callStub('consequence-boundary-public/api/evaluate.js', { authority: { revoked: true } }), empty_body: await callStub('consequence-boundary-public/api/evaluate.js', {}) };
  // F1 solaceframe computeAdmission (type import line removed so the file loads under Node type stripping)
  { const src = fs.readFileSync(path.join(D, 'solaceframe-public/apps/studio/lib/runtime/identity/identity-admission.ts'), 'utf8').split('\n').filter((l) => !/^import /.test(l)).join('\n');
    const tmp = path.join(os.tmpdir(), 'ia_' + crypto.randomUUID() + '.ts'); fs.writeFileSync(tmp, src);
    const code = `import('${tmp}').then(m=>{const s=(o)=>({identity_score:100,geometry_score:100,body_score:100,motion_score:100,wardrobe_score:100,hair_score:100,chronology_score:100,environment_score:100,...o});
      console.log(JSON.stringify({all_100:m.computeAdmission(s({})),one_60:m.computeAdmission(s({hair_score:60})),one_59:m.computeAdmission(s({hair_score:59})),one_0:m.computeAdmission(s({hair_score:0})),two_80:m.computeAdmission(s({hair_score:80,motion_score:80}))}))})`;
    const r = cp.spawnSync(process.execPath, ['--experimental-strip-types', '-e', code], { encoding: 'utf8' }); fs.unlinkSync(tmp);
    try { out.F1_solaceframe_computeAdmission = JSON.parse(r.stdout.trim().split('\n').pop()); } catch (e) { out.F1_solaceframe_computeAdmission = { error: (r.stderr || '').slice(0, 200) }; } }
  // N1 static web surfaces
  out.N1_surfaces = {}; for (const rp of ['solace-kernel-public', 'solace-public', 'solaceveil-public']) {
    const files = cp.execSync('git ls-files', { cwd: path.join(D, rp), encoding: 'utf8' }).split('\n').filter(Boolean);
    out.N1_surfaces[rp] = { code_files: files.filter((x) => /\.(js|ts|tsx|py)$/.test(x) && !/next-env|next\.config/.test(x)), api_dir: files.some((x) => x.startsWith('api/')) }; }
  console.log(JSON.stringify(out, null, 1));
}
main().catch((e) => { console.error(e); process.exit(1); });
