// repo: harmonic-public @ 7fe1597  | run: node i2_authority_flags.js <dir containing clones>
const path = require('path'), D = path.resolve(process.argv[2]);
const { evaluateHarmonicStabilizer: ev } = require(path.join(D, 'harmonic-public/api/evaluate.js'));
const pk = (authority) => ({ packet_id: 'p1', requested_action: 'release_document',
  truth: { claims: ['At T0 the NDA was valid.'], observations: [{ statement: 'the NDA remains valid' }], evidence: [{ ref: 'registry://nda' }], last_verified_at: new Date().toISOString(), stale_after_minutes: 60 },
  authority, compassion: { affected_parties: ['a'], potential_harms: ['h'], mitigations: ['m'], escalation_path: 'e' },
  accountability: { responsible_actor: 'a', authority_basis: 'b', consequence_owner: 'o', audit_ref: 'x', rollback_plan: 'r' } });
const a = ev(pk({})), b = ev(pk({ revoked: true, expires_at: '2020-01-01T00:00:00Z' }));
console.log('control (no flags):      ', a.outcome, a.admissible, a.recommended_action);
console.log('revoked + expired flags: ', b.outcome, b.admissible, b.recommended_action,
  '| runtime_continuity:', b.runtime_continuity.survivability, 'escalation_required=' + b.runtime_continuity.escalation_required, JSON.stringify(b.runtime_continuity.authority_risk));
// the same packet through the repository's own guard over HTTP
const http = require('http'), handler = require(path.join(D, 'harmonic-public/api/evaluate.js')), { guardedExecute } = require(path.join(D, 'harmonic-public/examples/raw-vs-governed/guard.js'));
const s = http.createServer((q, r) => q.url === '/api/evaluate' ? handler(q, r) : (r.statusCode = 404, r.end()));
s.listen(0, '127.0.0.1', async () => {
  const baseUrl = 'http://127.0.0.1:' + s.address().port; let effects = 0;
  const res = await guardedExecute({ baseUrl, packet: pk({ revoked: true, expires_at: '2020-01-01T00:00:00Z' }), execute: async () => { effects++; } });
  console.log('guardedExecute executed:', res.executed, 'effects:', effects); s.close();
});
