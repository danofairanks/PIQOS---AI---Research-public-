// repos: harmonic-public @ 7fe1597, runtime-admissibility-core-public @ 9305b82 | run: node i4_smaller.js <dir containing clones>
const path = require('path'), D = path.resolve(process.argv[2]);
const { evaluateHarmonicStabilizer: ev } = require(path.join(D, 'harmonic-public/api/evaluate.js'));
const iso = (ms) => new Date(ms).toISOString(), now = Date.now();
const base = () => ({ packet_id: 'x', requested_action: 'x', truth: { claims: ['x valid'], observations: [], evidence: [], last_verified_at: iso(now), stale_after_minutes: 60 },
  compassion: { affected_parties: ['x'], potential_harms: ['x'], mitigations: ['x'], escalation_path: 'x' }, accountability: { responsible_actor: 'x', authority_basis: 'x', consequence_owner: 'x', audit_ref: 'x', rollback_plan: 'x' } });
const show = (l, r) => console.log(l.padEnd(52), r.outcome, r.admissible, r.recommended_action);
for (const [l, e] of [['control: evidence []', []], ['evidence [""]', ['']], ['evidence [0]', [0]]]) { const p = base(); p.truth.evidence = e; show(l, ev(p)); }
const stale = (sa) => { const p = base(); p.truth.observations = [{ statement: 'x' }]; p.truth.evidence = [{ ref: 'r' }]; p.truth.last_verified_at = iso(now - 200 * 60000); if (sa === undefined) delete p.truth.stale_after_minutes; else p.truth.stale_after_minutes = sa; return ev(p); };
show('basis 200 min old, stale_after_minutes=1 (control)', stale(1)); show('basis 200 min old, stale_after_minutes omitted', stale()); show('basis 200 min old, stale_after_minutes=0', stale(0));
const ra = require(path.join(D, 'runtime-admissibility-core-public/api/evaluate.js')).evaluateRuntimeAdmissibility;
const pk = (o = {}) => { const p = { packet_id: 'r', authority_context: { issuer: 'registry', status: 'valid' }, runtime_state: { state_valid: true, last_verified_at: iso(now), assumptions: ['delegation valid'] },
  constraint_context: { allowed_actions: ['release'] }, consequence_boundary: { level: 'high' }, runtime_signals: [{ statement: 'registry reachable' }], freshness_policy: { state_stale_after_minutes: 1 } };
  for (const k of Object.keys(o)) p[k] = Object.assign({}, p[k], o[k]); return p; };
const s = (l, r) => console.log(l.padEnd(52), r.outcome, r.admissible, r.admissibility_signals.map((x) => x.code).join(','));
s('rac: status "revoked" (control)', ra(pk({ authority_context: { status: 'revoked' } })));
s('rac: status "terminated"', ra(pk({ authority_context: { status: 'terminated' } })));
s('rac: expires_at "tomorrow" (unparseable)', ra(pk({ authority_context: { expires_at: 'tomorrow' } })));
s('rac: last_verified_at "garbage" (unparseable)', ra(pk({ runtime_state: { last_verified_at: 'garbage' } })));
