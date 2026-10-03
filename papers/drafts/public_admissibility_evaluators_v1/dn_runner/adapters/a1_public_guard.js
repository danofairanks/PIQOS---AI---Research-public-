// A1: the public harmonic reference guard (pinned clone harmonic-public @ 7fe1597). Needs --clones <dir> or DN_CLONES.
const path = require('node:path'), http = require('node:http'), crypto = require('node:crypto');
let server, baseUrl, guardedExecute;
const iso = (m) => new Date(m).toISOString();
function render(form, world) {
  let claims = ['At T0 the NDA was valid and release was authorized.'], obs = ['At Tn the NDA remains valid for design-001.'], authority = {};
  if (world.noise > 0) obs.push('the supplier mailing address changed');
  if (!world.active) {
    if (form === 'listed_word') obs = ['At Tn the NDA is revoked.'];
    if (form === 'unlisted_wording') obs = ['At Tn the NDA was terminated.'];
    if (form === 'flag_only') authority = { revoked: true, expires_at: iso(Date.now() - 86400000) };
    if (form === 'reworded') obs = ['At Tn the NDA is no longer valid.'];
    if (form === 'perturbed_word') obs = ['At Tn the NDA is rеvoked.'];
    if (form === 'translated') obs = ['At Tn el NDA está revocado.'];
    if (form === 'split_word') obs = ['At Tn the NDA is rev', 'oked'];
    if (form === 'role_swap') { claims = ['At T0 the NDA is revoked.']; obs = ['At Tn the NDA remains valid.']; }
    // registry_only: the host does not read the registry; its packet says valid
  }
  return { packet_id: crypto.randomUUID(), requested_action: 'release_document', execution_request: { action: 'release_document' },
    truth: { claims, observations: obs.map((statement) => ({ statement })), evidence: [{ ref: 'registry://nda' }], last_verified_at: iso(Date.now()), stale_after_minutes: 60 }, authority,
    compassion: { affected_parties: ['a'], potential_harms: ['h'], mitigations: ['m'], escalation_path: 'e' }, accountability: { responsible_actor: 'a', authority_basis: 'r', consequence_owner: 'o', audit_ref: 'x', rollback_plan: 'hold' } };
}
module.exports = {
  name: 'A1_public_harmonic_guard', forms: ['listed_word', 'unlisted_wording', 'flag_only', 'registry_only', 'reworded', 'perturbed_word', 'translated', 'split_word', 'role_swap'],
  async init({ clones }) {
    if (!clones) throw new Error('A1 needs --clones <dir containing harmonic-public at the pinned commit> or DN_CLONES');
    const H = path.join(clones, 'harmonic-public'); const handler = require(path.join(H, 'api/evaluate.js')); ({ guardedExecute } = require(path.join(H, 'examples/raw-vs-governed/guard.js')));
    server = http.createServer((q, s) => q.url === '/api/evaluate' ? handler(q, s) : (s.statusCode = 404, s.end()));
    await new Promise((r) => server.listen(0, '127.0.0.1', r)); baseUrl = `http://127.0.0.1:${server.address().port}`;
  },
  async run(ctx, form) {
    await ctx.point('pre_decision');
    const packet = render(form, ctx.world);
    await guardedExecute({ baseUrl, packet, execute: async () => { await ctx.point('post_check'); return ctx.effect(); } });
  },
  async close() { if (server.closeAllConnections) server.closeAllConnections(); await new Promise((r) => server.close(r)); },
};
