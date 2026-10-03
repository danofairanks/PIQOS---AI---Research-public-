// repo: harmonic-public @ 7fe1597  | run: node i1_lexical.js <dir containing clones>
const { evaluateHarmonicStabilizer: ev } = require(require('path').resolve(process.argv[2], 'harmonic-public/api/evaluate.js'));
const pk = (obs, claims = ['At T0 the NDA was valid.']) => ({ packet_id: 'p1', requested_action: 'release_document',
  truth: { claims, observations: [{ statement: obs }], evidence: [{ ref: 'registry://nda' }], last_verified_at: new Date().toISOString(), stale_after_minutes: 60 },
  authority: {}, compassion: { affected_parties: ['a'], potential_harms: ['h'], mitigations: ['m'], escalation_path: 'e' },
  accountability: { responsible_actor: 'a', authority_basis: 'b', consequence_owner: 'o', audit_ref: 'x', rollback_plan: 'r' } });
const show = (l, r) => console.log(l.padEnd(46), r.outcome, r.admissible, r.recommended_action);
show('control: "the NDA is revoked"', ev(pk('the NDA is revoked')));
for (const w of ['the NDA was terminated', 'the NDA ended on 2026-10-01', 'the NDA was withdrawn by the supplier', 'the NDA is no longer in force', 'the NDA lapsed', 'the NDA was cancelled', 'the NDA was rescinded', 'the NDA was superseded by a new agreement'])
  show('"' + w + '"', ev(pk(w)));
show('claims without a listed term (obs revoked)', ev(pk('the NDA is revoked', ['the NDA exists'])));
