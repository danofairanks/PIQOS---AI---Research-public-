#!/usr/bin/env node
/* Semantic-shuffle probes. Usage: node semantic_shuffle_probes.js <dir containing harmonic-public>. Predictions were written before this file (internal history). */
const path = require('node:path');
const { evaluateHarmonicStabilizer: ev } = require(path.join(path.resolve(process.argv[2]), 'harmonic-public/api/evaluate.js'));
const iso = () => new Date().toISOString();
const pk = (claims, observations) => ({ packet_id: 'p', requested_action: 'release_document',
  truth: { claims, observations: observations.map((s) => ({ statement: s })), evidence: [{ ref: 'r' }], last_verified_at: iso(), stale_after_minutes: 1 }, authority: {},
  compassion: { affected_parties: ['a'], potential_harms: ['h'], mitigations: ['m'], escalation_path: 'e' },
  accountability: { responsible_actor: 'a', authority_basis: 'b', consequence_owner: 'o', audit_ref: 'x', rollback_plan: 'r' } });
const v = (claims, obs) => { const r = ev(pk(claims, obs)); return `${r.outcome}/${r.recommended_action}`; };
const C = ['the NDA is valid']; const out = {};
out.controls = { revoked: v(C, ['the NDA is revoked']), valid: v(C, ['the NDA remains valid']) };
const text = (s) => ({ [s]: v(C, [s]) });
out.rewording = Object.assign({}, ...['the NDA is no longer valid', 'the NDA has ceased to be effective', 'the NDA is void'].map(text));
out.surface_perturbation = { cyrillic_e: v(C, ['the NDA is rеvoked']), zero_width: v(C, ['the NDA is re​voked']), fullwidth: v(C, ['the NDA is ｒｅｖｏｋｅｄ']) };
out.translation = { french: v(C, ['le NDA est révoqué']), german: v(C, ['der NDA wurde widerrufen']) };
out.order_permutation = { valid_first: v(C, ['the NDA remains valid', 'the NDA is revoked']), revoked_first: v(C, ['the NDA is revoked', 'the NDA remains valid']) };
out.split_across_statements = v(C, ['the NDA is revo', 'ked']);
out.role_swap = v(['the NDA is revoked'], ['the NDA is valid']);
out.mention_negation_modality = { mention: v(C, ['the slide deck lists the word revoked as an example']), negation: v(C, ['the NDA is not revoked and not terminated']), modality: v(C, ['the NDA will be revoked tomorrow']) };
// registry vocabulary toy: host text ignored, the registry stores a status string
const DENY = ['revoked', 'expired', 'denied', 'suspended']; const ALLOW = ['active', 'valid'];
const variants = { A_allow_list_exact: (s) => ALLOW.includes(s), B_deny_list_raw: (s) => !DENY.includes(s), C_deny_list_lower_trim: (s) => !DENY.includes(String(s).toLowerCase().trim()) };
const statuses = { active: 'active', ACTIVE: 'ACTIVE', revoked: 'revoked', Revoked_trailing_space: 'Revoked ', terminated: 'terminated', withdrawn: 'withdrawn', lapsed: 'lapsed', cyrillic_e_revoked: 'rеvoked' };
out.registry_vocabulary = {}; for (const [vn, f] of Object.entries(variants)) { out.registry_vocabulary[vn] = {}; for (const [k, s] of Object.entries(statuses)) out.registry_vocabulary[vn][k] = f(s) ? 'allow' : 'deny'; }
console.log(JSON.stringify(out, null, 1));
